"""JoyAI backend — wraps two-component system (Qwen3VL + DiT EditModel Pipeline).

JoyAI uses a decoupled architecture:
  - Understanding: Qwen3VL (via und_model / und_processor)
  - Image Generation: DiT-based EditModel (via gen_model)

Implements two backend methods:
  - understand(): text understanding via und_model.generate()
  - draw(): image generation via gen_model.infer() with InferenceParams

No native interleave — use external_draw strategy for mixed text+image output.

Strategy mapping:
  direct              → understand()
  external_draw       → understand() + draw()
"""

from __future__ import annotations

import os
import time
import torch
from pathlib import Path
from typing import ClassVar

from ...types import Capabilities, Message, Prediction, TraceStep
from ...config import BackendConfig
from ...compat import apply as apply_compat
from ...messages import to_interleave_list, to_placeholder_prompt, strip_placeholders
from ...media import load_image
from ..base import Backend


class JoyAIBackend(Backend):
    """JoyAI backend with Qwen3VL understanding + DiT image generation."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False,             # serial inference only
        draw=True,               # can generate images via gen_model.infer()
        native_interleave=False,  # no native interleave (decoupled architecture)
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

        # Load understanding model from root path (has config.json + infer_config.py)
        from ...loader import load_model, load_processor, load_tokenizer
        from ...vendor.joyai_image.modeling_joyai_image import JoyAIImageModel

        und_path = os.path.join(model_path, "JoyAI-Image-Und")
        if not os.path.exists(und_path):
            und_path = model_path  # fallback to root

        # load_model needs root path: JoyAIImageConfig.from_pretrained reads
        # root config.json, and load_weights_from_checkpoint needs infer_config.py
        (self._und_model, _) = load_model(
            model_path, JoyAIImageModel,
            device=device, dtype=dtype,
        )
        self._und_processor = load_processor(und_path)
        self._tokenizer = load_tokenizer(und_path)

        # Load generation model via vendored build_model
        self._gen_model = None
        try:
            from ...vendor.joyai_image.infer_runtime.settings import load_settings
            from ...vendor.joyai_image.infer_runtime.model import build_model
            import torch
            settings = load_settings(ckpt_root=model_path)
            self._gen_model = build_model(
                settings, device=torch.device(device),
            )
        except Exception as e:
            print(f"WARNING: Failed to load JoyAI generation model: {e}")
            self._gen_model = None

        self._device = device

        # Generation params from config
        gen = cfg.generate
        self._temperature = gen.get("temperature", 0.0)
        self._max_new_tokens = gen.get("max_new_tokens", 512)

        # Draw params from backend_args
        ba = cfg.backend_args
        self._gen_height = ba.get("height", 1024)
        self._gen_width = ba.get("width", 1024)
        self._gen_steps = ba.get("steps", 50)
        self._gen_guidance = ba.get("guidance_scale", 7.5)
        self._gen_seed = ba.get("seed", 42)

        # System prompt
        self._system_prompt = cfg.system_prompt or None

    @property
    def model_name(self) -> str:
        return self._cfg.name

    # ------------------------------------------------------------------
    # understand()
    # ------------------------------------------------------------------

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        """Text-only understanding via und_model (Qwen3VL) generate().

        Uses und_processor to build inputs (input_ids, attention_mask,
        pixel_values), then calls und_model.generate() with greedy decoding.
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
        """Single-sample understanding matching VeOmni infer_joyai_image_understand."""
        from transformers import GenerationConfig

        device = self._device
        model = self._und_model
        processor = self._und_processor
        tokenizer = self._tokenizer

        # Extract text and images
        input_list = to_interleave_list(msg)
        text_parts = [item for item in input_list if isinstance(item, str)]
        images = [item for item in input_list if not isinstance(item, str)]
        prompt = "\n".join(text_parts)
        prompt = strip_placeholders(prompt)

        max_new_tokens = gen_kw.get("max_new_tokens", self._max_new_tokens)
        eos_id = tokenizer.eos_token_id

        # Build messages (VeOmni convention)
        if images:
            messages = [{"role": "user", "content": [
                *[{"type": "image", "image": img} for img in images],
                {"type": "text", "text": prompt},
            ]}]
        else:
            messages = [{"role": "user", "content": [
                {"type": "text", "text": prompt},
            ]}]

        text = processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True,
        )
        inputs = processor(
            text=[text], images=images if images else None,
            return_tensors="pt",
        )
        inputs = {
            k: v.to(device) if torch.is_tensor(v) else v
            for k, v in inputs.items()
        }

        gen_config = GenerationConfig(
            max_new_tokens=max_new_tokens,
            do_sample=False,
            eos_token_id=eos_id,
            pad_token_id=eos_id,
        )

        with torch.no_grad():
            output_ids = model.generate_text(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                pixel_values=inputs.get("pixel_values"),
                image_grid_thw=inputs.get("image_grid_thw"),
                generation_config=gen_config,
            )

        # Unwrap if HF GenerateOutput
        if hasattr(output_ids, "sequences"):
            output_ids = output_ids.sequences

        generated_ids = output_ids[0, inputs["input_ids"].shape[1]:]
        response = tokenizer.decode(generated_ids, skip_special_tokens=True)
        return response.strip()

    # ------------------------------------------------------------------
    # draw()
    # ------------------------------------------------------------------

    def draw(self, context: Message, instruction: str, **kw) -> "Image.Image":
        """Generate an image via JoyAIImageModel.generate_image() (DiT+VAE pipeline).

        Uses the model's built-in generation pipeline (built during
        load_weights_from_checkpoint) which combines Qwen3VL text encoder,
        MMDiT transformer, and Wan2.1 VAE.
        """
        import torch
        from PIL import Image

        # Extract context images for conditioning
        input_list = to_interleave_list(context)
        context_images = [item for item in input_list if not isinstance(item, str)]
        text_parts = [item for item in input_list if isinstance(item, str)]

        # Build the full prompt
        context_text = "\n".join(text_parts)
        prompt = f"{context_text}\n{instruction}" if context_text else instruction

        height = kw.get("height", self._gen_height)
        width = kw.get("width", self._gen_width)
        steps = kw.get("steps", self._gen_steps)
        guidance_scale = kw.get("guidance_scale", self._gen_guidance)
        seed = kw.get("seed", self._gen_seed)

        with torch.no_grad():
            # Use JoyAIImageModel's built-in generate_image method
            output = self._und_model.generate_image(
                prompt=prompt,
                height=height,
                width=width,
                num_inference_steps=steps,
                guidance_scale=guidance_scale,
                seed=seed,
                output_type="pil",
            )

        # Extract PIL image from output
        # Pipeline with return_dict=False returns a tuple (images,) or (images, ...)
        if isinstance(output, tuple) and len(output) > 0:
            output = output[0]
        if isinstance(output, Image.Image):
            return output
        if isinstance(output, (list, tuple)):
            for item in output:
                if isinstance(item, Image.Image):
                    return item
        if hasattr(output, "shape"):
            import numpy as np
            # JoyAI pipeline returns 6D tensor: (1, 1, 1, C, H, W)
            t = output
            while t.ndim > 4:
                t = t.squeeze(0)
            if t.ndim == 4:
                t = t[0]  # take first batch
            # t should be (C, H, W) now — pipeline already returns [0,1]
            pixels = (t.clamp(0, 1) * 255).cpu().permute(1, 2, 0).numpy().astype("uint8")
            return Image.fromarray(pixels)

        raise RuntimeError("JoyAI generate_image() did not produce an image")
