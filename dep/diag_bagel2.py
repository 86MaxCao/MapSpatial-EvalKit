"""Diagnostic: Bagel understand — trace where NaN appears in generation.

Text-only works ("4"), image input produces NaN logits.
KV cache is fine. Issue is in the generation forward pass.
"""
import os, sys, json, time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
import numpy as np
from PIL import Image

MODEL_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/BAGEL-7B-MoT"
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.bagel.modeling_bagel import BagelForConditionalGeneration, NaiveCache
import torch.nn.functional as F

print("Loading model...")
t0 = time.time()
model, config = load_model(MODEL_PATH, BagelForConditionalGeneration, device="cuda", dtype="bfloat16")
tokenizer = load_tokenizer(MODEL_PATH)
print(f"Loaded in {time.time()-t0:.1f}s")

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

# Image transform
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

vit_patch_size = getattr(config.vit_config, "patch_size", 14)
image_transform = _ImageTransform(980, 224, vit_patch_size)

device = next(model.parameters()).device

# Create test image and run ViT + text steps to build KV cache
print("\n--- Building KV cache with image ---")
test_image = Image.new("RGB", (512, 512), (200, 200, 200))
img = _vae_resize(test_image.convert("RGB"))
images = [img]

past_key_values = NaiveCache(config.llm_config.num_hidden_layers)
newlens = [0]
new_rope = [0]

# ViT step
gen_input, newlens, new_rope = model.prepare_vit_images(
    curr_kvlens=newlens, curr_rope=new_rope, images=images,
    transforms=image_transform, new_token_ids=new_token_ids,
)
for k, v in gen_input.items():
    if torch.is_tensor(v):
        gen_input[k] = v.to(device)
with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
    past_key_values = model.forward_cache_update_vit(past_key_values, **gen_input)
print(f"After ViT: newlens={newlens}, new_rope={new_rope}")

# Text step
prompt = "What color is this image?"
gen_input, newlens, new_rope = model.prepare_prompts(
    curr_kvlens=newlens, curr_rope=new_rope, prompts=[prompt],
    tokenizer=tokenizer, new_token_ids=new_token_ids,
)
for k, v in gen_input.items():
    if torch.is_tensor(v):
        gen_input[k] = v.to(device)
with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
    past_key_values = model.forward_cache_update_text(past_key_values, **gen_input)
print(f"After text: newlens={newlens}, new_rope={new_rope}")

# Now manually run ONE generation step with detailed NaN tracing
print("\n--- Generation step 0: detailed trace ---")
gen_input = model.prepare_start_tokens(newlens, new_rope, new_token_ids)
for k, v in gen_input.items():
    if torch.is_tensor(v):
        gen_input[k] = v.to(device)

curr_tokens = gen_input["packed_start_tokens"]
packed_key_value_indexes = gen_input["packed_key_value_indexes"]
key_values_lens = gen_input["key_values_lens"]
packed_query_position_ids = gen_input["packed_query_position_ids"]

print(f"curr_tokens: {curr_tokens.tolist()}")
print(f"packed_key_value_indexes: {packed_key_value_indexes[:5].tolist()}...{packed_key_value_indexes[-3:].tolist()} len={len(packed_key_value_indexes)}")
print(f"key_values_lens: {key_values_lens.tolist()}")
print(f"packed_query_position_ids: {packed_query_position_ids.tolist()}")

# Embed
packed_text_embedding = model.language_model.model.embed_tokens(curr_tokens)
print(f"\n1. embed_tokens output: dtype={packed_text_embedding.dtype} shape={packed_text_embedding.shape} nan={torch.isnan(packed_text_embedding).any().item()} sum={packed_text_embedding.float().sum().item():.4f}")

query_lens = torch.ones_like(curr_tokens)
packed_query_indexes = torch.cumsum(key_values_lens, dim=0) + torch.arange(
    0, len(key_values_lens), device=key_values_lens.device, dtype=key_values_lens.dtype,
)
print(f"2. packed_query_indexes: {packed_query_indexes.tolist()}")

uppacked = list(packed_key_value_indexes.split(key_values_lens.tolist(), dim=0))
for i in range(len(uppacked)):
    uppacked[i] = uppacked[i] + i
packed_key_value_indexes = torch.cat(uppacked, dim=0)
print(f"3. packed_key_value_indexes (after +i): first5={packed_key_value_indexes[:5].tolist()} last5={packed_key_value_indexes[-5:].tolist()} len={len(packed_key_value_indexes)}")

# Now trace through Qwen2Model.forward_inference manually
qwen_model = model.language_model.model

# Rotary embedding
cos, sin = qwen_model.rotary_emb(packed_text_embedding, packed_query_position_ids.unsqueeze(0))
cos, sin = cos.squeeze(0), sin.squeeze(0)
print(f"4. rotary cos: dtype={cos.dtype} shape={cos.shape} nan={torch.isnan(cos).any().item()} sum={cos.float().sum().item():.4f}")
print(f"4. rotary sin: dtype={sin.dtype} shape={sin.shape} nan={torch.isnan(sin).any().item()} sum={sin.float().sum().item():.4f}")
packed_query_position_embeddings = (cos, sin)

