"""VllmBackend — true batch vLLM inference.

Key principles (from docs/03-backends.md):
1. One llm.generate() call submits the entire batch — continuous batching works.
2. No torch.cuda.empty_cache() in the loop — it flushes KV cache.
3. Single-item prep failure doesn't block the batch (index_map).
4. limit_mm_per_prompt from config — t4 needs 4 images.

Borrowed from gate2building backends.py:418-521 (the correct implementation).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import ClassVar

from ..types import Capabilities, Message, Prediction
from ..config import BackendConfig
from ..compat import apply as apply_compat
from ..messages import to_qwen_content, to_placeholder_prompt, strip_placeholders
from .base import Backend


class VllmBackend(Backend):
    """vLLM backend with true batch inference."""

    caps: ClassVar[Capabilities] = Capabilities(
        batch=True, draw=False, native_interleave=False,
        max_images=24, video=False,
    )
    COMPAT: ClassVar[tuple[str, ...]] = ()

    def __init__(self, cfg: BackendConfig) -> None:
        # unset WORLD_SIZE to prevent HF auto tensor parallelism
        for var in ("WORLD_SIZE", "RANK", "LOCAL_RANK", "GROUP_RANK"):
            os.environ.pop(var, None)

        apply_compat(*self.COMPAT)

        from vllm import LLM, SamplingParams  # type: ignore
        from transformers import AutoProcessor

        load = cfg.load
        llm_kwargs = dict(
            model=cfg.model_path,
            max_model_len=load.get("max_model_len", 32768),
            gpu_memory_utilization=load.get("gpu_memory_utilization", 0.7),
            limit_mm_per_prompt=load.get("limit_mm_per_prompt", {"image": 24, "video": 1}),
            enforce_eager=load.get("enforce_eager", False),
            trust_remote_code=load.get("trust_remote_code", True),
            dtype=load.get("dtype", "bfloat16"),
        )
        # Only pass additional_config if it's a valid dict (vLLM rejects None)
        additional_config = load.get("additional_config")
        if additional_config is not None:
            llm_kwargs["additional_config"] = additional_config
        self._llm = LLM(**llm_kwargs)
        self._processor = AutoProcessor.from_pretrained(
            cfg.model_path, trust_remote_code=True
        )
        self._cfg = cfg
        self._SamplingParams = SamplingParams

        # Determine prompt style from config
        self._prompt_style = cfg.backend_args.get("prompt_style", "qwen")

    @property
    def model_name(self) -> str:
        return self._cfg.name

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        gen = {**self._cfg.generate, **gen_kw}
        sampling_params = self._SamplingParams(
            temperature=gen.get("temperature", 0.0),
            max_tokens=gen.get("max_new_tokens", gen.get("max_tokens", 4096)),
            top_p=gen.get("top_p", 1.0),
        )

        reqs: list[dict] = []
        index_map: list[int] = []  # maps valid index → original position

        for i, msg in enumerate(messages):
            try:
                req = self._to_vllm_request(msg)
                reqs.append(req)
                index_map.append(i)
            except Exception as e:
                # Don't block the batch — record error, skip this item
                index_map.append(-1)  # placeholder; we'll handle in output

        if not reqs:
            return [Prediction(error="all requests failed to prepare") for _ in messages]

        # Single generate call — true batch
        outputs = self._llm.generate(reqs, sampling_params)

        # Map outputs back to original positions
        results: list[Prediction] = [Prediction() for _ in messages]
        valid_idx = 0
        for orig_idx in range(len(messages)):
            mapped = index_map[orig_idx] if orig_idx < len(index_map) else -1
            if mapped == -1:
                # This was a failed prep — already has default Prediction()
                # But we need to find which ones failed
                pass

        # Rebuild: for each valid request, place output at its original position
        for out_idx, orig_pos in enumerate(
            [i for i in range(len(messages)) if i in set(index_map) and index_map[i] != -1]
        ):
            pass  # logic below is simpler

        # Simpler approach: build results by iterating valid indices
        results = []
        valid_positions = []
        for i, msg in enumerate(messages):
            try:
                req = self._to_vllm_request(msg)
                reqs_list = [req]
            except Exception as e:
                results.append(Prediction(error=str(e)))
                valid_positions.append(None)
                continue

        # Actually, let me simplify this
        return self._understand_impl(messages, sampling_params)

    def _understand_impl(self, messages, sampling_params) -> list[Prediction]:
        """Clean implementation with proper index mapping."""
        reqs = []
        index_map = []  # position in reqs → original index in messages

        for i, msg in enumerate(messages):
            try:
                req = self._to_vllm_request(msg)
                reqs.append(req)
                index_map.append(i)
            except Exception as e:
                # Skip — will fill error in results
                pass

        if not reqs:
            return [Prediction(error="request preparation failed") for _ in messages]

        # One generate call for the whole batch
        outputs = self._llm.generate(reqs, sampling_params)

        # Build results: default = error, overwrite successful ones
        results = [Prediction(error="not processed") for _ in messages]
        for out_idx, orig_idx in enumerate(index_map):
            text = outputs[out_idx].outputs[0].text
            results[orig_idx] = Prediction(text=text)

        return results

    def _to_vllm_request(self, msg: Message) -> dict:
        """Convert a Message to a vLLM request dict.

        Two styles based on config:
        - qwen: content list with {"type":"image","image":path} + {"type":"text","text":...}
        - placeholder: flat string with <image> tokens + multi_modal_data image list
        """
        if self._prompt_style == "placeholder":
            prompt_text, image_paths = to_placeholder_prompt(msg)
            images = [str(p) for p in image_paths]
            chat_messages = [{"role": "user", "content": prompt_text}]
            rendered = self._processor.apply_chat_template(
                chat_messages, tokenize=False, add_generation_prompt=True
            )
            return {
                "prompt": rendered,
                "multi_modal_data": {"image": images} if images else {},
            }
        else:
            # qwen style
            content = to_qwen_content(msg)
            chat_messages = [{"role": "user", "content": content}]
            rendered = self._processor.apply_chat_template(
                chat_messages, tokenize=False, add_generation_prompt=True
            )
            # Collect image paths/objects for vLLM
            images = []
            for item in msg:
                if item["type"] == "image":
                    v = item["value"]
                    if isinstance(v, str) or isinstance(v, Path):
                        images.append(str(v))
                    else:
                        # PIL Image — vLLM can accept PIL directly
                        images.append(v)
            return {
                "prompt": rendered,
                "multi_modal_data": {"image": images} if images else {},
            }
