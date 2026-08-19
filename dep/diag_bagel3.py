"""Diagnostic: Bagel — trace inside PackedAttentionMoT.forward_inference to find NaN source."""
import os, sys, time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
import numpy as np
from PIL import Image
import torch.nn.functional as F

MODEL_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/BAGEL-7B-MoT"
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.bagel.modeling_bagel import BagelForConditionalGeneration, NaiveCache

print("Loading model...")
model, config = load_model(MODEL_PATH, BagelForConditionalGeneration, device="cuda", dtype="bfloat16")
tokenizer = load_tokenizer(MODEL_PATH)
print(f"Loaded. use_moe={model.use_moe}")

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
device = next(model.parameters()).device

# Check attention weights
print("\n--- Attention weights check (layer 0) ---")
attn = model.language_model.model.layers[0].self_attn
for name, p in attn.named_parameters():
    nan = torch.isnan(p).any().item()
    zero = (p.abs() < 1e-10).all().item()
    print(f"  {name}: shape={p.shape} dtype={p.dtype} nan={nan} all_zero={zero} mean={p.float().mean().item():.6f} std={p.float().std().item():.6f}")

# Build KV cache
print("\n--- Building KV cache ---")
test_image = Image.new("RGB", (512, 512), (200, 200, 200))
img = _vae_resize(test_image.convert("RGB"))
past_key_values = NaiveCache(config.llm_config.num_hidden_layers)
newlens, new_rope = [0], [0]

gen_input, newlens, new_rope = model.prepare_vit_images(
    curr_kvlens=newlens, curr_rope=new_rope, images=[img],
    transforms=image_transform, new_token_ids=new_token_ids)
for k, v in gen_input.items():
    if torch.is_tensor(v):
        gen_input[k] = v.to(device)
with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
    past_key_values = model.forward_cache_update_vit(past_key_values, **gen_input)

prompt = "What color is this image?"
gen_input, newlens, new_rope = model.prepare_prompts(
    curr_kvlens=newlens, curr_rope=new_rope, prompts=[prompt],
    tokenizer=tokenizer, new_token_ids=new_token_ids)
for k, v in gen_input.items():
    if torch.is_tensor(v):
        gen_input[k] = v.to(device)
with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
    past_key_values = model.forward_cache_update_text(past_key_values, **gen_input)
print(f"KV cache: newlens={newlens}, new_rope={new_rope}")

# Generation step
gen_input = model.prepare_start_tokens(newlens, new_rope, new_token_ids)
for k, v in gen_input.items():
    if torch.is_tensor(v):
        gen_input[k] = v.to(device)

curr_tokens = gen_input["packed_start_tokens"]
packed_key_value_indexes = gen_input["packed_key_value_indexes"]
key_values_lens = gen_input["key_values_lens"]
packed_query_position_ids = gen_input["packed_query_position_ids"]

# Embed
packed_text_embedding = model.language_model.model.embed_tokens(curr_tokens)
query_lens = torch.ones_like(curr_tokens)
packed_query_indexes = torch.cumsum(key_values_lens, dim=0) + torch.arange(
    0, len(key_values_lens), device=key_values_lens.device, dtype=key_values_lens.dtype)
uppacked = list(packed_key_value_indexes.split(key_values_lens.tolist(), dim=0))
for i in range(len(uppacked)):
    uppacked[i] = uppacked[i] + i
packed_key_value_indexes = torch.cat(uppacked, dim=0)

# Rotary
qwen_model = model.language_model.model
cos, sin = qwen_model.rotary_emb(packed_text_embedding, packed_query_position_ids.unsqueeze(0))
cos, sin = cos.squeeze(0), sin.squeeze(0)
packed_query_position_embeddings = (cos, sin)

# Layer 0
layer = qwen_model.layers[0]
attn = layer.self_attn

# Input to attention
normed = layer.input_layernorm(packed_text_embedding)
print(f"\n--- Inside PackedAttentionMoT.forward_inference (layer 0) ---")
print(f"Input: dtype={normed.dtype} shape={normed.shape} nan={torch.isnan(normed).any().item()} sum={normed.float().sum().item():.4f}")

# Projections (und mode)
packed_query_states = attn.q_proj(normed).view(-1, attn.num_heads, attn.head_dim)
packed_key_states = attn.k_proj(normed).view(-1, attn.num_key_value_heads, attn.head_dim)
packed_value_states = attn.v_proj(normed).view(-1, attn.num_key_value_heads, attn.head_dim)
print(f"q_proj out: dtype={packed_query_states.dtype} shape={packed_query_states.shape} nan={torch.isnan(packed_query_states).any().item()} sum={packed_query_states.float().sum().item():.4f}")
print(f"k_proj out: dtype={packed_key_states.dtype} shape={packed_key_states.shape} nan={torch.isnan(packed_key_states).any().item()} sum={packed_key_states.float().sum().item():.4f}")
print(f"v_proj out: dtype={packed_value_states.dtype} shape={packed_value_states.shape} nan={torch.isnan(packed_value_states).any().item()} sum={packed_value_states.float().sum().item():.4f}")

