"""Test U1 (with dummy image), LatentUM, and ThinkMorph draw()."""
import os, sys, time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
import numpy as np
from PIL import Image
from copy import deepcopy

PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

PROMPTS = [
    "Draw a red arrow pointing from the bottom-left to the top-right of the image",
    "Add a blue circle in the center of this image",
    "Draw a green route line from the left side to the right side of the image",
]
output_dir = os.path.join(PROJECT, "gen_results")
os.makedirs(output_dir, exist_ok=True)

# Dummy condition image (white 256x256)
dummy_img = Image.new("RGB", (256, 256), (255, 255, 255))

# ===================== U1 =====================
print("=" * 60)
print("U1 draw test (with dummy condition image)")
print("=" * 60)

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.neo_chat.modeling_neo_chat import NEOChatModel

U1_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/SenseNova-U1-8B-MoT"
print("Loading U1...")
t0 = time.time()
u1_model, u1_config = load_model(U1_PATH, NEOChatModel, device="cuda", dtype="bfloat16")
u1_tokenizer = load_tokenizer(U1_PATH)
print(f"Loaded in {time.time()-t0:.1f}s")

for idx, prompt in enumerate(PROMPTS, 1):
    print(f"\n--- U1 Prompt {idx}: {prompt[:50]}... ---")
    t0 = time.time()
    try:
        output = u1_model.it2i_generate(
            u1_tokenizer,
            prompt,
            [dummy_img],  # pass dummy image as condition
            image_size=(256, 256),
            cfg_scale=4.0,
            img_cfg_scale=1.0,
            num_steps=50,
            batch_size=1,
            seed=42,
        )
        if isinstance(output, torch.Tensor):
            img = output * 0.5 + 0.5
            img = img.clamp(0, 1)
            img_np = (img[0].float().permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)
            result = Image.fromarray(img_np)
        elif isinstance(output, Image.Image):
            result = output
        else:
            print(f"  Unexpected output type: {type(output)}")
            continue

        save_path = os.path.join(output_dir, f"u1_prompt{idx}.png")
        result.save(save_path)
        arr = np.array(result)
        print(f"  Saved: {save_path}, Size: {result.size}, mean={arr.mean():.1f}, std={arr.std():.1f}, Time: {time.time()-t0:.1f}s")
    except Exception as e:
        import traceback
        print(f"  FAILED: {e}")
        traceback.print_exc()

del u1_model
torch.cuda.empty_cache()

# ===================== LatentUM =====================
print("\n" + "=" * 60)
print("LatentUM draw test")
print("=" * 60)

from mapspatial.vendor.latentum.modeling_latentum import LatentUMModel

LATENTUM_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/LatentUM-Base"
DECODER_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/LatentUM-Decoder"

print("Loading LatentUM...")
t0 = time.time()
lat_model, lat_config = load_model(LATENTUM_PATH, LatentUMModel, device="cuda", dtype="bfloat16")
lat_tokenizer = load_tokenizer(LATENTUM_PATH)
print(f"Loaded in {time.time()-t0:.1f}s")

# Load decoder
print("Loading LatentUM decoder...")
try:
    # Check if LatentUMDecoderModel exists
    from mapspatial.vendor.latentum.modeling_latentum import LatentUMDecoderModel
    decoder = LatentUMDecoderModel.from_pretrained(DECODER_PATH, torch_dtype=torch.bfloat16, device="cuda")
    decoder = decoder.to("cuda").to(torch.bfloat16).eval()
    print("Decoder loaded")
except Exception as e:
    print(f"Decoder load failed: {e}")
    decoder = None

if decoder is not None:
    for idx, prompt in enumerate(PROMPTS, 1):
        print(f"\n--- LatentUM Prompt {idx}: {prompt[:50]}... ---")
        t0 = time.time()
        try:
            images = lat_model.generate_images(
                prompt,
                decoder=decoder,
                num_images_per_prompt=1,
                cfg_scale=3.0,
                temperature=0.9,
                top_k=50,
                top_p=0.95,
                seed=42,
                num_inference_steps=25,
                guidance_scale=1.0,
                show_progress=True,
            )
            if isinstance(images, list) and len(images) > 0:
                result = images[0]
            elif isinstance(images, Image.Image):
                result = images
            elif isinstance(images, torch.Tensor):
                img = images * 0.5 + 0.5
                img = img.clamp(0, 1)
                img_np = (img[0].float().permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)
                result = Image.fromarray(img_np)
            else:
                print(f"  Unexpected type: {type(images)}")
                continue

            save_path = os.path.join(output_dir, f"latentum_prompt{idx}.png")
            result.save(save_path)
            arr = np.array(result)
            print(f"  Saved: {save_path}, Size: {result.size}, mean={arr.mean():.1f}, std={arr.std():.1f}, Time: {time.time()-t0:.1f}s")
        except Exception as e:
            import traceback
            print(f"  FAILED: {e}")
            traceback.print_exc()

del lat_model
if decoder:
    del decoder
torch.cuda.empty_cache()

print("\n=== Done ===")
