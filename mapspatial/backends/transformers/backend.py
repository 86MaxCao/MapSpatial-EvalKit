"""Transformers backend — shared base for HuggingFace transformers models.

Splits gate2building's 539-line monolithic TransformersBackend (9 branches)
into per-model-family submodules. Model class selection is explicit in config,
not guessed from model_id prefix.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import ClassVar

from ...types import Capabilities, Message, Prediction
from ...config import BackendConfig
from ...compat import apply as apply_compat
from ...messages import to_qwen_content, to_placeholder_prompt, strip_placeholders
from ...media import load_image
from ..base import Backend


class TransformersBackend(Backend):
    """Generic transformers backend. Dispatches to per-family inference logic.

    Config must specify model_class explicitly (not guessed from prefix):
      load:
        model_class: Qwen2_5_VLForConditionalGeneration
        processor_class: AutoProcessor
    """

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False, draw=False, native_interleave=False,
        max_images=24, video=False,
    )
    COMPAT: ClassVar[tuple[str, ...]] = ()

    def __init__(self, cfg: BackendConfig) -> None:
        # unset WORLD_SIZE to prevent HF auto TP
        for var in ("WORLD_SIZE", "RANK", "LOCAL_RANK"):
            os.environ.pop(var, None)

        apply_compat(*self.COMPAT)

        import torch
        from transformers import AutoProcessor

        load = cfg.load
        model_path = cfg.model_path

        # Determine model family from config
        self._model_family = load.get("model_family", "generic")
        self._prompt_style = cfg.backend_args.get("prompt_style", "qwen")
        self._image_key = cfg.backend_args.get("image_key", "image")
        self._cfg = cfg

        # Load processor
        self._processor = AutoProcessor.from_pretrained(
            model_path, trust_remote_code=load.get("trust_remote_code", True)
        )

        # Load model — delegate to family-specific loader
        self._model = self._load_model(model_path, load, torch)

        device = load.get("device", "auto")
        if device == "cuda":
            device = "auto"
        if device != "auto":
            self._model = self._model.to(device)

        self._model.eval()
        self._device = next(self._model.parameters()).device

    def _load_model(self, model_path: str, load: dict, torch):
        """Load model based on family. Override in subclasses or use config."""
        import torch
        from transformers import AutoModelForCausalLM

        model_class_name = load.get("model_class", "")
        dtype = getattr(torch, load.get("dtype", "bfloat16"))
        trust_remote = load.get("trust_remote_code", True)
        attn_impl = load.get("attn_implementation")

        kwargs = dict(trust_remote_code=trust_remote, torch_dtype=dtype)
        if attn_impl:
            kwargs["attn_implementation"] = attn_impl

        # Try to import the specific model class
        if model_class_name:
            import transformers
            cls = getattr(transformers, model_class_name, None)
            if cls is None:
                # Try AutoModel for custom code
                from transformers import AutoModel
                return AutoModel.from_pretrained(model_path, **kwargs)
            return cls.from_pretrained(model_path, **kwargs)

        return AutoModelForCausalLM.from_pretrained(model_path, **kwargs)

    @property
    def model_name(self) -> str:
        return self._cfg.name

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        """Serial inference — one message at a time."""
        gen = {**self._cfg.generate, **gen_kw}
        results = []
        for msg in messages:
            try:
                text = self._infer_one(msg, gen)
                results.append(Prediction(text=text))
            except Exception as e:
                results.append(Prediction(error=str(e)))
        return results

    def _infer_one(self, msg: Message, gen: dict) -> str:
        """Dispatch to family-specific inference."""
        family = self._model_family
        if family == "qwen_vl":
            return self._infer_qwen_vl(msg, gen)
        elif family == "internvl_custom":
            return self._infer_internvl_custom(msg, gen)
        elif family == "internvl_native":
            return self._infer_internvl_native(msg, gen)
        elif family == "glm":
            return self._infer_glm(msg, gen)
        else:
            return self._infer_generic(msg, gen)

    def _infer_qwen_vl(self, msg: Message, gen: dict) -> str:
        """Qwen2.5-VL / Qwen3-VL / Qwen3.5 / Qwen3.6 inference."""
        import torch
        from qwen_vl_utils import process_vision_info

        content = to_qwen_content(msg)
        messages = [{"role": "user", "content": content}]
        if self._cfg.system_prompt:
            messages.insert(0, {"role": "system", "content": self._cfg.system_prompt})

        text = self._processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self._processor(
            text=[text], images=image_inputs, videos=video_inputs,
            padding=True, return_tensors="pt"
        ).to(self._model.device)

        with torch.no_grad():
            output_ids = self._model.generate(
                **inputs,
                max_new_tokens=gen.get("max_new_tokens", 2048),
                do_sample=gen.get("temperature", 0.0) > 0,
                temperature=gen.get("temperature", 0.0) or 1.0,
            )

        # Trim input tokens
        input_len = inputs["input_ids"].shape[1]
        generated = output_ids[:, input_len:]
        text_out = self._processor.batch_decode(
            generated, skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )[0].strip()

        del inputs, output_ids
        torch.cuda.empty_cache()
        return text_out

    def _infer_glm(self, msg: Message, gen: dict) -> str:
        """GLM-4.6V / Step3-VL inference (url-style content)."""
        import torch
        from ...messages import to_url_content

        content = to_url_content(msg)
        messages = [{"role": "user", "content": content}]
        if self._cfg.system_prompt:
            messages.insert(0, {"role": "system", "content": self._cfg.system_prompt})

        inputs = self._processor.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True,
            return_dict=True, return_tensors="pt"
        )
        inputs = {k: v.to(self._model.device) for k, v in inputs.items()}
        inputs.pop("token_type_ids", None)

        with torch.no_grad():
            output_ids = self._model.generate(
                **inputs,
                max_new_tokens=gen.get("max_new_tokens", 4096),
                do_sample=gen.get("temperature", 0.0) > 0,
                temperature=gen.get("temperature", 0.0) or 1.0,
            )

        input_len = inputs["input_ids"].shape[1]
        generated = output_ids[:, input_len:]
        text_out = self._processor.batch_decode(
            generated, skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )[0].strip()

        del inputs, output_ids
        torch.cuda.empty_cache()
        return text_out

    def _infer_internvl_custom(self, msg: Message, gen: dict) -> str:
        """InternVL custom (trust_remote_code) — dynamic tiling + model.chat()."""
        import torch

        # Build placeholder prompt
        prompt_text, image_paths = to_placeholder_prompt(msg)
        clean_prompt = strip_placeholders(prompt_text)

        # Load and preprocess images
        from PIL import Image
        pixel_values_list = []
        num_patches_list = []
        for p in image_paths:
            img = load_image(p)
            tiles = self._internvl_preprocess(img)
            pixel_values_list.append(tiles)
            num_patches_list.append(tiles.shape[0])

        pixel_values = torch.cat(pixel_values_list, dim=0).to(
            dtype=torch.bfloat16, device=self._model.device
        )
        question = "\n".join(["<image>"] * len(image_paths)) + "\n" + clean_prompt
        generation_config = dict(
            max_new_tokens=gen.get("max_new_tokens", 2048),
            do_sample=gen.get("temperature", 0.0) > 0,
        )

        response = self._model.chat(
            self._tokenizer, pixel_values, question,
            generation_config, num_patches_list=num_patches_list,
        )
        del pixel_values
        torch.cuda.empty_cache()
        return response

    def _infer_internvl_native(self, msg: Message, gen: dict) -> str:
        """InternVL native (InternVLForConditionalGeneration)."""
        import torch
        from ...messages import to_url_content

        content = to_url_content(msg)
        messages = [{"role": "user", "content": content}]
        if self._cfg.system_prompt:
            messages.insert(0, {"role": "system", "content": self._cfg.system_prompt})

        inputs = self._processor.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True,
            return_dict=True, return_tensors="pt"
        )
        inputs = {k: v.to(self._model.device) for k, v in inputs.items()}
        inputs.pop("token_type_ids", None)

        with torch.no_grad():
            output_ids = self._model.generate(
                **inputs,
                max_new_tokens=gen.get("max_new_tokens", 2048),
                do_sample=gen.get("temperature", 0.0) > 0,
            )

        input_len = inputs["input_ids"].shape[1]
        generated = output_ids[:, input_len:]
        text_out = self._processor.batch_decode(
            generated, skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )[0].strip()

        del inputs, output_ids
        torch.cuda.empty_cache()
        return text_out

    def _infer_generic(self, msg: Message, gen: dict) -> str:
        """Generic fallback — AutoModelForCausalLM."""
        import torch

        # Collect images and build prompt
        images = []
        text_parts = []
        for item in msg:
            if item["type"] == "image":
                v = item["value"]
                if not isinstance(v, str) and not isinstance(v, Path):
                    images.append(v)  # PIL
                else:
                    images.append(load_image(v))
            elif item["type"] == "text":
                text_parts.append(item["value"])

        prompt = "\n".join(text_parts)
        if len(images) == 1:
            inputs = self._processor(
                images=images[0], text=prompt, return_tensors="pt"
            ).to(self._model.device)
        else:
            inputs = self._processor(
                images=images, text=prompt, return_tensors="pt"
            ).to(self._model.device)

        with torch.no_grad():
            output_ids = self._model.generate(
                **inputs, max_new_tokens=gen.get("max_new_tokens", 4096)
            )

        text_out = self._processor.batch_decode(
            output_ids, skip_special_tokens=True
        )[0].strip()

        del inputs, output_ids
        torch.cuda.empty_cache()
        return text_out

    def _internvl_preprocess(self, img):
        """InternVL dynamic preprocessing: 448x448 tiles + thumbnail."""
        import torch
        import torchvision.transforms as T
        from torchvision.transforms.functional import InterpolationMode
        import numpy as np

        input_size = 448
        max_num = 12
        mean = (0.485, 0.456, 0.406)
        std = (0.229, 0.224, 0.225)

        transform = T.Compose([
            T.Lambda(lambda img: img.convert("RGB")),
            T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
            T.ToTensor(),
            T.Normalize(mean=mean, std=std),
        ])

        w, h = img.size
        blocks = []
        # Find best aspect ratio match
        ratios = []
        for i in range(1, max_num + 1):
            for j in range(1, max_num + 1):
                if i * j <= max_num:
                    ratios.append((i, j, i / j, i * j))

        target_ratio = w / h
        best = min(ratios, key=lambda r: abs(r[2] - target_ratio))
        rows, cols = best[0], best[1]

        # Resize to (rows*input_size, cols*input_size)
        resized = img.resize((cols * input_size, rows * input_size))
        for i in range(rows):
            for j in range(cols):
                block = resized.crop((
                    j * input_size, i * input_size,
                    (j + 1) * input_size, (i + 1) * input_size
                ))
                blocks.append(transform(block))

        # Add thumbnail
        thumbnail = img.resize((input_size, input_size))
        blocks.append(transform(thumbnail))

        return torch.stack(blocks)
