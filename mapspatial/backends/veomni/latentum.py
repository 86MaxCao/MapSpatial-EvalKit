"""LatentUM backend — wraps official LatentUMModel.

Uses the official inference API (model.answer) for understanding, which
handles image preprocessing (448×448 + ImageNet normalization), vision
feature extraction (pixel-shuffle + mlp1), <IMG_CONTEXT> token injection,
InternVL2.5 chat template, and LLM generate with KV cache.
"""

from __future__ import annotations

import os
import sys
import torch
from pathlib import Path
from PIL import Image
from typing import ClassVar

from ...types import Capabilities, Message, Prediction
from ...config import BackendConfig
from ...compat import apply as apply_compat
from ...messages import to_interleave_list, strip_placeholders
from ..base import Backend

# Official LatentUM repo root
_OFFICIAL_REPO = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/LatentUM"


class LatentUMBackend(Backend):
    """LatentUM backend using official model.answer() for understanding."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False,
        draw=True,
        native_interleave=False,
        max_images=24,
        video=False,
    )
    COMPAT: ClassVar[tuple[str, ...]] = ()

    def __init__(self, cfg: BackendConfig) -> None:
        for var in ("WORLD_SIZE", "RANK", "LOCAL_RANK"):
            os.environ.pop(var, None)

        apply_compat(*self.COMPAT)

        self._cfg = cfg
        model_path = cfg.model_path
        device = cfg.load.get("device", "cuda")
        dtype = cfg.load.get("dtype", "bfloat16")
        dt = getattr(torch, dtype)

        # Load via official LatentUMModel.from_pretrained
        if _OFFICIAL_REPO not in sys.path:
            sys.path.insert(0, _OFFICIAL_REPO)
        from model.latentum import LatentUMModel

        self._model = LatentUMModel.from_pretrained(model_path, device=device, dtype=dt)
        self._model.eval()
        self._device = device

        # Apply attention implementation override from YAML (load.attn_implementation).
        # Used to force 'sdpa' to avoid the transformers 5.x flash_attention_2
        # degenerate-output bug ("A!!!..."). Only the Qwen3 LLM is patched; the
        # InternViT vision encoder is unaffected (its own attn impl is separate).
        attn_impl = cfg.load.get("attn_implementation")
        if attn_impl:
            llm = self._model.internvl.language_model
            llm.config._attn_implementation = attn_impl
            for _layer in llm.model.layers:
                _layer.self_attn.config._attn_implementation = attn_impl

        # Generation params
        gen = cfg.generate
        self._temperature = gen.get("temperature", 0.2)
        self._max_new_tokens = gen.get("max_new_tokens", 512)
        self._do_sample = gen.get("do_sample", False)

        # Draw params
        ba = cfg.backend_args
        self._cfg_scale = ba.get("cfg_scale", 3.0)
        self._draw_temperature = ba.get("draw_temperature", 0.9)

        # System prompt
        self._system_prompt = cfg.system_prompt or None

    @property
    def model_name(self) -> str:
        return self._cfg.name

    # ------------------------------------------------------------------
    # understand()
    # ------------------------------------------------------------------

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        """Understanding via official model.answer() — handles full pipeline."""
        results: list[Prediction] = []
        for msg in messages:
            try:
                text = self._understand_one(msg, gen_kw)
                results.append(Prediction(text=text))
            except Exception as e:
                results.append(Prediction(error=str(e)))
        return results

    def _understand_one(self, msg: Message, gen_kw: dict) -> str:
        """Call model.answer() — official image preprocessing + generation."""
        input_list = to_interleave_list(msg)
        text_parts = [item for item in input_list if isinstance(item, str)]
        images = [item for item in input_list if not isinstance(item, str)]
        prompt = strip_placeholders("\n".join(text_parts))

        max_new_tokens = gen_kw.get("max_new_tokens", self._max_new_tokens)
        do_sample = gen_kw.get("do_sample", self._do_sample)
        temperature = gen_kw.get("temperature", self._temperature)

        if images:
            # Official answer(): load_image (448×448 + ImageNet norm) +
            # internvl.chat (extract_feature + <IMG_CONTEXT> + generate)
            response = self._model.answer(
                images[0],
                prompt,
                max_new_tokens=max_new_tokens,
                do_sample=do_sample,
                temperature=temperature,
            )
        else:
            # Text-only: use internvl.chat without pixel_values
            generation_config = {
                "max_new_tokens": max_new_tokens,
                "do_sample": do_sample,
                "temperature": temperature,
            }
            response = self._model.internvl.chat(
                self._model.tokenizer,
                None,
                prompt,
                generation_config,
            )

        return response.strip() if response else ""

    # ------------------------------------------------------------------
    # draw()
    # ------------------------------------------------------------------

    def draw(self, context: Message, instruction: str, **kw):
        """Generate an image via official model.generate_latents + decoder."""
        text_parts = []
        for item in context:
            if item["type"] == "text":
                text_parts.append(item["value"])

        context_text = "\n".join(text_parts)
        full_prompt = f"{context_text}\n{instruction}" if context_text else instruction

        cfg_scale = kw.get("cfg_scale", self._cfg_scale)
        temperature = kw.get("temperature", self._draw_temperature)

        with torch.no_grad():
            latents = self._model.generate_latents(
                full_prompt,
                num_images_per_prompt=1,
                cfg_scale=cfg_scale,
                temperature=temperature,
                seed=kw.get("seed", 42),
            )

        # Decode latents to image using external decoder if available
        decoder_path = self._cfg.backend_args.get("decoder_path", "")
        if decoder_path:
            from model.latentum.modeling_latentum import LatentUMDecoderModel
            decoder = LatentUMDecoderModel.from_pretrained(decoder_path, dtype=torch.bfloat16)
            decoder = decoder.to(self._device).eval()
            image = decoder(latents)
            return image

        raise RuntimeError("No decoder available for image generation")
