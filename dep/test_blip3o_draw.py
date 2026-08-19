"""BLIP3o draw() — full 2-stage pipeline: LLM→DiT→UNet→VAE.

Stage 1: LLM → hidden states → DiT flow matching → conditioning latents [1, 1792, N]
Stage 2: UNet denoising with conditioning → VAE decode → image
"""
import os, sys, time

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch, numpy as np
from PIL import Image

PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

BLIP3O_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/BLIP3o-Model-8B"
DIFFUSION_PATH = os.path.join(BLIP3O_PATH, "diffusion-decoder")

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.blip3o.modeling_blip3o import BLIP3oQwenForCausalLM

print("Loading BLIP3o model...")
t0 = time.time()
model, config = load_model(BLIP3O_PATH, BLIP3oQwenForCausalLM, device="cuda", dtype="bfloat16")
tokenizer = load_tokenizer(BLIP3O_PATH)
print(f"  Loaded in {time.time()-t0:.1f}s")

# Load external UNet, VAE, scheduler from diffusion-decoder/
print("Loading diffusion pipeline components...")
from diffusers import AutoencoderKL, UNet2DConditionModel, EulerDiscreteScheduler

vae = AutoencoderKL.from_pretrained(DIFFUSION_PATH, subfolder="vae", torch_dtype=torch.bfloat16, variant="bf16").to("cuda")
unet = UNet2DConditionModel.from_pretrained(DIFFUSION_PATH, subfolder="unet", torch_dtype=torch.bfloat16, variant="bf16").to("cuda")
scheduler = EulerDiscreteScheduler.from_pretrained(DIFFUSION_PATH, subfolder="scheduler")
print(f"  UNet: {unet.config.in_channels}ch, cross_attn_dim={unet.config.cross_attention_dim}")
print(f"  VAE: {vae.config.latent_channels}ch, scale={vae.config.scaling_factor}")

# DiT scheduler (for stage 1)
from diffusers.schedulers import FlowMatchEulerDiscreteScheduler
try:
    dit_scheduler = FlowMatchEulerDiscreteScheduler.from_pretrained("Alpha-VLLM/Lumina-Next-SFT-diffusers", subfolder="scheduler")
except:
    dit_scheduler = FlowMatchEulerDiscreteScheduler(num_train_timesteps=1000, shift=3.0)

n_query = getattr(config, 'n_query', 64)
print(f"  n_query: {n_query}")

