"""U1 diagnostic: check model loading and understanding."""
import os, sys, time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
import numpy as np
from PIL import Image

MODEL_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/SenseNova-U1-8B-MoT"
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

from mapspatial.loader import load_model, load_tokenizer, _load_safetensors

# First check what keys are in the checkpoint
print("=== Checkpoint keys ===")
import json
with open(os.path.join(MODEL_PATH, "model.safetensors.index.json")) as f:
    idx = json.load(f)
wm = idx['weight_map']
print(f"Total keys: {len(wm)}")
# Check for attention keys
attn_keys = sorted([k for k in wm if 'self_attn' in k])
print(f"self_attn keys ({len(attn_keys)}):")
for k in attn_keys[:10]:
    print(f"  {k}")
qknorm = [k for k in wm if 'q_norm' in k or 'k_norm' in k]
print(f"q_norm/k_norm keys: {len(qknorm)}")
for k in sorted(qknorm)[:5]:
    print(f"  {k}")
# Check for bias
qkv_bias = [k for k in wm if 'q_proj.bias' in k or 'k_proj.bias' in k or 'v_proj.bias' in k]
print(f"q/k/v bias keys: {len(qkv_bias)}")

# Load model
print("\n=== Loading U1 model ===")
from mapspatial.vendor.neo_chat.modeling_neo_chat import NEOChatModel

try:
    model, config = load_model(MODEL_PATH, NEOChatModel, device="cuda", dtype="bfloat16")
    print(f"Model loaded. Params: {sum(p.numel() for p in model.parameters())/1e9:.2f}B")
except Exception as e:
    print(f"Load failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

tokenizer = load_tokenizer(MODEL_PATH)

# Check missing/unexpected
state_dict = _load_safetensors(MODEL_PATH)
model_params = dict(model.named_parameters())
missing = [k for k in model_params if k not in state_dict]
unexpected = [k for k in state_dict if k not in model_params]
print(f"Missing: {len(missing)}")
for k in sorted(missing)[:10]:
    print(f"  {k}")
print(f"Unexpected: {len(unexpected)}")
for k in sorted(unexpected)[:10]:
    print(f"  {k}")

# Check model structure
print("\n=== Model structure ===")
for name, mod in model.named_children():
    n = sum(p.numel() for p in mod.parameters())
    print(f"  {name}: {type(mod).__name__} ({n/1e6:.1f}M)")

# Check if language_model exists
if hasattr(model, 'language_model'):
    print(f"\n  language_model type: {type(model.language_model).__name__}")
    for name, mod in model.language_model.named_children():
        n = sum(p.numel() for p in mod.parameters())
        print(f"    language_model.{name}: {type(mod).__name__} ({n/1e6:.1f}M)")

# Test text-only
print("\n=== Test: Text-only understanding ===")
prompt = "What is 2+2? Answer with just the number."
chat = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
input_ids = tokenizer.encode(chat, return_tensors="pt").to("cuda")
print(f"Input shape: {input_ids.shape}")

try:
    with torch.no_grad():
        outputs = model.language_model(input_ids=input_ids, attention_mask=torch.ones_like(input_ids))
        logits = outputs.logits if hasattr(outputs, 'logits') else model.language_model.lm_head(outputs.last_hidden_state)
        print(f"Logits shape: {logits.shape}")
        print(f"Logits NaN: {torch.isnan(logits).any().item()}")
        if not torch.isnan(logits).any():
            top5 = logits[0, -1].topk(5)
            print(f"Top5: {top5.indices.tolist()} = {[tokenizer.decode([t]) for t in top5.indices.tolist()]}")
            print(f"Values: {[f'{v:.4f}' for v in top5.values.tolist()]}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Greedy decode 10 tokens
print("\n=== Greedy decode (10 tokens) ===")
try:
    generated = []
    eos_id = tokenizer.eos_token_id
    curr_ids = input_ids
    attn = torch.ones_like(input_ids)
    with torch.no_grad():
        for step in range(10):
            outputs = model.language_model(input_ids=curr_ids, attention_mask=attn)
            logits = outputs.logits if hasattr(outputs, 'logits') else model.language_model.lm_head(outputs.last_hidden_state)
            next_id = logits[0, -1].argmax(dim=-1).item()
            print(f"  Step {step}: token={next_id} = '{tokenizer.decode([next_id])}' nan={torch.isnan(logits).any().item()}")
            if next_id == eos_id:
                break
            generated.append(next_id)
            curr_ids = torch.cat([curr_ids, torch.tensor([[next_id]], device="cuda")], dim=1)
            attn = torch.ones_like(curr_ids)
    print(f"\nGenerated: '{tokenizer.decode(generated, skip_special_tokens=True)}'")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
