#!/usr/bin/env python
"""Test all 9 unified generation+understanding models.

Tests both understanding (direct) and generation (external_draw / native_interleave)
for each model. Uses GPU 1,2,3 only.

Usage:
    export MAMBA_ROOT_PREFIX=/mnt/nas-tbt/caoziqi/micromamba
    export PYTHONNOUSERSITE=1
    export CUDA_VISIBLE_DEVICES=1,2,3
    export CKPT_DIR=/mnt/nas-tbt/tbt/checkpoint/hf_cache
    export VLLM_DEEP_GEMM_WARMUP=skip
    /mnt/nas-tbt/caoziqi/micromamba/envs/mapspatial/bin/python test_unified_models.py
"""

from __future__ import annotations

import os
import sys
import time
import traceback
from pathlib import Path

# Env setup
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1,2,3")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")
os.environ.setdefault("CKPT_DIR", "/mnt/nas-tbt/tbt/checkpoint/hf_cache")

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Data paths
DATA_DIR = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data"
INPUT_DIR = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data-jsonl"

# Models to test (excluding Ming-UniVision per user request)
MODELS = [
    {"name": "Bagel-7B-MoT",        "config": "configs/models/bagel-7b.yaml",              "checkpoint": "BAGEL-7B-MoT"},
    {"name": "ThinkMorph-7B",       "config": "configs/models/thinkmorph-7b.yaml",         "checkpoint": "ThinkMorph-7B"},
    {"name": "BLIP3o-8B",           "config": "configs/models/blip3o-8b.yaml",              "checkpoint": "BLIP3o-Model-8B"},
    {"name": "SenseNova-U1-8B-MoT", "config": "configs/models/sensenova-u1-8b.yaml",       "checkpoint": "SenseNova-U1-8B-MoT"},
    {"name": "LatentUM-Base",       "config": "configs/models/latentum-base.yaml",          "checkpoint": "LatentUM-Base"},
    {"name": "Janus-Pro-7B",        "config": "configs/models/janus-pro-7b.yaml",            "checkpoint": "Janus-Pro-7B"},
    {"name": "InternVL-U",          "config": "configs/models/internvl-u.yaml",              "checkpoint": "InternVL-U"},
    {"name": "Show-o2-7B",          "config": "configs/models/show-o2-7b.yaml",              "checkpoint": "show-o2-7B"},
    {"name": "JoyAI-Image",         "config": "configs/models/joyai-image.yaml",            "checkpoint": "JoyAI-Image-Edit"},
]

# Number of samples to test per model
N_SAMPLES = 3

# Results storage
results = []


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


def test_understand(backend, samples, model_name: str):
    """Test understanding path (direct strategy)."""
    log(f"  Testing understand() with {len(samples)} samples...")
    from mapspatial.types import Prediction

    messages = [s.message for s in samples]
    try:
        preds = backend.understand(messages, temperature=0.0, max_new_tokens=512)
        success = 0
        errors = 0
        for i, (s, p) in enumerate(zip(samples, preds)):
            if p.error:
                log(f"    Sample {i}: ERROR: {p.error[:100]}", "ERROR")
                errors += 1
            elif p.text:
                log(f"    Sample {i}: gold={s.gold} pred={p.text[:60]}...")
                success += 1
            else:
                log(f"    Sample {i}: empty prediction", "WARN")
                errors += 1
        return {"status": "PASS" if success > 0 else "FAIL",
                "success": success, "errors": errors, "total": len(samples)}
    except Exception as e:
        log(f"    understand() crashed: {e}", "ERROR")
        traceback.print_exc()
        return {"status": "CRASH", "error": str(e)[:200]}


def test_draw(backend, samples, model_name: str):
    """Test generation path (draw)."""
    log(f"  Testing draw()...")
    try:
        sample = samples[0]
        img = backend.draw(sample.message, "Draw a helpful diagram for this question.",
                           temperature=0.0)
        if img is not None:
            # Save the generated image
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
        return {"status": "CRASH", "error": str(e)[:200]}


def test_interleave(backend, samples, model_name: str):
    """Test native interleave path."""
    log(f"  Testing interleave()...")
    try:
        sample = samples[0]
        pred = backend.interleave(sample.message, max_rounds=2, marker="<image_start>",
                                   temperature=0.3)
        if pred.error:
            log(f"    interleave() error: {pred.error[:100]}", "ERROR")
            return {"status": "FAIL", "error": pred.error[:200]}
        elif pred.text:
            draw_triggered = pred.meta.get("draw_triggered", False)
            n_images = len(pred.generated_images)
            log(f"    Output text: {pred.text[:60]}... draw_triggered={draw_triggered} images={n_images}")
            return {"status": "PASS", "draw_triggered": draw_triggered, "images": n_images}
        else:
            log(f"    interleave() returned empty", "WARN")
            return {"status": "FAIL", "error": "empty output"}
    except Exception as e:
        log(f"    interleave() crashed: {e}", "ERROR")
        return {"status": "CRASH", "error": str(e)[:200]}


