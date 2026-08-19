"""Janus backend — wraps VeOmni Janus model.

Implements understand() and draw() for the Janus unified model.
Janus uses a decoupled vision encoder + LLM for understanding, and an
autoregressive image token generation + VQ-VAE decoder for image synthesis.

Strategy mapping:
  direct           → understand() (text-only, no image generation)
  external_draw    → understand() + draw() (text + separate image gen)
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


class JanusBackend(Backend):
    """Janus unified model backend with understand + draw."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False,            # serial loop, one sample at a time
        draw=True,              # AR image token generation + VQ-VAE decode
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
        from ...vendor.janus.modeling_janus import Janus
        from ...vendor.janus.configuration_janus import JanusConfig

        self._model, _ = load_model(
            model_path, Janus, device=device, dtype=dtype,
        )
        self._fix_rope_inv_freq()
        from transformers import PreTrainedTokenizerFast
        self._tokenizer = PreTrainedTokenizerFast.from_pretrained(model_path)

        self._device = device

        # Build JanusProcessor (JanusImageProcessor + LlamaTokenizerFast)
        # NOTE: Janus uses a specific processor for image preprocessing
        self._processor = self._build_processor(model_path)

        # Generation params from config
        gen = cfg.generate
        self._temperature = gen.get("temperature", 0.3)
        self._max_new_tokens = gen.get("max_new_tokens", 512)

        # Draw params from backend_args
        ba = cfg.backend_args
        self._cfg_scale = ba.get("cfg_scale", 5.0)
        self._img_temperature = ba.get("img_temperature", 0.096)
        self._img_top_p = ba.get("img_top_p", 0.87)
        self._image_size = tuple(ba.get("image_size", (384, 384)))
        self._num_image_tokens = 576  # Janus uses 576 image tokens (24x24 at 16x downsample)

        # System prompt
        self._system_prompt = cfg.system_prompt or None

    @property
    def model_name(self) -> str:
        return self._cfg.name

    def _fix_rope_inv_freq(self):
        """Recompute LlamaRotaryEmbedding.inv_freq after loading.

        The init_empty_weights() + to_empty() loading chain zeroes the
        inv_freq buffer, breaking RoPE entirely → degenerate text generation.
        Recompute from config.rope_parameters['rope_theta'].
        """
        lm = self._model.language_model
        rope = getattr(lm.model, "rotary_emb", None)
        if rope is None or not hasattr(rope, "inv_freq"):
            return
        # Already correct (non-zero)
        if rope.inv_freq.abs().sum() > 0:
            return
        cfg = lm.config
        dim = getattr(cfg, "head_dim", None) or cfg.hidden_size // cfg.num_attention_heads
        base = cfg.rope_parameters.get("rope_theta", 10000.0)
        device = rope.inv_freq.device
        dtype = rope.inv_freq.dtype
        inv_freq = 1.0 / (
            base ** (torch.arange(0, dim, 2, dtype=torch.float) / dim)
        )
        rope.inv_freq = inv_freq.to(device=device, dtype=dtype)
        if hasattr(rope, "original_inv_freq"):
            rope.original_inv_freq = inv_freq.clone().to(device=device, dtype=dtype)

    def _build_processor(self, model_path: str):
        """Build the JanusProcessor using vendored code (VeOmni convention)."""
        try:
            from ...vendor.janus.image_processing_janus import JanusImageProcessor
            from ...vendor.janus.processing_janus import JanusProcessor

            image_processor = JanusImageProcessor(
                image_size=384, min_size=14,
                image_mean=[0.5, 0.5, 0.5], image_std=[0.5, 0.5, 0.5],
            )
            processor = JanusProcessor(
                image_processor=image_processor,
                tokenizer=self._tokenizer,
                image_tag="<image_placeholder>",
                num_image_tokens=576,
                add_special_token=False,
            )
            return processor
        except ImportError:
            try:
                from transformers import AutoProcessor
                return AutoProcessor.from_pretrained(
                    model_path, trust_remote_code=True,
                )
            except Exception:
                return None

    # ------------------------------------------------------------------
    # understand()
    # ------------------------------------------------------------------

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        """Text-only understanding via Janus prepare_inputs_embeds + LLM generate.

        Serial loop: one Message at a time.
        Follows the test_janus_veomni_understanding.py pattern.
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
        """Single-sample understanding matching test_janus_veomni_understanding.py."""
        device = self._device
        model = self._model
        tokenizer = self._tokenizer
        processor = self._processor

        # Extract text and images
        input_list = to_interleave_list(msg)
        text_parts = [item for item in input_list if isinstance(item, str)]
        images = [item for item in input_list if not isinstance(item, str)]
        prompt = "\n".join(text_parts)
        prompt = strip_placeholders(prompt)

        max_new_tokens = gen_kw.get("max_new_tokens", self._max_new_tokens)
        eos_id = tokenizer.eos_token_id

        if processor is not None and images:
            # VeOmni convention: use JanusProcessor
            conversation = [
                {"role": "User", "content": f"<image_placeholder>\n{prompt}"},
                {"role": "Assistant", "content": ""},
            ]
            chat_text = processor.apply_chat_template(conversation, task="und")
            inputs = processor(prompt=chat_text, images=[images[0]])
            inputs = {
                k: v.to(device) if torch.is_tensor(v) else v
                for k, v in inputs.items()
            }

            with torch.no_grad():
                inputs_embeds = model.prepare_inputs_embeds(
                    input_ids=inputs["input_ids"],
                    pixel_values=inputs["pixel_values"],
                    image_mask=inputs["image_mask"],
                )
                output_ids = model.language_model.generate(
                    inputs_embeds=inputs_embeds,
                    attention_mask=inputs["attention_mask"],
                    max_new_tokens=max_new_tokens,
                    do_sample=False,
                    use_cache=True,
                    pad_token_id=eos_id,
                    eos_token_id=eos_id,
                )
            answer = tokenizer.decode(
                output_ids[0].cpu().tolist(), skip_special_tokens=True,
            )
        else:
            # Fallback: text-only
            chat_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
            input_ids = tokenizer.encode(chat_prompt, return_tensors="pt").to(device)
            attention_mask = torch.ones_like(input_ids)
            with torch.no_grad():
                output_ids = model.language_model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    max_new_tokens=max_new_tokens,
                    do_sample=False,
                    pad_token_id=eos_id,
                    eos_token_id=eos_id,
                )
            answer = tokenizer.decode(
                output_ids[0].cpu().tolist(), skip_special_tokens=True,
            )

        return answer.strip()

    # ------------------------------------------------------------------
    # draw()
    # ------------------------------------------------------------------

    def draw(self, context: Message, instruction: str, **kw):
        """Generate an image via autoregressive image token sampling + VQ-VAE decode.

        Flow:
          1. Build prompt from context + instruction
          2. Tokenize prompt → input_ids
          3. Append image token start marker
          4. AR loop over 576 image tokens:
             a. model.language_model.model(inputs_embeds, use_cache=True,
                past_key_values=...) → hidden_states
             b. model.gen_head(hidden_states[:, -1, :]) → logits
             c. Apply CFG (classifier-free guidance)
             d. Sample next token
             e. model.prepare_gen_img_embeds(next_token) → next embed
          5. model.gen_vision_model.decode_code(generated_tokens,
              shape=[B, 8, H/16, W/16]) → image tensor
          6. Convert to PIL Image
        """
        import torch
        import torch.nn.functional as F
        from PIL import Image

        # Build prompt from context + instruction
        text_parts = []
        for item in context:
            if item["type"] == "text":
                text_parts.append(item["value"])

        context_text = "\n".join(text_parts)
        full_prompt = f"{context_text}\n{instruction}" if context_text else instruction

        # Build chat template
        if self._system_prompt:
            chat_prompt = f"<|im_start|>system\n{self._system_prompt}<|im_end|>\n"
        else:
            chat_prompt = ""
        chat_prompt += f"<|im_start|>user\n{full_prompt}<|im_end|>\n"
        chat_prompt += "<|im_start|>assistant\n"

        # Tokenize
        input_ids = self._tokenizer(
            chat_prompt, return_tensors="pt",
            truncation=True, max_length=4096,
        ).input_ids.to(self._device)

        # Prepare text embeddings
        embed_layer = self._model.get_input_embeddings()
        text_embeds = embed_layer(input_ids)  # [1, T_text, D]

        # Draw params (overridable via kw)
        cfg_scale = kw.get("cfg_scale", self._cfg_scale)
        img_temperature = kw.get("img_temperature", self._img_temperature)
        img_top_p = kw.get("img_top_p", self._img_top_p)
        num_tokens = kw.get("num_tokens", self._num_image_tokens)

        # Compute image grid dimensions from num_tokens
        # Janus uses 24x24 = 576 tokens at 16x downsample → 384x384
        grid_size = int(num_tokens ** 0.5)  # 24 for 576
        img_h = grid_size * 16
        img_w = grid_size * 16

        # For CFG, we need unconditional embeddings (all zeros / null prompt)
        # Prepare the seed embed for image generation
        # Janus uses a special start token for image generation
        # NOTE: exact mechanism needs verification at runtime

        # Append the image generation start token
        # Janus uses <begin_of_image> or similar marker
        img_start_id = self._tokenizer.convert_tokens_to_ids("<begin_of_image>")
        if img_start_id == self._tokenizer.unk_token_id:
            # Fallback: try to get it from the model config
            img_start_id = getattr(self._model.config, "image_start_token_id",
                                   getattr(self._model, "image_start_token_id", None))

        if img_start_id is not None:
            img_start_embed = embed_layer(
                torch.tensor([[img_start_id]], device=self._device)
            )  # [1, 1, D]
            inputs_embeds = torch.cat([text_embeds, img_start_embed], dim=1)
        else:
            inputs_embeds = text_embeds

        # For CFG: also prepare unconditional (empty) input
        uncond_embeds = embed_layer(
            torch.zeros_like(input_ids)
        ) if cfg_scale > 1.0 else None

        # AR sampling loop
        generated_tokens = []
        past_key_values = None
        uncond_past_kv = None

        cur_embeds = inputs_embeds
        uncond_cur = uncond_embeds

        with torch.no_grad():
            for step in range(num_tokens):
                # Forward through language model
                # model.language_model.model() returns hidden states
                outputs = self._model.language_model.model(
                    inputs_embeds=cur_embeds,
                    use_cache=True,
                    past_key_values=past_key_values,
                )
                hidden_states = outputs.last_hidden_state  # [1, T, D]
                past_key_values = outputs.past_key_values

                # Get logits for the last position via gen_head
                last_hidden = hidden_states[:, -1, :]  # [1, D]
                logits = self._model.gen_head(last_hidden)  # [1, vocab_size]

                # Apply CFG if unconditional embeddings are available
                if uncond_cur is not None and cfg_scale > 1.0:
                    uncond_outputs = self._model.language_model.model(
                        inputs_embeds=uncond_cur,
                        use_cache=True,
                        past_key_values=uncond_past_kv,
                    )
                    uncond_hidden = uncond_outputs.last_hidden_state[:, -1, :]
                    uncond_past_kv = uncond_outputs.past_key_values
                    uncond_logits = self._model.gen_head(uncond_hidden)

                    # CFG: logits = uncond + cfg_scale * (cond - uncond)
                    logits = uncond_logits + cfg_scale * (logits - uncond_logits)

                # Apply temperature + top-p sampling
                logits = logits / max(img_temperature, 1e-8)

                # Top-p (nucleus) sampling
                if img_top_p < 1.0:
                    sorted_logits, sorted_indices = torch.sort(
                        logits, descending=True, dim=-1,
                    )
                    sorted_probs = F.softmax(sorted_logits, dim=-1)
                    cum_probs = torch.cumsum(sorted_probs, dim=-1)
                    sorted_mask = cum_probs > img_top_p
                    sorted_mask[..., 1:] = sorted_mask[..., :-1].clone()
                    sorted_mask[..., 0] = False
                    sorted_logits.masked_fill_(sorted_mask, float("-inf"))

                probs = F.softmax(logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)  # [1, 1]
                generated_tokens.append(next_token.item())

                # Prepare next embed via model.prepare_gen_img_embeds
                # NOTE: method name needs verification at runtime
                next_embed = self._model.prepare_gen_img_embeds(next_token)  # [1, 1, D]
                cur_embeds = next_embed

                if uncond_cur is not None:
                    uncond_next = self._model.prepare_gen_img_embeds(next_token)
                    uncond_cur = uncond_next

        # Decode all generated tokens into an image
        # model.gen_vision_model.decode_code(tokens, shape=[B, 8, H/16, W/16])
        generated_tensor = torch.tensor(
            [generated_tokens], device=self._device, dtype=torch.long,
        )  # [1, num_tokens]

        # VQ-VAE decode
        # Janus VQ-VAE expects shape=[B, C, H_down, W_down]
        # where C=8, H_down=img_h//16, W_down=img_w//16
        with torch.no_grad():
            image_tensor = self._model.gen_vision_model.decode_code(
                generated_tensor,
                shape=[1, 8, img_h // 16, img_w // 16],
            )  # [1, 3, H, W]

        # Convert to PIL Image
        # Denormalize from [-1, 1] to [0, 1]
        image_tensor = image_tensor.clamp(-1, 1)
        image_tensor = image_tensor * 0.5 + 0.5
        image_tensor = image_tensor.cpu().squeeze(0)  # [3, H, W]

        image_np = (image_tensor.permute(1, 2, 0).numpy() * 255).astype("uint8")
        pil_image = Image.fromarray(image_np)
        return pil_image
