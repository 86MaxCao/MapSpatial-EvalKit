"""Test Bagel draw() — generate images from 3 prompts.

Prompts:
1. Draw a red arrow pointing from the bottom-left to the top-right of the image
2. Add a blue circle in the center of this image
3. Draw a green route line from the left side to the right side of the image

Uses the official diag_bagel_official.py approach: manual KV-cache + generate_image + VAE decode.
"""
import os, sys, time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
import numpy as np
from PIL import Image
from copy import deepcopy

MODEL_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/BAGEL-7B-MoT"
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.bagel.modeling_bagel import BagelForConditionalGeneration, NaiveCache, AutoEncoder
from mapspatial.vendor.bagel.configuration_bagel import BagelVaeConfig

print("Loading Bagel model...")
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

# Load VAE
vae_config = config.vae_config if config else BagelVaeConfig()
if isinstance(vae_config, dict):
    vae_config = BagelVaeConfig(**vae_config)
vae = AutoEncoder(vae_config).to("cuda").to(torch.bfloat16)
from safetensors.torch import load_file
vae_state = load_file(os.path.join(MODEL_PATH, "ae.safetensors"))
vae.load_state_dict(vae_state, strict=False)
vae.eval()
print("VAE loaded")

# Image transforms
class ImageTransform:
    def __init__(self, max_size, min_size, patch_size):
        self.max_size, self.min_size, self.patch_size = max_size, min_size, patch_size
    def _make_divisible(self, v, s):
        return max(s, int(round(v / s) * s))
    def resize(self, img):
        """Resize PIL image, return PIL image."""
        w, h = img.size
        scale = min(self.max_size / max(w, h), 1.0)
        scale = max(scale, self.min_size / min(w, h))
        new_w = self._make_divisible(round(w * scale), self.patch_size)
        new_h = self._make_divisible(round(h * scale), self.patch_size)
        return img.resize((new_w, new_h), Image.BICUBIC)
    def __call__(self, img):
        """Resize + convert to tensor."""
        img = self.resize(img)
        t = torch.tensor(np.array(img)).permute(2, 0, 1).float() / 255.0
        return (t - 0.5) / 0.5
    def resize_transform(self, img):
        """Return PIL image (resized only)."""
        return self.resize(img)

vit_transform = ImageTransform(980, 224, 14)
vae_transform = ImageTransform(1024, 512, 16)

