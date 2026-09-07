"""LatentUM backend — wraps official LatentUMModel.

Uses the official inference API (model.answer) for understanding, which
handles image preprocessing (448×448 + ImageNet normalization), vision
feature extraction (pixel-shuffle + mlp1), <IMG_CONTEXT> token injection,
InternVL2.5 chat template, and LLM generate with KV cache.
"""

from __future__ import annotations

import os
import time
from copy import deepcopy
from typing import ClassVar

import torch
from PIL import Image

from ...types import Capabilities, Message, Prediction, TraceStep
from ...config import BackendConfig
from ...compat import apply as apply_compat
from ...messages import to_interleave_list, strip_placeholders
from ..base import Backend
from ... import vendor as _vendor  # noqa: F401  — registers model.latentum / model.decoder


class LatentUMBackend(Backend):
    """LatentUM backend using official model.answer() for understanding."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False,
        draw=True,
        # Native marker-driven interleave NEVER fires for this checkpoint on
        # general reasoning prompts (measured 0/400 on MapSpatial t1): the
        # base model only learned to emit '<img>' in FrozenLake-style
        # planning training. Use forced_interleave instead.
        native_interleave=False,
        max_images=24,
        video=False,
        forced_interleave=True,
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

        # Load via official LatentUMModel.from_pretrained (vendored)
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
        self._decoder = None

    @property
    def model_name(self) -> str:
        return self._cfg.name

    def _get_decoder(self):
        """Lazy-load and cache the pixel decoder (sibling checkpoint)."""
        if self._decoder is not None:
            return self._decoder
        decoder_path = self._cfg.backend_args.get("decoder_path", "")
        if not decoder_path:
            raise RuntimeError("No decoder available for image generation")
        from model.latentum.modeling_latentum import LatentUMDecoderModel
        decoder = LatentUMDecoderModel.from_pretrained(
            decoder_path, device=self._device, dtype=torch.bfloat16,
        )
        self._decoder = decoder.eval()
        return self._decoder

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
                    pv = _load_img(img, max_num=1)
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
        """Image-first G: condition on input maps, emit one image, drop KV.

        Official LatentUM only exposes text-only ``generate_latents()``.
        ``generate_latents_with_images`` does not exist, so the previous
        hasattr fallback was silent T2I and ignored the source map. Use the
        same image-conditioned prefill as ``interleave(image_first=True)``.
        """
        kw = dict(kw)
        # ar_head CFG>1 expects a concatenated (cond, uncond) batch. This
        # path only has one hidden state, so cfg_scale must stay <= 1.
        kw["cfg_scale"] = 1.0
        kw.setdefault("temperature", self._draw_temperature)
        kw.setdefault("do_sample", True)
        pred = self.interleave(
            context,
            instruction=instruction,
            max_rounds=1,
            image_first=True,
            max_images=1,
            followup="",
            **kw,
        )
        if pred.error:
            raise RuntimeError(pred.error)
        if not pred.generated_images:
            raise RuntimeError("draw() did not produce an image")
        return pred.generated_images[0]

    # ------------------------------------------------------------------
    # interleave() — native save-rewind-reinject loop
    # ------------------------------------------------------------------

    @staticmethod
    def _sample(logits: torch.Tensor, temperature: float, top_k: int, top_p: float) -> torch.Tensor:
        """Top-k / top-p sampling (mirrors FrozenLakePlanner._sample)."""
        logits = logits / max(temperature, 1e-5)
        if top_k > 0:
            values, _ = torch.topk(logits, min(top_k, logits.size(-1)))
            logits = logits.masked_fill(logits < values[..., -1, None], float("-inf"))
        probs = torch.softmax(logits, dim=-1)
        if 0.0 < top_p < 1.0:
            sorted_probs, sorted_indices = torch.sort(probs, descending=True)
            cumulative_probs = torch.cumsum(sorted_probs, dim=-1)
            sorted_mask = cumulative_probs > top_p
            sorted_mask[..., 1:] = sorted_mask[..., :-1].clone()
            sorted_mask[..., 0] = False
            probs = probs.scatter(
                -1,
                sorted_indices,
                sorted_probs.masked_fill(sorted_mask, 0.0),
            )
            probs = probs / probs.sum(dim=-1, keepdim=True)
        return torch.multinomial(probs, num_samples=1)

    @torch.inference_mode()
    def interleave(
        self,
        message: Message,
        instruction: str = "",
        *,
        max_rounds: int = 3,
        marker: str = "<img>",
        force_image_at: int = 0,
        image_first: bool = False,
        max_images: int | None = None,
        followup: str = "",
        **kw,
    ) -> Prediction:
        """Interleaved reasoning loop using the save-rewind-reinject pattern.

        NOTE: with ``force_image_at=0`` this is the marker-driven (native)
        mode, which never triggers for this checkpoint on general reasoning
        prompts — it is kept only as the engine for ``forced_interleave()``
        and is not registered as a strategy (caps.native_interleave=False).

        Based on the official FrozenLakePlanner.generate() method:
        1. Pre-fill prompt through LLM (vision_token_mask=0, use_cache=True)
        2. AR text generation (vision_token_mask=0)
        3. When ``<img>`` is emitted: save kv_before_img
        4. Generate 256 VQ codes via ar_head (vision_token_mask=1)
        5. Rewind to kv_before_img
        6. Re-inject generated image embeddings via visual_projector (vision_token_mask=0)
        7. Feed ``</img>`` token (vision_token_mask=0)
        8. Continue text generation for final answer

        Key differences from FrozenLakePlanner:
        - General task prompts (not FrozenLake-specific)
        - Multi-image input support
        - Returns Prediction with text, generated_images, trace
        """
        IMG_START_TOKEN = "<img>"
        IMG_END_TOKEN = "</img>"
        IMG_CONTEXT_TOKEN = "<IMG_CONTEXT>"

        internvl = self._model.internvl
        tokenizer = self._model.tokenizer
        quantizer = self._model.quantizer
        device = self._device
        dtype = self._model._runtime_dtype

        num_image_token = internvl.num_image_token          # per-patch <IMG_CONTEXT> count (256)
        num_gen_tokens = self._model.config.num_image_tokens  # VQ codes to generate (256)

        img_start_id = tokenizer.convert_tokens_to_ids(IMG_START_TOKEN)
        img_end_id = tokenizer.convert_tokens_to_ids(IMG_END_TOKEN)
        img_context_id = tokenizer.convert_tokens_to_ids(IMG_CONTEXT_TOKEN)
        eos_id = tokenizer.eos_token_id

        # -- 1. Extract text + images from Message (same as _understand_one) ----
        input_list = to_interleave_list(message)
        images = [item for item in input_list if not isinstance(item, str)]
        text_parts = [item for item in input_list if isinstance(item, str)]
        if instruction:
            text_parts.append(instruction)
        prompt_text = strip_placeholders("\n".join(text_parts))

        # -- 2. Preprocess images with official load_image ----------------------
        pv_list: list[torch.Tensor] = []
        if images:
            from model.latentum.image_utils import load_image as _load_img
            for img in images:
                pv = _load_img(img, max_num=1)
                if pv is None:
                    raise RuntimeError(f"Failed to load image: {img}")
                pv_list.append(pv)
            pixel_values = torch.cat(pv_list, dim=0).to(device, dtype=dtype)
            visual_emb = internvl.extract_feature(pixel_values)  # (N_patches, T, D)
        else:
            visual_emb = None

        # -- 3. Build prompt with <image> placeholders --------------------------
        from model.latentum.internvl.conversation import get_conv_template

        template = get_conv_template(internvl.template)
        if self._system_prompt:
            template.system_message = self._system_prompt

        question = ("<image>\n" * len(images)) + prompt_text if images else prompt_text
        template.append_message(template.roles[0], question)
        template.append_message(template.roles[1], None)
        prompt = template.get_prompt()

        # Replace each <image> placeholder with image token sequence
        for pv in pv_list:
            n_patches = pv.shape[0]
            image_tokens = IMG_START_TOKEN + IMG_CONTEXT_TOKEN * (num_image_token * n_patches) + IMG_END_TOKEN
            prompt = prompt.replace("<image>", image_tokens, 1)

        # -- 4. Tokenize and build input_embeds ---------------------------------
        tok_out = tokenizer([prompt], padding=True, padding_side="left",
                            truncation=False, return_tensors="pt")
        input_ids = tok_out["input_ids"].to(device)
        attention_mask = tok_out["attention_mask"].to(device)

        input_embeds = internvl.language_model.get_input_embeddings()(input_ids).clone()

        # Inject visual embeddings at <IMG_CONTEXT> positions
        if visual_emb is not None:
            ctx_positions = (input_ids[0] == img_context_id).nonzero(as_tuple=True)[0]
            emb_offset = 0
            for patch_idx in range(visual_emb.shape[0]):
                input_embeds[0, ctx_positions[emb_offset:emb_offset + num_image_token]] = visual_emb[patch_idx]
                emb_offset += num_image_token

        # -- 5. Pre-fill through LLM (vision_token_mask=0, use_cache=True) ------
        vt_mask = torch.zeros(1, input_embeds.shape[1], device=device, dtype=dtype)
        outputs = internvl.language_model.model(
            inputs_embeds=input_embeds,
            attention_mask=attention_mask,
            vision_token_mask=vt_mask,
            use_cache=True,
        )
        past_key_values = outputs.past_key_values
        last_hidden = outputs.last_hidden_state[:, -1:, :]

        # -- Generation params --------------------------------------------------
        temperature = kw.get("temperature", self._temperature)
        do_sample = kw.get("do_sample", self._do_sample)
        max_text_tokens = kw.get("max_new_tokens", self._max_new_tokens)
        cfg_scale = kw.get("cfg_scale", 1.0)
        top_k = kw.get("top_k", 50)
        top_p = kw.get("top_p", 0.95)

        sampling_kwargs = {
            "temperature": temperature if do_sample else 1.0,
            "top_k": top_k,
            "top_p": top_p,
            "sample_logits": do_sample,
        }

        n_image_cap = max_images if max_images is not None else (1 if image_first else max_rounds)
        n_images = 0

        # -- 6-9. Main interleave loop ------------------------------------------
        all_tokens: list[int] = []
        trace_steps: list[TraceStep] = []
        all_generated_codes: list[torch.Tensor] = []
        round_idx = 0

        def _pick_token(logits: torch.Tensor) -> int:
            if do_sample:
                return self._sample(logits, temperature, top_k, top_p).item()
            return logits.argmax(dim=-1).item()

        def _begin_image_phase(kv):
            kv_before = deepcopy(kv)
            img_embed = internvl.language_model.get_input_embeddings()(
                torch.tensor([[img_start_id]], device=device)
            )
            out = internvl.language_model.model(
                inputs_embeds=img_embed,
                past_key_values=kv,
                vision_token_mask=torch.ones(1, 1, device=device, dtype=dtype),
                use_cache=True,
            )
            return kv_before, deepcopy(out.past_key_values), out.last_hidden_state

        while round_idx < max_rounds:
            round_idx += 1
            step_tokens: list[int] = []
            found_img = False
            forced_this_round = False
            t_round = time.time()

            skip_pre_image_ar = (
                image_first and round_idx == 1 and n_images < n_image_cap
            )

            if skip_pre_image_ar:
                kv_before_img, past_key_values_phase2, base_hidden = _begin_image_phase(
                    past_key_values
                )
                found_img = True
                forced_this_round = True
            else:
                # -- AR text generation -------------------------------------------
                for _ in range(max_text_tokens):
                    logits = internvl.language_model.lm_head(last_hidden)[:, -1, :]
                    next_id = _pick_token(logits)
                    step_tokens.append(next_id)
                    all_tokens.append(next_id)

                    if next_id == img_start_id:
                        if n_images >= n_image_cap:
                            step_tokens.pop()
                            all_tokens.pop()
                            break
                        kv_before_img, past_key_values_phase2, base_hidden = (
                            _begin_image_phase(past_key_values)
                        )
                        found_img = True
                        break

                    # Forced mode (legacy, not image-first): inject after N tokens.
                    force_img = (
                        (not image_first)
                        and force_image_at > 0
                        and round_idx == 1
                        and n_images < n_image_cap
                        and (next_id == eos_id or len(step_tokens) >= force_image_at)
                    )
                    if next_id == eos_id and not force_img:
                        break

                    if force_img:
                        if next_id != eos_id:
                            step_tokens.pop()
                            all_tokens.pop()
                        kv_before_img, past_key_values_phase2, base_hidden = (
                            _begin_image_phase(past_key_values)
                        )
                        found_img = True
                        forced_this_round = True
                        break

                    next_embed = internvl.language_model.get_input_embeddings()(
                        torch.tensor([[next_id]], device=device)
                    )
                    outputs = internvl.language_model.model(
                        inputs_embeds=next_embed,
                        past_key_values=past_key_values,
                        vision_token_mask=torch.zeros(1, 1, device=device, dtype=dtype),
                        use_cache=True,
                    )
                    past_key_values = outputs.past_key_values
                    last_hidden = outputs.last_hidden_state

            # Record text trace step (skip empty pre-image round)
            text_elapsed = time.time() - t_round
            if step_tokens:
                text_content = tokenizer.decode(step_tokens, skip_special_tokens=True)
                trace_steps.append(TraceStep(
                    round=round_idx,
                    kind="text",
                    text=text_content,
                    triggered_by=(
                        "forced_image_first" if (image_first and found_img)
                        else ("forced" if forced_this_round else "model_marker")
                    ) if found_img else None,
                    elapsed_s=text_elapsed,
                ))

            if not found_img:
                break

            n_images += 1

            # -- 6. Image generation phase (256 VQ codes) ----------------------
            t_img = time.time()
            generated_codes: list[torch.Tensor] = []

            # First VQ code from base_hidden
            code = internvl.ar_head.generate_from_base_token(
                base_hidden,
                cfg_scale=cfg_scale,
                sampling_kwargs=sampling_kwargs,
            )
            generated_codes.append(code)

            # Remaining 255 VQ codes
            for _ in range(num_gen_tokens - 1):
                z_q, _ = quantizer.indices_to_feature(code.unsqueeze(1))
                current_input = internvl.visual_projector(z_q)
                outputs = internvl.language_model.model(
                    inputs_embeds=current_input,
                    past_key_values=past_key_values_phase2,
                    vision_token_mask=torch.ones(1, 1, device=device, dtype=dtype),
                    use_cache=True,
                )
                past_key_values_phase2 = outputs.past_key_values
                code = internvl.ar_head.generate_from_base_token(
                    outputs.last_hidden_state,
                    cfg_scale=cfg_scale,
                    sampling_kwargs=sampling_kwargs,
                )
                generated_codes.append(code)

            generated_codes_tensor = torch.stack(generated_codes, dim=1)  # (1, 256, K)
            all_generated_codes.append(generated_codes_tensor)

            # -- 7. Rewind to kv_before_img -----------------------------------
            img_embed = internvl.language_model.get_input_embeddings()(
                torch.tensor([[img_start_id]], device=device)
            )
            outputs = internvl.language_model.model(
                inputs_embeds=img_embed,
                past_key_values=kv_before_img,
                vision_token_mask=torch.zeros(1, 1, device=device, dtype=dtype),
                use_cache=True,
            )

            # -- 8. Re-inject generated image embeddings (vision_token_mask=0) -
            z_q, _ = quantizer.indices_to_feature(generated_codes_tensor)
            x_proj = internvl.visual_projector(z_q)
            outputs = internvl.language_model.model(
                inputs_embeds=x_proj,
                past_key_values=outputs.past_key_values,
                vision_token_mask=torch.zeros(1, num_gen_tokens, device=device, dtype=dtype),
                use_cache=True,
            )
            past_key_values = outputs.past_key_values

            # Feed </img> token (vision_token_mask=0)
            img_end_embed = internvl.language_model.get_input_embeddings()(
                torch.tensor([[img_end_id]], device=device)
            )
            outputs = internvl.language_model.model(
                inputs_embeds=img_end_embed,
                past_key_values=past_key_values,
                vision_token_mask=torch.zeros(1, 1, device=device, dtype=dtype),
                use_cache=True,
            )
            past_key_values = outputs.past_key_values
            last_hidden = outputs.last_hidden_state

            all_tokens.append(img_end_id)

            if followup:
                follow_ids = tokenizer(followup, add_special_tokens=False)["input_ids"]
                for tid in follow_ids:
                    next_embed = internvl.language_model.get_input_embeddings()(
                        torch.tensor([[tid]], device=device)
                    )
                    outputs = internvl.language_model.model(
                        inputs_embeds=next_embed,
                        past_key_values=past_key_values,
                        vision_token_mask=torch.zeros(1, 1, device=device, dtype=dtype),
                        use_cache=True,
                    )
                    past_key_values = outputs.past_key_values
                    last_hidden = outputs.last_hidden_state
                followup = ""

            img_elapsed = time.time() - t_img
            trace_steps.append(TraceStep(
                round=round_idx,
                kind="image",
                triggered_by=(
                    "forced_image_first" if image_first
                    else ("forced" if forced_this_round else "model_marker")
                ),
                elapsed_s=img_elapsed,
            ))

        # -- 10. Decode generated VQ codes via decoder -------------------------
        generated_images: list[Image.Image] = []
        if all_generated_codes:
            decoder = self._get_decoder()
            num_inf_steps = kw.get("num_inference_steps", 25)
            guidance_scale = kw.get("guidance_scale", 1.0)
            seed = kw.get("seed", 42)
            for codes in all_generated_codes:
                z_q, _ = quantizer.indices_to_feature(codes.to(self._device))
                decoded = decoder.decode(
                    z_q,
                    seed=seed,
                    num_inference_steps=num_inf_steps,
                    guidance_scale=guidance_scale,
                    height=self._model.config.image_size,
                    width=self._model.config.image_size,
                )
                generated_images.append(decoded[0])

        # -- 11. Return Prediction ----------------------------------------------
        full_text = tokenizer.decode(all_tokens, skip_special_tokens=True)

        return Prediction(
            text=full_text.strip(),
            generated_images=generated_images,
            trace=trace_steps,
            meta={
                "strategy": (
                    "forced_interleave" if (image_first or force_image_at > 0)
                    else "native_interleave"
                ),
                "rounds": round_idx,
                "draw_triggered": len(all_generated_codes) > 0,
                "backend": self.model_name,
                "pre_image_text_tokens": 0 if image_first else None,
                "reconsume_mode": "latent",
                "post_image_prompt_mode": "followup_appended",
            },
        )

    def forced_interleave(
        self,
        message: Message,
        instruction: str = "",
        *,
        max_images: int = 1,
        image_first: bool = True,
        followup: str = "",
        **kw,
    ) -> Prediction:
        """Image-first stateful G2U on a shared KV cache.

        C-F reconsumes the generated VQ latent (not a pixel re-encode).
        PNG is still decoded for viewing/saving.
        """
        kw = dict(kw)
        kw.pop("max_images", None)
        kw.pop("image_first", None)
        kw.pop("followup", None)
        kw.pop("max_rounds", None)
        # yaml generate.max_new_tokens is 128 (U-direct). After I0 the model
        # often restates the draw instruction and never reaches <answer>.
        if int(kw.get("max_new_tokens") or 0) < 512:
            kw["max_new_tokens"] = 512
        return self.interleave(
            message,
            instruction=instruction,
            max_rounds=2 if image_first else 3,
            force_image_at=0 if image_first else int(
                self._cfg.backend_args.get("force_image_at", 96)
            ),
            image_first=image_first,
            max_images=max_images,
            followup=followup,
            **kw,
        )
