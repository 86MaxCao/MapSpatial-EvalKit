"""Test U1 and Janus draw() — generate images from 3 prompts."""
import os, sys, time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
import numpy as np
from PIL import Image

PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

PROMPTS = [
    "Draw a red arrow pointing from the bottom-left to the top-right of the image",
    "Add a blue circle in the center of this image",
    "Draw a green route line from the left side to the right side of the image",
]
output_dir = os.path.join(PROJECT, "gen_results")
os.makedirs(output_dir, exist_ok=True)

# ===================== U1 =====================
print("=" * 60)
print("U1 draw test")
print("=" * 60)

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.neo_chat.modeling_neo_chat import NEOChatModel

U1_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/SenseNova-U1-8B-MoT"
print("Loading U1...")
t0 = time.time()
u1_model, u1_config = load_model(U1_PATH, NEOChatModel, device="cuda", dtype="bfloat16")
u1_tokenizer = load_tokenizer(U1_PATH)
print(f"Loaded in {time.time()-t0:.1f}s")

for idx, prompt in enumerate(PROMPTS, 1):
    print(f"\n--- U1 Prompt {idx}: {prompt[:50]}... ---")
    t0 = time.time()
    try:
        # U1 uses model.it2i_generate()
        # For text-to-image, pass None for images
        output = u1_model.it2i_generate(
            u1_tokenizer,
            prompt,
            None,  # no condition images for t2i
            image_size=(256, 256),
            cfg_scale=4.0,
            img_cfg_scale=1.0,
            num_steps=50,
            batch_size=1,
            seed=42,
        )
        # Output is [B, C, H, W] in [-1, 1] range
        if isinstance(output, torch.Tensor):
            img = output * 0.5 + 0.5
            img = img.clamp(0, 1)
            img_np = (img[0].float().permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)
            result = Image.fromarray(img_np)
        elif isinstance(output, Image.Image):
            result = output
        else:
            print(f"  Unexpected output type: {type(output)}")
            continue

        save_path = os.path.join(output_dir, f"u1_prompt{idx}.png")
        result.save(save_path)
        arr = np.array(result)
        print(f"  Saved: {save_path}")
        print(f"  Size: {result.size}, mean={arr.mean():.1f}, std={arr.std():.1f}")
        print(f"  Time: {time.time()-t0:.1f}s")
    except Exception as e:
        import traceback
        print(f"  FAILED: {e}")
        traceback.print_exc()

del u1_model
torch.cuda.empty_cache()

# ===================== Janus =====================
print("\n" + "=" * 60)
print("Janus draw test")
print("=" * 60)

from mapspatial.vendor.janus.modeling_janus import Janus

JANUS_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/Janus-Pro-7B"
print("Loading Janus...")
t0 = time.time()
janus_model, janus_config = load_model(JANUS_PATH, Janus, device="cuda", dtype="bfloat16")
janus_tokenizer = load_tokenizer(JANUS_PATH)
print(f"Loaded in {time.time()-t0:.1f}s")

@torch.inference_mode()
def janus_generate(mmgpt, tokenizer, prompt, cfg_weight=5, seed=42,
                   image_token_num=576, img_size=384, patch_size=16):
    """Janus image generation via AR loop with CFG."""
    torch.manual_seed(seed)
    device = next(mmgpt.parameters()).device

    # Build prompt
    text = f"User: {prompt}\n\nAssistant:<begin_of_image>"
    input_ids = tokenizer.encode(text)
    tokens = torch.zeros((2, len(input_ids)), dtype=torch.int, device=device)
    tokens[0, :] = torch.tensor(input_ids, device=device)  # conditional
    tokens[1, :] = torch.tensor(input_ids, device=device)   # unconditional
    tokens[1, 1:-1] = tokenizer.pad_token_id if tokenizer.pad_token_id else 0  # pad middle

    inputs_embeds = mmgpt.language_model.get_input_embeddings()(tokens)
    generated_tokens = torch.zeros((1, image_token_num), dtype=torch.int, device=device)
    past_key_values = None

    for i in range(image_token_num):
        outputs = mmgpt.language_model.model(
            inputs_embeds=inputs_embeds, use_cache=True,
            past_key_values=past_key_values,
        )
        past_key_values = outputs.past_key_values
        hidden_states = outputs.last_hidden_state

        logits = mmgpt.gen_head(hidden_states[:, -1, :])
        logit_cond = logits[0:1, :]
        logit_uncond = logits[1:2, :]
        logits_final = logit_uncond + cfg_weight * (logit_cond - logit_uncond)
        probs = torch.softmax(logits_final, dim=-1)
        next_token = torch.multinomial(probs, num_samples=1)
        generated_tokens[:, i] = next_token.squeeze(dim=-1)

        # Feed back
        next_token_batch = torch.cat([next_token, next_token], dim=0).view(-1)
        img_embeds = mmgpt.prepare_gen_img_embeds(next_token_batch)
        inputs_embeds = img_embeds.unsqueeze(dim=1)

        if i == 0:
            print(f"  First token: {next_token.item()}")

    # VQ decode
    dec = mmgpt.gen_vision_model.decode_code(
        generated_tokens.to(dtype=torch.int),
        shape=[1, 8, img_size // patch_size, img_size // patch_size],
    )
    dec = dec.to(torch.float32).cpu().numpy().transpose(0, 2, 3, 1)
    dec = np.clip((dec + 1) / 2 * 255, 0, 255).astype(np.uint8)
    return Image.fromarray(dec[0])

for idx, prompt in enumerate(PROMPTS, 1):
    print(f"\n--- Janus Prompt {idx}: {prompt[:50]}... ---")
    t0 = time.time()
    try:
        result = janus_generate(janus_model, janus_tokenizer, prompt)
        save_path = os.path.join(output_dir, f"janus_prompt{idx}.png")
        result.save(save_path)
        arr = np.array(result)
        print(f"  Saved: {save_path}")
        print(f"  Size: {result.size}, mean={arr.mean():.1f}, std={arr.std():.1f}")
        print(f"  Time: {time.time()-t0:.1f}s")
    except Exception as e:
        import traceback
        print(f"  FAILED: {e}")
        traceback.print_exc()

del janus_model
torch.cuda.empty_cache()
print("\n=== Done ===")
