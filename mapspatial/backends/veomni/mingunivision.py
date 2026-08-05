"""MingUniVision backend — wraps VeOmni MingUniVisionForConditionalGeneration.

Implements all three backend methods:
  - understand(): text understanding via model.generate() with image inputs
  - draw(): image generation via unified generate() with image-gen tokens
  - interleave(): native token-level interleaving via model.generate()

MingUniVision is a unified architecture that handles both understanding and
generation through a single BailingMoe backbone with a diffusion loss head.
The model's unified generate() automatically routes between text and image
generation based on token patterns.

Strategy mapping:
  direct              → understand()
  native_interleave   → interleave() (native token-level interleaving)
  external_draw       → understand() + draw()
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import ClassVar

from ...types import Capabilities, Message, Prediction, TraceStep
from ...config import BackendConfig
from ...compat import apply as apply_compat
from ...messages import to_interleave_list, to_placeholder_prompt, strip_placeholders
from ...media import load_image
from ..base import Backend


class MingUniVisionBackend(Backend):
    """MingUniVision backend with native interleaved understanding + generation."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False,              # serial inference only
        draw=True,                # unified generate() supports image generation
        native_interleave=True,   # native token-level interleaving
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
        from ...loader import load_model, load_processor

        _MingModel = None
        try:
            from ...vendor.mingunivision.modeling_mingunivision import (
                MingUniVisionForConditionalGeneration as _MingModel,
            )
        except ImportError:
            try:
                from ...vendor.mingunivision.modeling_mingunivision import (
                    MingUniVisionVeOmniModel as _MingModel,
                )
            except ImportError:
                _MingModel = None

        if _MingModel is not None:
            (self._model, _) = load_model(
                model_path, _MingModel,
                device=device, dtype=dtype,
            )
        else:
            print("WARNING: vendored MingUniVision model not found; "
                  "self._model will be None")
            self._model = None

        self._processor = load_processor(model_path)
        self._mingtok = cfg.backend_args.get("mingtok", "<|image_gen|>")

        self._device = device

        # Generation params from config
        gen = cfg.generate
        self._temperature = gen.get("temperature", 0.0)
        self._max_new_tokens = gen.get("max_new_tokens", 512)

        # Draw params from backend_args
        ba = cfg.backend_args
        self._guidance_scale = ba.get("guidance_scale", 4.0)
        self._num_timesteps = ba.get("num_timesteps", 50)
        self._image_size = ba.get("image_size", 1024)

        # Interleave params
        self._max_rounds = cfg.backend_args.get("max_rounds", 3)

        # System prompt
        self._system_prompt = cfg.system_prompt or None

    @property
    def model_name(self) -> str:
        return self._cfg.name

    # ------------------------------------------------------------------
    # understand()
    # ------------------------------------------------------------------

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        """Text-only understanding via model.generate().

        Uses the processor to build input_ids + pixel_values from text + images,
        then calls model.generate() for text output.
        """
        results = []
        for msg in messages:
            try:
                text = self._understand_one(msg, gen_kw)
                results.append(Prediction(text=text))
            except Exception as e:
                results.append(Prediction(error=str(e)))
        return results

    def _understand_one(self, msg: Message, gen_kw: dict) -> str:
        """Single-sample understanding via model.generate()."""
        import torch

        # Convert message to interleave list [PIL, str, PIL, str, ...]
        input_list = to_interleave_list(msg)

        # Extract text and images
        text_parts = [item for item in input_list if isinstance(item, str)]
        images = [item for item in input_list if not isinstance(item, str)]
        prompt = "\n".join(text_parts)
        if self._system_prompt:
            prompt = f"{self._system_prompt}\n{prompt}"

        max_new_tokens = gen_kw.get("max_new_tokens", self._max_new_tokens)
        temperature = gen_kw.get("temperature", self._temperature)
        do_sample = temperature > 0

        with torch.no_grad():
            # --- Build inputs via processor ---
            # The processor handles text tokenization + image preprocessing
            # and returns input_ids, pixel_values (and attention_mask).
            # NOTE: exact processor call signature may need runtime verification.
            if images:
                inputs = self._processor(
                    text=prompt, images=images, return_tensors="pt",
                )
            else:
                inputs = self._processor(
                    text=prompt, return_tensors="pt",
                )

            # Move to device
            inputs = {
                k: v.to(self._device) if hasattr(v, "to") else v
                for k, v in inputs.items()
            }

            # --- Generate text ---
            # MingUniVision's unified generate() handles understanding when
            # no image-generation tokens are present in the input.
            input_ids = inputs.get("input_ids")
            pixel_values = inputs.get("pixel_values")

            output_ids = self._model.generate(
                input_ids=input_ids,
                pixel_values=pixel_values,
                max_new_tokens=max_new_tokens,
                do_sample=do_sample,
                temperature=temperature or 1.0,
            )

        # Decode generated token IDs to text
        # Strip the input portion if the model returns the full sequence
        input_len = input_ids.shape[1] if input_ids is not None else 0
        new_ids = output_ids[0, input_len:]
        text = self._processor.decode(new_ids, skip_special_tokens=True)
        return text

    # ------------------------------------------------------------------
    # draw()
    # ------------------------------------------------------------------

    def draw(self, context: Message, instruction: str, **kw) -> "Image.Image":
        """Generate an image via unified model.generate() with image-gen tokens.

        MingUniVision's unified generate() can produce image generation tokens
        when the prompt includes the appropriate trigger token. The BailingMoe
        backbone with diffloss handles the text→image decoding internally.
        """
        import torch
        from PIL import Image

        # Build the text prompt for image generation
        input_list = to_interleave_list(context)
        text_parts = [item for item in input_list if isinstance(item, str)]
        context_text = "\n".join(text_parts)
        prompt = f"{context_text}\n{instruction}" if context_text else instruction

        guidance_scale = kw.get("guidance_scale", self._guidance_scale)
        num_timesteps = kw.get("num_timesteps", self._num_timesteps)
        image_size = kw.get("image_size", self._image_size)

        with torch.no_grad():
            # --- Build inputs via processor ---
            # Append the image-generation trigger token (mingtok) to the prompt.
            # mingtok marks the transition from understanding to generation.
            # NOTE: exact token / processor convention may need runtime verification.
            gen_prompt = f"{prompt} {self._mingtok}"

            inputs = self._processor(
                text=gen_prompt, return_tensors="pt",
            )
            inputs = {
                k: v.to(self._device) if hasattr(v, "to") else v
                for k, v in inputs.items()
            }

            # --- Generate with image-gen mode ---
            # The model's unified generate() detects the image-gen token and
            # routes through BailingMoe + diffloss to produce an image.
            # Returns image tokens or direct pixel output depending on the
            # model version.
            output = self._model.generate(
                input_ids=inputs.get("input_ids"),
                pixel_values=None,  # no conditioning image for generation
                max_new_tokens=kw.get("max_new_tokens", 256),
                do_sample=False,
                guidance_scale=guidance_scale,
                num_inference_steps=num_timesteps,
                image_size=image_size,
            )

        # --- Extract generated image ---
        # MingUniVision may return a PIL Image directly, or a tensor
        # that needs conversion. Check the output type.
        if isinstance(output, Image.Image):
            return output

        # If output is a tensor (B, C, H, W), convert to PIL
        if hasattr(output, "shape") and len(output.shape) == 4:
            import numpy as np
            pixels = (output[0].clamp(-1, 1) + 1) / 2
            pixels = (pixels.cpu().permute(1, 2, 0).numpy() * 255).astype("uint8")
            return Image.fromarray(pixels)

        # If output is a list, look for an image
        if isinstance(output, (list, tuple)):
            for item in output:
                if isinstance(item, Image.Image):
                    return item
                if hasattr(item, "shape") and len(item.shape) == 4:
                    import numpy as np
                    pixels = (item[0].clamp(-1, 1) + 1) / 2
                    pixels = (pixels.cpu().permute(1, 2, 0).numpy() * 255).astype("uint8")
                    return Image.fromarray(pixels)

        raise RuntimeError("MingUniVision draw() did not produce an image")

    # ------------------------------------------------------------------
    # interleave()
    # ------------------------------------------------------------------

    def interleave(
        self,
        message: Message,
        *,
        max_rounds: int = 3,
        marker: str = "<image_start>",
        **kw,
    ) -> Prediction:
        """Native interleaved reasoning loop.

        MingUniVision has native token-level interleaving: the model's unified
        generate() can produce mixed text + image tokens in a single pass.
        The BailingMoe backbone routes between text and image heads based on
        the token type at each position.
        """
        import torch
        from PIL import Image

        # Convert Message to interleave input list
        input_list = to_interleave_list(message)

        # Build the full prompt from interleave list
        text_parts = [item for item in input_list if isinstance(item, str)]
        images = [item for item in input_list if not isinstance(item, str)]
        prompt = "\n".join(text_parts)
        if self._system_prompt:
            prompt = f"{self._system_prompt}\n{prompt}"

        max_new_tokens = kw.get("max_new_tokens", self._max_new_tokens)
        guidance_scale = kw.get("guidance_scale", self._guidance_scale)
        num_timesteps = kw.get("num_timesteps", self._num_timesteps)

        trace: list[TraceStep] = []
        t0 = time.time()

        with torch.no_grad():
            # --- Build inputs via processor ---
            if images:
                inputs = self._processor(
                    text=prompt, images=images, return_tensors="pt",
                )
            else:
                inputs = self._processor(
                    text=prompt, return_tensors="pt",
                )
            inputs = {
                k: v.to(self._device) if hasattr(v, "to") else v
                for k, v in inputs.items()
            }

            # --- Native interleaved generation ---
            # The model generates text and image tokens in a single forward pass.
            # When it encounters the image-gen trigger token, it switches to the
            # BailingMoe + diffloss path to produce an image, then continues
            # text generation. This gives true token-level interleaving.
            output = self._model.generate(
                input_ids=inputs.get("input_ids"),
                pixel_values=inputs.get("pixel_values"),
                max_new_tokens=max_new_tokens,
                do_sample=kw.get("temperature", self._temperature) > 0,
                temperature=kw.get("temperature", self._temperature) or 1.0,
                guidance_scale=guidance_scale,
                num_inference_steps=num_timesteps,
                interleaved=True,  # enable native interleaved output
            )

        elapsed = time.time() - t0

        # --- Parse output ---
        # The model may return a mixed list of text strings and PIL images,
        # or a structured output. Parse accordingly.
        text_parts_out = []
        generated_images = []
        round_num = 0

        if isinstance(output, (list, tuple)):
            for item in output:
                if isinstance(item, str):
                    trace.append(TraceStep(
                        round=round_num, kind="text",
                        text=item,
                        triggered_by=None,
                        elapsed_s=elapsed / max(len(output), 1),
                    ))
                    text_parts_out.append(item)
                    if marker in item:
                        round_num += 1
                elif isinstance(item, Image.Image):
                    trace.append(TraceStep(
                        round=round_num, kind="image",
                        triggered_by="model_marker",
                        elapsed_s=elapsed / max(len(output), 1),
                    ))
                    generated_images.append(item)
        elif isinstance(output, str):
            text_parts_out.append(output)
            trace.append(TraceStep(
                round=0, kind="text",
                text=output,
                triggered_by=None,
                elapsed_s=elapsed,
            ))
        elif isinstance(output, Image.Image):
            generated_images.append(output)
            trace.append(TraceStep(
                round=0, kind="image",
                triggered_by="model_marker",
                elapsed_s=elapsed,
            ))

        final_text = text_parts_out[-1] if text_parts_out else ""

        return Prediction(
            text=final_text,
            generated_images=generated_images,
            trace=trace,
            meta={
                "rounds": round_num,
                "draw_triggered": len(generated_images) > 0,
            },
        )
