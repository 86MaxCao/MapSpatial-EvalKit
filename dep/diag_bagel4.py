"""Test: replace flash_attn with F.scaled_dot_product_attention in generation step."""
import os, sys, time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image

MODEL_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/BAGEL-7B-MoT"
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.bagel.modeling_bagel import BagelForConditionalGeneration, NaiveCache
from mapspatial.vendor.bagel.modeling_bagel import _apply_rotary_pos_emb

print("Loading model...")
model, config = load_model(MODEL_PATH, BagelForConditionalGeneration, device="cuda", dtype="bfloat16")
tokenizer = load_tokenizer(MODEL_PATH)

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

# Build KV cache
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

# Generation step
gen_input = model.prepare_start_tokens(newlens, new_rope, new_token_ids)
for k, v in gen_input.items():
    if torch.is_tensor(v):
        gen_input[k] = v.to(device)

curr_tokens = gen_input["packed_start_tokens"]
packed_key_value_indexes = gen_input["packed_key_value_indexes"]
key_values_lens = gen_input["key_values_lens"]
packed_query_position_ids = gen_input["packed_query_position_ids"]

packed_text_embedding = model.language_model.model.embed_tokens(curr_tokens)
query_lens = torch.ones_like(curr_tokens)
packed_query_indexes = torch.cumsum(key_values_lens, dim=0) + torch.arange(
    0, len(key_values_lens), device=key_values_lens.device, dtype=key_values_lens.dtype)
uppacked = list(packed_key_value_indexes.split(key_values_lens.tolist(), dim=0))
for i in range(len(uppacked)):
    uppacked[i] = uppacked[i] + i
packed_key_value_indexes = torch.cat(uppacked, dim=0)

qwen_model = model.language_model.model
cos, sin = qwen_model.rotary_emb(packed_text_embedding, packed_query_position_ids.unsqueeze(0))
cos, sin = cos.squeeze(0), sin.squeeze(0)
packed_query_position_embeddings = (cos, sin)

attn = qwen_model.layers[0].self_attn
normed = qwen_model.layers[0].input_layernorm(packed_text_embedding)

# Projections
packed_query_states = attn.q_proj(normed).view(-1, attn.num_heads, attn.head_dim)
packed_key_states = attn.k_proj(normed).view(-1, attn.num_key_value_heads, attn.head_dim)
packed_value_states = attn.v_proj(normed).view(-1, attn.num_key_value_heads, attn.head_dim)
packed_query_states = attn.q_norm(packed_query_states)
packed_key_states = attn.k_norm(packed_key_states)

packed_query_states, packed_key_states = _apply_rotary_pos_emb(
    packed_query_states, packed_key_states, cos, sin)

packed_query_states = packed_query_states.to(torch.bfloat16)
packed_key_states = packed_key_states.to(torch.bfloat16)
packed_value_states = packed_value_states.to(torch.bfloat16)

# Merge
past_key_states = past_key_values.key_cache[0]
past_value_states = past_key_values.value_cache[0]
seqlens = sum(query_lens) + sum(key_values_lens)
merged_key_states = past_key_states.new_zeros((seqlens, attn.num_key_value_heads, attn.head_dim))
merged_value_states = past_value_states.new_zeros((seqlens, attn.num_key_value_heads, attn.head_dim))
merged_key_states[packed_query_indexes] = packed_key_states
merged_key_states[packed_key_value_indexes] = past_key_states
merged_value_states[packed_query_indexes] = packed_value_states
merged_value_states[packed_key_value_indexes] = past_value_states

print(f"Q shape: {packed_query_states.shape} (num_heads={attn.num_heads})")
print(f"K shape: {merged_key_states.shape} (num_kv_heads={attn.num_key_value_heads})")
print(f"num_key_value_groups = {attn.num_key_value_groups}")

# Method 1: flash_attn (original) — should produce NaN
from flash_attn import flash_attn_varlen_func
key_values_lens_new = key_values_lens + query_lens
cu_seqlens_q = F.pad(torch.cumsum(query_lens, dim=0), (1, 0)).to(torch.int32)
cu_seqlens_k = F.pad(torch.cumsum(key_values_lens_new, dim=0), (1, 0)).to(torch.int32)

