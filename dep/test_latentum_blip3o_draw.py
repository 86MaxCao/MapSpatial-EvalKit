"""Fix LatentUM and BLIP3o draw — Janus pending (environmental issue)."""
import os, sys, time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch, numpy as np
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

# ===================== LatentUM =====================
print("=" * 60)
print("LatentUM draw()")
print("=" * 60)

LATENTUM_OFFICIAL = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/LatentUM"
sys.path.insert(0, LATENTUM_OFFICIAL)  # for 'from model.decoder.reconstruct import ...'

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.latentum.modeling_latentum import LatentUMModel

LATENTUM_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/LatentUM-Base"
DECODER_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/LatentUM-Decoder"

print("Loading LatentUM model...")
t0 = time.time()
lat_model, _ = load_model(LATENTUM_PATH, LatentUMModel, device="cuda", dtype="bfloat16")
lat_tokenizer = load_tokenizer(LATENTUM_PATH)
print(f"  Loaded in {time.time()-t0:.1f}s")

print("Loading decoder...")
try:
    from model.latentum.modeling_latentum import LatentUMDecoderModel
    decoder = LatentUMDecoderModel.from_pretrained(DECODER_PATH, dtype=torch.bfloat16)
    decoder = decoder.to("cuda").eval()
    print("  Decoder loaded!")
except Exception as e:
    print(f"  Failed: {e}")
    import traceback; traceback.print_exc()
    decoder = None

if decoder:
    for idx, prompt in enumerate(PROMPTS, 1):
        print(f"\n  Prompt {idx}: {prompt[:50]}...")
        t0 = time.time()
        try:
            images = lat_model.generate_images(
                lat_tokenizer, [prompt], decoder=decoder,
                num_images_per_prompt=1, cfg_scale=3.0,
                temperature=0.9, top_k=50, top_p=0.95,
                seed=42, num_inference_steps=25, guidance_scale=1.0,
                show_progress=False,
            )
            result = images[0] if isinstance(images, list) else images
            save_path = os.path.join(output_dir, f"latentum_prompt{idx}.png")
            result.save(save_path)
            arr = np.array(result)
            print(f"    mean={arr.mean():.1f}, std={arr.std():.1f}, Time: {time.time()-t0:.1f}s")
        except Exception as e:
            import traceback; print(f"    FAILED: {e}"); traceback.print_exc()

del lat_model, decoder
torch.cuda.empty_cache()

# ===================== BLIP3o =====================
print("\n" + "=" * 60)
print("BLIP3o draw()")
print("=" * 60)

from mapspatial.vendor.blip3o.modeling_blip3o import BLIP3oQwenForCausalLM

BLIP3O_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/BLIP3o-Model-8B"
print("Loading BLIP3o...")
t0 = time.time()
blip_model, blip_config = load_model(BLIP3O_PATH, BLIP3oQwenForCausalLM, device="cuda", dtype="bfloat16")
blip_tokenizer = load_tokenizer(BLIP3O_PATH)
print(f"  Loaded in {time.time()-t0:.1f}s")

# Check components
has_dit = hasattr(blip_model.model, 'dit')
has_vae = hasattr(blip_model.model, 'vae')
has_lq = hasattr(blip_model.model, 'latent_queries')
n_query = getattr(blip_config, 'n_query', 64)
print(f"  dit={has_dit} vae={has_vae} latent_queries={has_lq} n_query={n_query}")
if has_lq:
    print(f"  latent_queries shape: {blip_model.model.latent_queries.shape}")

# Scheduler
from diffusers.schedulers import FlowMatchEulerDiscreteScheduler
try:
    scheduler = FlowMatchEulerDiscreteScheduler.from_pretrained("Alpha-VLLM/Lumina-Next-SFT-diffusers", subfolder="scheduler")
    print("  Scheduler loaded from Alpha-VLLM")