# Norms
packed_query_states = attn.q_norm(packed_query_states)
packed_key_states = attn.k_norm(packed_key_states)
print(f"q_norm out: dtype={packed_query_states.dtype} nan={torch.isnan(packed_query_states).any().item()} sum={packed_query_states.float().sum().item():.4f}")
print(f"k_norm out: dtype={packed_key_states.dtype} nan={torch.isnan(packed_key_states).any().item()} sum={packed_key_states.float().sum().item():.4f}")

# Rotary
from mapspatial.vendor.bagel.modeling_bagel import _apply_rotary_pos_emb
packed_query_states, packed_key_states = _apply_rotary_pos_emb(
    packed_query_states, packed_key_states, cos, sin)
print(f"rotary q: dtype={packed_query_states.dtype} nan={torch.isnan(packed_query_states).any().item()} sum={packed_query_states.float().sum().item():.4f}")
print(f"rotary k: dtype={packed_key_states.dtype} nan={torch.isnan(packed_key_states).any().item()} sum={packed_key_states.float().sum().item():.4f}")

# To bfloat16
packed_query_states = packed_query_states.to(torch.bfloat16)
packed_key_states = packed_key_states.to(torch.bfloat16)
packed_value_states = packed_value_states.to(torch.bfloat16)

# Merge with past
past_key_states = past_key_values.key_cache[0]
past_value_states = past_key_values.value_cache[0]
print(f"\npast_key_states: dtype={past_key_states.dtype} shape={past_key_states.shape} nan={torch.isnan(past_key_states).any().item()}")
print(f"past_value_states: dtype={past_value_states.dtype} shape={past_value_states.shape} nan={torch.isnan(past_value_states).any().item()}")

seqlens = sum(query_lens) + sum(key_values_lens)
print(f"seqlens = {seqlens} (query={sum(query_lens)} + kv={sum(key_values_lens)})")
print(f"packed_query_indexes: {packed_query_indexes.tolist()}")
print(f"packed_key_value_indexes: first5={packed_key_value_indexes[:5].tolist()} last5={packed_key_value_indexes[-5:].tolist()} len={len(packed_key_value_indexes)}")

merged_key_states = past_key_states.new_zeros((seqlens, attn.num_key_value_heads, attn.head_dim))
merged_value_states = past_value_states.new_zeros((seqlens, attn.num_key_value_heads, attn.head_dim))
merged_key_states[packed_query_indexes] = packed_key_states
merged_key_states[packed_key_value_indexes] = past_key_states
merged_value_states[packed_query_indexes] = packed_value_states
merged_value_states[packed_key_value_indexes] = past_value_states

print(f"merged_key_states: dtype={merged_key_states.dtype} shape={merged_key_states.shape} nan={torch.isnan(merged_key_states).any().item()} sum={merged_key_states.float().sum().item():.4f}")
print(f"merged_value_states: dtype={merged_value_states.dtype} shape={merged_value_states.shape} nan={torch.isnan(merged_value_states).any().item()} sum={merged_value_states.float().sum().item():.4f}")

key_values_lens_new = key_values_lens + query_lens
cu_seqlens_q = F.pad(torch.cumsum(query_lens, dim=0), (1, 0)).to(torch.int32)
cu_seqlens_k = F.pad(torch.cumsum(key_values_lens_new, dim=0), (1, 0)).to(torch.int32)
print(f"cu_seqlens_q: {cu_seqlens_q.tolist()}")
print(f"cu_seqlens_k: {cu_seqlens_k.tolist()}")
print(f"max_seqlen_q: {max(query_lens).item()}")
print(f"max_seqlen_k: {max(key_values_lens_new).item()}")

# Flash attention
from flash_attn import flash_attn_varlen_func
attn_output = flash_attn_varlen_func(
    q=packed_query_states,
    k=merged_key_states,
    v=merged_value_states,
    cu_seqlens_q=cu_seqlens_q,
    cu_seqlens_k=cu_seqlens_k,
    max_seqlen_q=max(query_lens).item(),
    max_seqlen_k=max(key_values_lens_new).item(),
    causal=True,
)
print(f"\nflash_attn output: dtype={attn_output.dtype} shape={attn_output.shape} nan={torch.isnan(attn_output).any().item()} sum={attn_output.float().sum().item():.4f}")

# o_proj
attn_output = attn_output.reshape(-1, attn.hidden_size)
output = attn.o_proj(attn_output)
print(f"o_proj output: dtype={output.dtype} shape={output.shape} nan={torch.isnan(output).any().item()} sum={output.float().sum().item():.4f}")
