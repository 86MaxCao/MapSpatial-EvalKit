#!/usr/bin/env python
"""Unified test script for the eight paper UMMs (understand + draw).

Models: Bagel, ThinkMorph, BLIP3o, U1 (SenseNova-U1), LatentUM, Janus,
         Show-o2, JoyAI-Image

Usage:
  python test_all_models.py --model bagel --phase understand
  python test_all_models.py --model showo2 --phase draw
  python test_all_models.py --model joyai --phase both
  python test_all_models.py --model all --phase both --gpu 0
"""

import os, sys, time, argparse, importlib.util, tempfile, json, shutil

# ── Env setup (must be before torch import) ────────────────────────────
GPU = sys.argv[sys.argv.index("--gpu") + 1] if "--gpu" in sys.argv else "1"
os.environ.setdefault("CUDA_VISIBLE_DEVICES", GPU)
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
import numpy as np
from PIL import Image
from copy import deepcopy

# ── Paths ──────────────────────────────────────────────────────────────
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
CKPT_BASE = "/mnt/nas-tbt/tbt/checkpoint/hf_cache"
VEOMNI_DIR = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/VeOmni"
BLIP3O_MAIN = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/BLIP3o_main"
LATENTUM_OFFICIAL = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/LatentUM"
OUTPUT_DIR = os.path.join(PROJECT, "gen_results")

sys.path.insert(0, PROJECT)

