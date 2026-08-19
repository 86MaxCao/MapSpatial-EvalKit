#!/usr/bin/env python3
"""Step3-VL-10B vLLM smoke test — verify PIL in multi_modal_data fixes the
images-only processor call that hangs mapspatial's glm style.

Mirrors mapspatial/backends/vllm.py glm style content ({"type":"image","url":path}
+ text, apply_chat_template) but passes PIL images in multi_modal_data (like
outdoor eval/backends.py).

Usage:
  CUDA_VISIBLE_DEVICES=0 VLLM_WORKER_MULTIPROC_METHOD=spawn python dep/_test_step3_vllm.py
"""
from __future__ import annotations

import os
import sys
import time
import traceback
from pathlib import Path

for v in ("WORLD_SIZE", "RANK", "LOCAL_RANK", "GROUP_RANK"):
    os.environ.pop(v, None)

CKPT = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/Step3-VL-10B"
IMG = ("/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/"
       "data/benchmark_images_t1/B000A07C0B_from_B000A8XLYF_to_B0FFFCQM37/"
       "推荐方案/B000A07C0B_from_B000A8XLYF_to_B0FFFCQM37_T1_angular_order_q0/base/direct/sat_direct.png")


def ts() -> str:
    return time.strftime("%H:%M:%S")


def main() -> int:
    print(f"[{ts()}] === Step3-VL vLLM smoke test (PIL in multi_modal_data) ===", flush=True)
    print(f"[{ts()}] CUDA_VISIBLE_DEVICES={os.environ.get('CUDA_VISIBLE_DEVICES')} "
          f"VLLM_WORKER_MULTIPROC_METHOD={os.environ.get('VLLM_WORKER_MULTIPROC_METHOD')}", flush=True)
    if not Path(CKPT).is_dir():
        print(f"[{ts()}] ERROR: model dir missing: {CKPT}", flush=True)
        return 2
    if not Path(IMG).is_file():
        print(f"[{ts()}] ERROR: test image missing: {IMG}", flush=True)
        return 2

    print(f"[{ts()}] importing vllm...", flush=True)
    from vllm import LLM, SamplingParams
    from transformers import AutoProcessor
    from PIL import Image
    print(f"[{ts()}] imports OK", flush=True)

    print(f"[{ts()}] constructing LLM(...) (spawn, non-eager)...", flush=True)
    try:
        llm = LLM(
            model=CKPT,
            max_model_len=32768,
            gpu_memory_utilization=0.7,
            limit_mm_per_prompt={"image": 24, "video": 1},
            enforce_eager=False,
            trust_remote_code=True,
            dtype="bfloat16",
        )
    except Exception:
        print(f"[{ts()}] LLM() FAILED:", flush=True)
        traceback.print_exc()
        return 1
    print(f"[{ts()}] LLM() constructed OK", flush=True)

    proc = AutoProcessor.from_pretrained(CKPT, trust_remote_code=True)
    print(f"[{ts()}] processor OK: {type(proc).__name__}", flush=True)

    # Mapspatial glm style content ({"type":"image","url":path} + text)
    messages = [{"role": "user", "content": [
        {"type": "image", "url": IMG},
        {"type": "text", "text": "What is shown in this image? Answer briefly."},
    ]}]
    prompt_text = proc.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    # THE KEY DIFFERENCE vs mapspatial: preload PIL instead of passing path strings
    pil_img = Image.open(IMG).convert("RGB")
    request = {"prompt": prompt_text, "multi_modal_data": {"image": [pil_img]}}
    print(f"[{ts()}] request built (PIL image), calling llm.generate() ...", flush=True)

    sp = SamplingParams(temperature=0.0, max_tokens=128)
    try:
        outs = llm.generate([request], sp)
        txt = outs[0].outputs[0].text
        print(f"[{ts()}] GENERATE OK: {txt!r}", flush=True)
        print(f"[{ts()}] === SMOKE TEST PASSED (PIL approach works for Step3) ===", flush=True)
        return 0
    except Exception:
        print(f"[{ts()}] llm.generate() FAILED:", flush=True)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
