"""Test Janus via standard from_pretrained vs custom loader."""
import os, sys
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "2")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
import torch
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

JANUS_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/Janus-Pro-7B"

# Method 1: Standard from_pretrained
print("=" * 60)
print("Method 1: Janus.from_pretrained (standard HF)")
print("=" * 60)
try:
    from mapspatial.vendor.janus.modeling_janus import Janus
    from mapspatial.vendor.janus.configuration_janus import JanusConfig
    model = Janus.from_pretrained(JANUS_PATH, torch_dtype=torch.bfloat16, device_map="cuda")
    model.eval()
    tokenizer = __import__("transformers").AutoTokenizer.from_pretrained(JANUS_PATH, trust_remote_code=True)

    prompt = "What is 2+2? Answer with just the number."
    chat = f"You are a helpful assistant.\n\nUser: {prompt}\n\nAssistant:"
    input_ids = tokenizer.encode(chat, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.language_model.generate(
            input_ids=input_ids,
            attention_mask=torch.ones_like(input_ids),
            max_new_tokens=20, do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    print(f"  Output: '{tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)}'")

    # Check config
    lc = model.config.language_config
    print(f"  LLM config: hidden={lc.hidden_size}, layers={lc.num_hidden_layers}, heads={lc.num_attention_heads}, kv_heads={lc.num_key_value_heads}, rope_theta={lc.rope_theta}, intermediate={lc.intermediate_size}")
    print(f"  Attn impl: {model.config._attn_implementation}")

    del model
    torch.cuda.empty_cache()
except Exception as e:
    import traceback; print(f"Method 1 failed: {e}"); traceback.print_exc()

# Method 2: Our custom loader
print("\n" + "=" * 60)
print("Method 2: custom load_model")
print("=" * 60)
try:
    from mapspatial.loader import load_model, load_tokenizer
    model, config = load_model(JANUS_PATH, Janus, device="cuda", dtype="bfloat16")
    tokenizer = load_tokenizer(JANUS_PATH)

    lc = config.language_config
    print(f"  LLM config: hidden={lc.hidden_size}, layers={lc.num_hidden_layers}, heads={lc.num_attention_heads}, kv_heads={lc.num_key_value_heads}, rope_theta={lc.rope_theta}, intermediate={lc.intermediate_size}")
    print(f"  Attn impl: {config._attn_implementation}")

    # Check for meta device params
    meta_count = sum(1 for n, p in model.named_parameters() if p.device.type == "meta")
    print(f"  Meta params: {meta_count}")
    # Check for meta buffers
    meta_bufs = [n for n, b in model.named_buffers() if b.device.type == "meta"]
    print(f"  Meta buffers: {len(meta_bufs)} {meta_bufs[:5]}")

    prompt = "What is 2+2? Answer with just the number."
    chat = f"You are a helpful assistant.\n\nUser: {prompt}\n\nAssistant:"
    input_ids = tokenizer.encode(chat, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.language_model.generate(
            input_ids=input_ids,
            attention_mask=torch.ones_like(input_ids),
            max_new_tokens=20, do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    print(f"  Output: '{tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)}'")

    del model
    torch.cuda.empty_cache()
except Exception as e:
    import traceback; print(f"Method 2 failed: {e}"); traceback.print_exc()