except:
    scheduler = FlowMatchEulerDiscreteScheduler(num_train_timesteps=1000, shift=3.0)
    print("  Using default scheduler")

@torch.inference_mode()
def blip3o_draw(model, tokenizer, prompt, scheduler, n_query=64,
                num_steps=30, guidance_scale=3.0, seed=42):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    device = next(model.parameters()).device
    param_dtype = next(model.parameters()).dtype

    # 1. Text -> embeddings + latent_queries
    text = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
    input_ids = tokenizer.encode(text, return_tensors="pt").to(device)
    img_token = torch.tensor([[151665]], device=device)  # [IMG]
    input_ids = torch.cat([input_ids, img_token], dim=1)

    text_embeds = model.get_input_embeddings()(input_ids)
    latent_queries = model.model.latent_queries.to(device).to(param_dtype)
    text_embeds = torch.cat([text_embeds, latent_queries], dim=1)
    seq_len = text_embeds.shape[1]

    # 2. LLM forward — use _llm_forward (not model.model() which has no forward)
    with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
        hidden = model._llm_forward(text_embeds)
    # Extract last n_query tokens as image conditioning
    img_hidden = hidden[:, -n_query:, :]
    print(f"    img_hidden: {img_hidden.shape} nan={torch.isnan(img_hidden).any().item()}")

    # 3. Flow matching denoising with DiT
    latent_channels = getattr(blip_config, 'vae_latent_channels', 16)
    latent_size = 16  # 448/28 = 16
    latents = torch.randn(1, latent_channels, latent_size, latent_size, device=device, dtype=param_dtype)

    # CFG setup
    latents = latents.repeat(2, 1, 1, 1)
    img_input = torch.cat([img_hidden, torch.zeros_like(img_hidden)], dim=0)

    scheduler.set_timesteps(num_steps, device=device)
    for i, t in enumerate(scheduler.timesteps):
        # Flow matching: no scale_model_input needed
        t_expanded = t.expand(latents.shape[0]).to(device)

        with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
            noise_pred = model.model.dit.model(
                latents,
                t_expanded,
                img_input,
            )

        noise_cond, noise_uncond = noise_pred.chunk(2, dim=0)
        noise_pred = noise_uncond + guidance_scale * (noise_cond - noise_uncond)
        latents = scheduler.step(noise_pred, t, latents).prev_sample

    # 4. VAE decode
    latents = latents[:1]  # only conditional
    if hasattr(model.model.vae, 'decode'):
        try:
            # diffusers-style VAE
            scale = getattr(model.model.vae.config, 'scaling_factor', 1.0) if hasattr(model.model.vae, 'config') else 1.0
            shift = getattr(model.model.vae.config, 'shift_factor', 0.0) if hasattr(model.model.vae, 'config') else 0.0
            latents = latents / scale + shift
            image = model.model.vae.decode(latents.to(param_dtype)).sample
        except:
            image = model.model.vae.decode(latents.to(param_dtype))
    else:
        print("    No VAE decode method!")
        return None

    image = (image * 0.5 + 0.5).clamp(0, 1)
    img_np = (image[0].float().permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)
    return Image.fromarray(img_np)

for idx, prompt in enumerate(PROMPTS, 1):
    print(f"\n  Prompt {idx}: {prompt[:50]}...")
    t0 = time.time()
    try:
        result = blip3o_draw(blip_model, blip_tokenizer, prompt, scheduler, n_query=n_query)
        if result:
            save_path = os.path.join(output_dir, f"blip3o_prompt{idx}.png")
            result.save(save_path)
            arr = np.array(result)
            print(f"    mean={arr.mean():.1f}, std={arr.std():.1f}, Time: {time.time()-t0:.1f}s")
        else:
            print("    No image")
    except Exception as e:
        import traceback; print(f"    FAILED: {e}"); traceback.print_exc()

del blip_model
torch.cuda.empty_cache()
print("\n=== Done ===")
