"""BLIP3o draw() — official pipeline with blip3oQwenForInferenceLM + EmuVisualGenerationPipeline."""
import os, sys, time, importlib.util

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
import numpy as np
from PIL import Image

BLIP3O_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/BLIP3o-Model-8B"
DIFFUSION_PATH = os.path.join(BLIP3O_PATH, "diffusion-decoder")
BLIP3O_MAIN = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/BLIP3o_main"
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"

sys.path.insert(0, BLIP3O_MAIN)
sys.path.insert(0, PROJECT)

# Monkey-patch diffusers gradient checkpointing (API changed in newer versions)
import diffusers.models.modeling_utils as _diffusers_mu
_orig_enable_gc = _diffusers_mu.ModelMixin.enable_gradient_checkpointing
def _noop_gc(self, *args, **kwargs):
    try:
        _orig_enable_gc(self, *args, **kwargs)
    except TypeError:
        pass
_diffusers_mu.ModelMixin.enable_gradient_checkpointing = _noop_gc

# Also patch _set_gradient_checkpointing directly
_orig_set_gc = getattr(_diffusers_mu.ModelMixin, '_set_gradient_checkpointing', None)
def _noop_set_gc(self, *args, **kwargs):
    pass
_diffusers_mu.ModelMixin._set_gradient_checkpointing = _noop_set_gc

# Monkey-patch LuminaFeedForward (2/3 SwiGLU factor)
from diffusers.models.attention import LuminaFeedForward as _LuminaFF
_orig_lff_init = _LuminaFF.__init__
def _patched_lff_init(self, dim=None, inner_dim=None, multiple_of=256, ffn_dim_multiplier=None, **kwargs):
    corrected_inner_dim = int(2 * inner_dim / 3)
    _orig_lff_init(self, dim, corrected_inner_dim, multiple_of, ffn_dim_multiplier)
_LuminaFF.__init__ = _patched_lff_init

# Disable torch init
from blip3o.utils import disable_torch_init
disable_torch_init()

# Import official model
from blip3o.model.language_model.blip3o_qwen_inference import blip3oQwenForInferenceLM
from blip3o.constants import DEFAULT_IMAGE_PATCH_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN, UND_IMAGE_TOKEN_IDX
from blip3o.conversation import conv_templates

# Fix checkpoint key mapping for transformers 5.9.0
# Qwen2_5_VLModel stores text model in self.language_model, so keys need remapping
blip3oQwenForInferenceLM._checkpoint_conversion_mapping = {
    "^visual": "model.visual",
    r"^model(?!\.(language_model|visual|dit|latent_queries|gen_vision_tower|down_projector|vae|noise_scheduler))": "model.language_model",
}

# Compatibility shim: embed_tokens property
from blip3o.model.language_model.blip3o_qwen_inference import blip3oQwenModel
if not hasattr(blip3oQwenModel, 'embed_tokens'):
    @property
    def _compat_embed_tokens(self):
        if hasattr(self, 'language_model') and hasattr(self.language_model, 'embed_tokens'):
            return self.language_model.embed_tokens
        raise AttributeError("Cannot find embed_tokens on model")
    blip3oQwenModel.embed_tokens = _compat_embed_tokens

print("Loading BLIP3o model...")
t0 = time.time()
from transformers import AutoConfig
config = AutoConfig.from_pretrained(BLIP3O_PATH, trust_remote_code=True)
# blip3oQwenConfig doesn't properly map all JSON keys — set them explicitly
for attr in ['hidden_size', 'vocab_size', 'num_hidden_layers', 'num_attention_heads', 'num_key_value_heads']:
    val = getattr(config, attr, None)
    if val is None:
        # Read from config.json
        import json
        with open(os.path.join(BLIP3O_PATH, 'config.json')) as f:
            raw = json.load(f)
        if attr in raw:
            setattr(config, attr, raw[attr])
            print(f"  Set config.{attr} = {raw[attr]}")
model = blip3oQwenForInferenceLM.from_pretrained(BLIP3O_PATH, config=config, low_cpu_mem_usage=True, torch_dtype=torch.float16)
model = model.to("cuda")
print(f"  Loaded in {time.time()-t0:.1f}s")

# Fix: recompute freqs_cis (was meta tensor from init_empty_weights)
from diffusers.models.embeddings import get_2d_rotary_pos_embed_lumina
dit = model.get_model().dit
mcfg = dit.model.config  # FrozenDict from diffusers
head_dim = mcfg["hidden_size"] // mcfg["num_attention_heads"]
input_size = dit.config.input_size  # from NextDiTCrossAttnConfig
dit.freqs_cis = get_2d_rotary_pos_embed_lumina(head_dim, input_size, input_size).to("cuda", dtype=torch.complex64)
print(f"  Recomputed freqs_cis: {dit.freqs_cis.shape} device={dit.freqs_cis.device}")

# Tokenizer
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained(BLIP3O_PATH)

# Resize embeddings
mm_use_im_start_end = getattr(model.config, "mm_use_im_start_end", False)
mm_use_im_patch_token = getattr(model.config, "mm_use_im_patch_token", True)
if mm_use_im_patch_token:
    tokenizer.add_tokens([DEFAULT_IMAGE_PATCH_TOKEN], special_tokens=True)
