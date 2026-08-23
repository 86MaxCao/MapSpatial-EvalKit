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
import numpy as np
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

# Token that signals start of image generation in BLIP3o
_IMG_START_TOKEN_ID = 151665


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

        # Generation pipeline components (loaded from diffusion-decoder/)
        # The vendored model has DIT (1792-ch) and VAE (16-ch) in incompatible
        # spaces. A UNet bridges them: DIT → features → UNet → image latents → VAE.
        self._unet = None
        self._gen_vae = None
        self._unet_scheduler = None
        self._dit_scheduler = None
        self._neg_unet_cond = None

        diffusion_path = os.path.join(model_path, "diffusion-decoder")
        if os.path.exists(diffusion_path):
            try:
                from diffusers import AutoencoderKL, UNet2DConditionModel
                from diffusers.schedulers import (
                    EulerDiscreteScheduler,
                    FlowMatchEulerDiscreteScheduler,
                )

                _dt = getattr(torch, dtype)
                self._unet = (
                    UNet2DConditionModel.from_pretrained(
                        diffusion_path, subfolder="unet",
                        torch_dtype=_dt, variant="bf16",
                    ).to(device).eval()
                )
                self._gen_vae = (
                    AutoencoderKL.from_pretrained(
                        diffusion_path, subfolder="vae",
                        torch_dtype=_dt, variant="bf16",
                    ).to(device).eval()
                )
                self._unet_scheduler = EulerDiscreteScheduler.from_pretrained(
                    diffusion_path, subfolder="scheduler"
                )
                self._dit_scheduler = FlowMatchEulerDiscreteScheduler()
                print(f"  Loaded UNet+VAE from {diffusion_path}")
            except Exception as e:
                print(f"  WARNING: Failed to load diffusion-decoder: {e}")
        else:
            print(f"  WARNING: diffusion-decoder not found at {diffusion_path}")

        # Draw / CFG params from backend_args
        ba = cfg.backend_args
        self._cfg_scale = ba.get("cfg_scale", 4.0)
        self._num_timesteps = ba.get("num_timesteps", 50)
        self._timestep_shift = ba.get("timestep_shift", 3.0)
        self._image_size = tuple(ba.get("image_size", (1024, 1024)))
        self._dit_guidance_scale = ba.get("dit_guidance_scale", 3.0)
        self._dit_num_steps = ba.get("dit_num_steps", 30)
        self._unet_num_steps = ba.get("unet_num_steps", 50)

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
        """Preprocess images: resize -> /255.0 -> bf16 -> (N, 3, H, W).

        All images are resized to the same dimensions (first image's size)
        to ensure torch.stack succeeds when images have different aspect ratios.
        """
        import numpy as np
        tensors = []
        # Determine target size from first image
        target_img = self._pil_img2rgb(pil_images[0])
        target_img = self._resize_image(target_img, 980, 224, 14)
        target_h, target_w = target_img.size[1], target_img.size[0]
        for img in pil_images:
            img = self._pil_img2rgb(img)
            img = self._resize_image(img, 980, 224, 14)
            # Force same size as first image
            if img.size[1] != target_h or img.size[0] != target_w:
                from PIL import Image as _PIL
                img = img.resize((target_w, target_h), _PIL.BICUBIC)
            tensor = torch.tensor(np.array(img)).permute(2, 0, 1).float() / 255.0
            tensors.append(tensor)
        pixel_values = torch.stack(tensors).to(device)
        pixel_values = pixel_values.to(dtype=next(self._model.parameters()).dtype)
        return pixel_values

    # ------------------------------------------------------------------
    # draw() — LLM → DIT → UNet → VAE pipeline
    # ------------------------------------------------------------------

    @torch.inference_mode()
    def _get_llm_features(self, prompt_text: str) -> torch.Tensor:
        """Run LLM forward with latent queries appended.

        Returns hidden states at the latent query positions: (1, n_query, hidden_size).
        """
        device = self._device
        model = self._model
        dtype = next(model.parameters()).dtype

        # Format prompt in CHATML template
        text = (
            "<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n"
            f"<|im_start|>user\n{prompt_text}<|im_end|>\n"
            "<|im_start|>assistant\n"
        )
        input_ids = self._tokenizer(text, return_tensors="pt").input_ids.to(device)

        # Append [IMG] token to signal generation start
        img_start = torch.tensor([[_IMG_START_TOKEN_ID]], device=device)
        input_ids = torch.cat([input_ids, img_start], dim=1)

        # Build input embeddings: text tokens + learnable latent queries
        embed_layer = model.get_input_embeddings()
        text_embeds = embed_layer(input_ids)
        n_query = model.config.n_query  # 64
        latent_queries = model.model.latent_queries.expand(
            text_embeds.shape[0], -1, -1
        ).to(dtype)
        inputs_embeds = torch.cat([text_embeds, latent_queries], dim=1)

        # LLM forward (causal attention + RoPE)
        hidden_states = model._llm_forward(inputs_embeds)

        # Extract the last n_query hidden states (latent query positions)
        return hidden_states[:, -n_query:, :]  # (1, 64, 3584)

    @torch.inference_mode()
    def _dit_denoise(self, llm_features: torch.Tensor) -> torch.Tensor:
        """Denoise random latent through the DIT (flow-matching).

        Uses the vendored DiTModel (self._model.model.dit.model) which
        matches checkpoint weights but lacks 2D RoPE — quality may be
        slightly lower than the official custom LuminaNextDiT2DModel.

        Args:
            llm_features: (B, n_query, hidden_size) from LLM.
        Returns:
            (B, n_query, dit_hidden_size) — reshaped DIT output for UNet.
        """
        device = llm_features.device
        dtype = llm_features.dtype
        B = llm_features.shape[0]

        config = self._model.config
        dit_dim = config.dit_hidden_size  # 1792
        latent_size = 8  # spatial size of DIT latent grid

        # Start from random noise in DIT channel space
        latents = torch.randn(
            B, dit_dim, latent_size, latent_size, device=device, dtype=dtype
        )

        # CFG: pair [null_conditioning, positive_conditioning]
        null_feat = torch.zeros_like(llm_features)
        cond_input = torch.cat([null_feat, llm_features], dim=0)  # (2B, 64, 3584)

        # Flow-matching sigma schedule
        dit_guidance = self._dit_guidance_scale
        num_steps = self._dit_num_steps
        sigmas = np.linspace(1.0, 1.0 / num_steps, num_steps)
        self._dit_scheduler.set_timesteps(num_steps, sigmas=sigmas)

        dit_model = self._model.model.dit.model  # DiTModel

        for t in self._dit_scheduler.timesteps:
            lat_in = latents.repeat(2, 1, 1, 1)  # (2B, 1792, 8, 8)
            t_expanded = t.unsqueeze(0).expand(lat_in.shape[0]).to(device, torch.long)

            pred = dit_model(lat_in, t_expanded, cond_input)

            pred_uncond, pred_cond = pred.chunk(2)
            pred = pred_uncond + dit_guidance * (pred_cond - pred_uncond)

            latents = self._dit_scheduler.step(pred, t, latents).prev_sample

        # Reshape (B, 1792, 8, 8) -> (B, 64, 1792) for UNet cross-attention
        return latents.view(B, dit_dim, -1).permute(0, 2, 1).contiguous()

    @torch.inference_mode()
    def _get_neg_unet_cond(self) -> torch.Tensor:
        """Compute (and cache) negative conditioning for UNet CFG."""
        if self._neg_unet_cond is None:
            llm_neg = self._get_llm_features(" ")
            self._neg_unet_cond = self._dit_denoise(llm_neg)
        return self._neg_unet_cond

    @torch.inference_mode()
    def _unet_denoise(
        self, pos_cond: torch.Tensor, height: int, width: int
    ) -> torch.Tensor:
        """Run UNet denoising loop.

        Args:
            pos_cond: (B, 64, 1792) positive conditioning from DIT.
        Returns:
            Image latents (B, 4, H/8, W/8).
        """
        device = pos_cond.device
        dtype = pos_cond.dtype
        B = pos_cond.shape[0]

        neg_cond = self._get_neg_unet_cond()
        # [positive, negative] order matching official pipeline
        prompt_embeds = torch.cat([pos_cond, neg_cond], dim=0)  # (2, 64, 1792)

        vae_sf = 2 ** (len(self._gen_vae.config.block_out_channels) - 1)  # 8
        latents = torch.randn(
            B, self._unet.config.in_channels,
            height // vae_sf, width // vae_sf,
            device=device, dtype=dtype,
        )

        self._unet_scheduler.set_timesteps(self._unet_num_steps, device=device)
        latents = latents * self._unet_scheduler.init_noise_sigma

        # SDXL-style additional conditioning
        time_ids = torch.tensor(
            [[height, width, 0, 0, height, width]],
            device=device, dtype=torch.long,
        ).expand(2, -1)
        added_cond = {
            "time_ids": time_ids,
            "text_embeds": prompt_embeds.mean(dim=1),  # (2, 1792)
        }

        guidance_scale = self._cfg_scale
        for t in self._unet_scheduler.timesteps:
            lat_in = torch.cat([latents, latents], dim=0)
            lat_in = self._unet_scheduler.scale_model_input(lat_in, t)

            pred = self._unet(
                lat_in, t,
                encoder_hidden_states=prompt_embeds,
                added_cond_kwargs=added_cond,
            ).sample

            pred_cond, pred_uncond = pred.chunk(2)
            pred = pred_uncond + guidance_scale * (pred_cond - pred_uncond)

            latents = self._unet_scheduler.step(pred, t, latents).prev_sample

        return latents

    @torch.inference_mode()
    def _gen_vae_decode(self, latents: torch.Tensor) -> "Image.Image":
        """Decode image latents using AutoencoderKL."""
        latents = latents / self._gen_vae.config.scaling_factor
        image = self._gen_vae.decode(latents.to(self._gen_vae.dtype)).sample
        image = (image / 2 + 0.5).clamp(0, 1)
        arr = image.cpu().permute(0, 2, 3, 1).float().numpy()
        arr = (arr * 255).round().astype(np.uint8)
        return Image.fromarray(arr[0])

    def draw(self, context: Message, instruction: str, **kw):
        """Generate an image using the LLM → DIT → UNet → VAE pipeline.

        Follows the official VeOmni BLIP3o inference approach:
          1. LLM forward with latent queries → hidden states (1, 64, 3584)
          2. DIT flow-matching denoising → compact features (1, 64, 1792)
          3. UNet diffusion denoising → image latents (1, 4, H/8, W/8)
          4. VAE decode → PIL Image

        The vendored model's DIT (1792-ch) and VAE (16-ch) are in
        incompatible spaces; a UNet (loaded from diffusion-decoder/)
        bridges them. Context images are not used — generation is
        text-conditioned only.
        """
        if self._unet is None or self._gen_vae is None:
            raise RuntimeError(
                "BLIP3o generation requires UNet+VAE from diffusion-decoder/. "
                "Ensure the checkpoint has a 'diffusion-decoder/' subdirectory "
                "with 'unet/' and 'vae/' subfolders."
            )

        # Allow kw overrides
        old_cfg = self._cfg_scale
        old_dit_guidance = self._dit_guidance_scale
        old_dit_steps = self._dit_num_steps
        old_unet_steps = self._unet_num_steps
        self._cfg_scale = kw.get("cfg_scale", old_cfg)
        self._dit_guidance_scale = kw.get("dit_guidance_scale", old_dit_guidance)
        self._dit_num_steps = kw.get("dit_num_steps", old_dit_steps)
        self._unet_num_steps = kw.get("unet_num_steps", old_unet_steps)

        height = kw.get("height", self._image_size[0])
        width = kw.get("width", self._image_size[1])

        try:
            # Build the prompt from context + instruction
            input_list = to_interleave_list(context)
            text_parts = [item for item in input_list if isinstance(item, str)]
            context_text = "\n".join(text_parts)
            prompt_text = (
                f"Please generate image based on the following caption: "
                f"{context_text}\n{instruction}" if context_text else
                f"Please generate image based on the following caption: {instruction}"
            )

            # Step 1: LLM features
            llm_feat = self._get_llm_features(prompt_text)

            # Step 2: DIT denoising → compact feature representation
            dit_feat = self._dit_denoise(llm_feat)

            # Step 3: UNet denoising → image latents
            img_latents = self._unet_denoise(dit_feat, height, width)

            # Step 4: VAE decode → PIL Image
            return self._gen_vae_decode(img_latents)
        finally:
            # Restore saved params
            self._cfg_scale = old_cfg
            self._dit_guidance_scale = old_dit_guidance
            self._dit_num_steps = old_dit_steps
            self._unet_num_steps = old_unet_steps
