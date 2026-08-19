"""BLIP3o understanding with Qwen2.5-VL style vision tokens."""
import os, sys, time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
import numpy as np
from PIL import Image

MODEL_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/BLIP3o-Model-8B"
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.blip3o.modeling_blip3o import BLIP3oQwenForCausalLM

print("Loading BLIP3o...")
model, config = load_model(MODEL_PATH, BLIP3oQwenForCausalLM, device="cuda", dtype="bfloat16")
tokenizer = load_tokenizer(MODEL_PATH)

IMAGE_PAD_ID = 151655  # <|image_pad|>
VISION_START_ID = 151652  # <|vision_start|>
VISION_END_ID = 151653  # <|vision_end|>

def blip3o_understand(model, tokenizer, prompt, images=None, max_new_tokens=256):
    """BLIP3o understanding with Qwen2.5-VL style vision token replacement."""
    device = next(model.parameters()).device
    embed_layer = model.get_input_embeddings()

    if images:
        # Preprocess images first to know num vision features
        tensors = []
        for img in images:
            img = img.convert("RGB")
            w, h = img.size
            scale = min(980 / max(w, h), 1.0)
            scale = max(scale, 224 / min(w, h))
            new_w = max(14, int(round(w * scale) / 14) * 14)
            new_h = max(14, int(round(h * scale) / 14) * 14)
            img = img.resize((new_w, new_h), Image.BICUBIC)
            t = torch.tensor(np.array(img)).permute(2, 0, 1).float() / 255.0
            tensors.append(t)
        pixel_values = torch.stack(tensors).to(device, dtype=torch.bfloat16)

        with torch.no_grad():
            vit_features = model.visual(pixel_values)  # [1, L, D]
        vit_embeds = vit_features.reshape(-1, vit_features.shape[-1])  # [L, D]
        num_vit = vit_embeds.shape[0]

        # Build prompt with vision tokens: <|vision_start|> + <|image_pad|>*N + <|vision_end|>
        vision_str = "<|vision_start|>" + "<|image_pad|>" * num_vit + "<|vision_end|>"
        text = f"<|im_start|>user\n{vision_str}{prompt}<|im_end|>\n<|im_start|>assistant\n"
    else:
        text = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"

    input_ids = tokenizer.encode(text, return_tensors="pt").to(device)
    inputs_embeds = embed_layer(input_ids[0])  # [T, D]

    if images:
        # Replace <|image_pad|> positions with vision features
        image_mask = (input_ids[0] == IMAGE_PAD_ID)
        num_pad = image_mask.sum().item()
        print(f"  vit features: {num_vit}, image_pad tokens: {num_pad}")
        assert num_pad == num_vit, f"Mismatch: {num_pad} vs {num_vit}"

        inputs_embeds[image_mask] = vit_embeds.to(inputs_embeds.dtype)

    # Greedy decoding
    eos_id = tokenizer.eos_token_id or tokenizer.convert_tokens_to_ids("<|im_end|>")
    lm_head = model.get_output_embeddings()
    generated = []

    with torch.no_grad():
        for step in range(max_new_tokens):
            hidden = model._llm_forward(inputs_embeds.unsqueeze(0))
            logits = lm_head(hidden[:, -1:, :])
            next_id = logits[0, -1].argmax(dim=-1).item()
            if next_id == eos_id:
                break
            generated.append(next_id)
            next_embed = embed_layer(torch.tensor([[next_id]], device=device))
            inputs_embeds = torch.cat([inputs_embeds, next_embed[0]], dim=0)

    return tokenizer.decode(generated, skip_special_tokens=True).strip()

# Test 1: Text-only
print("\n=== Test 1: Text-only ===")
response = blip3o_understand(model, tokenizer, "What is 2+2? Answer with just the number.")
print(f"Response: '{response}'")

# Test 2: Gray image
print("\n=== Test 2: Gray image ===")
img = Image.new("RGB", (512, 512), (200, 200, 200))
response = blip3o_understand(model, tokenizer, "What color is this image? Answer briefly.", images=[img])
print(f"Response: '{response}'")

# Test 3: Red image
print("\n=== Test 3: Red image ===")
img = Image.new("RGB", (256, 256), (255, 0, 0))
response = blip3o_understand(model, tokenizer, "What color is this image? Answer briefly.", images=[img])
print(f"Response: '{response}'")

# Test 4: Blue image
print("\n=== Test 4: Blue image ===")
img = Image.new("RGB", (256, 256), (0, 0, 255))
response = blip3o_understand(model, tokenizer, "What color is this image? Answer briefly.", images=[img])
print(f"Response: '{response}'")

# Test 5: Red and Blue
print("\n=== Test 5: Red and Blue ===")
img1 = Image.new("RGB", (256, 256), (255, 0, 0))
img2 = Image.new("RGB", (256, 256), (0, 0, 255))
response = blip3o_understand(model, tokenizer, "What are the colors in these two images?", images=[img1, img2])
print(f"Response: '{response}'")

print("\n=== Done ===")
