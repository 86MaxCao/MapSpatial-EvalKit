"""Spatial-MLLM backend.

Vendored from the official Spatial-MLLM repository into
mapspatial/vendor/spatial_mllm (Qwen2.5-VL + VGGT spatial encoder).
Uses prepare_spatial_mllm_inputs (vendor/processing.py) for spatial encoding.

Key: padding_side="left" for batched generation.
"""

from __future__ import annotations

import os
import tempfile
from typing import ClassVar

from ..types import Capabilities, Message, Prediction
from ..config import BackendConfig
from ..compat import apply as apply_compat
from ..messages import to_qwen_content, strip_placeholders
from ..media import load_image
from .base import Backend


class SpatialMLLMBackend(Backend):
    """Spatial-MLLM backend."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False, draw=False, native_interleave=False,
        max_images=24, video=True,
    )

    MAX_NEW_TOKENS = 262144
    VIDEO_NFRAMES = 16

    def __init__(self, cfg: BackendConfig) -> None:
        for var in ("WORLD_SIZE", "RANK", "LOCAL_RANK"):
            os.environ.pop(var, None)

        apply_compat(*self.COMPAT)

        self._cfg = cfg
        model_path = cfg.model_path
        self._model_type = cfg.backend_args.get("model_type", "spatial-mllm")

        from ..vendor.spatial_mllm.spatial_mllm import (
            SpatialMLLMConfig,
            SpatialMLLMForConditionalGeneration,
        )
        from ..vendor.spatial_mllm.processing import prepare_spatial_mllm_inputs
        from transformers import Qwen2_5_VLProcessor

        config = SpatialMLLMConfig.from_pretrained(model_path)
        # transformers 5.8 moved hidden_size into config.text_config; the vendored
        # connector (get_connector) reads config.hidden_size directly. Restore it.
        if not getattr(config, "hidden_size", None):
            import json
            with open(os.path.join(model_path, "config.json")) as f:
                config.hidden_size = json.load(f)["hidden_size"]
        self._model = SpatialMLLMForConditionalGeneration.from_pretrained(
            model_path,
            config=config,
            torch_dtype="bfloat16",
            device_map="cuda",
        )
        self._processor = Qwen2_5_VLProcessor.from_pretrained(model_path)
        self._prepare_inputs = prepare_spatial_mllm_inputs
        self._model.eval()
        self._device = next(self._model.parameters()).device
        self._model_name = cfg.name

    @property
    def model_name(self) -> str:
        return self._model_name

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
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
        import torch
        from qwen_vl_utils import process_vision_info

        # Build content list
        content = []
        temp_files = []
        for item in msg:
            if item["type"] == "text":
                clean = strip_placeholders(item["value"])
                content.append({"type": "text", "text": clean})
            elif item["type"] == "image":
                v = item["value"]
                if hasattr(v, "__fspath__") or isinstance(v, str):
                    content.append({"type": "image", "image": str(v)})
                else:
                    # PIL image — materialize to temp file
                    fd, tmp_path = tempfile.mkstemp(suffix=".jpg")
                    os.close(fd)
                    v.convert("RGB").save(tmp_path)
                    content.append({"type": "image", "image": tmp_path})
                    temp_files.append(tmp_path)

        messages_payload = [{"role": "user", "content": content}]
        if self._cfg.system_prompt:
            messages_payload.insert(0, {"role": "system", "content": self._cfg.system_prompt})

        try:
            prompt_text = self._processor.apply_chat_template(
                messages_payload, tokenize=False, add_generation_prompt=True
            )
            image_inputs, video_inputs = process_vision_info(messages_payload)

            batch = self._processor(
                text=[prompt_text],
                images=image_inputs or None,
                videos=video_inputs or None,
                return_tensors="pt", padding=True, padding_side="left",
            )

            if self._prepare_inputs and "spatial-mllm" in self._model_type:
                batch = self._prepare_inputs(batch, video_inputs, image_inputs)

            batch = batch.to(self._device)

            # Move image_tchw / video_tchw lists to device
            if hasattr(batch, "image_tchw") and batch.get("image_tchw"):
                batch["image_tchw"] = [t.to(self._device) for t in batch["image_tchw"]]
            if hasattr(batch, "video_tchw") and batch.get("video_tchw"):
                batch["video_tchw"] = [t.to(self._device) for t in batch["video_tchw"]]

            temperature = gen.get("temperature", 0.0)
            gen_kwargs = dict(
                max_new_tokens=gen.get("max_new_tokens", self.MAX_NEW_TOKENS),
                use_cache=True,
            )
            if temperature > 0:
                gen_kwargs.update(do_sample=True, temperature=temperature, top_p=0.001)
            else:
                gen_kwargs.update(do_sample=False)

            with torch.no_grad():
                generated_ids = self._model.generate(**batch, **gen_kwargs)

            # Trim input tokens
            input_len = batch["input_ids"].shape[1]
            generated_ids = generated_ids[:, input_len:]
            text_out = self._processor.batch_decode(
                generated_ids, skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )[0].strip()

            del batch, generated_ids
            torch.cuda.empty_cache()
            return text_out

        finally:
            for f in temp_files:
                try:
                    os.unlink(f)
                except OSError:
                    pass
