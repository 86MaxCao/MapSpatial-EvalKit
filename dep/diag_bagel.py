"""Diagnostic: Bagel understand — find where the model breaks.

Tests:
1. Token IDs check
2. Weight loading check (count matched/missing/unexpected)
3. Text-only chat (should produce text)
4. Image chat step-by-step:
   a. ViT forward output
   b. Connector output
   c. KV cache after ViT
   d. KV cache after text
   e. First token logits
"""
import os, sys, json, time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
import numpy as np
from PIL import Image

# Paths
MODEL_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/BAGEL-7B-MoT"
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

# 1. Load model via our loader
print("=" * 60)
print("Step 1: Load model")
print("=" * 60)

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.bagel.modeling_bagel import BagelForConditionalGeneration, NaiveCache

t0 = time.time()
model, config = load_model(MODEL_PATH, BagelForConditionalGeneration, device="cuda", dtype="bfloat16")
tokenizer = load_tokenizer(MODEL_PATH)
print(f"Loaded in {time.time()-t0:.1f}s")
print(f"Model dtype: {next(model.parameters()).dtype}")
print(f"Model device: {next(model.parameters()).device}")
print(f"use_moe: {model.use_moe}")

# 2. Token IDs
print("\n" + "=" * 60)
print("Step 2: Token IDs")
print("=" * 60)

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
print(f"new_token_ids: {new_token_ids}")
print(f"Token 0 = '{tokenizer.decode([0])}'")
print(f"Token 0 repr = {repr(tokenizer.decode([0]))}")

# 3. Weight check
print("\n" + "=" * 60)
print("Step 3: Weight check")
print("=" * 60)

model_params = dict(model.named_parameters())
print(f"Model params: {len(model_params)}")

# Check some key params are non-zero
for name in ["language_model.model.embed_tokens.weight",
             "language_model.lm_head.weight",
             "vit_model.vision_model.embeddings.patch_embedding.weight",
             "connector.fc1.weight",
             "connector.fc2.weight"]:
    if name in model_params:
        p = model_params[name]
        print(f"  {name}: shape={p.shape} dtype={p.dtype} mean={p.float().mean().item():.6f} std={p.float().std().item():.6f} has_nan={torch.isnan(p).any().item()}")
    else:
        print(f"  {name}: NOT FOUND")

# 4. Image transform
print("\n" + "=" * 60)
print("Step 4: Image transform")
print("=" * 60)

class _ImageTransform:
    def __init__(self, max_size, min_size, patch_size):
        self.max_size = max_size
        self.min_size = min_size
        self.patch_size = patch_size
    def _make_divisible(self, value, stride):
        return max(stride, int(round(value / stride) * stride))
    def __call__(self, img):
        w, h = img.size
        scale = min(self.max_size / max(w, h), 1.0)
        scale = max(scale, self.min_size / min(w, h))
        new_w = self._make_divisible(round(w * scale), self.patch_size)
        new_h = self._make_divisible(round(h * scale), self.patch_size)
        img = img.resize((new_w, new_h), Image.BICUBIC)
        tensor = torch.tensor(np.array(img)).permute(2, 0, 1).float() / 255.0
        tensor = (tensor - 0.5) / 0.5
        return tensor

def _vae_resize(img, max_size=1024, min_size=512, stride=16):
    w, h = img.size
    scale = min(max_size / max(w, h), 1.0)
    scale = max(scale, min_size / min(w, h))
    new_w = max(stride, int(round(round(w * scale) / stride) * stride))
    new_h = max(stride, int(round(round(h * scale) / stride) * stride))
    return img.resize((new_w, new_h), Image.BICUBIC)

vit_patch_size = getattr(config.vit_config, "patch_size", 14)
image_transform = _ImageTransform(980, 224, vit_patch_size)
print(f"ViT transform: max=980, min=224, patch={vit_patch_size}")
print(f"vit_max_num_patch_per_side: {model.vit_max_num_patch_per_side}")

# 5. Text-only chat
print("\n" + "=" * 60)
print("Step 5: Text-only chat (no image)")
print("=" * 60)

prompt_text_only = "What is 2+2? Answer with just the number."
with torch.no_grad():
    response = model.chat(
        tokenizer=tokenizer,
        new_token_ids=new_token_ids,
        image_transform=image_transform,
        images=[],
        prompt=prompt_text_only,
        max_length=512,
    )
print(f"Text-only response: '{response}'")

# 6. Image chat step-by-step
print("\n" + "=" * 60)
print("Step 6: Image chat step-by-step")
print("=" * 60)

# Create a test image
test_image = Image.new("RGB", (512, 512), (200, 200, 200))
img = test_image.convert("RGB")
img = _vae_resize(img)
print(f"Image after vae_resize: {img.size}")

images = [img]
device = next(model.parameters()).device

# Step 6a: prepare_vit_images + forward_cache_update_vit
print("\n--- Step 6a: ViT forward ---")
past_key_values = NaiveCache(config.llm_config.num_hidden_layers)
newlens = [0]
new_rope = [0]

