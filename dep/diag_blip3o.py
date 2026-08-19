"""BLIP3o diagnostic: check model loading, missing keys, and understand output."""
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

# Check checkpoint keys
print("=== Checkpoint keys ===")
import json
from safetensors import safe_open

index_file = os.path.join(MODEL_PATH, "model.safetensors.index.json")
with open(index_file) as f:
    idx = json.load(f)
wm = idx['weight_map']
print(f"Total keys in checkpoint: {len(wm)}")
# Sample some attention keys
attn_keys = sorted([k for k in wm if 'self_attn' in k])
print(f"self_attn keys ({len(attn_keys)}):")
for k in attn_keys[:15]:
    print(f"  {k}")
# Check for q_norm/k_norm
qknorm_keys = [k for k in wm if 'q_norm' in k or 'k_norm' in k]
print(f"\nq_norm/k_norm keys: {len(qknorm_keys)}")
for k in sorted(qknorm_keys)[:5]:
    print(f"  {k}")

# Load model
print("\n=== Loading model ===")
from mapspatial.loader import load_model, load_tokenizer, _load_safetensors
from mapspatial.vendor.blip3o.modeling_blip3o import BLIP3oQwenForCausalLM

model, config = load_model(MODEL_PATH, BLIP3oQwenForCausalLM, device="cuda", dtype="bfloat16")
tokenizer = load_tokenizer(MODEL_PATH)

# Check model params
model_params = dict(model.named_parameters())
print(f"\nModel params: {len(model_params)}")

# Check for missing/unexpected
state_dict = _load_safetensors(MODEL_PATH)
missing = [k for k in model_params if k not in state_dict]
unexpected = [k for k in state_dict if k not in model_params]
print(f"Missing (in model, not in checkpoint): {len(missing)}")
for k in sorted(missing)[:10]:
    print(f"  {k}")
print(f"Unexpected (in checkpoint, not in model): {len(unexpected)}")
for k in sorted(unexpected)[:10]:
    print(f"  {k}")

# Check key attention params
for name in ["model.layers.0.self_attn.q_proj.weight",
             "model.layers.0.self_attn.k_proj.weight",
             "model.layers.0.self_attn.q_norm.weight",
             "model.layers.0.self_attn.k_norm.weight",
             "lm_head.weight",
             "model.embed_tokens.weight"]:
    if name in model_params:
        p = model_params[name]
        print(f"\n  {name}: shape={p.shape} dtype={p.dtype} mean={p.float().mean().item():.6f} std={p.float().std().item():.6f}")
    else:
        print(f"\n  {name}: NOT IN MODEL")

# Test 1: Text-only (our method — full LLM forward)
print("\n=== Test 1: Text-only (our _llm_forward method) ===")
text = "<|im_start|>user\nWhat is 2+2? Answer with just the number.<|im_end|>\n<|im_start|>assistant\n"
input_ids = tokenizer.encode(text, return_tensors="pt").to("cuda")
embed_layer = model.get_input_embeddings()
inputs_embeds = embed_layer(input_ids[0])

with torch.no_grad():
    hidden = model._llm_forward(inputs_embeds.unsqueeze(0))
    print(f"  hidden shape: {hidden.shape}")
    print(f"  hidden nan: {torch.isnan(hidden).any().item()}")
    print(f"  hidden sum: {hidden.float().sum().item():.4f}")

    lm_head = model.get_output_embeddings()
    logits = lm_head(hidden[:, -1:, :])
    print(f"  logits shape: {logits.shape}")
    print(f"  logits nan: {torch.isnan(logits).any().item()}")
    if not torch.isnan(logits).any():
        top5 = logits[0, -1].topk(5)
        print(f"  top5 tokens: {top5.indices.tolist()}")
        print(f"  top5 values: {[f'{v:.4f}' for v in top5.values.tolist()]}")
        print(f"  top5 decoded: {[tokenizer.decode([t]) for t in top5.indices.tolist()]}")

# Test 2: Official VeOmni method (embeddings → lm_head directly, no LLM forward)
print("\n=== Test 2: Official method (embeddings → lm_head, no LLM) ===")
with torch.no_grad():
    logits2 = lm_head(inputs_embeds[-1:])
    print(f"  logits shape: {logits2.shape}")
    print(f"  logits nan: {torch.isnan(logits2).any().item()}")
    if not torch.isnan(logits2).any():
        top5 = logits2[0].topk(5)
        print(f"  top5 tokens: {top5.indices.tolist()}")
        print(f"  top5 values: {[f'{v:.4f}' for v in top5.values.tolist()]}")
        print(f"  top5 decoded: {[tokenizer.decode([t]) for t in top5.indices.tolist()]}")

# Test 3: Image input (our method)
print("\n=== Test 3: Image input (our _llm_forward method) ===")
test_image = Image.new("RGB", (512, 512), (200, 200, 200))
img = test_image.convert("RGB")
# Resize
def resize_image(img, max_size=980, min_size=224, patch_size=14):
    w, h = img.size
    scale = min(max_size / max(w, h), 1.0)
    scale = max(scale, min_size / min(w, h))
    def _make_divisible(v, s):
        return max(s, int(round(v / s) * s))
    new_w = _make_divisible(round(w * scale), patch_size)
    new_h = _make_divisible(round(h * scale), patch_size)
    return img.resize((new_w, new_h), Image.BICUBIC)

img = resize_image(img)
img_tensor = torch.tensor(np.array(img)).permute(2, 0, 1).float() / 255.0
pixel_values = img_tensor.unsqueeze(0).to(device="cuda", dtype=torch.bfloat16)

with torch.no_grad():
    vit_features = model.visual(pixel_values)
    print(f"  vit_features: shape={vit_features.shape} dtype={vit_features.dtype} nan={torch.isnan(vit_features).any().item()}")
    if hasattr(model, "visual_projector") and model.visual_projector is not None:
        vit_features = model.visual_projector(vit_features)
        print(f"  after projector: shape={vit_features.shape} nan={torch.isnan(vit_features).any().item()}")

    vit_embeds = vit_features.reshape(-1, vit_features.shape[-1])
    full_embeds = torch.cat([vit_embeds, inputs_embeds], dim=0)
    print(f"  full_embeds: shape={full_embeds.shape}")

    hidden = model._llm_forward(full_embeds.unsqueeze(0))
    print(f"  hidden: shape={hidden.shape} nan={torch.isnan(hidden).any().item()}")

    if not torch.isnan(hidden).any():
        logits = lm_head(hidden[:, -1:, :])
        print(f"  logits: nan={torch.isnan(logits).any().item()}")
        if not torch.isnan(logits).any():
            top5 = logits[0, -1].topk(5)
            print(f"  top5: {top5.indices.tolist()} = {[tokenizer.decode([t]) for t in top5.indices.tolist()]}")

print("\n=== Diagnostic complete ===")
