#!/usr/bin/env python3
"""Minimal vLLM smoke test for GLM-4.6V-Flash.

Mirrors mapspatial/backends/vllm.py init kwargs. Prints timestamped
progress so we can see exactly where (if anywhere) vLLM hangs.

Usage:
  CUDA_VISIBLE_DEVICES=0 python dep/_test_glm_vllm.py [--eager] [--no-eager]
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import traceback
from pathlib import Path

# unset env vars that confuse HF/vLLM tensor parallel auto-detection
for v in ("WORLD_SIZE", "RANK", "LOCAL_RANK", "GROUP_RANK"):
    os.environ.pop(v, None)

CKPT = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/GLM-4.6V-Flash"


def t() -> str:
    return time.strftime("%H:%M:%S")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--eager", dest="enforce_eager", action="store_true", default=True)
    ap.add_argument("--no-eager", dest="enforce_eager", action="store_false")
    ap.add_argument("--model", default=CKPT)
    args = ap.parse_args()

    print(f"[{t}] === GLM vLLM smoke test ===", flush=True)
    print(f"[{t}] model={args.model} enforce_eager={args.enforce_eager}", flush=True)
    print(f"[{t}] CUDA_VISIBLE_DEVICES={os.environ.get('CUDA_VISIBLE_DEVICES')}", flush=True)
    if not Path(args.model).is_dir():
        print(f"[{t}] ERROR: model dir does not exist: {args.model}", flush=True)
        return 2

    # 1. import vLLM
    print(f"[{t}] importing vllm...", flush=True)
    from vllm import LLM, SamplingParams
    print(f"[{t}] vllm imported OK", flush=True)

    # 2. build LLM (mirror mapspatial kwargs)
    print(f"[{t}] constructing LLM(...) — this loads weights + cudagraph", flush=True)
    llm_kwargs = dict(
        model=args.model,
        max_model_len=32768,
        gpu_memory_utilization=0.7,
        limit_mm_per_prompt={"image": 24, "video": 1},
        enforce_eager=args.enforce_eager,
        trust_remote_code=True,
        dtype="bfloat16",
    )
    try:
        llm = LLM(**llm_kwargs)
    except Exception:
        print(f"[{t}] LLM() construction FAILED:", flush=True)
        traceback.print_exc()
        return 1
    print(f"[{t}] LLM() constructed OK", flush=True)

    # 3. processor
    from transformers import AutoProcessor
    try:
        proc = AutoProcessor.from_pretrained(args.model, trust_remote_code=True)
        print(f"[{t}] processor OK: {type(proc).__name__}", flush=True)
    except Exception:
        print(f"[{t}] processor load FAILED (non-fatal):", flush=True)
        traceback.print_exc()
        proc = None

    # 4. build a single tiny prompt with one image via the chat template
    #    Use a 64x64 red image so we don't depend on any dataset.
    from PIL import Image
    img = Image.new("RGB", (64, 64), color=(255, 0, 0))

    prompt = None
    # Try standard apply_chat_template path
    messages = [{"role": "user", "content": [{"type": "image", "image": img}, {"type": "text", "text": "What color is this image? Answer in one word."}]}]
    try:
        if proc is not None and hasattr(proc, "apply_chat_template"):
            text = proc.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            # build multi_modal_data
            mm = {"image": [img]} if proc is not None else None
            prompt = {"prompt": text, "multi_modal_data": mm}
            print(f"[{t}] prompt built via processor chat template", flush=True)
    except Exception:
        print(f"[{t}] chat-template build failed, will fall back to raw text", flush=True)
        traceback.print_exc()

    if prompt is None:
        prompt = {"prompt": "What color is a red image? Answer in one word.", "multi_modal_data": {"image": [img]}}
        print(f"[{t}] using fallback raw-text prompt", flush=True)

    # 5. generate
    sp = SamplingParams(temperature=0.0, max_tokens=64)
    print(f"[{t}] calling llm.generate() ...", flush=True)
    try:
        outs = llm.generate([prompt], sp)
        txt = outs[0].outputs[0].text
        print(f"[{t}] GENERATE OK: {txt!r}", flush=True)
        print(f"[{t}] === SMOKE TEST PASSED ===", flush=True)
        return 0
    except Exception:
        print(f"[{t}] llm.generate() FAILED:", flush=True)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
