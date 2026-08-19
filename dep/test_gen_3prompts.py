#!/usr/bin/env python
"""Test JoyAI-Image and Show-o2 image generation with 3 prompts.

Results saved to gen_results/{model_name}/prompt{N}.png
"""
import os, sys, time, torch
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "3")
os.environ.setdefault("CKPT_DIR", "/mnt/nas-tbt/tbt/checkpoint/hf_cache")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

PROMPTS = [
    "Draw a red arrow pointing from the bottom-left to the top-right of the image",
    "Add a blue circle in the center of this image",
    "Draw a green route line from the left side to the right side of the image",
]

GEN_RESULTS = PROJECT_ROOT / "gen_results"

def log(msg, level="INFO"):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {level:5s} {msg}", flush=True)

def test_joyai():
    log("="*60)
    log("Testing JoyAI-Image generation")
    log("="*60)
    from mapspatial.config import load_model_config
    from mapspatial.backends.registry import get_backend_cls
    cfg = load_model_config("configs/models/joyai-image.yaml")
    BackendCls = get_backend_cls(cfg.backend)
    backend = BackendCls(cfg)
    log("Model loaded")
    
    out_dir = GEN_RESULTS / "JoyAI-Image"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for i, prompt in enumerate(PROMPTS, 1):
        log(f"Prompt {i}: {prompt[:60]}...")
        try:
            img = backend.draw(
                context=[{"type": "text", "value": prompt}],
                instruction=prompt,
            )
            if img is not None:
                path = out_dir / f"prompt{i}.png"
                img.save(str(path))
                log(f"  Saved: {path} ({img.size})")
            else:
                log(f"  draw() returned None", "WARN")
        except Exception as e:
            import traceback
            log(f"  CRASH: {e}", "ERROR")
            traceback.print_exc()
    
    del backend
    torch.cuda.empty_cache()
    log("JoyAI-Image done")

def test_showo2():
    log("="*60)
    log("Testing Show-o2-7B generation")
    log("="*60)
    from mapspatial.config import load_model_config
    from mapspatial.backends.registry import get_backend_cls
    cfg = load_model_config("configs/models/show-o2-7b.yaml")
    BackendCls = get_backend_cls(cfg.backend)
    backend = BackendCls(cfg)
    log("Model loaded")
    
    out_dir = GEN_RESULTS / "Show-o2"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for i, prompt in enumerate(PROMPTS, 1):
        log(f"Prompt {i}: {prompt[:60]}...")
        try:
            img = backend.draw(
                context=[{"type": "text", "value": prompt}],
                instruction=prompt,
            )
            if img is not None:
                path = out_dir / f"prompt{i}.png"
                img.save(str(path))
                log(f"  Saved: {path} ({img.size})")
            else:
                log(f"  draw() returned None", "WARN")
        except Exception as e:
            import traceback
            log(f"  CRASH: {e}", "ERROR")
            traceback.print_exc()
    
    del backend
    torch.cuda.empty_cache()
    log("Show-o2 done")

if __name__ == "__main__":
    print(f"torch: {torch.__version__}, CUDA: {torch.cuda.is_available()}")
    test_joyai()
    test_showo2()
    print("\n=== Done ===")