# ── Constants ──────────────────────────────────────────────────────────
UNDERSTAND_PROMPTS = [
    "What is 2+2? Answer with just the number.",
    "Describe the sky in one sentence.",
    "What color is the grass?",
]
DRAW_PROMPTS = [
    "Draw a red arrow pointing from the bottom-left to the top-right of the image",
    "Add a blue circle in the center of this image",
    "Draw a green route line from the left side to the right side of the image",
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Common utilities ───────────────────────────────────────────────────

def save_image(img_arr_or_pil, name):
    """Save image to gen_results/{name}.png"""
    if isinstance(img_arr_or_pil, np.ndarray):
        pil = Image.fromarray(img_arr_or_pil)
    else:
        pil = img_arr_or_pil
    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    pil.save(path)
    arr = np.array(pil)
    print(f"  Saved: {path}, mean={arr.mean():.1f}, std={arr.std():.1f}")
    return path


def gpu_cleanup():
    """Free GPU memory between models."""
    torch.cuda.empty_cache()


class ImageTransform:
    """ViT image transform: resize + normalize to [-1, 1]."""
    def __init__(self, max_size, min_size, patch_size):
        self.max_size, self.min_size, self.patch_size = max_size, min_size, patch_size
    def _make_divisible(self, v, s):
        return max(s, int(round(v / s) * s))
    def resize(self, img):
        w, h = img.size
        scale = min(self.max_size / max(w, h), 1.0)
        scale = max(scale, self.min_size / min(w, h))
        new_w = self._make_divisible(round(w * scale), self.patch_size)
        new_h = self._make_divisible(round(h * scale), self.patch_size)
        return img.resize((new_w, new_h), Image.BICUBIC)
    def __call__(self, img):
        img = self.resize(img)
        t = torch.tensor(np.array(img)).permute(2, 0, 1).float() / 255.0
        return (t - 0.5) / 0.5
    def resize_transform(self, img):
        return self.resize(img)


def denorm(t):
    """[-1,1] tensor [1,3,H,W] → uint8 numpy [H,W,3]."""
    return (t * 0.5 + 0.5).clamp(0, 1)[0].permute(1, 2, 0).float().cpu().numpy() * 255


# ════════════════════════════════════════════════════════════════════════
# BAGEL / THINKMORPH (shared code, different checkpoint)
# ════════════════════════════════════════════════════════════════════════

def bagel_understand(model_path):
    """Bagel/ThinkMorph understand via model.chat()."""
    from mapspatial.loader import load_model, load_tokenizer
    from mapspatial.vendor.bagel.modeling_bagel import BagelForConditionalGeneration

    model, config = load_model(model_path, BagelForConditionalGeneration, device="cuda", dtype="bfloat16")
    tokenizer = load_tokenizer(model_path)

    # Setup special tokens
    special_tokens = ["<|im_start|>", "<|im_end|>", "<|vision_start|>", "<|vision_end|>"]
    existing = []
    for k, v in tokenizer.special_tokens_map.items():
        if isinstance(v, str): existing.append(v)
        elif isinstance(v, list): existing.extend(v)
    new_tokens = [t for t in special_tokens if t not in existing]
    if new_tokens: tokenizer.add_tokens(new_tokens)
    new_token_ids = {
        "bos_token_id": tokenizer.convert_tokens_to_ids("<|im_start|>"),
        "eos_token_id": tokenizer.convert_tokens_to_ids("<|im_end|>"),
        "start_of_image": tokenizer.convert_tokens_to_ids("<|vision_start|>"),
        "end_of_image": tokenizer.convert_tokens_to_ids("<|vision_end|>"),
    }

    image_transform = ImageTransform(980, 224, 14)

    def _vae_resize(img, max_size=1024, min_size=512, stride=16):
        w, h = img.size
        scale = min(max_size / max(w, h), 1.0)
        scale = max(scale, min_size / min(w, h))
        new_w = max(stride, int(round(round(w * scale) / stride) * stride))
        new_h = max(stride, int(round(round(h * scale) / stride) * stride))
        return img.resize((new_w, new_h), Image.BICUBIC)

    for prompt in UNDERSTAND_PROMPTS:
        test_img = Image.new("RGB", (512, 512), (200, 200, 200))
        img = _vae_resize(test_img.convert("RGB"))
        with torch.no_grad():
            response = model.chat(
                tokenizer=tokenizer, new_token_ids=new_token_ids,
                image_transform=image_transform, images=[img],
                prompt=prompt, max_length=512,
            )
        print(f"  Q: {prompt}\n  A: {response}")

    del model
    gpu_cleanup()


def bagel_draw(model_path, model_name):
    """Bagel/ThinkMorph draw via manual KV-cache + generate_image + VAE."""
    from mapspatial.loader import load_model, load_tokenizer
    from mapspatial.vendor.bagel.modeling_bagel import BagelForConditionalGeneration, NaiveCache, AutoEncoder
    from mapspatial.vendor.bagel.configuration_bagel import BagelVaeConfig
    from safetensors.torch import load_file

    model, config = load_model(model_path, BagelForConditionalGeneration, device="cuda", dtype="bfloat16")
    tokenizer = load_tokenizer(model_path)

    # Setup tokens
    special_tokens = ["<|im_start|>", "<|im_end|>", "<|vision_start|>", "<|vision_end|>"]
    existing = []
    for k, v in tokenizer.special_tokens_map.items():
        if isinstance(v, str): existing.append(v)
        elif isinstance(v, list): existing.extend(v)
    new_tokens = [t for t in special_tokens if t not in existing]
    if new_tokens: tokenizer.add_tokens(new_tokens)
    new_token_ids = {
        "bos_token_id": tokenizer.convert_tokens_to_ids("<|im_start|>"),
        "eos_token_id": tokenizer.convert_tokens_to_ids("<|im_end|>"),
        "start_of_image": tokenizer.convert_tokens_to_ids("<|vision_start|>"),
        "end_of_image": tokenizer.convert_tokens_to_ids("<|vision_end|>"),
    }

    # Load VAE
    vae_config = config.vae_config if config else BagelVaeConfig()
    if isinstance(vae_config, dict): vae_config = BagelVaeConfig(**vae_config)
    vae = AutoEncoder(vae_config).to("cuda").to(torch.bfloat16)
    vae_state = load_file(os.path.join(model_path, "ae.safetensors"))
    vae.load_state_dict(vae_state, strict=False)
    vae.eval()

    vit_transform = ImageTransform(980, 224, 14)
    vae_transform = ImageTransform(1024, 512, 16)

    def generate(prompt, cfg_text_scale=4.0, cfg_img_scale=2.0,
                 num_timesteps=50, timestep_shift=3.0, image_shapes=(1024, 1024)):
        device = next(model.parameters()).device
        test_image = Image.new("RGB", (512, 512), (200, 200, 200))
        img_input = vae_transform.resize_transform(test_image.convert("RGB"))
        img_shape = img_input.size[::-1]

        gen_ctx = {"kv_lens": [0], "ropes": [0],
                    "past_key_values": NaiveCache(config.llm_config.num_hidden_layers)}
        cfg_img_ctx = deepcopy(gen_ctx)

        # 1. Image prefill (VAE then ViT)
        gen_input_vae, kv_lens, ropes = model.prepare_vae_images(
            curr_kvlens=gen_ctx["kv_lens"], curr_rope=gen_ctx["ropes"],
            images=[img_input], transforms=vae_transform, new_token_ids=new_token_ids)
        for k, v in gen_input_vae.items():
            if torch.is_tensor(v): gen_input_vae[k] = v.to(device)
        with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
            gen_ctx["past_key_values"] = model.forward_cache_update_vae(vae, gen_ctx["past_key_values"], **gen_input_vae)
        gen_ctx["kv_lens"], gen_ctx["ropes"] = kv_lens, ropes

        gen_input_vit, kv_lens, ropes = model.prepare_vit_images(
            curr_kvlens=gen_ctx["kv_lens"], curr_rope=gen_ctx["ropes"],
            images=[img_input], transforms=vit_transform, new_token_ids=new_token_ids)
        for k, v in gen_input_vit.items():
            if torch.is_tensor(v): gen_input_vit[k] = v.to(device)
        with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
            gen_ctx["past_key_values"] = model.forward_cache_update_vit(gen_ctx["past_key_values"], **gen_input_vit)
        gen_ctx["kv_lens"], gen_ctx["ropes"] = kv_lens, ropes

        # 2. Snapshot cfg_text = image-only
        cfg_text_ctx = deepcopy(gen_ctx)

        # 3. Text prefill on gen_ctx
        gen_input, gen_ctx["kv_lens"], gen_ctx["ropes"] = model.prepare_prompts(
            curr_kvlens=gen_ctx["kv_lens"], curr_rope=gen_ctx["ropes"],
            prompts=[prompt], tokenizer=tokenizer, new_token_ids=new_token_ids)
        for k, v in gen_input.items():
            if torch.is_tensor(v): gen_input[k] = v.to(device)
        with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
            gen_ctx["past_key_values"] = model.forward_cache_update_text(gen_ctx["past_key_values"], **gen_input)

        # 4. Text prefill on cfg_img_ctx
        cfg_img_in, cfg_img_ctx["kv_lens"], cfg_img_ctx["ropes"] = model.prepare_prompts(
            curr_kvlens=cfg_img_ctx["kv_lens"], curr_rope=cfg_img_ctx["ropes"],
            prompts=[prompt], tokenizer=tokenizer, new_token_ids=new_token_ids)
        for k, v in cfg_img_in.items():
            if torch.is_tensor(v): cfg_img_in[k] = v.to(device)
        with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
            cfg_img_ctx["past_key_values"] = model.forward_cache_update_text(cfg_img_ctx["past_key_values"], **cfg_img_in)

        # 5. Prepare latent + CFG inputs
        gen_input_latent = model.prepare_vae_latent(
            curr_kvlens=gen_ctx["kv_lens"], rope=gen_ctx["ropes"],
            image_sizes=[img_shape], new_token_ids=new_token_ids)
        cfg_text_input = model.prepare_vae_latent_cfg(
            curr_kvlens=cfg_text_ctx["kv_lens"], rope=cfg_text_ctx["ropes"], image_sizes=[img_shape])
        cfg_img_input = model.prepare_vae_latent_cfg(
            curr_kvlens=cfg_img_ctx["kv_lens"], rope=cfg_img_ctx["ropes"], image_sizes=[img_shape])
        for d in [gen_input_latent, cfg_text_input, cfg_img_input]:
            for k, v in d.items():
                if torch.is_tensor(v): d[k] = v.to(device)

        # 6. Generate
        with torch.amp.autocast("cuda", enabled=True, dtype=torch.bfloat16):
            unpacked = model.generate_image(
                past_key_values=gen_ctx["past_key_values"],
                cfg_text_past_key_values=cfg_text_ctx["past_key_values"],
                cfg_img_past_key_values=cfg_img_ctx["past_key_values"],
                num_timesteps=num_timesteps, cfg_text_scale=cfg_text_scale,
                cfg_img_scale=cfg_img_scale, cfg_interval=[0.0, 1.0],
                cfg_renorm_min=0.0, cfg_renorm_type="text_channel",
                timestep_shift=timestep_shift, **gen_input_latent,
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
        latent = unpacked[0].reshape(1, h, w, model.latent_patch_size, model.latent_patch_size, model.latent_channel)
        latent = torch.einsum("nhwpqc->nchpwq", latent)
        latent = latent.reshape(1, model.latent_channel, h * model.latent_patch_size, w * model.latent_patch_size).to(torch.bfloat16)
        with torch.no_grad():
            decoded = vae.decode(latent)
        return Image.fromarray((denorm(decoded)).astype(np.uint8))

    for idx, prompt in enumerate(DRAW_PROMPTS, 1):
        print(f"\n  Prompt {idx}: {prompt[:50]}...")
        t0 = time.time()
        try:
            result = generate(prompt)
            save_image(result, f"{model_name}_prompt{idx}")
            print(f"  Time: {time.time()-t0:.1f}s")
        except Exception as e:
            import traceback; print(f"  FAILED: {e}"); traceback.print_exc()

    del model, vae
    gpu_cleanup()


# ════════════════════════════════════════════════════════════════════════
# BLIP3o
# ════════════════════════════════════════════════════════════════════════

def blip3o_understand():
    """BLIP3o understand via vendor _llm_forward + Qwen2.5-VL token format."""
    from mapspatial.loader import load_model, load_tokenizer
    from mapspatial.vendor.blip3o.modeling_blip3o import BLIP3oQwenForCausalLM

    MODEL_PATH = os.path.join(CKPT_BASE, "BLIP3o-Model-8B")
    model, _ = load_model(MODEL_PATH, BLIP3oQwenForCausalLM, device="cuda", dtype="bfloat16")
    tokenizer = load_tokenizer(MODEL_PATH)

    IMAGE_PAD_ID = 151655
    device = "cuda"
    embed_layer = model.get_input_embeddings()

    for prompt in UNDERSTAND_PROMPTS:
        # With gray image
        img = Image.new("RGB", (512, 512), (200, 200, 200))
        w, h = img.size
        scale = min(980 / max(w, h), 1.0)
        scale = max(scale, 224 / min(w, h))
        new_w, new_h = max(14, int(round(w * scale) / 14) * 14), max(14, int(round(h * scale) / 14) * 14)
        img = img.resize((new_w, new_h), Image.BICUBIC)
        pixel_values = torch.tensor(np.array(img)).permute(2, 0, 1).float().unsqueeze(0).to(device, dtype=torch.bfloat16) / 255.0

        with torch.no_grad():
            vit_features = model.visual(pixel_values)
        vit_embeds = vit_features.reshape(-1, vit_features.shape[-1])
        num_vit = vit_embeds.shape[0]

        vision_str = "<|vision_start|>" + "<|image_pad|>" * num_vit + "<|vision_end|>"
        text = f"<|im_start|>user\n{vision_str}{prompt}<|im_end|>\n<|im_start|>assistant\n"
        input_ids = tokenizer.encode(text, return_tensors="pt").to(device)
        inputs_embeds = embed_layer(input_ids[0])
        image_mask = (input_ids[0] == IMAGE_PAD_ID)
        inputs_embeds[image_mask] = vit_embeds.to(inputs_embeds.dtype)

        eos_id = tokenizer.eos_token_id or tokenizer.convert_tokens_to_ids("<|im_end|>")
        lm_head = model.get_output_embeddings()
        generated = []
        with torch.no_grad():
            for _ in range(256):
                hidden = model._llm_forward(inputs_embeds.unsqueeze(0))
                logits = lm_head(hidden[:, -1:, :])
                next_id = logits[0, -1].argmax(dim=-1).item()
                if next_id == eos_id: break
                generated.append(next_id)
                inputs_embeds = torch.cat([inputs_embeds, embed_layer(torch.tensor([[next_id]], device=device))[0]], dim=0)
        response = tokenizer.decode(generated, skip_special_tokens=True).strip()
        print(f"  Q: {prompt}\n  A: {response}")

    del model
    gpu_cleanup()


def blip3o_draw():
    """BLIP3o draw via official BLIP3o_main repo + EmuVisualGenerationPipeline."""
    BLIP3O_PATH = os.path.join(CKPT_BASE, "BLIP3o-Model-8B")
    DIFFUSION_PATH = os.path.join(BLIP3O_PATH, "diffusion-decoder")
    sys.path.insert(0, BLIP3O_MAIN)

    # Monkey-patches for diffusers compatibility
    import diffusers.models.modeling_utils as _dmu
    _orig_gc = _dmu.ModelMixin.enable_gradient_checkpointing
    def _noop_gc(self, *a, **kw):
        try: _orig_gc(self, *a, **kw)
        except TypeError: pass
    _dmu.ModelMixin.enable_gradient_checkpointing = _noop_gc
    _dmu.ModelMixin._set_gradient_checkpointing = lambda self, *a, **kw: None

    from diffusers.models.attention import LuminaFeedForward as _LFF
    _orig_lff = _LFF.__init__
    def _patched_lff(self, dim=None, inner_dim=None, multiple_of=256, ffn_dim_multiplier=None, **kw):
        _orig_lff(self, dim, int(2 * inner_dim / 3), multiple_of, ffn_dim_multiplier)
    _LFF.__init__ = _patched_lff

    from blip3o.utils import disable_torch_init
    disable_torch_init()
    from blip3o.model.language_model.blip3o_qwen_inference import blip3oQwenForInferenceLM, blip3oQwenModel
    from blip3o.constants import DEFAULT_IMAGE_PATCH_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN, UND_IMAGE_TOKEN_IDX
    from blip3o.conversation import conv_templates

    # Fix checkpoint key mapping
    blip3oQwenForInferenceLM._checkpoint_conversion_mapping = {
        "^visual": "model.visual",
        r"^model(?!\.(language_model|visual|dit|latent_queries|gen_vision_tower|down_projector|vae|noise_scheduler))": "model.language_model",
    }
    # embed_tokens shim
    if not hasattr(blip3oQwenModel, 'embed_tokens'):
        blip3oQwenModel.embed_tokens = property(lambda self: self.language_model.embed_tokens)

    from transformers import AutoConfig
    config = AutoConfig.from_pretrained(BLIP3O_PATH, trust_remote_code=True)
    for attr in ['hidden_size', 'vocab_size', 'num_hidden_layers', 'num_attention_heads', 'num_key_value_heads']:
        if getattr(config, attr, None) is None:
            with open(os.path.join(BLIP3O_PATH, 'config.json')) as f:
                raw = json.load(f)
            if attr in raw: setattr(config, attr, raw[attr])

    model = blip3oQwenForInferenceLM.from_pretrained(BLIP3O_PATH, config=config, low_cpu_mem_usage=True, torch_dtype=torch.float16)
    model = model.to("cuda")

    # Recompute freqs_cis
    from diffusers.models.embeddings import get_2d_rotary_pos_embed_lumina
    dit = model.get_model().dit
    mcfg = dit.model.config
    head_dim = mcfg["hidden_size"] // mcfg["num_attention_heads"]
    input_size = dit.config.input_size
    dit.freqs_cis = get_2d_rotary_pos_embed_lumina(head_dim, input_size, input_size).to("cuda", dtype=torch.complex64)

    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(BLIP3O_PATH)
    if getattr(model.config, "mm_use_im_patch_token", True):
        tokenizer.add_tokens([DEFAULT_IMAGE_PATCH_TOKEN], special_tokens=True)
    if getattr(model.config, "mm_use_im_start_end", False):
        tokenizer.add_tokens([DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN], special_tokens=True)
    model.resize_token_embeddings(len(tokenizer))
    model.eval()

    # Diffusion pipeline
    from diffusers import AutoencoderKL, UNet2DConditionModel, EulerDiscreteScheduler
    from transformers import CLIPImageProcessor
    scheduler = EulerDiscreteScheduler.from_pretrained(DIFFUSION_PATH, subfolder="scheduler")
    vae = AutoencoderKL.from_pretrained(DIFFUSION_PATH, subfolder="vae", torch_dtype=torch.bfloat16, use_safetensors=True, variant="bf16")
    unet = UNet2DConditionModel.from_pretrained(DIFFUSION_PATH, subfolder="unet", torch_dtype=torch.bfloat16, use_safetensors=True, variant="bf16")
    feature_extractor = CLIPImageProcessor.from_pretrained(DIFFUSION_PATH, subfolder="feature_extractor")

    pipeline_file = os.path.join(DIFFUSION_PATH, "pipeline_llava_gen.py")
    spec = importlib.util.spec_from_file_location("pipeline_llava_gen", pipeline_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    pipe = module.EmuVisualGenerationPipeline(tokenizer=tokenizer, multimodal_encoder=model, scheduler=scheduler,
                                               unet=unet, vae=vae, feature_extractor=feature_extractor, safety_checker=None)
    pipe.vae.to("cuda"); pipe.unet.to("cuda")

    # Patch generate_image for M-RoPE
    from diffusers.schedulers import FlowMatchEulerDiscreteScheduler as _FMEDS
    @torch.no_grad()
    def _patched_gen(self, text, tokenizer, pixel_values=None, image_grid_thw=None, max_var=None):
        sched = _FMEDS.from_pretrained("Alpha-VLLM/Lumina-Next-SFT-diffusers", subfolder="scheduler")
        N_QUERY = self.get_n_query()
        inputs = tokenizer(text, padding="longest", return_tensors="pt")
        device = self.get_model().device
        attn_mask = inputs.attention_mask.to(device)
        input_ids = inputs.input_ids.to(device)
        input_ids = torch.cat([input_ids, torch.tensor([[151665]]).to(device)], dim=1)
        text_embeds = self.get_model().embed_tokens(input_ids)
        lq = self.get_model().latent_queries.repeat(text_embeds.shape[0], 1, 1)
        if pixel_values is not None:
            und_idx = (input_ids == UND_IMAGE_TOKEN_IDX)
            pixel_values = pixel_values.type(self.visual.dtype)
            und_embeds = self.visual(pixel_values, grid_thw=image_grid_thw)
            text_embeds[und_idx] = und_embeds.to(text_embeds.device)[:und_idx.sum(), :]
        text_embeds = torch.cat([text_embeds, lq], dim=1)
        attn_mask = torch.cat([attn_mask, torch.ones_like(lq[:, :, 0])], dim=1)
        B, S, _ = text_embeds.shape
        pos = torch.arange(S, device=device)
        pos_ids = pos.view(1, 1, -1).expand(3, B, -1)
        out = self.model(inputs_embeds=text_embeds, attention_mask=attn_mask, position_ids=pos_ids, output_hidden_states=True, return_dict=True)
        hidden = out.hidden_states[-1][:, -N_QUERY:, :]
        return self.sample_images(hidden, sched).view(1, 1792, -1).permute(0, 2, 1).contiguous()
    blip3oQwenForInferenceLM.generate_image = _patched_gen

    for idx, prompt in enumerate(DRAW_PROMPTS, 1):
        print(f"\n  Prompt {idx}: {prompt[:50]}...")
        t0 = time.time()
        try:
            conv = conv_templates["qwen"].copy()
            conv.append_message(conv.roles[0], f"Please generate image based on the following caption: {prompt}")
            conv.append_message(conv.roles[1], None)
            gen_result = pipe([conv.get_prompt()], guidance_scale=3.0)
            save_image(gen_result.image, f"blip3o_prompt{idx}")
            print(f"  Time: {time.time()-t0:.1f}s")
        except Exception as e:
            import traceback; print(f"  FAILED: {e}"); traceback.print_exc()

    del model, pipe, vae, unet
    gpu_cleanup()


# ════════════════════════════════════════════════════════════════════════
# U1 (SenseNova-U1)
# ════════════════════════════════════════════════════════════════════════

def u1_understand():
    """U1 understand via model.language_model() with M-RoPE indexes."""
    from mapspatial.loader import load_model, load_tokenizer
    from mapspatial.vendor.neo_chat.modeling_neo_chat import NEOChatModel

    MODEL_PATH = os.path.join(CKPT_BASE, "SenseNova-U1-8B-MoT")
    model, _ = load_model(MODEL_PATH, NEOChatModel, device="cuda", dtype="bfloat16")
    tokenizer = load_tokenizer(MODEL_PATH)
    device = "cuda"

    for prompt in UNDERSTAND_PROMPTS:
        chat = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        input_ids = tokenizer.encode(chat, return_tensors="pt").to(device)
        eos_id = tokenizer.eos_token_id
        generated = []
        with torch.no_grad():
            for _ in range(64):
                seq_len = input_ids.shape[1]
                pos = torch.arange(seq_len, device=device)
                indexes = torch.stack([pos, pos, pos])
                outputs = model.language_model(input_ids=input_ids, attention_mask=torch.ones_like(input_ids), indexes=indexes)
                next_id = outputs.logits[0, -1].argmax(dim=-1).item()
                if next_id == eos_id: break
                generated.append(next_id)
                input_ids = torch.cat([input_ids, torch.tensor([[next_id]], device=device)], dim=1)
        response = tokenizer.decode(generated, skip_special_tokens=True).strip()
        print(f"  Q: {prompt}\n  A: {response}")

    del model
    gpu_cleanup()


def u1_draw():
    """U1 draw via model.it2i_generate() — 512x512, default timestep_shift=1."""
    from mapspatial.loader import load_model, load_tokenizer
    from mapspatial.vendor.neo_chat.modeling_neo_chat import NEOChatModel

    MODEL_PATH = os.path.join(CKPT_BASE, "SenseNova-U1-8B-MoT")
    model, _ = load_model(MODEL_PATH, NEOChatModel, device="cuda", dtype="bfloat16")
    tokenizer = load_tokenizer(MODEL_PATH)

    dummy_img = Image.new("RGB", (512, 512), (200, 200, 200))
    for idx, prompt in enumerate(DRAW_PROMPTS, 1):
        print(f"\n  Prompt {idx}: {prompt[:50]}...")
        t0 = time.time()
        try:
            with torch.inference_mode():
                output = model.it2i_generate(
                    tokenizer, prompt, [dummy_img],
                    image_size=(512, 512), cfg_scale=4.0, img_cfg_scale=1.0,
                    num_steps=50, batch_size=1, seed=42,
                )
            img_np = denorm(output.clamp(-1, 1) * 0.5 + 0.5).astype(np.uint8) if False else \
                     ((output * 0.5 + 0.5).clamp(0, 1)[0].float().permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)
            save_image(img_np, f"u1_prompt{idx}")
            print(f"  Time: {time.time()-t0:.1f}s")
        except Exception as e:
            import traceback; print(f"  FAILED: {e}"); traceback.print_exc()

    del model
    gpu_cleanup()


# ════════════════════════════════════════════════════════════════════════
# LatentUM
# ════════════════════════════════════════════════════════════════════════

def latentum_understand():
    """LatentUM understand via model._llm_forward() with vision_token_mask."""
    from mapspatial.loader import load_model, load_tokenizer
    from mapspatial.vendor.latentum.modeling_latentum import LatentUMModel

    MODEL_PATH = os.path.join(CKPT_BASE, "LatentUM-Base")
    model, _ = load_model(MODEL_PATH, LatentUMModel, device="cuda", dtype="bfloat16")
    tokenizer = load_tokenizer(MODEL_PATH)
    device = "cuda"
    internvl = model.internvl
    lm = internvl.language_model
    embed_layer = lm.get_input_embeddings()

    for prompt in UNDERSTAND_PROMPTS:
        text = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        input_ids = tokenizer.encode(text, return_tensors="pt").to(device)
        inputs_embeds = embed_layer(input_ids[0])
        eos_id = tokenizer.eos_token_id
        output_layer = lm.lm_head
        generated = []
        dtype = next(model.parameters()).dtype
        with torch.no_grad():
            for _ in range(128):
                vision_mask = torch.zeros(1, inputs_embeds.shape[0], device=device, dtype=dtype)
                hidden = model._llm_forward(inputs_embeds.unsqueeze(0), vision_token_mask=vision_mask)
                logits = output_layer(hidden[:, -1:, :])
                next_id = logits[0, -1].argmax(dim=-1).item()
                if next_id == eos_id: break
                generated.append(next_id)
                inputs_embeds = torch.cat([inputs_embeds, embed_layer(torch.tensor([[next_id]], device=device))[0]], dim=0)
        response = tokenizer.decode(generated, skip_special_tokens=True).strip()
        print(f"  Q: {prompt}\n  A: {response}")

    del model
    gpu_cleanup()


def latentum_draw():
    """LatentUM draw via model.generate_images() with external decoder."""
    sys.path.insert(0, LATENTUM_OFFICIAL)
    from mapspatial.loader import load_model, load_tokenizer
    from mapspatial.vendor.latentum.modeling_latentum import LatentUMModel

    MODEL_PATH = os.path.join(CKPT_BASE, "LatentUM-Base")
    DECODER_PATH = os.path.join(CKPT_BASE, "LatentUM-Decoder")
    model, _ = load_model(MODEL_PATH, LatentUMModel, device="cuda", dtype="bfloat16")
    tokenizer = load_tokenizer(MODEL_PATH)

    from model.latentum.modeling_latentum import LatentUMDecoderModel
    decoder = LatentUMDecoderModel.from_pretrained(DECODER_PATH, dtype=torch.bfloat16)
    decoder = decoder.to("cuda").eval()

    for idx, prompt in enumerate(DRAW_PROMPTS, 1):
        print(f"\n  Prompt {idx}: {prompt[:50]}...")
        t0 = time.time()
        try:
            images = model.generate_images(
                tokenizer, [prompt], decoder=decoder,
                num_images_per_prompt=1, cfg_scale=3.0,
                temperature=0.9, top_k=50, top_p=0.95,
                seed=42, num_inference_steps=25, guidance_scale=1.0,
                show_progress=False,
            )
            result = images[0] if isinstance(images, list) else images
            save_image(result, f"latentum_prompt{idx}")
            print(f"  Time: {time.time()-t0:.1f}s")
        except Exception as e:
            import traceback; print(f"  FAILED: {e}"); traceback.print_exc()

    del model, decoder
    gpu_cleanup()


# ════════════════════════════════════════════════════════════════════════
# Janus
# ════════════════════════════════════════════════════════════════════════

def janus_understand():
    """Janus understand via model.language_model.generate()."""
    from mapspatial.loader import load_model, load_tokenizer
    from mapspatial.vendor.janus.modeling_janus import Janus

    MODEL_PATH = os.path.join(CKPT_BASE, "Janus-Pro-7B")
    model, _ = load_model(MODEL_PATH, Janus, device="cuda", dtype="bfloat16")
    tokenizer = load_tokenizer(MODEL_PATH)
    device = "cuda"

    for prompt in UNDERSTAND_PROMPTS:
        text = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        input_ids = tokenizer.encode(text, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model.language_model.generate(
                input_ids=input_ids, attention_mask=torch.ones_like(input_ids),
                max_new_tokens=64, do_sample=False,
                pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        response = tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True).strip()
        print(f"  Q: {prompt}\n  A: {response}")

    del model
    gpu_cleanup()


def janus_draw():
    """Janus draw via VeOmni patched LlamaForCausalLM."""
    sys.path.insert(0, VEOMNI_DIR)
    from veomni.models.transformers.janus.configuration_janus import JanusConfig
    from veomni.models.transformers.janus.modeling_janus import Janus
    from veomni.models.module_utils import init_empty_weights, load_model_weights

    JANUS_PATH = os.path.join(CKPT_BASE, "Janus-Pro-7B")
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

    config = JanusConfig.from_pretrained(tmp_dir)
    config._attn_implementation = "eager"
    with init_empty_weights():
        model = Janus._from_config(config=config, attn_implementation="eager")
    load_model_weights(model, tmp_dir, "cuda")
    model = model.to(dtype=torch.bfloat16).eval()

    from transformers import LlamaTokenizerFast
    from tokenizers import Tokenizer as TokenizerBackend
    tokenizer = LlamaTokenizerFast.from_pretrained(tmp_dir)
    _tb = TokenizerBackend.from_file(os.path.join(tmp_dir, "tokenizer.json"))
    tokenizer._tokenizer.pre_tokenizer = _tb.pre_tokenizer
    tokenizer._tokenizer.decoder = _tb.decoder
    pad_id = tokenizer.vocab.get("<｜▁pad▁｜>")

    @torch.inference_mode()
    def generate(prompt, cfg_weight=5, seed=42, parallel_size=4, image_token_num=576, img_size=384, patch_size=16):
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        device = next(model.parameters()).device
        input_ids = torch.LongTensor(tokenizer.encode(prompt))
        tokens = torch.zeros((parallel_size*2, len(input_ids)), dtype=torch.int, device=device)
        for i in range(parallel_size*2):
            tokens[i, :] = input_ids
            if i % 2: tokens[i, 1:-1] = pad_id
        inputs_embeds = model.language_model.get_input_embeddings()(tokens)
        generated = torch.zeros((parallel_size, image_token_num), dtype=torch.int, device=device)
        outputs = None
        for i in range(image_token_num):
            outputs = model.language_model.model(inputs_embeds=inputs_embeds, use_cache=True,
                past_key_values=outputs.past_key_values if outputs else None)
            logits = model.gen_head(outputs.last_hidden_state[:, -1, :])
            lc, lu = logits[0::2, :], logits[1::2, :]
            logits = lu + cfg_weight * (lc - lu)
            probs = torch.softmax(logits, dim=-1)
            nxt = torch.multinomial(probs, num_samples=1)
            generated[:, i] = nxt.squeeze(-1)
            nxt = torch.cat([nxt.unsqueeze(1)]*2, dim=1).view(-1)
            inputs_embeds = model.prepare_gen_img_embeds(nxt).unsqueeze(1)
        dec = model.gen_vision_model.decode_code(generated.int(), shape=[parallel_size, 8, img_size//patch_size, img_size//patch_size])
        return np.clip((dec.float().cpu().numpy().transpose(0, 2, 3, 1)+1)/2*255, 0, 255).astype(np.uint8)[0]

    for idx, prompt in enumerate(DRAW_PROMPTS, 1):
        print(f"\n  Prompt {idx}: {prompt[:50]}...")
        t0 = time.time()
        try:
            full_prompt = f"User: {prompt}\n\nAssistant:<begin_of_image>"
            img_arr = generate(full_prompt)
            save_image(img_arr, f"janus_prompt{idx}")
            print(f"  Time: {time.time()-t0:.1f}s")
        except Exception as e:
            import traceback; print(f"  FAILED: {e}"); traceback.print_exc()

    del model
    shutil.rmtree(tmp_dir, ignore_errors=True)
    gpu_cleanup()


# ════════════════════════════════════════════════════════════════════════
# InternVL-U (backend abstraction: InternVLUBackend)
# ════════════════════════════════════════════════════════════════════════

def internvlu_understand():
    """InternVL-U understand via backend.understand() with float32 attention fix."""
    from mapspatial.config import load_model_config
    from mapspatial.backends.registry import get_backend_cls

    cfg = load_model_config("configs/models/internvl-u.yaml")
    BackendCls = get_backend_cls(cfg.backend)
    backend = BackendCls(cfg)

    test_img = Image.new("RGB", (512, 512), (200, 200, 200))
    for prompt in UNDERSTAND_PROMPTS:
        messages = [[
            {"type": "image", "value": test_img},
            {"type": "text", "value": prompt},
        ]]
        try:
            preds = backend.understand(messages, max_new_tokens=256)
            response = preds[0].text if preds else "(no response)"
        except Exception as e:
            response = f"ERROR: {e}"
        print(f"  Q: {prompt}\n  A: {response}")

    del backend
    gpu_cleanup()


def internvlu_draw():
    """InternVL-U draw via backend.draw() (diffusion pipeline)."""
    from mapspatial.config import load_model_config
    from mapspatial.backends.registry import get_backend_cls

    cfg = load_model_config("configs/models/internvl-u.yaml")
    BackendCls = get_backend_cls(cfg.backend)
    backend = BackendCls(cfg)

    for idx, prompt in enumerate(DRAW_PROMPTS, 1):
        print(f"\n  Prompt {idx}: {prompt[:50]}...")
        t0 = time.time()
        try:
            img = backend.draw(
                context=[{"type": "text", "value": prompt}],
                instruction=prompt,
            )
            if img is not None:
                save_image(img, f"internvlu_prompt{idx}")
                print(f"  Time: {time.time()-t0:.1f}s")
            else:
                print(f"  draw() returned None")
        except Exception as e:
            import traceback; print(f"  FAILED: {e}"); traceback.print_exc()

    del backend
    gpu_cleanup()


# ════════════════════════════════════════════════════════════════════════
# Show-o2 (backend abstraction: ShowO2Backend)
# ════════════════════════════════════════════════════════════════════════

def showo2_understand():
    """Show-o2-7B understand via backend.understand() — VAE encode + 432x432."""
    from mapspatial.config import load_model_config
    from mapspatial.backends.registry import get_backend_cls

    cfg = load_model_config("configs/models/show-o2-7b.yaml")
    BackendCls = get_backend_cls(cfg.backend)
    backend = BackendCls(cfg)

    test_img = Image.new("RGB", (432, 432), (200, 200, 200))
    for prompt in UNDERSTAND_PROMPTS:
        messages = [[
            {"type": "image", "value": test_img},
            {"type": "text", "value": prompt},
        ]]
        try:
            preds = backend.understand(messages, max_new_tokens=256)
            response = preds[0].text if preds else "(no response)"
        except Exception as e:
            response = f"ERROR: {e}"
        print(f"  Q: {prompt}\n  A: {response}")

    del backend
    gpu_cleanup()


def showo2_draw():
    """Show-o2-7B draw via backend.draw() — ODE sampler (50 steps) + VAE decode."""
    from mapspatial.config import load_model_config
    from mapspatial.backends.registry import get_backend_cls

    cfg = load_model_config("configs/models/show-o2-7b.yaml")
    BackendCls = get_backend_cls(cfg.backend)
    backend = BackendCls(cfg)

    for idx, prompt in enumerate(DRAW_PROMPTS, 1):
        print(f"\n  Prompt {idx}: {prompt[:50]}...")
        t0 = time.time()
        try:
            img = backend.draw(
                context=[{"type": "text", "value": prompt}],
                instruction=prompt,
            )
            if img is not None:
                save_image(img, f"showo2_prompt{idx}")
                print(f"  Time: {time.time()-t0:.1f}s")
            else:
                print(f"  draw() returned None")
        except Exception as e:
            import traceback; print(f"  FAILED: {e}"); traceback.print_exc()

    del backend
    gpu_cleanup()


# ════════════════════════════════════════════════════════════════════════
# JoyAI-Image (backend abstraction: JoyAIBackend)
# ════════════════════════════════════════════════════════════════════════

def joyai_understand():
    """JoyAI-Image understand via backend.understand() — Qwen3VL."""
    from mapspatial.config import load_model_config
    from mapspatial.backends.registry import get_backend_cls

    cfg = load_model_config("configs/models/joyai-image.yaml")
    BackendCls = get_backend_cls(cfg.backend)
    backend = BackendCls(cfg)

    test_img = Image.new("RGB", (512, 512), (200, 200, 200))
    for prompt in UNDERSTAND_PROMPTS:
        messages = [[
            {"type": "image", "value": test_img},
            {"type": "text", "value": prompt},
        ]]
        try:
            preds = backend.understand(messages, max_new_tokens=256)
            response = preds[0].text if preds else "(no response)"
        except Exception as e:
            response = f"ERROR: {e}"
        print(f"  Q: {prompt}\n  A: {response}")

    del backend
    gpu_cleanup()


def joyai_draw():
    """JoyAI-Image draw via backend.draw() — DiT + VAE pipeline (1024x1024)."""
    from mapspatial.config import load_model_config
    from mapspatial.backends.registry import get_backend_cls

    cfg = load_model_config("configs/models/joyai-image.yaml")
    BackendCls = get_backend_cls(cfg.backend)
    backend = BackendCls(cfg)

    for idx, prompt in enumerate(DRAW_PROMPTS, 1):
        print(f"\n  Prompt {idx}: {prompt[:50]}...")
        t0 = time.time()
        try:
            img = backend.draw(
                context=[{"type": "text", "value": prompt}],
                instruction=prompt,
            )
            if img is not None:
                save_image(img, f"joyai_prompt{idx}")
                print(f"  Time: {time.time()-t0:.1f}s")
            else:
                print(f"  draw() returned None")
        except Exception as e:
            import traceback; print(f"  FAILED: {e}"); traceback.print_exc()

    del backend
    gpu_cleanup()


# ════════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════════

MODEL_REGISTRY = {
    "bagel":      {"understand": lambda: bagel_understand(os.path.join(CKPT_BASE, "BAGEL-7B-MoT")),
                   "draw":       lambda: bagel_draw(os.path.join(CKPT_BASE, "BAGEL-7B-MoT"), "bagel")},
    "thinkmorph": {"understand": lambda: bagel_understand(os.path.join(CKPT_BASE, "ThinkMorph-7B")),
                   "draw":       lambda: bagel_draw(os.path.join(CKPT_BASE, "ThinkMorph-7B"), "thinkmorph")},
    "blip3o":     {"understand": blip3o_understand, "draw": blip3o_draw},
    "u1":         {"understand": u1_understand,     "draw": u1_draw},
    "latentum":   {"understand": latentum_understand, "draw": latentum_draw},
    "janus":      {"understand": janus_understand,  "draw": janus_draw},
    "showo2":     {"understand": showo2_understand,  "draw": showo2_draw},
    "joyai":      {"understand": joyai_understand,   "draw": joyai_draw},
}


def main():
    parser = argparse.ArgumentParser(description="Test all unified models (understand + draw)")
    parser.add_argument("--model", default="all", choices=list(MODEL_REGISTRY.keys()) + ["all"])
    parser.add_argument("--phase", default="both", choices=["understand", "draw", "both"])
    parser.add_argument("--gpu", default="1")
    args = parser.parse_args()

    models = list(MODEL_REGISTRY.keys()) if args.model == "all" else [args.model]

    for model_name in models:
        print(f"\n{'='*60}")
        print(f"  Model: {model_name}")
        print(f"{'='*60}")

        funcs = MODEL_REGISTRY[model_name]
        if args.phase in ("understand", "both"):
            print(f"\n--- {model_name} understand ---")
            try:
                funcs["understand"]()
            except Exception as e:
                import traceback; print(f"  FAILED: {e}"); traceback.print_exc()

        if args.phase in ("draw", "both"):
            print(f"\n--- {model_name} draw ---")
            try:
                funcs["draw"]()
            except Exception as e:
                import traceback; print(f"  FAILED: {e}"); traceback.print_exc()

    print(f"\n{'='*60}")
    print("  All tests complete!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
