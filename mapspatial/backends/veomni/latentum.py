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
        """Call model.answer() — official image preprocessing + generation.

        Handles multiple images: when more than one image is present (e.g.
        external_draw restart with original map + generated image), all
        images are passed to internvl.chat() with <image> placeholders.
        """
        input_list = to_interleave_list(msg)
        text_parts = [item for item in input_list if isinstance(item, str)]
        images = [item for item in input_list if not isinstance(item, str)]
        prompt = strip_placeholders("\n".join(text_parts))

        max_new_tokens = gen_kw.get("max_new_tokens", self._max_new_tokens)
        do_sample = gen_kw.get("do_sample", self._do_sample)
        temperature = gen_kw.get("temperature", self._temperature)

        if images:
            if len(images) == 1:
                # Single image — use official answer() directly
                response = self._model.answer(
                    images[0],
                    prompt,
                    max_new_tokens=max_new_tokens,
                    do_sample=do_sample,
                    temperature=temperature,
                )
            else:
                # Multiple images — call internvl.chat() directly
                from model.latentum.image_utils import load_image as _load_img
                pv_list = []
                for img in images:
                    pv = _load_img(img, mode="RGB", max_num_patches=1)
                    pv_list.append(pv)
                pixel_values = torch.cat(pv_list, dim=0).to(
                    self._device, dtype=next(self._model.internvl.parameters()).dtype,
                )
                # Prepend <image> placeholder for each image
                question = ("<image>\n" * len(images)) + prompt
                generation_config = {
                    "max_new_tokens": max_new_tokens,
                    "do_sample": do_sample,
                    "temperature": temperature,
                }
                response = self._model.internvl.chat(
                    self._model.tokenizer,
                    pixel_values,
                    question,
                    generation_config,
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
        """Generate an image via official model.generate_latents + decoder.

        If context images are present, uses generate_latents_with_images()
        for image-conditioned generation (I2I). Otherwise falls back to
        text-only generate_latents() (T2I).
        """
        text_parts = []
        context_images = []
        for item in context:
            if item["type"] == "text":
                text_parts.append(item["value"])
            elif item["type"] == "image":
                v = item["value"]
                if isinstance(v, (Path, str)):
                    from ...media import load_image as _load_pil
                    v = _load_pil(v)
                context_images.append(v)

        context_text = "\n".join(text_parts)
        full_prompt = f"{context_text}\n{instruction}" if context_text else instruction

        cfg_scale = kw.get("cfg_scale", self._cfg_scale)
        temperature = kw.get("temperature", self._draw_temperature)
        seed = kw.get("seed", 42)

        with torch.no_grad():
            if context_images and hasattr(self._model, 'generate_latents_with_images'):
                # Image-conditioned generation (I2I)
                latents = self._model.generate_latents_with_images(
                    context_images,
                    full_prompt,
                    num_images_per_prompt=1,
                    cfg_scale=cfg_scale,
                    temperature=temperature,
                    seed=seed,
                )
            else:
                # Text-only generation (T2I) — no context images
                latents = self._model.generate_latents(
                    full_prompt,
                    num_images_per_prompt=1,
                    cfg_scale=cfg_scale,
                    temperature=temperature,
                    seed=seed,
                )

        # Decode latents to image using external decoder if available.
        # The decoder is a sibling checkpoint (e.g. LatentUM-Decoder), not a
        # subdirectory of the main model.  Follow the official generate_images()
        # pipeline: convert latent token IDs to continuous features via the
        # quantizer, then call decoder.decode() which runs SD3.5 + VAE.
        decoder_path = self._cfg.backend_args.get("decoder_path", "")
        if decoder_path:
            from model.latentum.modeling_latentum import LatentUMDecoderModel
            decoder = LatentUMDecoderModel.from_pretrained(
                decoder_path, device=self._device, dtype=torch.bfloat16,
            )
            decoder = decoder.eval()
            # Official pipeline: indices_to_feature → decoder.decode → [PIL]
            z_q, _ = self._model.quantizer.indices_to_feature(
                latents.to(self._device),
            )
            images = decoder.decode(z_q, seed=seed)
            return images[0]

        raise RuntimeError("No decoder available for image generation")