def test_model(model_info: dict):
    """Test a single model: load, understand, draw, interleave."""
    name = model_info["name"]
    config_path = model_info["config"]
    checkpoint = model_info["checkpoint"]

    log(f"{'='*60}")
    log(f"Testing {name} (checkpoint: {checkpoint})")
    log(f"{'='*60}")

    # Check checkpoint exists
    ckpt_path = os.path.join(os.environ["CKPT_DIR"], checkpoint)
    if not os.path.exists(ckpt_path):
        log(f"  Checkpoint not found: {ckpt_path}", "ERROR")
        return {"model": name, "load": "SKIP", "understand": "SKIP",
                "draw": "SKIP", "interleave": "SKIP", "error": "checkpoint not found"}

    # Load config
    try:
        from mapspatial.config import load_model_config
        cfg = load_model_config(config_path)
        log(f"  Config loaded: backend={cfg.backend}")
    except Exception as e:
        log(f"  Config load failed: {e}", "ERROR")
        return {"model": name, "load": "FAIL", "error": str(e)[:200]}

    # Get backend class
    try:
        from mapspatial.backends.registry import get_backend_cls
        BackendCls = get_backend_cls(cfg.backend)
        caps = BackendCls.caps
        log(f"  Backend: {cfg.backend} caps: batch={caps.batch} draw={caps.draw} interleave={caps.native_interleave}")
    except Exception as e:
        log(f"  Backend import failed: {e}", "ERROR")
        return {"model": name, "load": "FAIL", "error": str(e)[:200]}

    # Load model
    t0 = time.time()
    try:
        backend = BackendCls(cfg)
        load_time = time.time() - t0
        log(f"  Model loaded in {load_time:.1f}s")
    except Exception as e:
        load_time = time.time() - t0
        log(f"  Model load FAILED after {load_time:.1f}s: {e}", "ERROR")
        traceback.print_exc()
        return {"model": name, "load": f"FAIL ({load_time:.0f}s)",
                "understand": "SKIP", "draw": "SKIP", "interleave": "SKIP",
                "error": str(e)[:200]}

    # Get test samples
    samples = get_test_samples(N_SAMPLES)
    if not samples:
        log(f"  No test samples available", "ERROR")
        return {"model": name, "load": "PASS", "understand": "SKIP",
                "draw": "SKIP", "interleave": "SKIP", "error": "no samples"}

    result = {
        "model": name,
        "load": f"PASS ({load_time:.0f}s)",
        "understand": "SKIP",
        "draw": "SKIP",
        "interleave": "SKIP",
    }

    # Test understand
    u_result = test_understand(backend, samples, name)
    result["understand"] = u_result["status"]
    result["understand_detail"] = u_result

    # Test draw (if supported)
    if caps.draw:
        d_result = test_draw(backend, samples, name)
        result["draw"] = d_result["status"]
        result["draw_detail"] = d_result
    else:
        log(f"  Skipping draw() (not supported)")
        result["draw"] = "N/A"

    # Test interleave (if supported)
    if caps.native_interleave:
        i_result = test_interleave(backend, samples, name)
        result["interleave"] = i_result["status"]
        result["interleave_detail"] = i_result
    else:
        log(f"  Skipping interleave() (not supported)")
        result["interleave"] = "N/A"

    # Cleanup
    del backend
    try:
        import torch
        torch.cuda.empty_cache()
        log(f"  GPU memory cleared")
    except:
        pass

    return result


def print_summary(results: list[dict]):
    """Print summary table."""
    print("\n" + "=" * 90)
    print("SUMMARY: 9 Unified Model Test Results")
    print("=" * 90)
    print(f"{'Model':<25} {'Load':<15} {'Understand':<15} {'Draw':<15} {'Interleave':<15}")
    print("-" * 90)

    for r in results:
        print(f"{r['model']:<25} {r['load']:<15} {r.get('understand','?'):<15} "
              f"{r.get('draw','?'):<15} {r.get('interleave','?'):<15}")

    print("-" * 90)

    # Count results
    n_pass_load = sum(1 for r in results if r.get("load", "").startswith("PASS"))
    n_pass_und = sum(1 for r in results if r.get("understand") == "PASS")
    n_pass_draw = sum(1 for r in results if r.get("draw") == "PASS")
    n_pass_int = sum(1 for r in results if r.get("interleave") == "PASS")
    n_total = len(results)

    print(f"\nLoad: {n_pass_load}/{n_total}  |  Understand: {n_pass_und}/{n_total}  |  "
          f"Draw: {n_pass_draw}/{n_total}  |  Interleave: {n_pass_int}/{n_total}")
    print("=" * 90)


def main():
    print("=" * 60)
    print("MapSpatial-EvalKit: 9 Unified Model Test")
    print(f"GPU: {os.environ.get('CUDA_VISIBLE_DEVICES', '1,2,3')}")
    print(f"Env: mapspatial (micromamba)")
    print(f"Samples per model: {N_SAMPLES}")
    print("=" * 60)

    # Verify torch
    import torch
    print(f"\ntorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}, "
          f"GPUs: {torch.cuda.device_count()}")

    # Get test samples once
    samples = get_test_samples(N_SAMPLES)
    print(f"Loaded {len(samples)} test samples from sat/t1/direct")
    if samples:
        print(f"  Sample 0: id={samples[0].id[:50]}... gold={samples[0].gold}")
    print()

    # Test each model
    for model_info in MODELS:
        try:
            result = test_model(model_info)
            results.append(result)
        except Exception as e:
            log(f"Unexpected error testing {model_info['name']}: {e}", "ERROR")
            traceback.print_exc()
            results.append({
                "model": model_info["name"],
                "load": "CRASH",
                "understand": "CRASH",
                "draw": "CRASH",
                "interleave": "CRASH",
                "error": str(e)[:200],
            })

    # Print summary
    print_summary(results)

    # Save results to JSON
    import json
    out_path = Path("/tmp/mapspatial-test") / "unified_model_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
