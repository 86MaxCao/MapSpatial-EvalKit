"""Test Janus, LatentUM, and BLIP3o draw() with all fixes."""
import os, sys, json, time, tempfile, shutil

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

# ===================== JANUS =====================
print("=" * 60)
print("Janus draw() — with attn_implementation=eager")
print("=" * 60)

JANUS_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/Janus-Pro-7B"
VEOMNI_CONFIG = {
    "model_type": "janus",
    "vision_config": {"width":1024,"layers":24,"heads":16,"patch_size":16,"image_size":384,"global_pool":"map","mlp_ratio":4.0,"class_token":False,"num_classes":0,"select_feature":"same","select_layer":-1,"ignore_head":True,"weight_init":"skip"},
    "gen_vision_config": {"codebook_size":16384,"codebook_embed_dim":8,"codebook_l2_norm":True,"codebook_show_usage":True,"commit_loss_beta":0.25,"entropy_loss_ratio":0.0,"encoder_ch_mult":[1,1,2,2,4],"decoder_ch_mult":[1,1,2,2,4],"z_channels":256,"dropout_p":0.0},
    "language_config": {"model_type":"llama","hidden_size":4096,"intermediate_size":11008,"num_hidden_layers":30,"num_attention_heads":32,"num_key_value_heads":32,"max_position_embeddings":16384,"vocab_size":102400,"torch_dtype":"bfloat16","rms_norm_eps":1e-6},
    "aligner_depth":2,"aligner_projector_type":"mlp_gelu","gen_aligner_depth":2,"gen_aligner_projector_type":"mlp_gelu","gen_head_embed":4096,"torch_dtype":"bfloat16",
}

tmp_dir = tempfile.mkdtemp(prefix="janus_")
with open(os.path.join(tmp_dir, "config.json"), "w") as f:
    json.dump(VEOMNI_CONFIG, f)
for fname in os.listdir(JANUS_PATH):
    src, dst = os.path.join(JANUS_PATH, fname), os.path.join(tmp_dir, fname)
    if fname != "config.json" and os.path.isfile(src) and not os.path.exists(dst):
        os.symlink(src, dst)

from mapspatial.vendor.janus.configuration_janus import JanusConfig
from mapspatial.vendor.janus.modeling_janus import Janus
from mapspatial.loader import init_empty_weights, _load_safetensors

# KEY FIX: set attn_implementation BEFORE model creation
config = JanusConfig.from_pretrained(tmp_dir)
config._attn_implementation = "eager"  # Critical: must be set before _from_config

print("Loading Janus with eager attention...")
t0 = time.time()
with init_empty_weights():
    model = Janus._from_config(config=config, attn_implementation="eager")
model = model.to_empty(device="cuda").to(torch.bfloat16)
state_dict = _load_safetensors(tmp_dir)
model.load_state_dict(state_dict, strict=False)
model.eval()
print(f"  Loaded in {time.time()-t0:.1f}s")
print(f"  lm._attn_impl: {model.language_model.config._attn_implementation}")

# Tokenizer with pre-tokenizer fix
from transformers import LlamaTokenizerFast
from tokenizers import Tokenizer as TokenizerBackend
tokenizer = LlamaTokenizerFast.from_pretrained(tmp_dir)
_tb = TokenizerBackend.from_file(os.path.join(tmp_dir, "tokenizer.json"))
tokenizer._tokenizer.pre_tokenizer = _tb.pre_tokenizer
tokenizer._tokenizer.decoder = _tb.decoder
pad_id = tokenizer.vocab.get("<｜▁pad▁｜>")