generation_input, newlens, new_rope = model.prepare_vit_images(
    curr_kvlens=newlens,
    curr_rope=new_rope,
    images=images,
    transforms=image_transform,
    new_token_ids=new_token_ids,
)
for k, v in generation_input.items():
    if torch.is_tensor(v):
        generation_input[k] = v.to(device)

print(f"  packed_vit_tokens: shape={generation_input['packed_vit_tokens'].shape} dtype={generation_input['packed_vit_tokens'].dtype}")
print(f"  packed_vit_tokens sum={generation_input['packed_vit_tokens'].sum().item():.4f}")

with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
    past_key_values = model.forward_cache_update_vit(past_key_values, **generation_input)

# Check KV cache
k0 = past_key_values.key_cache[0]
print(f"  KV cache layer 0: shape={k0.shape} dtype={k0.dtype}")
print(f"  KV cache sum={k0.float().sum().item():.4f} has_nan={torch.isnan(k0).any().item()}")
print(f"  KV cache mean={k0.float().mean().item():.6f} std={k0.float().std().item():.6f}")

# Step 6b: prepare_prompts + forward_cache_update_text
print("\n--- Step 6b: Text forward ---")
prompt = "What color is this image? Answer briefly."
generation_input, newlens, new_rope = model.prepare_prompts(
    curr_kvlens=newlens,
    curr_rope=new_rope,
    prompts=[prompt],
    tokenizer=tokenizer,
    new_token_ids=new_token_ids,
)
for k, v in generation_input.items():
    if torch.is_tensor(v):
        generation_input[k] = v.to(device)

print(f"  Text tokens: {generation_input['packed_text_ids'].tolist()}")
print(f"  Text decoded: '{tokenizer.decode(generation_input['packed_text_ids'])}'")

with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
    past_key_values = model.forward_cache_update_text(past_key_values, **generation_input)

k0 = past_key_values.key_cache[0]
print(f"  KV cache after text: shape={k0.shape} sum={k0.float().sum().item():.4f}")

# Step 6c: prepare_start_tokens + generate_text (first 5 tokens)
print("\n--- Step 6c: Generate text ---")
generation_input = model.prepare_start_tokens(newlens, new_rope, new_token_ids)
for k, v in generation_input.items():
    if torch.is_tensor(v):
        generation_input[k] = v.to(device)

# Manually run first 3 generation steps to inspect logits
curr_tokens = generation_input["packed_start_tokens"]
packed_key_value_indexes = generation_input["packed_key_value_indexes"]
key_values_lens = generation_input["key_values_lens"]
packed_query_position_ids = generation_input["packed_query_position_ids"]

for step in range(5):
    packed_text_embedding = model.language_model.model.embed_tokens(curr_tokens)
    query_lens = torch.ones_like(curr_tokens)
    packed_query_indexes = torch.cumsum(key_values_lens, dim=0) + torch.arange(
        0, len(key_values_lens), device=key_values_lens.device, dtype=key_values_lens.dtype,
    )

    uppacked = list(packed_key_value_indexes.split(key_values_lens.tolist(), dim=0))
    for i in range(len(uppacked)):
        uppacked[i] = uppacked[i] + i
    packed_key_value_indexes = torch.cat(uppacked, dim=0)

    extra_inputs = {"mode": "und"} if model.use_moe else {}

    with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
        output = model.language_model.forward_inference(
            packed_query_sequence=packed_text_embedding,
            query_lens=query_lens,
            packed_query_position_ids=packed_query_position_ids,
            packed_query_indexes=packed_query_indexes,
            past_key_values=past_key_values,
            key_values_lens=key_values_lens,
            packed_key_value_indexes=packed_key_value_indexes,
            update_past_key_values=True,
            is_causal=True,
            **extra_inputs,
        )
    past_key_values = output.past_key_values
    pred_logits = model.language_model.lm_head(output.packed_query_sequence)

    print(f"  Step {step}: logits shape={pred_logits.shape} dtype={pred_logits.dtype}")
    print(f"    logits[0] top5: {pred_logits[0].topk(5).indices.tolist()}")
    print(f"    logits[0] top5 values: {[f'{v:.4f}' for v in pred_logits[0].topk(5).values.tolist()]}")
    print(f"    logits[0] min={pred_logits[0].min().item():.4f} max={pred_logits[0].max().item():.4f}")
    print(f"    logits[0] token 0 logit={pred_logits[0, 0].item():.4f}")
    print(f"    argmax token={pred_logits.argmax(dim=-1)[0].item()} = '{tokenizer.decode([pred_logits.argmax(dim=-1)[0].item()])}'")

    curr_tokens = torch.argmax(pred_logits, dim=-1)

    uppacked = list(packed_key_value_indexes.split(key_values_lens.tolist(), dim=0))
    for i in range(len(uppacked)):
        uppacked[i] = torch.cat(
            [uppacked[i], torch.tensor([uppacked[i][-1] + 1], device=uppacked[i].device)], dim=0
        )
    packed_key_value_indexes = torch.cat(uppacked, dim=0)
    key_values_lens = key_values_lens + 1
    packed_query_position_ids = packed_query_position_ids + 1

print("\n" + "=" * 60)
print("Diagnostic complete")
print("=" * 60)
