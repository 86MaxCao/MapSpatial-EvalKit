"""Cambrian-S backend.

Ported from an internal predecessor evaluation codebase.
Also references VLMEvalKit vlm/cambrian_s.py (cleaner version).

Uses vendored cambrian package (vendor/cambrian/cambrian_pkg/).
LLaVA-style conv template + tokenizer_image_token + dynamic tiling.
"""

from __future__ import annotations

import os
from typing import ClassVar

from ..types import Capabilities, Message, Prediction
from ..config import BackendConfig
from ..compat import apply as apply_compat
from ..messages import to_placeholder_prompt, strip_placeholders
from ..media import load_image
from .base import Backend


class CambrianBackend(Backend):
    """Cambrian-S-7B-LFP backend."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False, draw=False, native_interleave=False,
        max_images=24, video=False,
    )

    MAX_NEW_TOKENS = 512
    CONV_TEMPLATE = "qwen_2"

    def __init__(self, cfg: BackendConfig) -> None:
        for var in ("WORLD_SIZE", "RANK", "LOCAL_RANK"):
            os.environ.pop(var, None)

        apply_compat(*self.COMPAT)

        self._cfg = cfg
        model_path = cfg.model_path
        device = cfg.load.get("device", "cuda:0")
        self._device = device if ":" in device else "cuda:0"

        # Import from vendored cambrian package
        from ..vendor.cambrian.cambrian_pkg.constants import IMAGE_TOKEN_INDEX
        from ..vendor.cambrian.cambrian_pkg.conversation import conv_templates
        from ..vendor.cambrian.cambrian_pkg.model.builder import load_pretrained_model
        from ..vendor.cambrian.cambrian_pkg.mm_utils import (
            tokenizer_image_token, process_images,
            get_model_name_from_path,
        )

        self._IMAGE_TOKEN_INDEX = IMAGE_TOKEN_INDEX
        self._conv_templates = conv_templates
        self._tokenizer_image_token = tokenizer_image_token
        self._process_images = process_images

        device_map = {"": self._device} if self._device.startswith("cuda") else self._device
        model_name = get_model_name_from_path(model_path)

        self._tokenizer, self._model, self._image_processor, _ = load_pretrained_model(
            model_path, None, model_name,
            device_map=device_map, device=self._device,
        )
        self._model.eval()
        self._model_name = model_name or cfg.name

    @property
    def model_name(self) -> str:
        return self._model_name

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        gen = {**self._cfg.generate, **gen_kw}
        results = []
        for msg in messages:
            try:
                text = self._infer_one(msg, gen)
                results.append(Prediction(text=text))
            except Exception as e:
                results.append(Prediction(error=str(e)))
        return results

    def _infer_one(self, msg: Message, gen: dict) -> str:
        import torch

        # Build placeholder prompt
        prompt_text, image_paths = to_placeholder_prompt(msg)
        clean_prompt = strip_placeholders(prompt_text)

        # Load images
        pil_images = [load_image(p) for p in image_paths]

        # Process images
        visual_tensors, visual_sizes = self._process_images(
            pil_images, self._image_processor, self._model.config
        )

        # Build conversation
        question = "\n".join(["<image>\n"] * len(pil_images)) + clean_prompt
        conv = self._conv_templates[self.CONV_TEMPLATE].copy()
        conv.append_message(conv.roles[0], question)
        conv.append_message(conv.roles[1], None)
        full_prompt = conv.get_prompt()

        input_ids = self._tokenizer_image_token(
            full_prompt, self._tokenizer, self._IMAGE_TOKEN_INDEX,
            return_tensors="pt",
        ).unsqueeze(0).to(self._device)

        # Fix tensor shapes: process_images returns [N, 1, C, H, W], we need [1, N, C, H, W]
        fixed_tensors = []
        for t in visual_tensors:
            if t.dim() == 5 and t.size(1) == 1:
                t = t.squeeze(1)
            if t.dim() == 4:
                t = t.unsqueeze(0)
            fixed_tensors.append(t.half().to(self._device))

        temperature = gen.get("temperature", 0.0)
        with torch.inference_mode():
            output_ids = self._model.generate(
                inputs=input_ids,
                images=fixed_tensors,
                image_sizes=visual_sizes,
                use_cache=True,
                do_sample=temperature > 0,
                temperature=temperature or 1.0,
                top_p=gen.get("top_p"),
                num_beams=1,
                max_new_tokens=gen.get("max_new_tokens", self.MAX_NEW_TOKENS),
            )

        return self._tokenizer.batch_decode(
            output_ids, skip_special_tokens=True
        )[0].strip()
