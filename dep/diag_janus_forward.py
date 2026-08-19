"""Test Janus LLM forward pass directly (no generate/KV-cache) to isolate the issue."""
import os, sys
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "2")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
import torch
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.janus.modeling_janus import Janus

JANUS_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/Janus-Pro-7B"
model, config = load_model(JANUS_PATH, Janus, device="cuda", dtype="bfloat16")
tokenizer = load_tokenizer(JANUS_PATH)
model.eval()

# Check config details
lc = config.language_config
print(f"LLM: hidden={lc.hidden_size}, layers={lc.num_hidden_layers}, heads={lc.num_attention_heads}")
print(f"  kv_heads={getattr(lc, 'num_key_value_heads', 'N/A')}, intermediate={lc.intermediate_size}")
print(f"  rope_scaling={getattr(lc, 'rope_scaling', 'N/A')}")
print(f"  tie_word_embeddings={lc.tie_word_embeddings}")
print(f"  max_pos={lc.max_position_embeddings}")
print(f"  attn_impl={lc._attn_implementation}")

# Check embed_tokens vs lm_head
embed = model.language_model.get_input_embeddings()
lm_head = model.language_model.get_output_embeddings()
print(f"\nembed_tokens: shape={embed.weight.shape}, mean={embed.weight.float().mean():.6f}")
print(f"lm_head: shape={lm_head.weight.shape}, mean={lm_head.weight.float().mean():.6f}")
print(f"  same data ptr: {embed.weight.data_ptr() == lm_head.weight.data_ptr()}")

# Direct forward pass (no generate, no KV cache)
prompt = "What is 2+2? Answer with just the number."
chat = f"You are a helpful assistant.\n\nUser: {prompt}\n\nAssistant:"
input_ids = tokenizer.encode(chat, return_tensors="pt").to("cuda")
print(f"\nInput shape: {input_ids.shape}")

with torch.no_grad():
    out = model.language_model(input_ids=input_ids, use_cache=False)
    logits = out.logits  # [1, T, V]
    print(f"Logits shape: {logits.shape}, nan={torch.isnan(logits).any().item()}")

    # Check top-5 predictions at the LAST position (should be the first generated token)
    last_logits = logits[0, -1, :]
    top5 = last_logits.topk(5)
    print(f"\nTop-5 next tokens: {top5.indices.tolist()}")
    print(f"  Decoded: {[tokenizer.decode([t]) for t in top5.indices.tolist()]}")
    print(f"  Logits: {[f'{v:.2f}' for v in top5.values.tolist()]}")

    # Also check token at position 0 (should be reasonable continuation after BOS)
    pos0_logits = logits[0, 0, :]
    top5_0 = pos0_logits.topk(5)
    print(f"\nTop-5 at pos 0: {top5_0.indices.tolist()}")
    print(f"  Decoded: {[tokenizer.decode([t]) for t in top5_0.indices.tolist()]}")

# Now test greedy decode manually (step by step, no KV cache)
print("\n--- Manual greedy decode (no KV cache) ---")
cur_ids = input_ids.clone()
with torch.no_grad():
    for step in range(10):
        out = model.language_model(input_ids=cur_ids, use_cache=False)
        next_id = out.logits[0, -1].argmax().item()
        print(f"  Step {step}: next_id={next_id} = '{tokenizer.decode([next_id])}'")
        if next_id == tokenizer.eos_token_id:
            print("  EOS"); break
        cur_ids = torch.cat([cur_ids, torch.tensor([[next_id]], device="cuda")], dim=1)

del model
torch.cuda.empty_cache()