try:
    attn_out_flash = flash_attn_varlen_func(
        q=packed_query_states, k=merged_key_states, v=merged_value_states,
        cu_seqlens_q=cu_seqlens_q, cu_seqlens_k=cu_seqlens_k,
        max_seqlen_q=max(query_lens).item(), max_seqlen_k=max(key_values_lens_new).item(),
        causal=True,
    )
    print(f"flash_attn: nan={torch.isnan(attn_out_flash).any().item()} sum={attn_out_flash.float().sum().item():.4f}")
except Exception as e:
    print(f"flash_attn error: {e}")

# Method 2: Expand KV heads to match Q heads, then use F.scaled_dot_product_attention
# GQA: repeat_interleave KV heads
merged_key_expanded = merged_key_states.repeat_interleave(attn.num_key_value_groups, dim=1)  # (1380, 28, 128)
merged_value_expanded = merged_value_states.repeat_interleave(attn.num_key_value_groups, dim=1)
print(f"Expanded K shape: {merged_key_expanded.shape}")
print(f"Expanded V shape: {merged_value_expanded.shape}")

# Reshape to (batch=1, seq, heads, head_dim) for SDPA
q_4d = packed_query_states.unsqueeze(0)  # (1, 1, 28, 128)
k_4d = merged_key_expanded.unsqueeze(0)   # (1, 1380, 28, 128)
v_4d = merged_value_expanded.unsqueeze(0) # (1, 1380, 28, 128)

attn_out_sdpa = F.scaled_dot_product_attention(
    q_4d, k_4d, v_4d, is_causal=True,
)
print(f"SDPA: nan={torch.isnan(attn_out_sdpa).any().item()} sum={attn_out_sdpa.float().sum().item():.4f}")
print(f"SDPA shape: {attn_out_sdpa.shape}")

# Method 3: flash_attn without causal
try:
    attn_out_no_causal = flash_attn_varlen_func(
        q=packed_query_states, k=merged_key_states, v=merged_value_states,
        cu_seqlens_q=cu_seqlens_q, cu_seqlens_k=cu_seqlens_k,
        max_seqlen_q=max(query_lens).item(), max_seqlen_k=max(key_values_lens_new).item(),
        causal=False,
    )
    print(f"flash_attn (no causal): nan={torch.isnan(attn_out_no_causal).any().item()} sum={attn_out_no_causal.float().sum().item():.4f}")
except Exception as e:
    print(f"flash_attn (no causal) error: {e}")

# Method 4: flash_attn with expanded KV
try:
    attn_out_expanded = flash_attn_varlen_func(
        q=packed_query_states, k=merged_key_expanded, v=merged_value_expanded,
        cu_seqlens_q=cu_seqlens_q, cu_seqlens_k=cu_seqlens_k,
        max_seqlen_q=max(query_lens).item(), max_seqlen_k=max(key_values_lens_new).item(),
        causal=True,
    )
    print(f"flash_attn (expanded KV): nan={torch.isnan(attn_out_expanded).any().item()} sum={attn_out_expanded.float().sum().item():.4f}")
except Exception as e:
    print(f"flash_attn (expanded KV) error: {e}")

# Method 5: flash_attn with Q=8 (simulated by repeating the query 8 times)
packed_query_states_8 = packed_query_states.repeat(8, 1, 1)  # (8, 28, 128)
query_lens_8 = torch.tensor([8], dtype=torch.int, device=device)
packed_query_indexes_8 = torch.cumsum(key_values_lens, dim=0) + torch.arange(
    0, 1, device=device, dtype=key_values_lens.dtype)
cu_seqlens_q_8 = F.pad(torch.cumsum(query_lens_8, dim=0), (1, 0)).to(torch.int32)
try:
    attn_out_q8 = flash_attn_varlen_func(
        q=packed_query_states_8, k=merged_key_states, v=merged_value_states,
        cu_seqlens_q=cu_seqlens_q_8, cu_seqlens_k=cu_seqlens_k,
        max_seqlen_q=8, max_seqlen_k=max(key_values_lens_new).item(),
        causal=True,
    )
    print(f"flash_attn (Q=8): nan={torch.isnan(attn_out_q8).any().item()} sum={attn_out_q8.float().sum().item():.4f}")
    print(f"  first token: nan={torch.isnan(attn_out_q8[0]).any().item()}")
except Exception as e:
    print(f"flash_attn (Q=8) error: {e}")
