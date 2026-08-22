"""ShowO2 backend — wraps VeOmni Showo2Qwen2_5.

Implements all three backend methods:
  - understand(): text understanding via model.mmu_generate() with image embeddings
  - draw(): image generation via model.t2i_generate() + VAE decode
  - (no native interleave — use external_draw strategy for mixed output)

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


class ShowO2Backend(Backend):
    """ShowO2-Qwen2.5 backend with understanding + image generation."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False,             # serial inference only
        draw=True,               # can generate images via t2i_generate()
        native_interleave=False,  # no native interleave loop
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
        from ...vendor.showo2.modeling_showo2 import Showo2Model

        (self._model, _) = load_model(
            model_path, Showo2Model,
            device=device, dtype=dtype,
        )

        # Show-o2 checkpoint has no tokenizer files; load from Qwen2.5-VL-7B-Instruct
        tok_path = model_path
        if not os.path.exists(os.path.join(tok_path, "tokenizer_config.json")):
            qwen_path = os.path.join(
                os.environ.get("CKPT_DIR", "/mnt/nas-tbt/tbt/checkpoint/hf_cache"),
                "Qwen2.5-VL-7B-Instruct",
            )
            if os.path.exists(qwen_path):
                tok_path = qwen_path
        self._tokenizer = load_tokenizer(tok_path)

        # Add special tokens (VeOmni convention)
        self._tokenizer.add_special_tokens({"pad_token": "[PAD]"})
        self._tokenizer.add_tokens(["<image>", "<|vid_start|>", "<|vid_end|>"])

        # Token IDs — use Qwen2.5-VL native tokens for image delimiters
        self._showo_token_ids = {
            "bos_id": self._tokenizer.get_vocab()["<|im_start|>"],
            "eos_id": self._tokenizer.eos_token_id,
            "boi_id": self._tokenizer.get_vocab()["<|vision_start|>"],
            "eoi_id": self._tokenizer.get_vocab()["<|vision_end|>"],
            "img_pad_id": self._tokenizer.get_vocab()["<|image_pad|>"],
            "img_id": self._tokenizer.get_vocab()["<image>"],
        }

        # Load WanVAE for image encoding
        import torch as _torch
        from ...vendor.showo2.models.wan21_vae import WanVAE
        vae_pth = os.path.join(
            os.environ.get("CKPT_DIR", "/mnt/nas-tbt/tbt/checkpoint/hf_cache"),
            "JoyAI-Image-Edit", "vae", "Wan2.1_VAE.pth",
        )
        if not os.path.exists(vae_pth):
            # Fallback: check model's own directory
            vae_pth = os.path.join(model_path, "vae", "Wan2.1_VAE.pth")
        if os.path.exists(vae_pth):
            _dt = getattr(_torch, dtype)
            self._vae = WanVAE(vae_pth=vae_pth, dtype=_dt, device=device)
            self._model.set_vae(self._vae)
            print(f"  Loaded WanVAE from {vae_pth}")
        else:
            print(f"  WARNING: WanVAE not found at {vae_pth}")
            self._vae = None

        self._device = device

        # Generation params from config
        gen = cfg.generate
        self._temperature = gen.get("temperature", 0.0)
        self._max_new_tokens = gen.get("max_new_tokens", 512)

        # Draw params from backend_args
        ba = cfg.backend_args
        self._guidance_scale = ba.get("guidance_scale", 5.0)
        self._image_size = ba.get("image_size", 432)
        self._num_steps = ba.get("num_steps", 50)
        self._time_shifting_factor = ba.get("time_shifting_factor", 3.0)

        # System prompt
        self._system_prompt = cfg.system_prompt or None

    @property
    def model_name(self) -> str:
        return self._cfg.name

    # ------------------------------------------------------------------
    # understand()
    # ------------------------------------------------------------------

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        """Text-only understanding via model.showo2.mmu_generate().

        Matches VeOmni infer_showo2_understand calling convention.
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
        """Single-sample understanding — aligned with official inference_mmu.py.

        Flow: VAE encode image → image_embedder_und + image_embedder_gen + und_trans + fusion_proj
        → build embeds: [sys_prompt] + [boi] + [time_embed] + [image_embeds] + [eoi + question + assistant]
        → omni_attn_mask_naive with bidirectional for image block
        → mmu_generate
        """
        import torch
        import numpy as np
        from PIL import Image
        from ...vendor.showo2.models import omni_attn_mask_naive
        import torchvision.transforms as T

        device = self._device
        model = self._model
        tokenizer = self._tokenizer
        tids = self._showo_token_ids
        inner = model.showo2

        # Extract text and images
        input_list = to_interleave_list(msg)
        text_parts = [item for item in input_list if isinstance(item, str)]
        images = [item for item in input_list if not isinstance(item, str)]
        prompt = "\n".join(text_parts)
        prompt = strip_placeholders(prompt)

        max_new_tokens = gen_kw.get("max_new_tokens", self._max_new_tokens)

        # Config
        config = inner.config
        h_lat = getattr(config, "image_latent_height", 27)
        w_lat = getattr(config, "image_latent_width", 27)
        patch_size = getattr(config, "patch_size", 2)
        add_time_embeds = getattr(config, "add_time_embeds", False)
        num_img_tokens = (h_lat // patch_size) * (w_lat // patch_size)
        num_mmu_tokens = num_img_tokens + (1 if add_time_embeds else 0)

        # Build system prompt tokens (official convention)
        sys_ids = tokenizer("system\nYou are a helpful assistant.<|im_end|>\nuser\n",
                            add_special_tokens=False)["input_ids"]
        question_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
        assistant_ids = tokenizer("\nassistant\n", add_special_tokens=False)["input_ids"]

        # Token sequence: [bos] + sys + [boi, eoi] + question + assistant
        text_tokens_a = [tids["bos_id"]] + sys_ids
        text_tokens_b = [tids["boi_id"], tids["eoi_id"]] + question_ids + assistant_ids

        text_tokens_a_t = torch.tensor([text_tokens_a], device=device)
        text_tokens_b_t = torch.tensor([text_tokens_b], device=device)

        text_embeds_a = inner.showo.model.embed_tokens(text_tokens_a_t)
        text_embeds_b = inner.showo.model.embed_tokens(text_tokens_b_t)

        with torch.no_grad():
            if images and self._vae is not None:
                # Preprocess each image and build concatenated image embeds
                all_image_embeds = []
                for img in images:
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    img_t = T.Compose([
                        T.Resize(432, interpolation=T.InterpolationMode.BICUBIC),
                        T.CenterCrop(432),
                        T.ToTensor(),
                        T.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
                    ])(img).to(device, dtype=next(inner.parameters()).dtype)

                    image_latents = self._vae.sample(
                        img_t.unsqueeze(0).unsqueeze(2)
                    ).squeeze(2).to(model_dtype)

                    img_embeds_und = inner.image_embedder_und(image_latents)
                    img_embeds_gen = inner.image_embedder_gen(image_latents)
                    img_embeds_und = img_embeds_und + inner.position_embedding(inner.image_position_ids)
                    img_embeds_und = inner.und_trans(img_embeds_und)["last_hidden_state"]
                    img_embeds = inner.fusion_proj(torch.cat([img_embeds_und, img_embeds_gen], dim=-1))
                    all_image_embeds.append(img_embeds)

                # Concatenate all image embeddings
                image_embeds = torch.cat(all_image_embeds, dim=1)
                total_img_tokens = image_embeds.shape[1]

                # Time embedding (shared)
                time_embeds = None
                if add_time_embeds:
                    time_embeds = inner.time_embed(
                        torch.Tensor([[1.0]]).to(device), text_embeds_a.dtype
                    )
                    if hasattr(inner, "time_embed_proj"):
                        time_embeds = inner.time_embed_proj(time_embeds)

                # Concatenate: [sys] + [boi] + [time_embed] + [all_image_embeds] + [eoi+question+assistant]
                if time_embeds is not None:
                    input_embeds = torch.cat([
                        text_embeds_a,
                        text_embeds_b[:, :1],   # boi
                        time_embeds,
                        image_embeds,
                        text_embeds_b[:, 1:],    # eoi + question + assistant
                    ], dim=1)
                    modality_positions = torch.tensor(
                        [text_tokens_a_t.shape[1] + 2, total_img_tokens]
                    )[None, None, :].to(device)
                else:
                    input_embeds = torch.cat([
                        text_embeds_a,
                        text_embeds_b[:, :1],   # boi
                        image_embeds,
                        text_embeds_b[:, 1:],    # eoi + question + assistant
                    ], dim=1)
                    modality_positions = torch.tensor(
                        [text_tokens_a_t.shape[1] + 1, total_img_tokens]
                    )[None, None, :].to(device)
            else:
                # No image — text only
                input_embeds = torch.cat([
                    text_embeds_a,
                    text_embeds_b[:, :1],
                    text_embeds_b[:, 1:],
                ], dim=1)
                modality_positions = torch.tensor([0, 0])[None, None, :].to(device)

            # Build attention mask: causal + bidirectional within image block
            seq_len = input_embeds.size(1)
            attention_mask = omni_attn_mask_naive(
                B=input_embeds.size(0),
                LEN=seq_len,
                modalities=modality_positions,
                device=device,
                inverted=True,
            ).to(input_embeds.dtype)

            # Generate
            generated = inner.mmu_generate(
                input_embeds=input_embeds,
                attention_mask=attention_mask,
                max_new_tokens=max_new_tokens,
                temperature=1.0,
                top_k=1,
                eos_token=tids["eos_id"],
            )

        generated_ids = [t.item() if torch.is_tensor(t) else t for t in generated]
        response = tokenizer.decode(generated_ids, skip_special_tokens=True)
        return response.strip()

    # ------------------------------------------------------------------
    # draw()
    # ------------------------------------------------------------------

    def draw(self, context: Message, instruction: str, **kw) -> "Image.Image":
        """Generate an image via ODE sampling + VAE decode.

        Aligned with official inference_t2i.py:
        1. create_transport (Linear/velocity) + Sampler
        2. prepare_gen_input → text tokens + modality positions
        3. Sample noise z, duplicate for CFG if guidance_scale > 0
        4. sampler.sample_ode(euler, num_steps, time_shifting_factor)
        5. VAE batch_decode → PIL image
        """
        import torch
        from PIL import Image
        from ...vendor.showo2.transport import create_transport
        from ...vendor.showo2.transport.transport import Sampler
        from ...vendor.showo2.models import omni_attn_mask_naive
        from ...vendor.showo2.models.misc import prepare_gen_input

        device = self._device
        model = self._model
        tokenizer = self._tokenizer
        tids = self._showo_token_ids
        inner = model.showo2

        # Config parameters
        config = inner.config
        image_latent_dim = getattr(config, "image_latent_dim", 16)
        latent_height = getattr(config, "image_latent_height", 27)
        latent_width = getattr(config, "image_latent_width", 27)
        patch_size = getattr(config, "patch_size", 2)
        add_time_embeds = getattr(config, "add_time_embeds", False)

        # Token counts (official convention)
        num_t2i_image_tokens = latent_height * latent_width  # 27*27 = 729
        if add_time_embeds:
            num_t2i_image_tokens += 1  # 730
        max_seq_len = 1024
        max_text_len = max_seq_len - num_t2i_image_tokens - 4  # 290

        # Build prompt — extract text AND images from context
        input_list = to_interleave_list(context)
        text_parts = [item for item in input_list if isinstance(item, str)]
        context_images = [item for item in input_list if not isinstance(item, str)]
        context_text = "\n".join(text_parts)
        prompt = f"{context_text}\n{instruction}" if context_text else instruction
        prompts = [prompt]

        # NOTE: Show-o2's t2i_generate does not natively support image
        # conditioning. Context images are extracted here for future I2I
        # support, but current generation is text-conditioned only.

        # Generation parameters
        guidance_scale = kw.get("guidance_scale", self._guidance_scale)
        num_steps = kw.get("num_steps", self._num_steps)
        time_shifting_factor = kw.get("time_shifting_factor", self._time_shifting_factor)
        model_dtype = next(inner.parameters()).dtype

        with torch.no_grad():
            # 1. Transport + sampler
            transport = create_transport(
                path_type="Linear",
                prediction="velocity",
                snr_type="lognorm",
                do_shift=True,
                seq_len=num_t2i_image_tokens,
            )
            sampler = Sampler(transport)

            # 2. Text tokens via prepare_gen_input
            batch_text_tokens, batch_text_tokens_null, batch_modality_positions, batch_modality_positions_null = \
                prepare_gen_input(
                    prompts, tokenizer, num_t2i_image_tokens,
                    tids["bos_id"], tids["eos_id"],
                    tids["boi_id"], tids["eoi_id"],
                    tokenizer.pad_token_id, tids["img_pad_id"],
                    max_text_len, device,
                )

            # 3. Sample noise z: (B, C, H, W) = (1, 16, 54, 54)
            z = torch.randn(
                (len(prompts), image_latent_dim,
                 latent_height * patch_size, latent_width * patch_size),
                dtype=model_dtype, device=device,
            )

            # 4. CFG: duplicate for cond + uncond
            if guidance_scale > 0:
                z = torch.cat([z, z], dim=0)
                text_tokens = torch.cat([batch_text_tokens, batch_text_tokens_null], dim=0)
                modality_positions = torch.cat([batch_modality_positions, batch_modality_positions_null], dim=0)
            else:
                text_tokens = batch_text_tokens
                modality_positions = batch_modality_positions

            # 5. Attention mask
            block_mask = omni_attn_mask_naive(
                B=text_tokens.size(0),
                LEN=max_seq_len,
                modalities=modality_positions,
                device=device,
            ).to(model_dtype)

            # 6. ODE sampling
            model_kwargs = dict(
                text_tokens=text_tokens,
                attention_mask=block_mask,
                modality_positions=modality_positions,
                output_hidden_states=True,
                max_seq_len=max_seq_len,
                guidance_scale=guidance_scale,
            )

            # Wrap t2i_generate: ODE solver calls model(x, t, **kwargs) positionally,
            # but t2i_generate expects image_latents=, t= as keyword args.
            def _model_fn(x, t, **kwargs):
                return model.t2i_generate(image_latents=x, t=t, **kwargs)

            sample_fn = sampler.sample_ode(
                sampling_method="euler",
                num_steps=num_steps,
                atol=1e-6,
                rtol=1e-3,
                do_shift=True,
                time_shifting_factor=time_shifting_factor,
            )
            samples = sample_fn(z, _model_fn, **model_kwargs)[-1]

            # 7. Take conditional half (drop CFG duplicate)
            if guidance_scale > 0:
                samples = torch.chunk(samples, 2)[0]

            # 8. VAE decode
            if self._vae is None:
                raise RuntimeError("ShowO2 model has no VAE for latent decoding")
            samples = samples.unsqueeze(2)  # (B, C, 1, H, W)
            images = self._vae.batch_decode(samples)  # (B, 3, 1, H, W) in [-1, 1]
            images = images.squeeze(2)  # (B, 3, H, W)

            # 9. Convert to PIL
            images = torch.clamp((images + 1.0) / 2.0, 0.0, 1.0)
            arr = (images[0] * 255.0).to(torch.uint8).permute(1, 2, 0).cpu().numpy()
            return Image.fromarray(arr)
