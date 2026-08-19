"""ViLaSR backend.

Ported from gate2building backends.py:1253-1340.
ViLaSR uses vLLM internally for both image and video inference.
For images, it delegates to VilasrModel.run().

VLMEvalKit's approach is simpler — uses Qwen2VLChat wrapper.
We support both via config.
"""

from __future__ import annotations

import os
from typing import ClassVar

from ..types import Capabilities, Message, Prediction
from ..config import BackendConfig
from ..compat import apply as apply_compat
from ..messages import to_placeholder_prompt, strip_placeholders
from ..media import load_image
from .base import Backend


class VilasrBackend(Backend):
    """ViLaSR backend — delegates to VilasrModel (vLLM-based)."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False, draw=False, native_interleave=False,
        max_images=24, video=True,
    )

    def __init__(self, cfg: BackendConfig) -> None:
        for var in ("WORLD_SIZE", "RANK", "LOCAL_RANK"):
            os.environ.pop(var, None)

        apply_compat(*self.COMPAT)

        self._cfg = cfg
        model_path = cfg.model_path

        from ..vendor.vilasr_model import VilasrModel

        temperature = cfg.generate.get("temperature", 0.0)
        max_tokens = cfg.generate.get("max_new_tokens", cfg.generate.get("max_tokens", 262144))

        self._model = VilasrModel(
            model_id=model_path,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=cfg.generate.get("top_p", 0.9),
        )
        self._max_steps = cfg.backend_args.get("max_steps", 10)
        self._timeout = cfg.backend_args.get("timeout", 30)
        self._model_name = cfg.name

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
        # Extract image paths and prompt
        prompt_parts = []
        image_paths = []
        for item in msg:
            if item["type"] == "text":
                prompt_parts.append(item["value"])
            elif item["type"] == "image":
                v = item["value"]
                if hasattr(v, "__fspath__"):
                    image_paths.append(str(v))
                else:
                    image_paths.append(str(v))

        prompt = "\n".join(prompt_parts)
        prompt = strip_placeholders(prompt)

        return self._model.run(
            image_paths=image_paths,
            prompt=prompt,
            max_num_steps=self._max_steps,
            timeout=self._timeout,
        )
