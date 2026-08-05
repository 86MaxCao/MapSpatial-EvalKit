# --------------------------------------------------------
# VeOmni Integration of InternVL-U
# Copyright (c) 2026 OpenGVLab (original code)
# Licensed under The MIT License
# --------------------------------------------------------

import os
from types import SimpleNamespace
from typing import List, Optional, Tuple, Union

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers.modeling_outputs import CausalLMOutputWithPast
from transformers.modeling_utils import PreTrainedModel
from transformers.utils import logging

from .configuration_internvlu import InternVLUConfig

logger = logging.get_logger(__name__)


class InternVLUModel(PreTrainedModel):
    """Unified InternVL-U model for VeOmni.

    Wraps three components:
    - VLM (InternVLUChatModel): InternViT + Qwen3 LLM for understanding
    - Generation Decoder (InternVLUGenerationDecoder): DiT for image generation
    - VAE (AutoencoderKLQwenImage): for latent encoding/decoding

    The model supports both understanding (CE loss) and generation (flow-matching loss)
    in a single forward pass, enabling unified training.
    """

    config_class = InternVLUConfig
    main_input_name = "input_ids"
    base_model_prefix = ""
    _supports_flash_attn_2 = True
    supports_gradient_checkpointing = True
    _no_split_modules = ["InternVisionEncoderLayer", "Qwen3DecoderLayer"]

    def __init__(self, config: InternVLUConfig, **kwargs):
        super().__init__(config)

        # Build VLM (InternViT + Qwen3 + projector)
        from .vlm.modeling_internvlu_chat import InternVLUChatModel

        self.vlm = InternVLUChatModel(config.vlm_config)

        # Build generation decoder (DiT)
        from .diffusion.modeling_internvlu_generation_decoder import (
            InternVLUGenerationDecoder,
        )

        self.generation_decoder = InternVLUGenerationDecoder(
            config.generation_decoder_config
        )

        # VAE is loaded separately (from diffusers), not a submodule of this model
        self.vae = None  # Set externally by the trainer or inference script

        # Initialize special token IDs (set after tokenizer is loaded)
        self._special_token_ids_initialized = False

    @property
    def lm_head(self):
        return self.vlm.language_model.get_output_embeddings()

    def get_input_embeddings(self):
        return self.vlm.language_model.get_input_embeddings()

    def get_output_embeddings(self):
        return self.vlm.language_model.get_output_embeddings()

    def set_vae(self, vae):
        """Set the VAE module (loaded externally from diffusers)."""
        self.vae = vae

    def init_special_tokens(self, tokenizer):
        """Initialize special token IDs from the tokenizer.

        Must be called before forward() if using special token embeddings.
        """
        from .vlm.constants import SPECIAL_TOKEN_LIST

        self.vlm.special_token_id_list = [
            tokenizer.convert_tokens_to_ids(tok) for tok in SPECIAL_TOKEN_LIST
        ]
        # Set key token IDs
        self.vlm.img_context_token_id = tokenizer.convert_tokens_to_ids("<IMG_CONTEXT>")
        self.vlm.img_start_token_id = tokenizer.convert_tokens_to_ids("<img>")
        self.vlm.img_end_token_id = tokenizer.convert_tokens_to_ids("</img>")
        self.vlm.img_uncond_token_id = tokenizer.convert_tokens_to_ids("<img_uncond>")
        self._special_token_ids_initialized = True

    def forward(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        pixel_values: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        image_flags: Optional[torch.LongTensor] = None,
        image_grid_thw: Optional[torch.LongTensor] = None,
        output_hidden_states: bool = False,
        **kwargs,
    ) -> Union[Tuple, CausalLMOutputWithPast, SimpleNamespace]:
        """Forward pass for training.

        For understanding-only training: returns CausalLMOutputWithPast with .loss (CE).
        For unified training: returns SimpleNamespace with .ce_loss and .mse_loss.

        Args:
            input_ids: Token IDs, shape [B, N].
            attention_mask: Attention mask, shape [B, N].
            pixel_values: Image pixels for understanding (ViT input), shape [B, C, H, W] or [B*npatch, C, H, W].
            labels: Label IDs for CE loss, shape [B, N].
            image_flags: Flags indicating which images are used, shape [B, 1].
            image_grid_thw: Grid metadata for dynamic resolution images.
            output_hidden_states: Whether to return LLM hidden states.
        """
        # Ensure special tokens are initialized
        if not self._special_token_ids_initialized and self.vlm.img_context_token_id is None:
            logger.warning("Special token IDs not initialized. Call init_special_tokens() first.")

        # Prepare image_flags default
        if image_flags is None and pixel_values is not None:
            num_images = pixel_values.shape[0]
            image_flags = torch.ones(num_images, 1, device=pixel_values.device, dtype=torch.long)
        elif image_flags is not None:
            image_flags = image_flags.reshape(-1, 1)

        # VLM forward
        vlm_outputs = self.vlm(
            pixel_values=pixel_values,
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
            image_flags=image_flags,
            image_grid_thw=image_grid_thw,
            output_hidden_states=output_hidden_states,
            return_dict=True,
        )

        return vlm_outputs

    @torch.no_grad()
    def generate_text(
        self,
        input_ids: torch.LongTensor,
        attention_mask: torch.Tensor,
        pixel_values: Optional[torch.FloatTensor] = None,
        generation_config=None,
        **kwargs,
    ) -> torch.LongTensor:
        """Understanding inference: autoregressive text generation.

        Args:
            input_ids: Token IDs, shape [B, N].
            attention_mask: Attention mask, shape [B, N].
            pixel_values: Image pixels for understanding.
            generation_config: HuggingFace GenerationConfig.

        Returns:
            Generated token IDs, shape [B, N+new_tokens].
        """
        return self.vlm.generate(
            pixel_values=pixel_values,
            input_ids=input_ids,
            attention_mask=attention_mask,
            generation_config=generation_config,
            **kwargs,
        )

    @torch.no_grad()
    def generate_hidden_states(
        self,
        input_ids: torch.LongTensor,
        attention_mask: torch.Tensor,
        pixel_values: Optional[torch.FloatTensor] = None,
    ) -> CausalLMOutputWithPast:
        """Forward pass returning hidden states (for generation conditioning).

        Returns:
            CausalLMOutputWithPast with .hidden_states containing all layer hidden states.
        """
        return self.vlm.generate_hidden_states(
            pixel_values=pixel_values,
            input_ids=input_ids,
            attention_mask=attention_mask,
        )

    def load_weights_from_checkpoint(self, checkpoint_path: str):
        """Load weights from a multi-directory InternVL-U checkpoint.

        The checkpoint has:
          vlm/model.safetensors
          generation_decoder/model.safetensors
          vae/diffusion_pytorch_model.safetensors
        """
        from safetensors.torch import load_file

        # Load VLM weights
        vlm_weights_path = os.path.join(checkpoint_path, "vlm", "model.safetensors")
        if os.path.exists(vlm_weights_path):
            vlm_state_dict = load_file(vlm_weights_path)
            # VLM weights are saved as top-level keys; add "vlm." prefix
            prefixed = {f"vlm.{k}": v for k, v in vlm_state_dict.items()}
            missing, unexpected = self.load_state_dict(prefixed, strict=False)
            logger.info(f"Loaded VLM weights: {len(vlm_state_dict)} keys, "
                        f"missing={len(missing)}, unexpected={len(unexpected)}")

        # Load generation decoder weights
        gen_weights_path = os.path.join(checkpoint_path, "generation_decoder", "model.safetensors")
        if os.path.exists(gen_weights_path):
            gen_state_dict = load_file(gen_weights_path)
            prefixed = {f"generation_decoder.{k}": v for k, v in gen_state_dict.items()}
            missing, unexpected = self.load_state_dict(prefixed, strict=False)
            logger.info(f"Loaded generation decoder weights: {len(gen_state_dict)} keys, "
                        f"missing={len(missing)}, unexpected={len(unexpected)}")

        # VAE weights are loaded separately via diffusers
        vae_weights_path = os.path.join(checkpoint_path, "vae", "diffusion_pytorch_model.safetensors")
        if os.path.exists(vae_weights_path) and self.vae is not None:
            vae_state_dict = load_file(vae_weights_path)
            self.vae.load_state_dict(vae_state_dict, strict=False)
            logger.info(f"Loaded VAE weights: {len(vae_state_dict)} keys")
