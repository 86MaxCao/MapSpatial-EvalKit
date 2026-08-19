"""Test U1 draw() with flash_attn GQA fix (SDPA fallback)."""
import os, sys, time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
import numpy as np
from PIL import Image

PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.neo_chat.modeling_neo_chat import NEOChatModel

U1_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/SenseNova-U1-8B-MoT"
print("Loading U1...")
model, _ = load_model(U1_PATH, NEOChatModel, device="cuda", dtype="bfloat16")
tokenizer = load_tokenizer(U1_PATH)
print("Loaded")

PROMPTS = [
    "Draw a red arrow pointing from the bottom-left to the top-right of the image",
    "Add a blue circle in the center of this image",
    "Draw a green route line from the left side to the right side of the image",
]
output_dir = os.path.join(PROJECT, "gen_results")
os.makedirs(output_dir, exist_ok=True)

dummy_img = Image.new("RGB", (512, 512), (200, 200, 200))

for idx, prompt in enumerate(PROMPTS, 1):
    print(f"\n=== U1 Prompt {idx}: {prompt[:50]}... ===")
    t0 = time.time()
    try:
        with torch.inference_mode():
            output = model.it2i_generate(
                tokenizer, prompt, [dummy_img],
                image_size=(512, 512), cfg_scale=4.0, img_cfg_scale=1.0,
                num_steps=50, batch_size=1, seed=42,
            )
        # Denormalize [-1,1] → [0,255]
        img = (output * 0.5 + 0.5).clamp(0, 1)
        img_np = (img[0].float().permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)
        result = Image.fromarray(img_np)
        save_path = os.path.join(output_dir, f"u1_prompt{idx}.png")
        result.save(save_path)
        print(f"  Saved: {save_path}, mean={img_np.mean():.1f}, std={img_np.std():.1f}, Time: {time.time()-t0:.1f}s")
    except Exception as e:
        import traceback
        print(f"  FAILED: {e}")
        traceback.print_exc()

print("\n=== Done ===")
