import os
from typing import Any

import torch
from transformers import AutoModel, AutoTokenizer

from models.sensenova_si.model import Model
from models.sensenova_si.utils import load_image, reorganize_prompt, split_model


class SenseNovaSIInternVLModel(Model):
    def __init__(
        self,
        model_path: str,
        generation_config: dict[str, Any] | str | os.PathLike | None = None,
    ):
        super().__init__(generation_config)
        self.device_map = split_model(model_path)
        # transformers 5.8: get_total_byte_count reads model.all_tied_weights_keys
        # (renamed from _tied_weights_keys); InternVLChatModel remote code lacks it.
        # Patch get_total_byte_count to default the attribute when missing.
        import transformers.modeling_utils as _mu
        _orig_get_total = getattr(_mu, "get_total_byte_count", None)
        if _orig_get_total and not getattr(_orig_get_total, "_spatial_patched", False):
            def _safe_get_total(model, *a, **kw):
                if not hasattr(model, "all_tied_weights_keys"):
                    model.all_tied_weights_keys = {}
                return _orig_get_total(model, *a, **kw)
            _safe_get_total._spatial_patched = True
            _mu.get_total_byte_count = _safe_get_total
        self.model = AutoModel.from_pretrained(
            model_path,
            dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
            device_map=self.device_map,
        ).eval()

        # transformers 5.8: flash_attention_2 has a causal-mask bug — output
        # degenerates to repeated token-0 ("A!!!..."). Force SDPA on the LLM
        # (explicit 4D causal mask). See docs/latentum-transformers5-flash-attn-bug.md.
        llm = self.model.language_model
        llm.config._attn_implementation = "sdpa"
        for layer in llm.model.layers:
            layer.self_attn.config._attn_implementation = "sdpa"

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path, trust_remote_code=True, use_fast=False
        )

        self.max_num_per_image = 6
        self.total_max_num = 64

    def generate(self, question: str, images: list[str] | None = None, **kwargs) -> str:
        generation_config = self.default_generation_config.copy()
        generation_config.update(kwargs)

        # generate prompt
        message = []
        if images:
            for _ in images:
                message.append({"type": "image", "value": ""})
        message.append({"type": "text", "value": question})

        images_num = len(images) if images else 0

        prompt = reorganize_prompt(message, images_num)

        pixel_values, num_patches_list = None, []
        if images:
            pixel_values, num_patches_list = self.get_pixel_values(images)

        # print(generation_config)
        response = self.model.chat(
            self.tokenizer,
            pixel_values=pixel_values,
            num_patches_list=num_patches_list,
            question=prompt,
            generation_config=generation_config,
            history=None,
        )
        return response

    def get_pixel_values(self, image_paths):
        pixel_values_list = []
        num_patches_list = []

        # dynamic max number
        if len(image_paths) > 1:
            max_num = max(
                1, min(self.max_num_per_image, self.total_max_num // len(image_paths))
            )
        else:
            max_num = self.max_num_per_image

        print(f"Load {len(image_paths)} images...")
        for path in image_paths:
            print(f"Load image {path}...")
            try:
                pixel_values = (
                    load_image(path, max_num=max_num).to(torch.bfloat16).cuda()
                )
                num_patches_list.append(pixel_values.size(0))
                pixel_values_list.append(pixel_values)
            except Exception as e:
                print(f"Error loading image {path}: {e}")
                continue

        if len(pixel_values_list) > 1:
            pixel_values = torch.cat(pixel_values_list, dim=0)
        elif len(pixel_values_list) == 1:
            pixel_values = pixel_values_list[0]
        else:
            raise ValueError(f"No valid images found in {image_paths}")
        return pixel_values, num_patches_list
