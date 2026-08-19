from typing import List, Optional, Tuple, Union

import torch
import torch.nn as nn
from torch.nn import CrossEntropyLoss
from transformers import Qwen2_5_VLConfig, Qwen2_5_VLForConditionalGeneration
from transformers.models.qwen2_5_vl.modeling_qwen2_5_vl import Qwen2_5_VLCausalLMOutputWithPast

from .connector import get_connector
from .spatial_encoder import VGGTSpatialEncoderConfig, VGGTSpatialEncoderPreTrainedModel


class SpatialMLLMConfig(Qwen2_5_VLConfig):
    model_type = "spatial-mllm"

    def __init__(self, spatial_config=None, connector_config=None, **kwargs):
        super().__init__(**kwargs)
        self.sub_configs["spatial_config"] = VGGTSpatialEncoderConfig
        if isinstance(spatial_config, dict):
            self.spatial_config = self.sub_configs["spatial_config"](**spatial_config)
        elif spatial_config is None:
            self.spatial_config = self.sub_configs["spatial_config"]()

        self.connector_config = connector_config if connector_config is not None else {}


class SpatialMLLMForConditionalGeneration(Qwen2_5_VLForConditionalGeneration):
    """Spatial-MLLM: Qwen2.5-VL + VGGT spatial encoder + connector for spatial understanding.

    Strategy for transformers 5.8 compatibility:
    - Override forward to inject spatial fusion on the first iteration
    - Let the parent handle all position_ids, attention masks, language model, etc.
    """

    def __init__(self, config):
        super().__init__(config)
        self.spatial_encoder = VGGTSpatialEncoderPreTrainedModel(config.spatial_config)
        self.connector = get_connector(config)

        # Initialize weights and apply final processing
        self.post_init()

    @property
    def visual(self):
        """In transformers 5.8, the vision encoder lives on self.model."""
        return self.model.visual

    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values=None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        pixel_values: Optional[torch.Tensor] = None,
        pixel_values_videos: Optional[torch.FloatTensor] = None,
        image_grid_thw: Optional[torch.LongTensor] = None,
        video_grid_thw: Optional[torch.LongTensor] = None,
        image_tchw: Optional[List[torch.FloatTensor]] = None,
        video_tchw: Optional[List[torch.FloatTensor]] = None,
        rope_deltas: Optional[torch.LongTensor] = None,
        second_per_grid_ts: Optional[torch.Tensor] = None,
        mm_token_type_ids: Optional[torch.Tensor] = None,
        **kwargs,
    ) -> Union[Tuple, Qwen2_5_VLCausalLMOutputWithPast]:
        """Forward with spatial encoder fusion.

        On the first iteration (pixel_values present), we:
        1. Compute text embeddings
        2. Run the vision encoder to get image/video embeddings
        3. Run the spatial encoder on raw image_tchw/video_tchw
        4. Fuse via connector
        5. Scatter fused embeddings into inputs_embeds
        6. Call parent forward with inputs_embeds (pixel_values=None to skip parent's vision)
        """

        # If we have pixel_values, do our custom spatial fusion
        if inputs_embeds is None and (pixel_values is not None or pixel_values_videos is not None):
            inputs_embeds = self.model.get_input_embeddings()(input_ids)

            if pixel_values is not None and image_tchw is not None:
                pixel_values = pixel_values.type(self.visual.dtype)
                image_tchw = [t.type(self.visual.dtype) for t in image_tchw]

                # Get image embeddings from vision encoder
                vision_output = self.visual(pixel_values, grid_thw=image_grid_thw)
                image_embeds = vision_output.pooler_output
                if isinstance(image_embeds, (list, tuple)):
                    image_embeds = torch.cat(image_embeds, dim=0)

                # Get spatial embeddings (spatial encoder expects [T,C,H,W])
                image_tchw_4d = [t.unsqueeze(0) if t.dim() == 3 else t for t in image_tchw]
                spatial_embeds_list, patch_start_idx = self.spatial_encoder(image_tchw_4d)

                # Fuse image and spatial embeddings via connector
                fused_embeds = self.connector(
                    image_embeds=image_embeds,
                    spatial_embeds_list=spatial_embeds_list,
                    patch_start_idx=patch_start_idx,
                    grid_thw=image_grid_thw,
                )

                # Scatter fused embeddings at image token positions
                mask = (input_ids == self.config.image_token_id).unsqueeze(-1).expand_as(inputs_embeds)
                fused_embeds = fused_embeds.to(inputs_embeds.device, inputs_embeds.dtype)
                inputs_embeds = inputs_embeds.masked_scatter(mask, fused_embeds)

            if pixel_values_videos is not None and video_tchw is not None:
                pixel_values_videos = pixel_values_videos.type(self.visual.dtype)
                video_tchw = [t.type(self.visual.dtype) for t in video_tchw]

                # Get video embeddings from vision encoder
                vision_output = self.visual(pixel_values_videos, grid_thw=video_grid_thw)
                video_embeds = vision_output.pooler_output
                if isinstance(video_embeds, (list, tuple)):
                    video_embeds = torch.cat(video_embeds, dim=0)

                # Get spatial embeddings
                spatial_embeds_list, patch_start_idx = self.spatial_encoder(video_tchw, grid_thw=video_grid_thw)

                # Fuse video and spatial embeddings
                fused_embeds = self.connector(
                    video_embeds=video_embeds,
                    spatial_embeds_list=spatial_embeds_list,
                    patch_start_idx=patch_start_idx,
                    grid_thw=video_grid_thw,
                )

                # Scatter fused embeddings at video token positions
                mask = (input_ids == self.config.video_token_id).unsqueeze(-1).expand_as(inputs_embeds)
                fused_embeds = fused_embeds.to(inputs_embeds.device, inputs_embeds.dtype)
                inputs_embeds = inputs_embeds.masked_scatter(mask, fused_embeds)

            # Call parent forward with pre-computed inputs_embeds, skip parent's vision processing
            return super().forward(
                input_ids=input_ids,
                attention_mask=attention_mask,
                position_ids=position_ids,
                past_key_values=past_key_values,
                inputs_embeds=inputs_embeds,
                labels=labels,
                use_cache=use_cache,
                pixel_values=None,  # skip parent's vision processing
                pixel_values_videos=None,
                image_grid_thw=image_grid_thw,
                video_grid_thw=video_grid_thw,
                rope_deltas=rope_deltas,
                second_per_grid_ts=second_per_grid_ts,
                mm_token_type_ids=mm_token_type_ids,
                **kwargs,
            )

        # No pixel_values: either decode step or text-only; delegate entirely to parent
        return super().forward(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            labels=labels,
            use_cache=use_cache,
            pixel_values=pixel_values,
            pixel_values_videos=pixel_values_videos,
            image_grid_thw=image_grid_thw,
            video_grid_thw=video_grid_thw,
            rope_deltas=rope_deltas,
            second_per_grid_ts=second_per_grid_ts,
            mm_token_type_ids=mm_token_type_ids,
            **kwargs,
        )

    def prepare_inputs_for_generation(
        self,
        input_ids,
        past_key_values=None,
        attention_mask=None,
        inputs_embeds=None,
        position_ids=None,
        use_cache=True,
        pixel_values=None,
        pixel_values_videos=None,
        image_grid_thw=None,
        video_grid_thw=None,
        second_per_grid_ts=None,
        is_first_iteration=False,
        **kwargs,
    ):
        # Extract image_tchw/video_tchw from kwargs before passing to super
        image_tchw = kwargs.pop("image_tchw", None)
        video_tchw = kwargs.pop("video_tchw", None)

        model_inputs = super().prepare_inputs_for_generation(
            input_ids,
            past_key_values=past_key_values,
            attention_mask=attention_mask,
            inputs_embeds=inputs_embeds,
            position_ids=position_ids,
            pixel_values=pixel_values,
            pixel_values_videos=pixel_values_videos,
            image_grid_thw=image_grid_thw,
            video_grid_thw=video_grid_thw,
            second_per_grid_ts=second_per_grid_ts,
            use_cache=use_cache,
            is_first_iteration=is_first_iteration,
            **kwargs,
        )

        if is_first_iteration:
            model_inputs["image_tchw"] = image_tchw
            model_inputs["video_tchw"] = video_tchw
        else:
            model_inputs["image_tchw"] = None
            model_inputs["video_tchw"] = None

        return model_inputs
