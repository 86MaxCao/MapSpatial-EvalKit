"""LatentUM backend — wraps VeOmni LatentUMModel.

Implements understand() and draw() for the LatentUM unified model.
LatentUM uses InternVL vision encoder + LLM for understanding, and a
VQ-GAN codebook + pixel decoder for image generation.

Strategy mapping:
  direct           → understand() (text-only, no image generation)
  external_draw    → understand() + draw() (text + separate image gen)
"""

from __future__ import annotations

import os
import time
import torch
from pathlib import Path
from PIL import Image
from typing import ClassVar

from ...types import Capabilities, Message, Prediction, TraceStep
from ...config import BackendConfig
from ...compat import apply as apply_compat
from ...messages import to_interleave_list, to_placeholder_prompt, strip_placeholders
from ...media import load_image
from ..base import Backend


class LatentUMBackend(Backend):
    """LatentUM (LatentUMModel) backend with understand + draw."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False,            # serial loop, one sample at a time
        draw=True,              # VQ-GAN codebook + pixel decoder generation
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

        # Load model via our own loader
        from ...loader import load_model, load_tokenizer
        from ...vendor.latentum.modeling_latentum import LatentUMModel

        (self._model, _) = load_model(
            model_path, LatentUMModel,
            device=device, dtype=dtype,
        )
        self._tokenizer = load_tokenizer(model_path)

        self._device = device

        # LatentUM needs a separate pixel decoder path
        self._decoder_path = cfg.backend_args.get("decoder_path", "")

        # Load the pixel decoder if path is provided
        self._pixel_decoder = None
        if self._decoder_path:
            self._pixel_decoder = self._load_pixel_decoder(self._decoder_path)

        # Generation params from config
        gen = cfg.generate
        self._temperature = gen.get("temperature", 0.3)
        self._max_new_tokens = gen.get("max_new_tokens", 1024)

        # Draw params from backend_args
        ba = cfg.backend_args
        self._cfg_scale = ba.get("cfg_scale", 3.0)
        self._draw_temperature = ba.get("draw_temperature", 0.9)

        # System prompt
        self._system_prompt = cfg.system_prompt or None

    @property
    def model_name(self) -> str:
        return self._cfg.name

    def _load_pixel_decoder(self, decoder_path: str):
        """Load the pixel decoder (VQ-GAN decoder) from a separate checkpoint.

        NOTE: exact loading mechanism needs verification at runtime.
        LatentUM may store the decoder as a separate torch checkpoint.
        """
        import torch

        try:
            decoder = torch.load(decoder_path, map_location=self._device)
            if hasattr(decoder, "eval"):
                decoder.eval()
            return decoder
        except Exception:
            # Fallback: the decoder may be embedded in the main model
            return getattr(self._model, "pixel_decoder", None)

    # ------------------------------------------------------------------
    # understand()
    # ------------------------------------------------------------------

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        """Text-only understanding via InternVL vision encoder + LLM generate.

        Serial loop: one Message at a time.
        """
        results: list[Prediction] = []
        for msg in messages:
            try:
                text = self._understand_one(msg, gen_kw)
                results.append(Prediction(text=text))
            except Exception as e:
                results.append(Prediction(error=str(e)))
        return results

    def _understand_one(self, msg: Message, gen_kw: dict) -> str:
        """Single-sample understanding matching VeOmni infer_latentum_understand."""
        import numpy as np

        device = self._device
        model = self._model
        tokenizer = self._tokenizer

        # Extract text and images
        input_list = to_interleave_list(msg)
        text_parts = [item for item in input_list if isinstance(item, str)]
        images = [item for item in input_list if not isinstance(item, str)]
        prompt = "\n".join(text_parts)
        prompt = strip_placeholders(prompt)

        # Build chat template (VeOmni convention -- no system prompt)
        text = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        input_ids = tokenizer.encode(text, return_tensors="pt").to(device)

        # Access InternVL sub-module
        internvl = model.internvl
        lm = internvl.language_model  # Qwen3MoTForCausalLM

        embed_layer = lm.get_input_embeddings()
        inputs_embeds = embed_layer(input_ids[0])  # [T, D]

        if images:
            # Preprocess: pil_img2rgb -> resize_image(448, 224, 14) -> /255.0 -> bf16
            pixel_values = self._prepare_vision_input(images, device)  # [1, 3, H, W]

            with torch.no_grad():
                vit_features = internvl.vision_model(pixel_values)
                vit_projected = internvl.mlp1(vit_features)  # [1, L, D_llm]

            # Prepend vision features to text embeddings
            inputs_embeds = torch.cat(
                [vit_projected.squeeze(0), inputs_embeds], dim=0,
            )  # [L+T, D]

        # Greedy decoding loop — LatentUM uses model._llm_forward (not lm.model)
        max_new_tokens = gen_kw.get("max_new_tokens", self._max_new_tokens)
        eos_id = tokenizer.eos_token_id
        output_layer = lm.lm_head  # model.internvl.language_model.lm_head
        generated = []
        dtype = next(model.parameters()).dtype

        with torch.no_grad():
            for _ in range(max_new_tokens):
                vision_mask = torch.zeros(1, inputs_embeds.shape[0],
                                          device=device, dtype=dtype)
                hidden = model._llm_forward(
                    inputs_embeds.unsqueeze(0),
                    vision_token_mask=vision_mask,
                )
                logits = output_layer(hidden[:, -1:, :])
                next_id = logits[0, -1].argmax(dim=-1).item()
                if next_id == eos_id:
                    break
                generated.append(next_id)
                next_embed = embed_layer(
                    torch.tensor([[next_id]], device=device),
                )
                inputs_embeds = torch.cat(
                    [inputs_embeds, next_embed[0]], dim=0,
                )

        text = tokenizer.decode(generated, skip_special_tokens=True)
        return text.strip()

    @staticmethod
    def _pil_img2rgb(img):
        """Convert PIL image to RGB."""
        if img.mode != "RGB":
            img = img.convert("RGB")
        return img

    @staticmethod
    def _resize_image(img, max_size=448, min_size=224, patch_size=14):
        """Resize image so dimensions are divisible by patch_size,
        bounded by [min_size, max_size]."""
        w, h = img.size
        scale = min(max_size / max(w, h), 1.0)
        scale = max(scale, min_size / min(w, h))

        def _make_divisible(v, s):
            return max(s, int(round(v / s) * s))

        new_w = _make_divisible(round(w * scale), patch_size)
        new_h = _make_divisible(round(h * scale), patch_size)
        return img.resize((new_w, new_h), Image.BICUBIC)

    def _prepare_vision_input(self, pil_images, device):
        """Preprocess images: resize -> /255.0 -> bf16 -> (N, 3, H, W)."""
        import numpy as np
        tensors = []
        for img in pil_images:
            img = self._pil_img2rgb(img)
            img = self._resize_image(img, 448, 224, 14)
            tensor = torch.tensor(np.array(img)).permute(2, 0, 1).float() / 255.0
            tensors.append(tensor)
        pixel_values = torch.stack(tensors).to(device)
        pixel_values = pixel_values.to(dtype=next(self._model.parameters()).dtype)
        return pixel_values

    # ------------------------------------------------------------------
    # draw()
    # ------------------------------------------------------------------

    def draw(self, context: Message, instruction: str, **kw):
        """Generate an image using VQ-GAN codebook + pixel decoder.

        Flow:
          1. Build prompt from context + instruction
          2. model.generate_latents(tokenizer, prompt, cfg_scale, temperature)
             → codebook indices
          3. model.quantizer.indices_to_feature(indices) → continuous features
          4. Run pixel decoder to reconstruct image
          5. Convert to PIL Image
        """
        import torch
        from PIL import Image

        # Build prompt from context + instruction
        text_parts = []
        for item in context:
            if item["type"] == "text":
                text_parts.append(item["value"])

        context_text = "\n".join(text_parts)
        full_prompt = f"{context_text}\n{instruction}" if context_text else instruction

        # Draw params (overridable via kw)
        cfg_scale = kw.get("cfg_scale", self._cfg_scale)
        temperature = kw.get("temperature", self._draw_temperature)

        # Step 1: Generate codebook indices via model.generate_latents
        # NOTE: exact signature needs verification at runtime
        with torch.no_grad():
            indices = self._model.generate_latents(
                self._tokenizer,
                full_prompt,
                cfg_scale=cfg_scale,
                temperature=temperature,
            )  # [B, L] codebook indices

        # Step 2: Convert indices to continuous features via quantizer
        # NOTE: model.quantizer.indices_to_feature may need verification
        with torch.no_grad():
            features = self._model.quantizer.indices_to_feature(indices)  # [B, L, D]

        # Step 3: Run pixel decoder to reconstruct the image
        # NOTE: decoder may be self._pixel_decoder or model.pixel_decoder
        decoder = self._pixel_decoder or getattr(self._model, "pixel_decoder", None)
        if decoder is None:
            raise RuntimeError("No pixel decoder available for image generation")

        with torch.no_grad():
            image_tensor = decoder(features)  # [1, 3, H, W]

        # Convert to PIL Image
        # Denormalize from [-1, 1] to [0, 1]
        image_tensor = image_tensor.clamp(-1, 1)
        image_tensor = image_tensor * 0.5 + 0.5
        image_tensor = image_tensor.cpu().squeeze(0)  # [3, H, W]

        image_np = (image_tensor.permute(1, 2, 0).numpy() * 255).astype("uint8")
        pil_image = Image.fromarray(image_np)
        return pil_image
