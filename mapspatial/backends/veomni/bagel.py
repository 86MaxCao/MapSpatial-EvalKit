"""Bagel backend — wraps VeOmni BagelForConditionalGeneration.

Implements all three backend methods:
  - understand(): understanding_output=True (text-only, no image generation)
  - draw(): generate_image() wrapper for external_draw strategy
  - interleave(): vendor InterleaveInferencer with understanding_output=False

Strategy → understanding_output mapping:
  direct              → understand() (understanding_output=True)
  native_interleave   → interleave() (understanding_output=False, full loop)
  external_draw       → understand() + draw() (text + separate image gen)
"""

from __future__ import annotations

import os
import time
import glob
from pathlib import Path
from typing import ClassVar

import torch
from PIL import Image

from ...types import Capabilities, Message, Prediction, TraceStep
from ...config import BackendConfig
from ...compat import apply as apply_compat
from ...messages import to_interleave_list, to_placeholder_prompt
from ...media import load_image
from ..base import Backend


class BagelBackend(Backend):
    """Bagel-7B-MoT backend with draw + native interleave support."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=True,           # vendor batch_inferencer supports packed KV
        draw=True,            # can generate images via generate_image()
        native_interleave=True,  # has InterleaveInferencer
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
        from ...vendor.bagel.modeling_bagel import BagelForConditionalGeneration, AutoEncoder
        from ...vendor.bagel.configuration_bagel import BagelVaeConfig

        (self._model, config) = load_model(
            model_path, BagelForConditionalGeneration,
            device=device, dtype=dtype,
        )
        self._tokenizer = load_tokenizer(model_path)

        # Setup special tokens (VeOmni approach — manual, not via add_special_tokens)
        special_tokens = ["<|im_start|>", "<|im_end|>", "<|vision_start|>", "<|vision_end|>"]
        existing = []
        for k, v in self._tokenizer.special_tokens_map.items():
            if isinstance(v, str):
                existing.append(v)
            elif isinstance(v, list):
                existing.extend(v)
        new_tokens = [t for t in special_tokens if t not in existing]
        if new_tokens:
            self._tokenizer.add_tokens(new_tokens)
        self._new_token_ids = {
            "bos_token_id": self._tokenizer.convert_tokens_to_ids("<|im_start|>"),
            "eos_token_id": self._tokenizer.convert_tokens_to_ids("<|im_end|>"),
            "start_of_image": self._tokenizer.convert_tokens_to_ids("<|vision_start|>"),
            "end_of_image": self._tokenizer.convert_tokens_to_ids("<|vision_end|>"),
        }

        # Build ViT image transform (inline class matching VeOmni's infer_unified.py)
        import numpy as np
        vit_config = config.vit_config if config is not None else None
        vit_patch_size = getattr(vit_config, "patch_size", 14) if vit_config else 14
        vit_max_size = getattr(vit_config, "image_size", 980) if vit_config else 980

        class _ImageTransform:
            def __init__(self, max_size, min_size, patch_size):
                self.max_size = max_size
                self.min_size = min_size
                self.patch_size = patch_size
            def _make_divisible(self, value, stride):
                return max(stride, int(round(value / stride) * stride))
            def resize_transform(self, img):
                """Resize a PIL Image and return PIL (no tensor conversion)."""
                w, h = img.size
                scale = min(self.max_size / max(w, h), 1.0)
                scale = max(scale, self.min_size / min(w, h))
                new_w = max(self.patch_size, int(round(round(w * scale) / self.patch_size) * self.patch_size))
                new_h = max(self.patch_size, int(round(round(h * scale) / self.patch_size) * self.patch_size))
                return img.resize((new_w, new_h), Image.BICUBIC)
            def __call__(self, img):
                img = self.resize_transform(img)
                tensor = torch.tensor(np.array(img)).permute(2, 0, 1).float() / 255.0
                tensor = (tensor - 0.5) / 0.5
                return tensor

        self._image_transform = _ImageTransform(vit_max_size, 224, vit_patch_size)

        # Load VAE model (MoVQGAN / AutoEncoder) — needed for draw/interleave
        self._vae_model = None
        self._vae_transform = None
        try:
            import torch as _torch
            vae_config = config.vae_config if config is not None else None
            if vae_config is None:
                vae_config = BagelVaeConfig()
            vae = AutoEncoder(vae_config).to(device).to(getattr(_torch, dtype))
            vae_candidates = (
                glob.glob(os.path.join(model_path, "vae*.safetensors")) +
                glob.glob(os.path.join(model_path, "*vae*.safetensors")) +
                glob.glob(os.path.join(model_path, "ae*.safetensors")) +
                glob.glob(os.path.join(model_path, "*ae*.safetensors"))
            )
            if vae_candidates:
                from safetensors.torch import load_file as _load_safetensors
                if vae_candidates[0].endswith(".safetensors"):
                    vae_state = _load_safetensors(vae_candidates[0])
                else:
                    vae_state = _torch.load(vae_candidates[0], map_location="cpu")
                vae.load_state_dict(vae_state, strict=False)
            vae.eval()
            self._vae_model = vae
        except Exception as e:
            print(f"WARNING: Failed to load VAE model: {e}")

        self._device = device

        # VAE transform (for generation input — larger images, stride 16)
        self._vae_transform = _ImageTransform(1024, 512, 16)

        # Create interleave inferencer (lazy — only needed for native_interleave)
        self._inferencer = None
        self._batch_inferencer = None

        # Generation params from config
        gen = cfg.generate
        self._temperature = gen.get("temperature", 0.3)
        self._max_think_tokens = gen.get("max_think_tokens", 4096)
        self._max_rounds = cfg.backend_args.get("max_rounds", 3)

        # CFG params from backend_args
        ba = cfg.backend_args
        self._cfg_text_scale = ba.get("cfg_text_scale", 4.0)
        self._cfg_img_scale = ba.get("cfg_img_scale", 2.0)
        self._num_timesteps = ba.get("num_timesteps", 50)
        self._timestep_shift = ba.get("timestep_shift", 3.0)
        self._cfg_interval = ba.get("cfg_interval", [0.4, 1.0])
        self._cfg_renorm_type = ba.get("cfg_renorm_type", "global")
        self._cfg_renorm_min = ba.get("cfg_renorm_min", 0.0)
        self._image_shapes = tuple(ba.get("image_shapes", (1024, 1024)))

        # System prompt
        self._system_prompt = cfg.system_prompt or None

    @property
    def model_name(self) -> str:
        return self._cfg.name

    def _get_inferencer(self):
        """Lazy-create the InterleaveInferencer from vendored imports."""
        if self._inferencer is None:
            # Ensure new_token_ids are tensors on the model device
            nti = self._new_token_ids
            nti = {
                k: torch.tensor(v, device=self._device) if not torch.is_tensor(v) else v.to(self._device)
                for k, v in nti.items()
            }
            self._new_token_ids = nti
            from ...vendor.bagel_interleave.inferencer import InterleaveInferencer
            self._inferencer = InterleaveInferencer(
                model=self._model,
                vae_model=self._vae_model,
                tokenizer=self._tokenizer,
                vae_transform=self._vae_transform,
                vit_transform=self._image_transform,
                new_token_ids=nti,
            )
        return self._inferencer

    @staticmethod
    def _vae_resize_inner(img, max_size=1024, min_size=512, stride=16):
        """Resize image for VAE input (matching VeOmni infer_unified.py)."""
        w, h = img.size
        scale = min(max_size / max(w, h), 1.0)
        scale = max(scale, min_size / min(w, h))
        new_w = max(stride, int(round(round(w * scale) / stride) * stride))
        new_h = max(stride, int(round(round(h * scale) / stride) * stride))
        return img.resize((new_w, new_h), Image.BICUBIC)

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        """Text-only understanding (understanding_output=True).

        Uses model.chat() for single-sample, or batch_inferencer for batch.
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
        """Single-sample understanding via model.chat()."""

        # Ensure new_token_ids tensor values are on model device
        nti = self._new_token_ids
        if isinstance(nti, dict):
            nti = {k: v.to(self._device) if torch.is_tensor(v) else v for k, v in nti.items()}
        self._new_token_ids = nti

        # Extract text and images from Message
        text_parts = []
        raw_images = []
        for item in msg:
            if item["type"] == "text":
                text_parts.append(item["value"])
            elif item["type"] == "image":
                img = item["value"]
                if isinstance(img, (str, Path)):
                    img = load_image(img)
                raw_images.append(img)

        prompt = "\n".join(text_parts)

        # Resize images with VAE resize (matching VeOmni infer_unified.py)
        images = []
        for img in raw_images:
            if img.mode != "RGB":
                img = img.convert("RGB")
            img = self._vae_resize_inner(img)
            images.append(img)

        with torch.no_grad():
            response = self._model.chat(
                tokenizer=self._tokenizer,
                new_token_ids=self._new_token_ids,
                image_transform=self._image_transform,
                images=images,
                prompt=prompt,
                max_length=gen_kw.get("max_new_tokens", 512),
            )
        return response

    def draw(self, context: Message, instruction: str, **kw) -> "Image.Image":
        """Generate an intermediate image using forced interleave.

        Uses forced_interleave_inference() which unconditionally generates
        an image after text reasoning, without requiring the model to emit
        a marker token. This is needed because base Bagel was not trained
        to emit <image_start>.
        """
        import torch
        from PIL import Image

        inferencer = self._get_inferencer()

        # Build input list for the inferencer
        input_list = to_interleave_list(context)
        # Append the draw instruction
        input_list.append(instruction)

        # Use forced_interleave_inference — no marker check, always generates
        output = inferencer.forced_interleave_inference(
            input_lists=input_list,
            think=True,
            max_think_token_n=500,
            do_sample=False,
            text_temperature=self._temperature,
            cfg_text_scale=self._cfg_text_scale,
            cfg_img_scale=self._cfg_img_scale,
            cfg_interval=self._cfg_interval,
            timestep_shift=self._timestep_shift,
            num_timesteps=self._num_timesteps,
            cfg_renorm_min=self._cfg_renorm_min,
            cfg_renorm_type=self._cfg_renorm_type,
            image_shapes=self._image_shapes,
            max_rounds=1,
        )

        # Find the generated image in output
        for item in reversed(output):
            if isinstance(item, Image.Image):
                return item

        raise RuntimeError("draw() did not produce an image")

    def interleave(
        self,
        message: Message,
        *,
        max_rounds: int = 3,
        marker: str = "<image_start>",
        **kw,
    ) -> Prediction:
        """Native interleaved reasoning loop.

        Delegates to vendor InterleaveInferencer with understanding_output=False.
        The model decides when to generate images (triggered by marker in text).
        """
        import torch
        from PIL import Image

        inferencer = self._get_inferencer()

        # Convert Message to interleave input list
        input_list = to_interleave_list(message)

        trace: list[TraceStep] = []
        t0 = time.time()

        with torch.no_grad():
            output = inferencer.interleave_inference(
                input_lists=input_list,
                think=True,
                understanding_output=False,
                max_think_token_n=kw.get("max_think_tokens", self._max_think_tokens),
                do_sample=kw.get("temperature", self._temperature) > 0,
                text_temperature=kw.get("temperature", self._temperature) or 1.0,
                cfg_text_scale=self._cfg_text_scale,
                cfg_img_scale=self._cfg_img_scale,
                cfg_interval=self._cfg_interval,
                timestep_shift=self._timestep_shift,
                num_timesteps=self._num_timesteps,
                cfg_renorm_min=self._cfg_renorm_min,
                cfg_renorm_type=self._cfg_renorm_type,
                image_shapes=self._image_shapes,
                max_rounds=max_rounds,
            )

        elapsed = time.time() - t0

        # Parse output: alternating text and image items
        text_parts = []
        generated_images = []
        round_num = 0

        for item in output:
            if isinstance(item, str):
                trace.append(TraceStep(
                    round=round_num, kind="text",
                    text=item,
                    triggered_by=None,
                    elapsed_s=elapsed / max(len(output), 1),
                ))
                text_parts.append(item)
                # Check if this text triggered image generation
                if marker in item:
                    round_num += 1
            elif isinstance(item, Image.Image):
                trace.append(TraceStep(
                    round=round_num, kind="image",
                    triggered_by="model_marker",
                    elapsed_s=elapsed / max(len(output), 1),
                ))
                generated_images.append(item)  # Will be saved by strategy

        # The last text part should contain the answer
        final_text = text_parts[-1] if text_parts else ""

        return Prediction(
            text=final_text,
            generated_images=generated_images,  # PIL Images; strategy saves them
            trace=trace,
            meta={
                "rounds": round_num,
                "draw_triggered": len(generated_images) > 0,
            },
        )

    def forced_interleave(
        self,
        message: Message,
        *,
        max_rounds: int = 1,
        **kw,
    ) -> Prediction:
        """Forced interleaved reasoning — no marker needed.

        Generates text reasoning, then unconditionally generates an image,
        feeds it back into the shared KV cache, and generates the final answer.

        For base Bagel which was not trained to emit '<image_start>' markers.
        """
        import torch
        from PIL import Image

        inferencer = self._get_inferencer()
        input_list = to_interleave_list(message)

        trace: list[TraceStep] = []
        t0 = time.time()

        with torch.no_grad():
            output = inferencer.forced_interleave_inference(
                input_lists=input_list,
                think=True,
                max_think_token_n=kw.get("max_think_tokens", self._max_think_tokens),
                do_sample=kw.get("temperature", self._temperature) > 0,
                text_temperature=kw.get("temperature", self._temperature) or 1.0,
                cfg_text_scale=self._cfg_text_scale,
                cfg_img_scale=self._cfg_img_scale,
                cfg_interval=self._cfg_interval,
                timestep_shift=self._timestep_shift,
                num_timesteps=self._num_timesteps,
                cfg_renorm_min=self._cfg_renorm_min,
                cfg_renorm_type=self._cfg_renorm_type,
                image_shapes=self._image_shapes,
                max_rounds=max_rounds,
            )

        elapsed = time.time() - t0

        # Parse output: [text_reasoning, image, text_answer]
        text_parts = []
        generated_images = []
        round_num = 0

        for item in output:
            if isinstance(item, str):
                trace.append(TraceStep(
                    round=round_num, kind="text",
                    text=item,
                    triggered_by=None,
                    elapsed_s=elapsed / max(len(output), 1),
                ))
                text_parts.append(item)
            elif isinstance(item, Image.Image):
                trace.append(TraceStep(
                    round=round_num, kind="image",
                    triggered_by="forced",
                    elapsed_s=elapsed / max(len(output), 1),
                ))
                generated_images.append(item)
                round_num += 1

        # Last text part is the final answer
        final_text = text_parts[-1] if text_parts else ""

        return Prediction(
            text=final_text,
            generated_images=generated_images,
            trace=trace,
            meta={
                "rounds": round_num,
                "draw_triggered": len(generated_images) > 0,
            },
        )