@torch.inference_mode()
def janus_generate(mmgpt, tokenizer, prompt, pad_id, cfg_weight=5, seed=42,
                   parallel_size=4, image_token_num=576, img_size=384, patch_size=16):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    device = next(mmgpt.parameters()).device
    input_ids = torch.LongTensor(tokenizer.encode(prompt))
    tokens = torch.zeros((parallel_size * 2, len(input_ids)), dtype=torch.int, device=device)
    for i in range(parallel_size * 2):
        tokens[i, :] = input_ids
        if i % 2 != 0:
            tokens[i, 1:-1] = pad_id
    inputs_embeds = mmgpt.language_model.get_input_embeddings()(tokens)
    generated_tokens = torch.zeros((parallel_size, image_token_num), dtype=torch.int, device=device)
    outputs = None
    for i in range(image_token_num):
        outputs = mmgpt.language_model.model(
            inputs_embeds=inputs_embeds, use_cache=True,
            past_key_values=outputs.past_key_values if outputs is not None else None,
        )
        logits = mmgpt.gen_head(outputs.last_hidden_state[:, -1, :])
        l_cond, l_uncond = logits[0::2, :], logits[1::2, :]
        logits = l_uncond + cfg_weight * (l_cond - l_uncond)
        probs = torch.softmax(logits, dim=-1)
        nxt = torch.multinomial(probs, num_samples=1)
        generated_tokens[:, i] = nxt.squeeze(dim=-1)
        nxt = torch.cat([nxt.unsqueeze(1), nxt.unsqueeze(1)], dim=1).view(-1)
        inputs_embeds = mmgpt.prepare_gen_img_embeds(nxt).unsqueeze(dim=1)
    dec = mmgpt.gen_vision_model.decode_code(
        generated_tokens.to(dtype=torch.int),
        shape=[parallel_size, 8, img_size // patch_size, img_size // patch_size],
    )
    dec = dec.to(torch.float32).cpu().numpy().transpose(0, 2, 3, 1)
    return np.clip((dec + 1) / 2 * 255, 0, 255).astype(np.uint8)[0]

for idx, prompt_text in enumerate(PROMPTS, 1):
    print(f"\n  Prompt {idx}: {prompt_text[:50]}...")
    t0 = time.time()
    prompt = f"User: {prompt_text}\n\nAssistant:<begin_of_image>"
    try:
        img_arr = janus_generate(model, tokenizer, prompt, pad_id, parallel_size=4, seed=42)
        result = Image.fromarray(img_arr)
        result.save(os.path.join(output_dir, f"janus_prompt{idx}.png"))
        print(f"    mean={img_arr.mean():.1f}, std={img_arr.std():.1f}, Time: {time.time()-t0:.1f}s")
    except Exception as e:
        print(f"    FAILED: {e}")

shutil.rmtree(tmp_dir, ignore_errors=True)
del model
torch.cuda.empty_cache()

# ===================== LatentUM =====================
print("\n" + "=" * 60)
print("LatentUM draw() — with external decoder")
print("=" * 60)

LATENTUM_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/LatentUM-Base"
DECODER_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/LatentUM-Decoder"
LATENTUM_OFFICIAL = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/LatentUM"

# Add official code to path for LatentUMDecoderModel
sys.path.insert(0, os.path.join(LATENTUM_OFFICIAL, "model"))

from mapspatial.loader import load_model, load_tokenizer
from mapspatial.vendor.latentum.modeling_latentum import LatentUMModel

print("Loading LatentUM model...")
t0 = time.time()
lat_model, lat_config = load_model(LATENTUM_PATH, LatentUMModel, device="cuda", dtype="bfloat16")
lat_tokenizer = load_tokenizer(LATENTUM_PATH)
print(f"  Loaded in {time.time()-t0:.1f}s")

# Load decoder from official code
print("Loading LatentUM decoder...")
try:
    from latentum.modeling_latentum import LatentUMDecoderModel
    decoder = LatentUMDecoderModel.from_pretrained(DECODER_PATH, torch_dtype=torch.bfloat16)
    decoder = decoder.to("cuda").eval()
    print("  Decoder loaded from official code")
except Exception as e:
    print(f"  Official decoder failed: {e}")
    try:
        from decoder.modeling_decoder import LatentUMDecoderModel as LatentDecoder
        decoder = LatentDecoder.from_pretrained(DECODER_PATH, torch_dtype=torch.bfloat16)
        decoder = decoder.to("cuda").eval()
        print("  Decoder loaded from decoder module")
    except Exception as e2:
        print(f"  All decoder attempts failed: {e2}")
        decoder = None

if decoder is not None:
    for idx, prompt in enumerate(PROMPTS, 1):
        print(f"\n  Prompt {idx}: {prompt[:50]}...")
        t0 = time.time()
        try:
            images = lat_model.generate_images(
                lat_tokenizer, [prompt],
                decoder=decoder,
                num_images_per_prompt=1,
                cfg_scale=3.0, temperature=0.9, top_k=50, top_p=0.95,
                seed=42, num_inference_steps=25, guidance_scale=1.0,
                show_progress=False,
            )
            if isinstance(images, list) and len(images) > 0:
                result = images[0]
            elif isinstance(images, Image.Image):
                result = images
            else:
                result = images[0] if hasattr(images, '__getitem__') else images
            save_path = os.path.join(output_dir, f"latentum_prompt{idx}.png")
            result.save(save_path)
            arr = np.array(result)
            print(f"    mean={arr.mean():.1f}, std={arr.std():.1f}, Time: {time.time()-t0:.1f}s")
        except Exception as e:
            import traceback
            print(f"    FAILED: {e}")
            traceback.print_exc()
else:
    print("  Skipping LatentUM draw (no decoder)")

del lat_model
if 'decoder' in dir():
    del decoder
torch.cuda.empty_cache()

# ===================== BLIP3o =====================
print("\n" + "=" * 60)
print("BLIP3o draw() — implement sample_images with internal DiT+VAE")
print("=" * 60)

BLIP3O_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/BLIP3o-Model-8B"

from mapspatial.vendor.blip3o.modeling_blip3o import BLIP3oQwenForCausalLM

print("Loading BLIP3o...")
t0 = time.time()
blip_model, blip_config = load_model(BLIP3O_PATH, BLIP3oQwenForCausalLM, device="cuda", dtype="bfloat16")
blip_tokenizer = load_tokenizer(BLIP3O_PATH)
print(f"  Loaded in {time.time()-t0:.1f}s")

# Check if model has DiT and VAE
print(f"  has model.dit: {hasattr(blip_model, 'model') and hasattr(blip_model.model, 'dit')}")
print(f"  has model.vae: {hasattr(blip_model, 'model') and hasattr(blip_model.model, 'vae')}")
print(f"  has model.latent_queries: {hasattr(blip_model.model, 'latent_queries')}")

# Check n_query
n_query = getattr(blip_config, 'n_query', 64)
print(f"  n_query: {n_query}")

# Check latent_queries
if hasattr(blip_model.model, 'latent_queries'):
    lq = blip_model.model.latent_queries
    print(f"  latent_queries shape: {lq.shape}")

try:
    from diffusers.schedulers import FlowMatchEulerDiscreteScheduler
    print("  FlowMatchEulerDiscreteScheduler available")
    scheduler = FlowMatchEulerDiscreteScheduler.from_pretrained(
        "Alpha-VLLM/Lumina-Next-SFT-diffusers", subfolder="scheduler"
    )
except Exception as e:
    print(f"  Scheduler from Alpha-VLLM failed: {e}")
    try:
        from diffusers.schedulers import FlowMatchEulerDiscreteScheduler as FMEDS
        scheduler = FMEDS(num_train_timesteps=1000, shift=3.0)
        print("  Using default scheduler")
    except Exception as e2:
        print(f"  Scheduler unavailable: {e2}")
        scheduler = None

if scheduler is not None:
    @torch.inference_mode()
    def blip3o_generate(model, tokenizer, prompt, scheduler, n_query=64,
                         num_steps=30, guidance_scale=3.0, seed=42):
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        device = next(model.parameters()).device

        # 1. Text -> embeddings + latent_queries
        text = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        input_ids = tokenizer.encode(text, return_tensors="pt").to(device)
        # Append image token
        img_token = torch.tensor([[151665]], device=device)  # [IMG]
        input_ids = torch.cat([input_ids, img_token], dim=1)

        text_embeds = model.get_input_embeddings()(input_ids)
        latent_queries = model.model.latent_queries.to(device).to(text_embeds.dtype)
        text_embeds = torch.cat([text_embeds, latent_queries], dim=1)

        # 2. LLM forward to get hidden states
        # M-RoPE position_ids
        seq_len = text_embeds.shape[1]
        pos = torch.arange(seq_len, device=device)
        position_ids = pos.view(1, 1, -1).expand(3, 1, -1)

        outputs = model.model(
            inputs_embeds=text_embeds,
            attention_mask=torch.ones(1, seq_len, device=device),
            position_ids=position_ids,
            output_hidden_states=True,
            return_dict=True,
        )
        hidden_states = outputs.hidden_states[-1][:, -n_query:, :]
        print(f"    hidden_states: {hidden_states.shape}")

        # 3. Flow matching denoising with DiT
        # Determine latent shape from VAE config
        latent_channels = getattr(blip_config, 'vae_latent_channels', 16)
        latent_size = 16  # default
        latents = torch.randn(1, latent_channels, latent_size, latent_size, device=device, dtype=torch.bfloat16)

        # CFG: duplicate for conditional + unconditional
        if guidance_scale > 1:
            latents = torch.cat([latents, latents], dim=0)
            hidden_input = torch.cat([hidden_states, torch.zeros_like(hidden_states)], dim=0)
        else:
            hidden_input = hidden_states

        scheduler.set_timesteps(num_steps, device=device)
        for i, t in enumerate(scheduler.timesteps):
            latent_model_input = scheduler.scale_model_input(latents, t)
            t_expanded = t.expand(latent_model_input.shape[0]).to(device)

            # DiT forward
            noise_pred = model.model.dit(
                x=latent_model_input,
                timestep=t_expanded,
                z_latents=hidden_input,
            )

            # CFG
            if guidance_scale > 1:
                noise_pred_cond, noise_pred_uncond = noise_pred.chunk(2, dim=0)
                noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_cond - noise_pred_uncond)

            latents = scheduler.step(noise_pred, t, latents).prev_sample

        # 4. VAE decode
        # Try model's internal VAE
        if hasattr(model.model, 'vae'):
            vae = model.model.vae
            # Check if it's a diffusers VAE or custom
            if hasattr(vae, 'decode'):
                try:
                    # diffusers VAE: decode(latents).sample
                    latents = latents / getattr(vae.config, 'scaling_factor', 1.0)
                    latents = latents + getattr(vae.config, 'shift_factor', 0.0)
                    image = vae.decode(latents).sample
                except:
                    # Custom VAE
                    image = vae.decode(latents)
            else:
                print("    VAE has no decode method")
                return None
        else:
            print("    No VAE available")
            return None

        # Denormalize
        image = (image * 0.5 + 0.5).clamp(0, 1)
        img_np = (image[0].float().permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)
        return Image.fromarray(img_np)

    for idx, prompt in enumerate(PROMPTS, 1):
        print(f"\n  Prompt {idx}: {prompt[:50]}...")
        t0 = time.time()
        try:
            result = blip3o_generate(blip_model, blip_tokenizer, prompt, scheduler, n_query=n_query)
            if result is not None:
                save_path = os.path.join(output_dir, f"blip3o_prompt{idx}.png")
                result.save(save_path)
                arr = np.array(result)
                print(f"    mean={arr.mean():.1f}, std={arr.std():.1f}, Time: {time.time()-t0:.1f}s")
            else:
                print(f"    No image generated")
        except Exception as e:
            import traceback
            print(f"    FAILED: {e}")
            traceback.print_exc()

del blip_model
torch.cuda.empty_cache()
print("\n=== All done ===")