@torch.inference_mode()
def blip3o_draw(model, tokenizer, prompt, dit_scheduler, unet, vae, scheduler,
                n_query=64, dit_steps=30, unet_steps=50, guidance_scale=3.0, seed=42):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    device = next(model.parameters()).device
    param_dtype = next(model.parameters()).dtype

    # === Stage 1: LLM → DiT → conditioning latents ===
    # 1a. Text → embeddings + latent_queries
    text = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
    input_ids = tokenizer.encode(text, return_tensors="pt").to(device)
    img_token = torch.tensor([[151665]], device=device)  # [IMG]
    input_ids = torch.cat([input_ids, img_token], dim=1)

    text_embeds = model.get_input_embeddings()(input_ids)
    latent_queries = model.model.latent_queries.to(device).to(param_dtype)
    text_embeds = torch.cat([text_embeds, latent_queries], dim=1)

    # 1b. LLM forward
    with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
        hidden = model._llm_forward(text_embeds)
    img_hidden = hidden[:, -n_query:, :]  # [1, 64, 3584]
    print(f"    img_hidden: {img_hidden.shape} nan={torch.isnan(img_hidden).any().item()}")

    # 1c. DiT flow matching
    # DiT config: in_channels=1792, input_size=8, patch_size=1
    latent_channels = 1792
    latent_size = 8
    latents = torch.randn(1, latent_channels, latent_size, latent_size, device=device, dtype=param_dtype)

    # CFG: [uncond, cond]
    latents = latents.repeat(2, 1, 1, 1)
    img_input = torch.cat([torch.zeros_like(img_hidden), img_hidden], dim=0)

    # DiT flow matching — use official sigmas approach
    sigmas = np.linspace(1.0, 1 / dit_steps, dit_steps)
    dit_scheduler.set_timesteps(dit_steps, device=device, sigmas=sigmas)

    for i, t in enumerate(dit_scheduler.timesteps):
        t_batch = torch.tensor([t], device=device, dtype=param_dtype).expand(latents.shape[0])
        with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
            noise_pred = model.model.dit.model(latents, t_batch, img_input)
        noise_uncond, noise_cond = noise_pred.chunk(2, dim=0)
        noise_pred = noise_uncond + guidance_scale * (noise_cond - noise_uncond)
        latents = dit_scheduler.step(noise_pred, t, latents).prev_sample

    # Reshape: [1, 1792, 8, 8] → [1, 64, 1792] (N = 8*8 = 64)
    dit_output = latents[:1]  # conditional only
    conditioning = dit_output.flatten(2).transpose(1, 2)  # [1, 64, 1792]
    print(f"    DiT output: {dit_output.shape} → conditioning: {conditioning.shape}")

    # === Stage 2: UNet → VAE → image ===
    # 2a. Create VAE latents
    vae_latent_channels = vae.config.latent_channels  # 4
    vae_latent_size = unet.config.sample_size  # from UNet config
    print(f"    VAE latent: {vae_latent_channels}ch, size={vae_latent_size}")

    vae_latents = torch.randn(1, vae_latent_channels, vae_latent_size, vae_latent_size, device=device, dtype=param_dtype)

    # CFG for UNet
    vae_latents = vae_latents.repeat(2, 1, 1, 1)
    cond_input = torch.cat([torch.zeros(1, n_query, conditioning.shape[-1], device=device, dtype=param_dtype), conditioning], dim=0)

    scheduler.set_timesteps(unet_steps, device=device)
    for i, t in enumerate(scheduler.timesteps):
        latent_input = vae_latents
        t_batch = t.expand(latent_input.shape[0]).to(device)
        with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
            text_embeds = cond_input.mean(dim=1)  # [2, 1792] pooled
            time_ids = torch.tensor([[512, 512, 0, 0, 512, 512]], device=device, dtype=param_dtype).repeat(cond_input.shape[0], 1)
            noise_pred = unet(latent_input, t_batch, encoder_hidden_states=cond_input, added_cond_kwargs={"text_embeds": text_embeds, "time_ids": time_ids}).sample
        noise_uncond, noise_cond = noise_pred.chunk(2, dim=0)
        noise_pred = noise_uncond + guidance_scale * (noise_cond - noise_uncond)
        vae_latents = scheduler.step(noise_pred, t, vae_latents).prev_sample

    # 2b. VAE decode
    vae_latents = vae_latents[:1]  # conditional only
    scale = getattr(vae.config, 'scaling_factor', 1.0)
    vae_latents = vae_latents / scale
    image = vae.decode(vae_latents.to(param_dtype)).sample
    image = (image * 0.5 + 0.5).clamp(0, 1)
    img_np = (image[0].float().permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)
    return Image.fromarray(img_np)

PROMPTS = [
    "Draw a red arrow pointing from the bottom-left to the top-right of the image",
    "Add a blue circle in the center of this image",
    "Draw a green route line from the left side to the right side of the image",
]
output_dir = os.path.join(PROJECT, "gen_results")
os.makedirs(output_dir, exist_ok=True)

for idx, prompt in enumerate(PROMPTS, 1):
    print(f"\n=== BLIP3o Prompt {idx}: {prompt[:50]}... ===")
    t0 = time.time()
    try:
        result = blip3o_draw(model, tokenizer, prompt, dit_scheduler, unet, vae, scheduler, n_query=n_query)
        save_path = os.path.join(output_dir, f"blip3o_prompt{idx}.png")
        result.save(save_path)
        arr = np.array(result)
        print(f"  Saved: {save_path}, mean={arr.mean():.1f}, std={arr.std():.1f}, Time: {time.time()-t0:.1f}s")
    except Exception as e:
        import traceback; print(f"  FAILED: {e}"); traceback.print_exc()

print("\n=== Done ===")