# Check KV cache state
k0 = past_key_values.key_cache[0]
v0 = past_key_values.value_cache[0]
print(f"5. KV cache layer 0 key: dtype={k0.dtype} shape={k0.shape} nan={torch.isnan(k0).any().item()} sum={k0.float().sum().item():.4f}")
print(f"5. KV cache layer 0 val: dtype={v0.dtype} shape={v0.shape} nan={torch.isnan(v0).any().item()} sum={v0.float().sum().item():.4f}")

# Trace through first layer
layer = qwen_model.layers[0]
extra = dict(mode="und", packed_vae_token_indexes=None, packed_text_indexes=None)

# Layer norm
residual = packed_text_embedding
normed = layer.input_layernorm(packed_text_embedding)
print(f"6. input_layernorm: dtype={normed.dtype} shape={normed.shape} nan={torch.isnan(normed).any().item()} sum={normed.float().sum().item():.4f}")

# Attention
attn_out, pkv = layer.self_attn.forward_inference(
    packed_query_sequence=normed,
    query_lens=query_lens,
    packed_query_position_embeddings=packed_query_position_embeddings,
    packed_query_indexes=packed_query_indexes,
    past_key_values=past_key_values,
    key_values_lens=key_values_lens,
    packed_key_value_indexes=packed_key_value_indexes,
    update_past_key_values=True,
    is_causal=True,
    **extra,
)
print(f"7. attn output: dtype={attn_out.dtype} shape={attn_out.shape} nan={torch.isnan(attn_out).any().item()} sum={attn_out.float().sum().item():.4f}")

packed_query_sequence = residual + attn_out
print(f"8. residual+attn: dtype={packed_query_sequence.dtype} shape={packed_query_sequence.shape} nan={torch.isnan(packed_query_sequence).any().item()} sum={packed_query_sequence.float().sum().item():.4f}")

# MLP
residual2 = packed_query_sequence
normed2 = layer.post_attention_layernorm(packed_query_sequence)
print(f"9. post_attn_layernorm: dtype={normed2.dtype} nan={torch.isnan(normed2).any().item()} sum={normed2.float().sum().item():.4f}")
mlp_out = layer.mlp(normed2)
print(f"10. mlp output: dtype={mlp_out.dtype} shape={mlp_out.shape} nan={torch.isnan(mlp_out).any().item()} sum={mlp_out.float().sum().item():.4f}")
packed_query_sequence = residual2 + mlp_out
print(f"11. residual+mlp: dtype={packed_query_sequence.dtype} nan={torch.isnan(packed_query_sequence).any().item()} sum={packed_query_sequence.float().sum().item():.4f}")

# Run remaining layers
for i in range(1, len(qwen_model.layers)):
    layer = qwen_model.layers[i]
    packed_query_sequence, pkv = layer.forward_inference(
        packed_query_sequence=packed_query_sequence,
        query_lens=query_lens,
        packed_query_position_embeddings=packed_query_position_embeddings,
        packed_query_indexes=packed_query_indexes,
        past_key_values=pkv,
        key_values_lens=key_values_lens,
        packed_key_value_indexes=packed_key_value_indexes,
        update_past_key_values=True,
        is_causal=True,
        **extra,
    )
    if torch.isnan(packed_query_sequence).any():
        print(f"12. Layer {i}: NaN detected! sum={packed_query_sequence.float().sum().item():.4f}")
        break
else:
    print(f"12. All layers done: dtype={packed_query_sequence.dtype} nan={torch.isnan(packed_query_sequence).any().item()} sum={packed_query_sequence.float().sum().item():.4f}")

# Final norm
if model.use_moe:
    packed_query_sequence = qwen_model.norm(packed_query_sequence)
else:
    packed_query_sequence = qwen_model.norm(packed_query_sequence)
print(f"13. After final norm: dtype={packed_query_sequence.dtype} nan={torch.isnan(packed_query_sequence).any().item()} sum={packed_query_sequence.float().sum().item():.4f}")

# LM head
pred_logits = model.language_model.lm_head(packed_query_sequence)
print(f"14. lm_head logits: dtype={pred_logits.dtype} shape={pred_logits.shape} nan={torch.isnan(pred_logits).any().item()}")
if not torch.isnan(pred_logits).any():
    print(f"    top5 tokens: {pred_logits[0].topk(5).indices.tolist()}")
    print(f"    top5 values: {[f'{v:.4f}' for v in pred_logits[0].topk(5).values.tolist()]}")
    print(f"    argmax={pred_logits.argmax(dim=-1)[0].item()} = '{tokenizer.decode([pred_logits.argmax(dim=-1)[0].item()])}'")
