"""U1 backend — SenseNova-U1 (NEOChatModel) understanding via our vendor model.

The understanding path is aligned with the official ``model.chat()`` /
``model.generate()`` flow from the SenseNova-U1 repo
(``examples/vqa/inference.py``):

  * images are preprocessed with the official ``load_image_native`` →
    ``(pixel_values, grid_hw)``;
  * the prompt is built with the ``neo1_0`` (Qwen) chat template and one
    ``<img><IMG_CONTEXT*N></img>`` block per image;
  * M-RoPE ``indexes`` are built with ``get_thw_indexes`` (temporal cumsum +
    2D grid h/w for image-context tokens);
  * ViT features from ``extract_feature`` are injected at ``<IMG_CONTEXT>``
    positions of ``inputs_embeds``;
  * greedy decoding runs over ``inputs_embeds`` with the correct indexes.

We cannot import the official ``sensenova_u1`` package directly because it
pins ``transformers==4.57.1`` while this environment runs transformers 5.x.
Instead we vendor the pure (image/tensor) helpers in
``mapspatial/vendor/neo_chat/inference_utils.py`` and drive our own
transformers-5-compatible ``NEOChatModel`` (which loads the checkpoint fine)
through the same logic.

Strategy mapping:
  direct           → understand() (vision Q&A, no image generation)
  external_draw    → understand() + draw() (text + separate image gen)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import ClassVar

import torch

from ...config import BackendConfig
from ...compat import apply as apply_compat
from ...messages import to_interleave_list, strip_placeholders
from ...media import load_image
from ...types import Capabilities, Message, Prediction
from ...vendor.neo_chat.inference_utils import (
    load_image_native,
    get_thw_indexes,
    THINK_SKIP_SUFFIX,
)
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

        from ...loader import load_model, load_tokenizer
        from ...vendor.neo_chat.modeling_neo_chat import NEOChatModel

        (self._model, _) = load_model(model_path, NEOChatModel, device=device, dtype=dtype)
        self._tokenizer = load_tokenizer(model_path)
        self._device = device

        # Generation params from config
        gen = cfg.generate
        self._temperature = float(gen.get("temperature", 0.0))
        self._max_new_tokens = gen.get("max_new_tokens", 1024)

        # think_mode=False appends an empty <think></think> block so the model
        # emits a direct answer (short output, reliable extraction, fast).
        # Set backend_args.think_mode: true to enable reasoning.
        ba = cfg.backend_args
        self._think_mode = bool(ba.get("think_mode", False))

        # Draw params from backend_args
        self._image_size = tuple(ba.get("image_size", (512, 512)))
        self._cfg_scale = ba.get("cfg_scale", 4.0)
        self._num_steps = ba.get("num_steps", 30)
        self._seed = ba.get("seed", 42)

        self._system_prompt = cfg.system_prompt or ""

    @property
    def model_name(self) -> str:
        return self._cfg.name

    # ------------------------------------------------------------------
    # understand()
    # ------------------------------------------------------------------

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        """Vision understanding aligned with official examples/vqa/inference.py."""
        results: list[Prediction] = []
        for msg in messages:
            try:
                text = self._understand_one(msg, gen_kw)
                results.append(Prediction(text=text))
            except Exception as e:
                results.append(Prediction(error=str(e)))
        return results

    def _understand_one(self, msg: Message, gen_kw: dict) -> str:
        """Single-sample understanding mirroring official model.chat()/generate()."""
        device = self._device
        model = self._model
        tokenizer = self._tokenizer

        # Split interleaved message into text + PIL images.
        input_list = to_interleave_list(msg)
        text_parts = [item for item in input_list if isinstance(item, str)]
        images = [item for item in input_list if not isinstance(item, str)]
        question = strip_placeholders("\n".join(text_parts))

        max_new_tokens = gen_kw.get("max_new_tokens", self._max_new_tokens)

        # ── Preprocess images (official load_image_native) ──────────────
        if images:
            n = len(images)
            max_pixels = min(2048 * 2048, (4096 * 4096) // max(1, n))
            pv_list, gh_list = [], []
            for img in images:
                pv, gh = load_image_native(
                    img,
                    patch_size=model.patch_size,
                    downsample_ratio=model.downsample_ratio,
                    min_pixels=512 * 512,
                    max_pixels=max_pixels,
                    upscale=False,
                )
                pv_list.append(pv)
                gh_list.append(gh)
            pixel_values = torch.cat(pv_list).to(device, dtype=model.dtype)
            grid_hw = torch.cat(gh_list).to(device)
            # One <image> placeholder per image so each is injected.
            question = ("<image>\n" * n) + question
        else:
            pixel_values = None
            grid_hw = None

        # ── Build prompt with the neo1_0 (Qwen) chat template ───────────
        # Matches official get_conv_template('neo1_0').get_prompt().
        sys_msg = self._system_prompt or getattr(model, "system_message", "") or ""
        query = (
            f"<|im_start|>system\n{sys_msg}<|im_end|>\n"
            f"<|im_start|>user\n{question}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )
        if not self._think_mode:
            query += THINK_SKIP_SUFFIX  # empty <think></think> → direct answer

        # Replace each <image> with <img><IMG_CONTEXT*N></img>.
        if pixel_values is not None:
            for i in range(grid_hw.shape[0]):
                num_patch_token = int(
                    grid_hw[i, 0] * grid_hw[i, 1] * model.downsample_ratio ** 2
                )
                image_tokens = (
                    "<img>" + "<IMG_CONTEXT>" * num_patch_token + "</img>"
                )
                query = query.replace("<image>", image_tokens, 1)

        input_ids = tokenizer.encode(query, return_tensors="pt").to(device)  # [1, T]
        eos_id = tokenizer.convert_tokens_to_ids("<|im_end|>")

        # ── Build M-RoPE indexes (official get_thw_indexes) ────────────
        indexes = get_thw_indexes(
            input_ids[0], grid_hw,
            img_start_token_id=model.img_start_token_id,
            img_context_token_id=model.img_context_token_id,
            downsample_ratio=model.downsample_ratio,
        )  # [3, T]

        # ── Embed tokens + inject ViT features at <IMG_CONTEXT> ─────────
        embed_tokens = model.language_model.model.embed_tokens
        lm_head = model.language_model.lm_head
        inputs_embeds = embed_tokens(input_ids[0])  # [T, D]
        if pixel_values is not None:
            with torch.inference_mode():
                vit_embeds = model.extract_feature(
                    pixel_values, gen_model=False, grid_hw=grid_hw
                )  # [N, D]
            selected = (input_ids[0] == model.img_context_token_id)
            inputs_embeds[selected] = vit_embeds.reshape(-1, inputs_embeds.shape[-1]).to(
                inputs_embeds.dtype
            )
        cur_embeds = inputs_embeds.unsqueeze(0)  # [1, T, D]

        # ── Greedy decoding over inputs_embeds ──────────────────────────
        # No KV cache (recompute each step); fine for think_mode=False where
        # the model emits only a few tokens before <eos>.
        generated = []
        with torch.inference_mode():
            for _ in range(max_new_tokens):
                out = model.language_model.model(
                    inputs_embeds=cur_embeds,
                    indexes=indexes,
                    attention_mask=None,
                    use_cache=False,
                )
                logits = lm_head(out.last_hidden_state[:, -1, :])  # [1, vocab]
                next_id = int(logits[0].argmax(dim=-1).item())
                if next_id == eos_id:
                    break
                generated.append(next_id)
                next_embed = embed_tokens(
                    torch.tensor([[next_id]], device=device)
                )  # [1, 1, D]
                cur_embeds = torch.cat([cur_embeds, next_embed], dim=1)
                new_t = int(indexes[0].max().item()) + 1
                new_idx = torch.tensor(
                    [[new_t], [0], [0]], device=device, dtype=torch.long
                )  # [3, 1]
                indexes = torch.cat([indexes, new_idx], dim=1)

        return tokenizer.decode(generated, skip_special_tokens=True).strip()

    # ------------------------------------------------------------------
    # draw()
    # ------------------------------------------------------------------

    def draw(self, context: Message, instruction: str, **kw):
        """Image-to-image generation via model.it2i_generate().

        The model is loaded in bfloat16 but some generation ops (VAE conv,
        flash attention) don't support it. Temporarily cast to float32
        for generation, then restore original dtype.
        """
        from PIL import Image

        pil_images: list = []
        text_parts: list[str] = []
        for item in context:
            if item["type"] == "image":
                v = item["value"]
                if isinstance(v, (Path, str)):
                    pil_images.append(load_image(v))
                else:
                    pil_images.append(v)
            elif item["type"] == "text":
                text_parts.append(item["value"])

        context_text = "\n".join(text_parts)
        full_prompt = f"{context_text}\n{instruction}" if context_text else instruction

        image_size = tuple(kw.get("image_size", self._image_size))
        cfg_scale = kw.get("cfg_scale", self._cfg_scale)
        num_steps = kw.get("num_steps", self._num_steps)
        seed = kw.get("seed", self._seed)

        # Use autocast: keep bfloat16 for flash attention, auto-upcast to
        # float32 for ops that don't support bfloat16 (VAE conv, etc.)
        with torch.inference_mode():
            with torch.autocast(device_type="cuda", dtype=torch.float32):
                output = self._model.it2i_generate(
                    tokenizer=self._tokenizer,
                    prompt=full_prompt,
                    images=pil_images if pil_images else None,
                    image_size=image_size,
                    cfg_scale=cfg_scale,
                    img_cfg_scale=1.0,
                    num_steps=num_steps,
                    seed=seed,
                    think_mode=self._think_mode,
                )

        if isinstance(output, torch.Tensor):
            image_tensor = output.clamp(-1, 1) * 0.5 + 0.5
            image_tensor = image_tensor.cpu().squeeze(0)
            image_np = (image_tensor.permute(1, 2, 0).numpy() * 255).astype("uint8")
            pil_image = Image.fromarray(image_np)
        elif isinstance(output, Image.Image):
            pil_image = output
        else:
            raise RuntimeError(f"it2i_generate returned unexpected type: {type(output)}")

        return pil_image
