"""SenseNova-SI backend.

Ported from gate2building backends.py:1121-1248.
Handles both regular SenseNova-SI models and SenseNova-SI-BAGEL variant.

Key: auto-inserts <image> placeholders to match image count.
For BAGEL mode, warns if model returns image path instead of text.
"""

from __future__ import annotations

import os
import tempfile
from typing import ClassVar

from ..types import Capabilities, Message, Prediction
from ..config import BackendConfig
from ..compat import apply as apply_compat
from ..messages import strip_placeholders
from ..media import load_image
from .base import Backend


class SenseNovaSIBackend(Backend):
    """SenseNova-SI backend (InternVL3/Qwen3-VL based, fine-tuned)."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False, draw=False, native_interleave=False,
        max_images=24, video=True,
    )

    VIDEO_NFRAMES = 16

    def __init__(self, cfg: BackendConfig) -> None:
        for var in ("WORLD_SIZE", "RANK", "LOCAL_RANK"):
            os.environ.pop(var, None)

        apply_compat(*self.COMPAT)

        self._cfg = cfg
        model_path = cfg.model_path
        model_id = cfg.name

        self._is_bagel = "bagel" in model_id.lower()

        from ...vendor.sensenova_si_pkg import get_model, SenseNovaSIBagelModel

        if self._is_bagel:
            mode = cfg.backend_args.get("mode", "understanding")
            self._model = SenseNovaSIBagelModel(
                model_path=model_path, mode=mode, dtype="bf16",
            )
        else:
            model_type = cfg.backend_args.get("model_type", "auto")
            self._model = get_model(model_path, model_type=model_type)

        self._model_name = model_id

    @property
    def model_name(self) -> str:
        return self._model_name

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        results = []
        for msg in messages:
            try:
                text = self._infer_one(msg, gen_kw)
                results.append(Prediction(text=text))
            except Exception as e:
                results.append(Prediction(error=str(e)))
        return results

    def _infer_one(self, msg: Message, gen_kw: dict) -> str:
        temp_files = []

        # Extract images and text
        image_paths = []
        text_parts = []
        for item in msg:
            if item["type"] == "image":
                v = item["value"]
                if hasattr(v, "__fspath__"):
                    image_paths.append(str(v))
                elif isinstance(v, str):
                    if v.startswith(("http://", "https://")):
                        img = load_image(v)
                        fd, tmp = tempfile.mkstemp(suffix=".jpg")
                        os.close(fd)
                        img.save(tmp)
                        image_paths.append(tmp)
                        temp_files.append(tmp)
                    else:
                        image_paths.append(v)
                else:
                    # PIL image
                    fd, tmp = tempfile.mkstemp(suffix=".jpg")
                    os.close(fd)
                    v.convert("RGB").save(tmp)
                    image_paths.append(tmp)
                    temp_files.append(tmp)
            elif item["type"] == "text":
                text_parts.append(item["value"])

        prompt = "\n".join(text_parts)
        prompt = strip_placeholders(prompt)

        # Auto-insert <image> placeholders to match image count
        num_images = len(image_paths)
        if num_images > 0:
            # Check existing <image> count
            existing = prompt.count("<image>")
            if existing == 0:
                prompt = "\n".join(["<image>"] * num_images) + "\n" + prompt
            elif existing != num_images:
                import sys
                print(f"WARNING: <image> count ({existing}) != image count ({num_images}), "
                      f"rebuilding placeholders", file=sys.stderr)
                prompt = "\n".join(["<image>"] * num_images) + "\n" + strip_placeholders(prompt)

        try:
            response = self._model.generate(
                question=prompt,
                images=image_paths or None,
            )

            # BAGEL safeguard
            if self._is_bagel:
                mode = self._cfg.backend_args.get("mode", "understanding")
                if mode != "understanding" and isinstance(response, str):
                    return response
                elif not isinstance(response, str) and not isinstance(response, list):
                    raise ValueError(f"BAGEL model returned unexpected type: {type(response)}")

            # Coerce to string
            if isinstance(response, list):
                response = response[0] if response else ""
            if not isinstance(response, str):
                response = str(response)

            return response

        finally:
            for f in temp_files:
                try:
                    os.unlink(f)
                except OSError:
                    pass
