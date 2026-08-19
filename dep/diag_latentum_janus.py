"""Quick load test for LatentUM and Janus."""
import os, sys, time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

from mapspatial.loader import load_model, load_tokenizer, _load_safetensors

# === LatentUM ===
print("=" * 60)
print("LatentUM")
print("=" * 60)
LATENTUM_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/LatentUM-Base"
try:
    from mapspatial.vendor.latentum.modeling_latentum import LatentUMModel
    model, config = load_model(LATENTUM_PATH, LatentUMModel, device="cuda", dtype="bfloat16")
    tokenizer = load_tokenizer(LATENTUM_PATH)
    state_dict = _load_safetensors(LATENTUM_PATH)
    model_params = dict(model.named_parameters())
    missing = [k for k in model_params if k not in state_dict]
    unexpected = [k for k in state_dict if k not in model_params]
    print(f"Params: {sum(p.numel() for p in model.parameters())/1e9:.2f}B, Missing: {len(missing)}, Unexpected: {len(unexpected)}")
    if missing: print(f"  Missing first 5: {sorted(missing)[:5]}")
    if unexpected: print(f"  Unexpected first 5: {sorted(unexpected)[:5]}")

    # Quick text test
    prompt = "What is 2+2? Answer with just the number."
    text = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
    input_ids = tokenizer.encode(text, return_tensors="pt").to("cuda")
    lm = model.internvl.language_model
    embed_layer = lm.get_input_embeddings()
    inputs_embeds = embed_layer(input_ids[0])

    with torch.no_grad():
        hidden = lm.model(inputs_embeds=inputs_embeds.unsqueeze(0))
        hs = hidden.last_hidden_state if hasattr(hidden, 'last_hidden_state') else hidden[0]
        logits = lm.lm_head(hs[:, -1:, :])
        print(f"Text logits: nan={torch.isnan(logits).any().item()}")
        if not torch.isnan(logits).any():
            top5 = logits[0, -1].topk(5)
            print(f"  Top5: {top5.indices.tolist()} = {[tokenizer.decode([t]) for t in top5.indices.tolist()]}")
except Exception as e:
    import traceback
    print(f"LatentUM failed: {e}")
    traceback.print_exc()

# Free memory
del model
torch.cuda.empty_cache()

# === Janus ===
print("\n" + "=" * 60)
print("Janus-Pro-7B")
print("=" * 60)
JANUS_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/Janus-Pro-7B"
try:
    from mapspatial.vendor.janus.modeling_janus import Janus
    model, config = load_model(JANUS_PATH, Janus, device="cuda", dtype="bfloat16")
    tokenizer = load_tokenizer(JANUS_PATH)
    state_dict = _load_safetensors(JANUS_PATH)
    model_params = dict(model.named_parameters())
    missing = [k for k in model_params if k not in state_dict]
    unexpected = [k for k in state_dict if k not in model_params]
    print(f"Params: {sum(p.numel() for p in model.parameters())/1e9:.2f}B, Missing: {len(missing)}, Unexpected: {len(unexpected)}")
    if missing: print(f"  Missing first 5: {sorted(missing)[:5]}")
    if unexpected: print(f"  Unexpected first 5: {sorted(unexpected)[:5]}")

    # Quick text test — Janus uses LLaMA
    prompt = "What is 2+2? Answer with just the number."
    text = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
    input_ids = tokenizer.encode(text, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.language_model.generate(
            input_ids=input_ids,
            attention_mask=torch.ones_like(input_ids),
            max_new_tokens=10,
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    print(f"Generated: '{tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)}'")
except Exception as e:
    import traceback
    print(f"Janus failed: {e}")
    traceback.print_exc()

del model
torch.cuda.empty_cache()
print("\n=== Done ===")