if mm_use_im_start_end:
    tokenizer.add_tokens([DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN], special_tokens=True)
model.resize_token_embeddings(len(tokenizer))
model.eval()

# Load diffusion pipeline
print("Loading diffusion pipeline...")
from diffusers import AutoencoderKL, UNet2DConditionModel, EulerDiscreteScheduler
from transformers import CLIPImageProcessor

scheduler = EulerDiscreteScheduler.from_pretrained(DIFFUSION_PATH, subfolder="scheduler")
vae = AutoencoderKL.from_pretrained(DIFFUSION_PATH, subfolder="vae", torch_dtype=torch.bfloat16, use_safetensors=True, variant="bf16")
unet = UNet2DConditionModel.from_pretrained(DIFFUSION_PATH, subfolder="unet", torch_dtype=torch.bfloat16, use_safetensors=True, variant="bf16")
feature_extractor = CLIPImageProcessor.from_pretrained(DIFFUSION_PATH, subfolder="feature_extractor")

# Load pipeline class
pipeline_file = os.path.join(DIFFUSION_PATH, "pipeline_llava_gen.py")
spec = importlib.util.spec_from_file_location("pipeline_llava_gen", pipeline_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
EmuVisualGenerationPipeline = module.EmuVisualGenerationPipeline

pipe = EmuVisualGenerationPipeline(
    tokenizer=tokenizer,
    multimodal_encoder=model,
    scheduler=scheduler,
    unet=unet,
    vae=vae,
    feature_extractor=feature_extractor,
    safety_checker=None,
)
pipe.vae.to("cuda")
pipe.unet.to("cuda")
print(f"  Pipeline loaded")

# Patch generate_image for M-RoPE
from typing import List, Optional
from diffusers.schedulers import FlowMatchEulerDiscreteScheduler as _FMEDS

@torch.no_grad()
def _patched_generate_image(self, text, tokenizer, pixel_values=None, image_grid_thw=None, max_var=None):
    scheduler = _FMEDS.from_pretrained("Alpha-VLLM/Lumina-Next-SFT-diffusers", subfolder="scheduler")
    N_QUERY = self.get_n_query()
    inputs = tokenizer(text, padding="longest", return_tensors="pt")
    device = self.get_model().device
    attention_mask = inputs.attention_mask.to(device)
    input_ids = inputs.input_ids.to(device)
    input_ids = torch.cat([input_ids, torch.tensor([[151665]]).to(device)], dim=1)
    text_embeds = self.get_model().embed_tokens(input_ids)
    latent_queries = self.get_model().latent_queries.repeat(text_embeds.shape[0], 1, 1)
    if pixel_values is not None:
        und_image_idx = (input_ids == UND_IMAGE_TOKEN_IDX)
        pixel_values = pixel_values.type(self.visual.dtype)
        und_image_embeds = self.visual(pixel_values, grid_thw=image_grid_thw)
        text_embeds[und_image_idx] = und_image_embeds.to(text_embeds.device)[:und_image_idx.sum(), :]
    text_embeds = torch.cat([text_embeds, latent_queries], dim=1)
    attention_mask = torch.cat([attention_mask, torch.ones_like(latent_queries[:, :, 0])], dim=1)
    batch_size, seq_len, _ = text_embeds.shape
    pos = torch.arange(seq_len, device=device)
    position_ids = pos.view(1, 1, -1).expand(3, batch_size, -1)
    outputs = self.model(inputs_embeds=text_embeds, attention_mask=attention_mask, position_ids=position_ids, output_hidden_states=True, return_dict=True)
    hidden_states = outputs.hidden_states[-1][:, -N_QUERY:, :]
    img_hidden_states = hidden_states
    output_img = self.sample_images(img_hidden_states, scheduler)
    output_img = output_img.view(1, 1792, -1).permute(0, 2, 1).contiguous()
    return output_img

blip3oQwenForInferenceLM.generate_image = _patched_generate_image

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
        conv = conv_templates["qwen"].copy()
        conv.append_message(conv.roles[0], f"Please generate image based on the following caption: {prompt}")
        conv.append_message(conv.roles[1], None)
        prompt_text = conv.get_prompt()
        gen_result = pipe([prompt_text], guidance_scale=3.0)
        result_image = gen_result.image
        save_path = os.path.join(output_dir, f"blip3o_prompt{idx}.png")
        result_image.save(save_path)
        arr = np.array(result_image)
        print(f"  Saved: {save_path}, size={result_image.size}, mean={arr.mean():.1f}, std={arr.std():.1f}, Time: {time.time()-t0:.1f}s")
    except Exception as e:
        import traceback
        print(f"  FAILED: {e}")
        traceback.print_exc()
        # Check meta tensors
        for name, buf in model.named_buffers():
            if buf.is_meta:
                print(f"  META BUFFER: {name}"); break
        try:
            et = model.get_model().embed_tokens
            print(f"  embed_tokens.weight: is_meta={et.weight.is_meta} device={et.weight.device}")
        except Exception as e2:
            print(f"  embed_tokens error: {e2}")

print("\n=== Done ===")