def generate_image(model, vae, tokenizer, new_token_ids, prompt,
                   cfg_text_scale=4.0, cfg_img_scale=2.0,
                   num_timesteps=50, timestep_shift=3.0,
                   image_shapes=(1024, 1024)):
    """Generate image from text prompt using Bagel's generate_image method."""
    device = next(model.parameters()).device

    # Create a dummy condition image (gray 512x512 — matching official)
    test_image = Image.new("RGB", (512, 512), (200, 200, 200))
    img_input = vae_transform.resize_transform(test_image.convert("RGB"))
    img_shape = img_input.size[::-1]  # (H, W)

    # Build generation context — order matters for CFG!
    gen_ctx = {
        "kv_lens": [0], "ropes": [0],
        "past_key_values": NaiveCache(config.llm_config.num_hidden_layers),
    }
    cfg_img_ctx = deepcopy(gen_ctx)  # will get text-only (no image)

    # 1. Image prefill FIRST (VAE then ViT)
    if hasattr(model, "prepare_vae_images"):
        gen_input_vae, kv_lens, ropes = model.prepare_vae_images(
            curr_kvlens=gen_ctx["kv_lens"], curr_rope=gen_ctx["ropes"],
            images=[img_input], transforms=vae_transform, new_token_ids=new_token_ids,
        )
        for k, v in gen_input_vae.items():
            if torch.is_tensor(v): gen_input_vae[k] = v.to(device)
        with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
            gen_ctx["past_key_values"] = model.forward_cache_update_vae(
                vae, gen_ctx["past_key_values"], **gen_input_vae)
        gen_ctx["kv_lens"] = kv_lens
        gen_ctx["ropes"] = ropes

    gen_input_vit, kv_lens, ropes = model.prepare_vit_images(
        curr_kvlens=gen_ctx["kv_lens"], curr_rope=gen_ctx["ropes"],
        images=[img_input], transforms=vit_transform, new_token_ids=new_token_ids,
    )
    for k, v in gen_input_vit.items():
        if torch.is_tensor(v): gen_input_vit[k] = v.to(device)
    with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
        gen_ctx["past_key_values"] = model.forward_cache_update_vit(
            gen_ctx["past_key_values"], **gen_input_vit)
    gen_ctx["kv_lens"] = kv_lens
    gen_ctx["ropes"] = ropes

    # 2. Snapshot cfg_text_context = image-only (no text)
    cfg_text_ctx = deepcopy(gen_ctx)

    # 3. Text prefill on gen_context → image + text (full conditional)
    gen_input, gen_ctx["kv_lens"], gen_ctx["ropes"] = model.prepare_prompts(
        curr_kvlens=gen_ctx["kv_lens"], curr_rope=gen_ctx["ropes"],
        prompts=[prompt], tokenizer=tokenizer, new_token_ids=new_token_ids,
    )
    for k, v in gen_input.items():
        if torch.is_tensor(v): gen_input[k] = v.to(device)
    with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
        gen_ctx["past_key_values"] = model.forward_cache_update_text(
            gen_ctx["past_key_values"], **gen_input)

    # 4. Text prefill on cfg_img_context → text-only (no image)
    cfg_img_in, cfg_img_ctx["kv_lens"], cfg_img_ctx["ropes"] = model.prepare_prompts(
        curr_kvlens=cfg_img_ctx["kv_lens"], curr_rope=cfg_img_ctx["ropes"],
        prompts=[prompt], tokenizer=tokenizer, new_token_ids=new_token_ids,
    )
    for k, v in cfg_img_in.items():
        if torch.is_tensor(v): cfg_img_in[k] = v.to(device)
    with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
        cfg_img_ctx["past_key_values"] = model.forward_cache_update_text(
            cfg_img_ctx["past_key_values"], **cfg_img_in)

    # 5. Prepare latent + CFG inputs
    gen_input_latent = model.prepare_vae_latent(
        curr_kvlens=gen_ctx["kv_lens"], curr_rope=gen_ctx["ropes"],
        image_sizes=[img_shape], new_token_ids=new_token_ids,
    )
    cfg_text_input = model.prepare_vae_latent_cfg(
        curr_kvlens=cfg_text_ctx["kv_lens"], curr_rope=cfg_text_ctx["ropes"],
        image_sizes=[img_shape],
    )
    cfg_img_input = model.prepare_vae_latent_cfg(
        curr_kvlens=cfg_img_ctx["kv_lens"], curr_rope=cfg_img_ctx["ropes"],
        image_sizes=[img_shape],
    )

    for d in [gen_input_latent, cfg_text_input, cfg_img_input]:
        for k, v in d.items():
            if torch.is_tensor(v):
                d[k] = v.to(device)

    # 6. Generate
    with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
        unpacked_latent = model.generate_image(
            past_key_values=gen_ctx["past_key_values"],
            cfg_text_past_key_values=cfg_text_ctx["past_key_values"],
            cfg_img_past_key_values=cfg_img_ctx["past_key_values"],
            num_timesteps=num_timesteps,
            cfg_text_scale=cfg_text_scale,
            cfg_img_scale=cfg_img_scale,
            cfg_interval=[0.0, 1.0],
            cfg_renorm_min=0.0,
            cfg_renorm_type="text_channel",
            timestep_shift=timestep_shift,
            **gen_input_latent,
            cfg_text_packed_position_ids=cfg_text_input["cfg_packed_position_ids"],
            cfg_text_packed_query_indexes=cfg_text_input["cfg_packed_query_indexes"],
            cfg_text_key_values_lens=cfg_text_input["cfg_key_values_lens"],
            cfg_text_packed_key_value_indexes=cfg_text_input["cfg_packed_key_value_indexes"],
            cfg_img_packed_position_ids=cfg_img_input["cfg_packed_position_ids"],
            cfg_img_packed_query_indexes=cfg_img_input["cfg_packed_query_indexes"],
            cfg_img_key_values_lens=cfg_img_input["cfg_key_values_lens"],
            cfg_img_packed_key_value_indexes=cfg_img_input["cfg_packed_key_value_indexes"],
        )

    # 7. VAE decode
    H, W = img_shape
    h, w = H // model.latent_downsample, W // model.latent_downsample
    latent = unpacked_latent[0].reshape(
        1, h, w, model.latent_patch_size, model.latent_patch_size, model.latent_channel
    )
    latent = torch.einsum("nhwpqc->nchpwq", latent)
    latent = latent.reshape(1, model.latent_channel,
                            h * model.latent_patch_size,
                            w * model.latent_patch_size).to(torch.bfloat16)
    with torch.no_grad():
        decoded = vae.decode(latent)
    decoded = (decoded * 0.5 + 0.5).clamp(0, 1)[0].permute(1, 2, 0) * 255
    result = Image.fromarray(decoded.to(torch.uint8).cpu().numpy())
    return result

# Test 3 prompts
PROMPTS = [
    "Draw a red arrow pointing from the bottom-left to the top-right of the image",
    "Add a blue circle in the center of this image",
    "Draw a green route line from the left side to the right side of the image",
]

output_dir = os.path.join(PROJECT, "gen_results")
os.makedirs(output_dir, exist_ok=True)

for idx, prompt in enumerate(PROMPTS, 1):
    print(f"\n=== Prompt {idx}: {prompt[:50]}... ===")
    t0 = time.time()
    try:
        result = generate_image(model, vae, tokenizer, new_token_ids, prompt)
        save_path = os.path.join(output_dir, f"bagel_prompt{idx}.png")
        result.save(save_path)
        arr = np.array(result)
        print(f"  Saved: {save_path}")
        print(f"  Size: {result.size}, mean={arr.mean():.1f}, std={arr.std():.1f}")
        print(f"  Time: {time.time()-t0:.1f}s")
    except Exception as e:
        import traceback
        print(f"  FAILED: {e}")
        traceback.print_exc()

print("\n=== Done ===")
