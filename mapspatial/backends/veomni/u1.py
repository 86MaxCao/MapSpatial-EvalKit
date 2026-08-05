"""U1 backend — wraps VeOmni NEOChatModel (SenseNova-U1).

Implements understand() and draw() for the U1 unified model.
U1 uses model.language_model() for understanding and model.it2i_generate()
for image-to-image generation.

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


class U1Backend(Backend):
    """SenseNova-U1 (NEOChatModel) backend with understand + draw."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False,            # serial loop, one sample at a time
        draw=True,              # it2i_generate for image generation
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
        from ...vendor.neo_chat.modeling_neo_chat import NEOChatModel

        (self._model, _) = load_model(
            model_path, NEOChatModel,
            device=device, dtype=dtype,
        )
        self._tokenizer = load_tokenizer(model_path)

        # Load processor (Qwen3-VL style) for image+text processing
        try:
            from ...loader import load_processor
            self._processor = load_processor(model_path)
        except Exception:
            self._processor = None

        self._device = device

        # Generation params from config
        gen = cfg.generate
        self._temperature = gen.get("temperature", 0.3)
        self._max_new_tokens = gen.get("max_new_tokens", 1024)

        # Draw params from backend_args
        ba = cfg.backend_args
        self._image_size = tuple(ba.get("image_size", (256, 256)))
        self._cfg_scale = ba.get("cfg_scale", 4.0)
        self._num_steps = ba.get("num_steps", 30)
        self._seed = ba.get("seed", 42)

        # System prompt
        self._system_prompt = cfg.system_prompt or None

    @property
    def model_name(self) -> str:
        return self._cfg.name

    # ------------------------------------------------------------------
    # understand()
    # ------------------------------------------------------------------

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        """Text-only understanding via model.language_model greedy loop.

        Serial loop: one Message at a time.
        Matches VeOmni infer_u1_understand calling convention.
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
        """Single-sample understanding matching VeOmni infer_u1_understand."""
        device = self._device
        model = self._model
        tokenizer = self._tokenizer

        # Extract text and images
        input_list = to_interleave_list(msg)
        text_parts = [item for item in input_list if isinstance(item, str)]
        images = [item for item in input_list if not isinstance(item, str)]
        prompt = "\n".join(text_parts)
        prompt = strip_placeholders(prompt)

        max_new_tokens = gen_kw.get("max_new_tokens", self._max_new_tokens)
        eos_id = tokenizer.eos_token_id

        if self._processor is not None and images:
            # Use processor to build input_ids + pixel_values (Qwen3-VL style)
            messages = [{"role": "user", "content": [
                *[{"type": "image", "image": img} for img in images],
                {"type": "text", "text": prompt},
            ]}]
            text = self._processor.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True,
            )
            inputs = self._processor(
                text=[text], images=images, return_tensors="pt",
            )
            input_ids = inputs["input_ids"].to(device)
            attention_mask = inputs["attention_mask"].to(device)
        else:
            # Fallback: text-only with manual chat template
            chat_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
            input_ids = tokenizer.encode(chat_prompt, return_tensors="pt").to(device)
            attention_mask = torch.ones_like(input_ids)

        # Greedy decoding loop — U1 requires indexes (M-RoPE position IDs)
        generated = []
        with torch.no_grad():
            for _ in range(max_new_tokens):
                seq_len = input_ids.shape[1]
                pos = torch.arange(seq_len, device=device)
                indexes = torch.stack([pos, pos, pos])  # [3, seq_len] — M-RoPE
                outputs = model.language_model(
                    input_ids=input_ids, attention_mask=attention_mask,
                    indexes=indexes,
                )
                logits = outputs.logits
                next_id = logits[0, -1].argmax(dim=-1).item()
                if next_id == eos_id:
                    break
                generated.append(next_id)
                input_ids = torch.cat(
                    [input_ids, torch.tensor([[next_id]], device=device)], dim=1,
                )
                attention_mask = torch.ones_like(input_ids)

        text = tokenizer.decode(generated, skip_special_tokens=True)
        return text.strip()

    # ------------------------------------------------------------------
    # draw()
    # ------------------------------------------------------------------

    def draw(self, context: Message, instruction: str, **kw):
        """Generate an image using model.it2i_generate().

        Flow:
          1. Extract context images + build prompt
          2. Call model.it2i_generate() with images, prompt, and params
          3. Convert output tensor to PIL Image (*0.5+0.5 denorm)
        """
        import torch
        from PIL import Image

        # Extract context images
        pil_images = []
        text_parts = []
        for item in context:
            if item["type"] == "image":
                v = item["value"]
                if isinstance(v, Path) or isinstance(v, str):
                    pil_images.append(load_image(v))
                else:
                    pil_images.append(v)
            elif item["type"] == "text":
                text_parts.append(item["value"])

        context_text = "\n".join(text_parts)
        full_prompt = f"{context_text}\n{instruction}" if context_text else instruction

        # Draw params (overridable via kw)
        image_size = tuple(kw.get("image_size", self._image_size))
        cfg_scale = kw.get("cfg_scale", self._cfg_scale)
        num_steps = kw.get("num_steps", self._num_steps)
        seed = kw.get("seed", self._seed)

        # Call it2i_generate — image-to-image generation
        # NOTE: exact signature may differ; needs verification at runtime
        with torch.no_grad():
            output = self._model.it2i_generate(
                tokenizer=self._tokenizer,
                prompt=full_prompt,
                images=pil_images if pil_images else None,
                image_size=image_size,
                cfg_scale=cfg_scale,
                num_steps=num_steps,
                seed=seed,
            )

        # Output is a tensor [1, 3, H, W] in [-1, 1] range
        # Denormalize: x * 0.5 + 0.5 → [0, 1]
        if isinstance(output, torch.Tensor):
            image_tensor = output.clamp(-1, 1)
            image_tensor = image_tensor * 0.5 + 0.5
            image_tensor = image_tensor.cpu().squeeze(0)  # [3, H, W]
            image_np = (image_tensor.permute(1, 2, 0).numpy() * 255).astype("uint8")
            pil_image = Image.fromarray(image_np)
        elif isinstance(output, Image.Image):
            pil_image = output
        else:
            raise RuntimeError(
                f"it2i_generate returned unexpected type: {type(output)}"
            )

        return pil_image
