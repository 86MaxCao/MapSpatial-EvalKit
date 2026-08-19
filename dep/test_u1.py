"""U1 diagnostic with indexes (position IDs) fix."""
import os, sys, time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
from PIL import Image

MODEL_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/SenseNova-U1-8B-MoT"
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.neo_chat.modeling_neo_chat import NEOChatModel

print("Loading U1...")
model, config = load_model(MODEL_PATH, NEOChatModel, device="cuda", dtype="bfloat16")
tokenizer = load_tokenizer(MODEL_PATH)
print(f"Loaded. Params: {sum(p.numel() for p in model.parameters())/1e9:.2f}B")

def u1_understand(model, tokenizer, prompt, max_new_tokens=64):
    """U1 understanding with M-RoPE position IDs."""
    device = next(model.parameters()).device
    chat = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
    input_ids = tokenizer.encode(chat, return_tensors="pt").to(device)
    eos_id = tokenizer.eos_token_id

    generated = []
    with torch.no_grad():
        for step in range(max_new_tokens):
            seq_len = input_ids.shape[1]
            pos = torch.arange(seq_len, device=device)
            indexes = torch.stack([pos, pos, pos])  # [3, seq_len] — M-RoPE

            outputs = model.language_model(
                input_ids=input_ids,
                attention_mask=torch.ones_like(input_ids),
                indexes=indexes,
            )
            logits = outputs.logits
            next_id = logits[0, -1].argmax(dim=-1).item()
            if next_id == eos_id:
                break
            generated.append(next_id)
            input_ids = torch.cat([input_ids, torch.tensor([[next_id]], device=device)], dim=1)
            if step < 5:
                print(f"  Step {step}: {next_id} = '{tokenizer.decode([next_id])}' nan={torch.isnan(logits).any().item()}")

    return tokenizer.decode(generated, skip_special_tokens=True).strip()

# Test 1: Text-only
print("\n=== Test 1: Text-only ===")
response = u1_understand(model, tokenizer, "What is 2+2? Answer with just the number.")
print(f"Response: '{response}'")

# Test 2: Description
print("\n=== Test 2: Description ===")
response = u1_understand(model, tokenizer, "Describe the sky in one sentence.")
print(f"Response: '{response}'")

print("\n=== Done ===")
