"""API backend — HTTP-based inference for cloud models (Qwen Plus, Gemini, etc.).

Fixes issues from the predecessor internal pipeline:
  - Hardcoded API keys → environment variables (MAPSPATIAL_API_KEYS)
  - Key rotation self._idx race condition → threading.Lock
  - Concurrency granularity: (view,variant) → sample-level (runner handles this)
  - All keys treated as leaked → user should rotate

Preserves the predecessor pipeline's strengths:
  - Multi-key rotation on rate-limit
  - Per-model image compression (gemini=512/75, qwen/gpt=768/80, default=1024/85)
  - Exponential backoff + jitter
  - Response validation
"""

from __future__ import annotations

import base64
import io
import os
import random
import threading
import time
from pathlib import Path
from typing import ClassVar

from ..types import Capabilities, Message, Prediction
from ..config import BackendConfig
from ..messages import to_openai_content
from .base import Backend


class APIBackend(Backend):
    """HTTP API backend for cloud-hosted models."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=False, draw=False, native_interleave=False,
        max_images=24, video=False,
    )

    def __init__(self, cfg: BackendConfig) -> None:
        self._cfg = cfg
        self._model_name = cfg.name
        self._base_url = cfg.backend_args.get("api_url", "")
        # Unset env vars leave the literal "${VAR}" unexpanded; treat as empty
        # so the default endpoint below applies.
        if self._base_url.startswith("${"):
            self._base_url = ""

        # Read API keys from env or config
        env_keys = os.environ.get("MAPSPATIAL_API_KEYS", "")
        if env_keys:
            self._keys = [k.strip() for k in env_keys.split(",") if k.strip()]
        elif cfg.backend_args.get("api_key"):
            self._keys = [cfg.backend_args["api_key"]]
        else:
            raise ValueError(
                "No API keys configured. Set MAPSPATIAL_API_KEYS env var "
                "(comma-separated) or api_key in backend_args."
            )

        self._idx = 0
        self._lock = threading.Lock()
        self._max_retries = cfg.backend_args.get("max_retries", 5)
        self._initial_delay = cfg.backend_args.get("initial_delay", 2.0)
        self._timeout = tuple(cfg.backend_args.get("timeout", (180, 600)))
        self._enable_thinking = cfg.backend_args.get("enable_thinking", False)

    @property
    def model_name(self) -> str:
        return self._model_name

    def _rotate_key(self) -> None:
        """Thread-safe key rotation."""
        with self._lock:
            self._idx = (self._idx + 1) % len(self._keys)

    def _current_key(self) -> str:
        with self._lock:
            return self._keys[self._idx]

    def _get_image_sizing(self) -> tuple[int, int]:
        """Per-model image compression: (max_side, quality)."""
        name = self._model_name.lower()
        if "gemini" in name:
            return 512, 75
        if "qwen" in name or "gpt" in name:
            return 768, 80
        return 1024, 85

    def _encode_image(self, src) -> str:
        """Encode image to base64 data URL for API payload."""
        from PIL import Image

        if isinstance(src, str) and (src.startswith("http://") or src.startswith("https://")):
            return src
        if isinstance(src, str) and src.startswith("data:"):
            return src

        # Local path or PIL → compress to JPEG base64
        if isinstance(src, (str, Path)):
            img = Image.open(src).convert("RGB")
        elif isinstance(src, Image.Image):
            img = src.convert("RGB")
        else:
            raise TypeError(f"unsupported image type: {type(src)}")

        max_side, quality = self._get_image_sizing()
        if max(img.size) > max_side:
            ratio = max_side / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size)

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality)
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f"data:image/jpeg;base64,{b64}"

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        """Serial API calls — one per message."""
        results = []
        for msg in messages:
            try:
                text = self._call_api(msg, gen_kw)
                results.append(Prediction(text=text))
            except Exception as e:
                results.append(Prediction(error=str(e)))
        return results

    def _call_api(self, msg: Message, gen_kw: dict) -> str:
        """Build and send API request with retry + key rotation."""
        import requests

        # Build content
        content = []
        for item in msg:
            if item["type"] == "image":
                url = self._encode_image(item["value"])
                content.append({"type": "image_url", "image_url": {"url": url}})
            elif item["type"] == "text":
                content.append({"type": "text", "text": item["value"]})

        messages_payload = [{"role": "user", "content": content}]
        # Per-cell system prompt (from records) takes precedence over the
        # static YAML-level one.
        system_prompt = gen_kw.get("system_prompt") or self._cfg.system_prompt
        if system_prompt:
            messages_payload.insert(0, {"role": "system", "content": system_prompt})

        payload = {
            "model": self._cfg.backend_args.get("api_model", self._model_name),
            "messages": messages_payload,
            "modalities": ["text"],
            "temperature": float(gen_kw.get("temperature", 0.0)),
            "max_tokens": int(gen_kw.get("max_new_tokens", 2048)),
        }
        if self._enable_thinking:
            payload["enable_thinking"] = True

        max_tries = max(len(self._keys), 1) + 1
        last_err = None
        conn_fail = 0

        for attempt in range(max_tries):
            api_key = self._current_key()
            base_url = self._base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1"
            api_url = base_url.rstrip("/") + "/chat/completions"

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Connection": "close",
            }

            # After connection failure, disable thinking
            if conn_fail >= 1:
                payload.pop("enable_thinking", None)

            try:
                session = requests.Session()
                resp = session.post(
                    api_url, json=payload, headers=headers,
                    timeout=self._timeout,
                )
                session.close()

                if resp.status_code != 200:
                    err_text = resp.text[:500]
                    if "rate" in err_text.lower() or "limit" in err_text.lower():
                        self._rotate_key()
                        time.sleep(1)
                        continue
                    last_err = f"HTTP {resp.status_code}: {err_text}"
                    continue

                data = resp.json()
                if "error" in data:
                    err_msg = str(data["error"])
                    if "rate" in err_msg.lower() or "limit" in err_msg.lower():
                        self._rotate_key()
                        time.sleep(1)
                        continue
                    last_err = f"API error: {err_msg}"
                    continue

                return data["choices"][0]["message"]["content"]

            except (requests.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
                conn_fail += 1
                last_err = str(e)
            except Exception as e:
                err_str = str(e)
                if "rate" in err_str.lower() or "limit" in err_str.lower():
                    self._rotate_key()
                    time.sleep(1)
                    continue
                last_err = err_str

            # Backoff
            if attempt < max_tries - 1:
                delay = self._initial_delay * (2 ** attempt) + random.uniform(
                    0, 0.1 * self._initial_delay
                )
                time.sleep(delay)

        raise RuntimeError(
            f"API call failed after {max_tries} attempts: {last_err}"
        )
