#!/usr/bin/env python
"""Test InternVL-U / Show-o2 / JoyAI-Image understanding + draw.

Usage:
    export MAMBA_ROOT_PREFIX=/mnt/nas-tbt/caoziqi/micromamba
    export PYTHONNOUSERSITE=1
    export CUDA_VISIBLE_DEVICES=1,2,3
    export CKPT_DIR=/mnt/nas-tbt/tbt/checkpoint/hf_cache
    export VLLM_DEEP_GEMM_WARMUP=skip
    /mnt/nas-tbt/caoziqi/micromamba/envs/mapspatial/bin/python test_3models.py [--model internvlu|showo2|joyai] [--phase understand|draw]
"""

from __future__ import annotations

import os
import sys
import time
import json
import traceback
from pathlib import Path
from PIL import Image

# Env setup
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1,2,3")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")
os.environ.setdefault("CKPT_DIR", "/mnt/nas-tbt/tbt/checkpoint/hf_cache")
os.environ.setdefault("PYTHONNOUSERSITE", "1")

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Data paths
DATA_DIR = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data"
INPUT_DIR = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data-jsonl"

N_SAMPLES = 3


def log(msg: str, level: str = "INFO"):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {level:5s} {msg}", flush=True)


def get_test_samples(n: int = N_SAMPLES):
    """Load n test samples from sat/t1/direct."""
    from mapspatial.data.loader import iter_samples
    data_root = Path(DATA_DIR)
    for (view, task, variant), samples in iter_samples(
        Path(INPUT_DIR), data_root, ["sat"], ["t1"], ["direct"]
    ):
        return samples[:n]
    return []


def load_backend(config_path: str):
    """Load a backend from config."""
    from mapspatial.config import load_model_config
    from mapspatial.backends.registry import get_backend_cls

    cfg = load_model_config(config_path)
    log(f"  Config loaded: backend={cfg.backend}")
    BackendCls = get_backend_cls(cfg.backend)
    caps = BackendCls.caps
    log(f"  Backend: {cfg.backend} caps: batch={caps.batch} draw={caps.draw} interleave={caps.native_interleave}")
    backend = BackendCls(cfg)
    return backend, caps


def test_understand(backend, samples, model_name: str):
    """Test understanding path."""
    log(f"  Testing understand() with {len(samples)} samples...")
    messages = [s.message for s in samples]
    try:
        preds = backend.understand(messages, temperature=0.0, max_new_tokens=512)
        success = 0
        errors = 0
        for i, (s, p) in enumerate(zip(samples, preds)):
            if p.error:
                log(f"    Sample {i}: ERROR: {p.error[:200]}", "ERROR")
                errors += 1
            elif p.text:
                log(f"    Sample {i}: gold={s.gold} pred={p.text[:80]}...")
                success += 1
            else:
                log(f"    Sample {i}: empty prediction", "WARN")
                errors += 1
        log(f"  understand() result: {success} success, {errors} errors out of {len(samples)}")
        return {"status": "PASS" if success > 0 else "FAIL", "success": success, "errors": errors, "total": len(samples)}
    except Exception as e:
        log(f"    understand() crashed: {e}", "ERROR")
        traceback.print_exc()
        return {"status": "CRASH", "error": str(e)[:500]}


def test_draw(backend, samples, model_name: str):
    """Test generation path."""
    log(f"  Testing draw()...")
    try:
        sample = samples[0]
        img = backend.draw(sample.message, "Draw a helpful diagram for this question.", temperature=0.0)
        if img is not None:
            out_dir = Path("/tmp/mapspatial-test") / model_name.replace(" ", "_")
            out_dir.mkdir(parents=True, exist_ok=True)
            img_path = out_dir / "draw_test.png"
            img.save(str(img_path))
            log(f"    Generated image saved to {img_path} ({img.size})")
            return {"status": "PASS", "image_size": str(img.size)}
        else:
            log(f"    draw() returned None", "WARN")
            return {"status": "FAIL", "error": "returned None"}
    except Exception as e:
        log(f"    draw() crashed: {e}", "ERROR")
        traceback.print_exc()
        return {"status": "CRASH", "error": str(e)[:500]}


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["internvlu", "showo2", "joyai", "all"], default="all")
    parser.add_argument("--phase", choices=["understand", "draw", "both"], default="both")
    args = parser.parse_args()

    print("=" * 60)
    print("MapSpatial-EvalKit: 3 Model Test (InternVL-U, Show-o2, JoyAI)")
    print(f"GPU: {os.environ.get('CUDA_VISIBLE_DEVICES', '1,2,3')}")
    print(f"Env: mapspatial (micromamba)")
    print("=" * 60)

    import torch
    print(f"torch: {torch.__version__}, CUDA: {torch.cuda.is_available()}, GPUs: {torch.cuda.device_count()}")

    models = []
    if args.model in ("internvlu", "all"):
        models.append({"name": "InternVL-U", "config": "configs/models/internvl-u.yaml"})
    if args.model in ("showo2", "all"):
        models.append({"name": "Show-o2-7B", "config": "configs/models/show-o2-7b.yaml"})
    if args.model in ("joyai", "all"):
        models.append({"name": "JoyAI-Image", "config": "configs/models/joyai-image.yaml"})

    samples = get_test_samples(N_SAMPLES)
    print(f"\nLoaded {len(samples)} test samples from sat/t1/direct")
    if samples:
        print(f"  Sample 0: id={samples[0].id[:50]}... gold={samples[0].gold}")
    print()

    results = []
    for model_info in models:
        name = model_info["name"]
        config_path = model_info["config"]

        log(f"{'='*60}")
        log(f"Testing {name}")
        log(f"{'='*60}")

        result = {"model": name, "load": "SKIP", "understand": "SKIP", "draw": "SKIP"}

        # Load model
        t0 = time.time()
        try:
            backend, caps = load_backend(config_path)
            load_time = time.time() - t0
            log(f"  Model loaded in {load_time:.1f}s")
            result["load"] = f"PASS ({load_time:.0f}s)"
        except Exception as e:
            load_time = time.time() - t0
            log(f"  Model load FAILED after {load_time:.1f}s: {e}", "ERROR")
            traceback.print_exc()
            result["load"] = f"FAIL ({load_time:.0f}s)"
            result["error"] = str(e)[:500]
            results.append(result)
            continue

        if not samples:
            log(f"  No test samples available", "ERROR")
            result["error"] = "no samples"
            results.append(result)
            del backend
            continue

        # Test understand
        if args.phase in ("understand", "both"):
            u_result = test_understand(backend, samples, name)
            result["understand"] = u_result["status"]
            result["understand_detail"] = u_result

        # Test draw
        if args.phase in ("draw", "both") and caps.draw:
            d_result = test_draw(backend, samples, name)
            result["draw"] = d_result["status"]
            result["draw_detail"] = d_result
        elif args.phase in ("draw", "both") and not caps.draw:
            log(f"  Skipping draw() (not supported)")
            result["draw"] = "N/A"

        # Cleanup
        del backend
        try:
            import torch
            torch.cuda.empty_cache()
            log(f"  GPU memory cleared")
        except:
            pass

        results.append(result)

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"{'Model':<20} {'Load':<15} {'Understand':<15} {'Draw':<15}")
    print("-" * 80)
    for r in results:
        print(f"{r['model']:<20} {r.get('load','?'):<15} {r.get('understand','?'):<15} {r.get('draw','?'):<15}")
    print("-" * 80)

    out_path = Path("/tmp/mapspatial-test") / "3model_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
