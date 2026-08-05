"""BLIP3o backend — wraps VeOmni BLIP3oQwenForCausalLM.

Implements understand() and draw() for the BLIP3o unified model.
BLIP3o uses a ViT vision encoder + Qwen LLM for understanding, and a
DIT + VAE pipeline for image generation.

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


class BLIP3oBackend(Backend):
    """BLIP3o (BLIP3oQwenForCausalLM) backend with understand + draw."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False,            # serial loop, one sample at a time
        draw=True,              # DIT+VAE image generation
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
        from ...vendor.blip3o.modeling_blip3o import BLIP3oQwenForCausalLM

        (self._model, _) = load_model(
            model_path, BLIP3oQwenForCausalLM,
            device=device, dtype=dtype,
        )
        self._tokenizer = load_tokenizer(model_path)

        self._device = device

        # Generation params from config
        gen = cfg.generate
        self._temperature = gen.get("temperature", 0.3)
        self._max_new_tokens = gen.get("max_new_tokens", 1024)

        # Draw / CFG params from backend_args
        ba = cfg.backend_args
        self._cfg_scale = ba.get("cfg_scale", 4.0)
        self._num_timesteps = ba.get("num_timesteps", 50)
        self._timestep_shift = ba.get("timestep_shift", 3.0)
        self._image_size = tuple(ba.get("image_size", (1024, 1024)))

        # System prompt
        self._system_prompt = cfg.system_prompt or None

    @property
    def model_name(self) -> str:
        return self._cfg.name

    # ------------------------------------------------------------------
    # understand()
    # ------------------------------------------------------------------

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        """Text-only understanding via vision encoder + LLM generate.

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
        """Single-sample understanding with Qwen2.5-VL vision token format."""
        import numpy as np

        device = self._device
        model = self._model
        tokenizer = self._tokenizer
        embed_layer = model.get_input_embeddings()

        IMAGE_PAD_ID = 151655  # <|image_pad|>

        # Extract text and images
        input_list = to_interleave_list(msg)
        text_parts = [item for item in input_list if isinstance(item, str)]
        images = [item for item in input_list if not isinstance(item, str)]
        prompt = "\n".join(text_parts)
        prompt = strip_placeholders(prompt)

        if images:
            # Preprocess images first to know num vision features
            pixel_values = self._prepare_vision_input(images, device)
            with torch.no_grad():
                vit_features = model.visual(pixel_values)  # [1, L, D]
            vit_embeds = vit_features.reshape(-1, vit_features.shape[-1])  # [L, D]
            num_vit = vit_embeds.shape[0]

            # Build prompt with Qwen2.5-VL vision tokens
            vision_str = "<|vision_start|>" + "<|image_pad|>" * num_vit + "<|vision_end|>"
            text = f"<|im_start|>user\n{vision_str}{prompt}<|im_end|>\n<|im_start|>assistant\n"
        else:
            text = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"

        input_ids = tokenizer.encode(text, return_tensors="pt").to(device)
        inputs_embeds = embed_layer(input_ids[0])  # [T, D]

        if images:
            # Replace <|image_pad|> positions with vision features
            image_mask = (input_ids[0] == IMAGE_PAD_ID)
            inputs_embeds[image_mask] = vit_embeds.to(inputs_embeds.dtype)

        # Greedy decoding loop
        max_new_tokens = gen_kw.get("max_new_tokens", self._max_new_tokens)
        eos_id = tokenizer.eos_token_id
        output_layer = model.get_output_embeddings()  # lm_head
        generated = []

        with torch.no_grad():
            for _ in range(max_new_tokens):
                hidden = model._llm_forward(inputs_embeds.unsqueeze(0))  # [1, T, D]
                logits = output_layer(hidden[:, -1:, :])  # [1, 1, vocab]
                next_id = logits[0, -1].argmax(dim=-1).item()
                if next_id == eos_id:
                    break
                generated.append(next_id)
                next_embed = embed_layer(torch.tensor([[next_id]], device=device))
                inputs_embeds = torch.cat([inputs_embeds, next_embed[0]], dim=0)

        text = tokenizer.decode(generated, skip_special_tokens=True)
        return text.strip()

    @staticmethod
    def _pil_img2rgb(img):
        """Convert PIL image to RGB."""
        if img.mode != "RGB":
            img = img.convert("RGB")
        return img

    @staticmethod
    def _resize_image(img, max_size=980, min_size=224, patch_size=14):
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
            img = self._resize_image(img, 980, 224, 14)
            tensor = torch.tensor(np.array(img)).permute(2, 0, 1).float() / 255.0
            tensors.append(tensor)
        pixel_values = torch.stack(tensors).to(device)
        pixel_values = pixel_values.to(dtype=next(self._model.parameters()).dtype)
        return pixel_values

    # ------------------------------------------------------------------
    # draw()
    # ------------------------------------------------------------------

    def draw(self, context: Message, instruction: str, **kw):
        """Generate an image using the DIT + VAE pipeline.

        Flow:
          1. Tokenize prompt + append latent_queries
          2. Run _llm_forward to get hidden states
          3. Run DIT denoising over hidden states
          4. VAE decode → image tensor
          5. Convert to PIL Image

        NOTE: exact method names for DIT/VAE pipeline need verification
        at runtime. BLIP3o's generation pipeline may differ slightly.
        """
        import torch
        from PIL import Image

        # Build the prompt from context + instruction
        input_list = to_interleave_list(context)
        text_parts = [item for item in input_list if isinstance(item, str)]
        context_text = "\n".join(text_parts)
        full_prompt = f"{context_text}\n{instruction}" if context_text else instruction

        # Tokenize prompt
        prompt_ids = self._tokenizer(
            full_prompt, return_tensors="pt",
            truncation=True, max_length=512,
        ).input_ids.to(self._device)

        # Prepare latent queries for image tokens
        # BLIP3o uses self.model.latent_queries (nn.Parameter of shape [1, n_query, hidden_size])
        num_latent_tokens = kw.get("num_latent_tokens", getattr(self._model.model, 'latent_queries', None).shape[1] if hasattr(self._model.model, 'latent_queries') else 256)
        latent_queries = None
        if hasattr(self._model.model, 'latent_queries'):
            latent_queries = self._model.model.latent_queries.to(
                device=self._device,
                dtype=next(self._model.parameters()).dtype,
            )

        # Concatenate prompt embeddings + latent queries
        embed_layer = self._model.get_input_embeddings()
        prompt_embeds = embed_layer(prompt_ids)  # [1, T_text, D]

        if latent_queries is not None:
            inputs_embeds = torch.cat([prompt_embeds, latent_queries], dim=1)
        else:
            inputs_embeds = prompt_embeds

        # Run LLM forward to get hidden states
        # NOTE: _llm_forward may be model._llm_forward or model.language_model
        with torch.no_grad():
            hidden = self._model._llm_forward(inputs_embeds)  # [1, T, D]

        # Extract the latent portion (last num_latent_tokens)
        latent_hidden = hidden[:, -num_latent_tokens:, :]

        # Run DIT denoising
        # NOTE: exact DIT method name needs verification
        cfg_scale = kw.get("cfg_scale", self._cfg_scale)
        num_timesteps = kw.get("num_timesteps", self._num_timesteps)
        timestep_shift = kw.get("timestep_shift", self._timestep_shift)
        image_size = kw.get("image_size", self._image_size)

        with torch.no_grad():
            # DIT denoising loop
            # NOTE: model.dit or model.denoiser — needs verification
            latents = self._model.dit_denoise(
                latent_hidden,
                num_timesteps=num_timesteps,
                cfg_scale=cfg_scale,
                timestep_shift=timestep_shift,
                image_size=image_size,
            )  # [1, C, H_lat, W_lat]

        # VAE decode
        # NOTE: model.vae.decode or model.decode_latents — needs verification
        with torch.no_grad():
            image_tensor = self._model.vae.decode(latents)  # [1, 3, H, W]

        # Convert to PIL Image
        # Denormalize from [-1, 1] to [0, 1]
        image_tensor = image_tensor.clamp(-1, 1)
        image_tensor = (image_tensor * 0.5 + 0.5)  # [0, 1]
        image_tensor = image_tensor.cpu().squeeze(0)  # [3, H, W]

        # Convert to PIL
        image_np = (image_tensor.permute(1, 2, 0).numpy() * 255).astype("uint8")
        pil_image = Image.fromarray(image_np)
        return pil_image
