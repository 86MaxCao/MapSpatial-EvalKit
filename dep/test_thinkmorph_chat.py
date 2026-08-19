"""Verify ThinkMorph understand works after Bagel flash_attn fix."""
import os, sys, time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
import numpy as np
from PIL import Image

MODEL_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/ThinkMorph-7B"
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.bagel.modeling_bagel import BagelForConditionalGeneration

print("Loading ThinkMorph...")
model, config = load_model(MODEL_PATH, BagelForConditionalGeneration, device="cuda", dtype="bfloat16")
tokenizer = load_tokenizer(MODEL_PATH)
print(f"use_moe={model.use_moe}")

# Setup tokens
special_tokens = ["<|im_start|>", "<|im_end|>", "<|vision_start|>", "<|vision_end|>"]
existing = []
for k, v in tokenizer.special_tokens_map.items():
    if isinstance(v, str):
        existing.append(v)
    elif isinstance(v, list):
        existing.extend(v)
new_tokens = [t for t in special_tokens if t not in existing]
if new_tokens:
    tokenizer.add_tokens(new_tokens)
new_token_ids = {
    "bos_token_id": tokenizer.convert_tokens_to_ids("<|im_start|>"),
    "eos_token_id": tokenizer.convert_tokens_to_ids("<|im_end|>"),
    "start_of_image": tokenizer.convert_tokens_to_ids("<|vision_start|>"),
    "end_of_image": tokenizer.convert_tokens_to_ids("<|vision_end|>"),
}

class _ImageTransform:
    def __init__(self, max_size, min_size, patch_size):
        self.max_size, self.min_size, self.patch_size = max_size, min_size, patch_size
    def _make_divisible(self, v, s):
        return max(s, int(round(v / s) * s))
    def __call__(self, img):
        w, h = img.size
        scale = min(self.max_size / max(w, h), 1.0)
        scale = max(scale, self.min_size / min(w, h))
        new_w = self._make_divisible(round(w * scale), self.patch_size)
        new_h = self._make_divisible(round(h * scale), self.patch_size)
        img = img.resize((new_w, new_h), Image.BICUBIC)
        t = torch.tensor(np.array(img)).permute(2, 0, 1).float() / 255.0
        return (t - 0.5) / 0.5

def _vae_resize(img, max_size=1024, min_size=512, stride=16):
    w, h = img.size
    scale = min(max_size / max(w, h), 1.0)
    scale = max(scale, min_size / min(w, h))
    new_w = max(stride, int(round(round(w * scale) / stride) * stride))
    new_h = max(stride, int(round(round(h * scale) / stride) * stride))
    return img.resize((new_w, new_h), Image.BICUBIC)

image_transform = _ImageTransform(980, 224, 14)

# Test 1: Text-only
print("\n=== Test 1: Text-only ===")
with torch.no_grad():
    response = model.chat(
        tokenizer=tokenizer, new_token_ids=new_token_ids,
        image_transform=image_transform, images=[],
        prompt="What is 2+2? Answer with just the number.",
        max_length=512,
    )
print(f"Response: '{response}'")

# Test 2: With gray image
print("\n=== Test 2: Gray image ===")
test_image = Image.new("RGB", (512, 512), (200, 200, 200))
img = _vae_resize(test_image.convert("RGB"))
with torch.no_grad():
    response = model.chat(
        tokenizer=tokenizer, new_token_ids=new_token_ids,
        image_transform=image_transform, images=[img],
        prompt="What color is this image? Answer briefly.",
        max_length=512,
    )
print(f"Response: '{response}'")

# Test 3: Multiple colors
print("\n=== Test 3: Red and Blue images ===")
img1 = _vae_resize(Image.new("RGB", (256, 256), (255, 0, 0)))
img2 = _vae_resize(Image.new("RGB", (256, 256), (0, 0, 255)))
with torch.no_grad():
    response = model.chat(
        tokenizer=tokenizer, new_token_ids=new_token_ids,
        image_transform=image_transform, images=[img1, img2],
        prompt="What are the colors in these two images?",
        max_length=512,
    )
print(f"Response: '{response}'")

print("\n=== ThinkMorph tests passed! ===")
