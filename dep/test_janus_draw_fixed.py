"""Test Janus draw() — using VeOmni's expanded config approach (temp dir)."""
import os, sys, json, time, tempfile, shutil

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

import torch
import numpy as np
from PIL import Image

PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
JANUS_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/Janus-Pro-7B"

# VeOmni expanded config (exact copy from test_janus_veomni_generation.py)
VEOMNI_CONFIG = {
    "model_type": "janus",
    "vision_config": {
        "width": 1024, "layers": 24, "heads": 16, "patch_size": 16,
        "image_size": 384, "global_pool": "map", "mlp_ratio": 4.0,
        "class_token": False, "num_classes": 0, "select_feature": "same",
        "select_layer": -1, "ignore_head": True, "weight_init": "skip",
    },
    "gen_vision_config": {
        "codebook_size": 16384, "codebook_embed_dim": 8,
        "codebook_l2_norm": True, "codebook_show_usage": True,
        "commit_loss_beta": 0.25, "entropy_loss_ratio": 0.0,
        "encoder_ch_mult": [1, 1, 2, 2, 4], "decoder_ch_mult": [1, 1, 2, 2, 4],
        "z_channels": 256, "dropout_p": 0.0,
    },
    "language_config": {
        "model_type": "llama", "hidden_size": 4096, "intermediate_size": 11008,
        "num_hidden_layers": 30, "num_attention_heads": 32, "num_key_value_heads": 32,
        "max_position_embeddings": 16384, "vocab_size": 102400,
        "torch_dtype": "bfloat16", "rms_norm_eps": 1e-6,
    },
    "aligner_depth": 2, "aligner_projector_type": "mlp_gelu",
    "gen_aligner_depth": 2, "gen_aligner_projector_type": "mlp_gelu",
    "gen_head_embed": 4096, "torch_dtype": "bfloat16",
}

# Create temp dir with expanded config + symlink weights
tmp_dir = tempfile.mkdtemp(prefix="janus_gen_")
with open(os.path.join(tmp_dir, "config.json"), "w") as f:
    json.dump(VEOMNI_CONFIG, f, indent=2)
for fname in os.listdir(JANUS_PATH):
    src = os.path.join(JANUS_PATH, fname)
    dst = os.path.join(tmp_dir, fname)
    if fname == "config.json":
        continue
    if os.path.isfile(src) and not os.path.exists(dst):
        os.symlink(src, dst)

sys.path.insert(0, PROJECT)
from mapspatial.loader import load_model
from mapspatial.vendor.janus.modeling_janus import Janus

print("Loading Janus with expanded config...")
t0 = time.time()
model, config = load_model(tmp_dir, Janus, device="cuda", dtype="bfloat16")
print(f"Loaded in {time.time()-t0:.1f}s")

# Check VQ-VAE
vq = model.gen_vision_model
q = vq.quantize
print(f"  quantize type: {type(q).__name__}")
if hasattr(q, 'codebook_l2_norm'):
    print(f"  codebook_l2_norm: {q.codebook_l2_norm}")
# Check if codebook is L2-normalized
if hasattr(q, 'embedding'):
    emb = q.embedding.weight
    norms = emb.norm(dim=-1)
    print(f"  codebook norms: mean={norms.mean().item():.4f}, std={norms.std().item():.4f}")

# Tokenizer with fix
from transformers import LlamaTokenizerFast
from tokenizers import Tokenizer as TokenizerBackend
tokenizer = LlamaTokenizerFast.from_pretrained(tmp_dir)
_tok_backend = TokenizerBackend.from_file(os.path.join(tmp_dir, "tokenizer.json"))
tokenizer._tokenizer.pre_tokenizer = _tok_backend.pre_tokenizer
tokenizer._tokenizer.decoder = _tok_backend.decoder
pad_id = tokenizer.vocab.get("<｜▁pad▁｜>")

@torch.inference_mode()
def janus_generate(mmgpt, tokenizer, prompt, pad_id, cfg_weight=5, seed=42,
                   parallel_size=4, image_token_num=576, img_size=384, patch_size=16):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    device = next(mmgpt.parameters()).device

    input_ids = tokenizer.encode(prompt)
    input_ids = torch.LongTensor(input_ids)
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
        hidden_states = outputs.last_hidden_state
        logits = mmgpt.gen_head(hidden_states[:, -1, :])
        logit_cond = logits[0::2, :]
        logit_uncond = logits[1::2, :]
        logits = logit_uncond + cfg_weight * (logit_cond - logit_uncond)
        probs = torch.softmax(logits, dim=-1)
        next_token = torch.multinomial(probs, num_samples=1)
        generated_tokens[:, i] = next_token.squeeze(dim=-1)
        next_token = torch.cat([next_token.unsqueeze(1), next_token.unsqueeze(1)], dim=1).view(-1)
        img_embeds = mmgpt.prepare_gen_img_embeds(next_token)
        inputs_embeds = img_embeds.unsqueeze(dim=1)

    dec = mmgpt.gen_vision_model.decode_code(
        generated_tokens.to(dtype=torch.int),
        shape=[parallel_size, 8, img_size // patch_size, img_size // patch_size],
    )
    dec = dec.to(torch.float32).cpu().numpy().transpose(0, 2, 3, 1)
    dec = np.clip((dec + 1) / 2 * 255, 0, 255).astype(np.uint8)
    return dec[0]

PROMPTS = [
    "Draw a red arrow pointing from the bottom-left to the top-right of the image",
    "Add a blue circle in the center of this image",
    "Draw a green route line from the left side to the right side of the image",
]
output_dir = os.path.join(PROJECT, "gen_results")
os.makedirs(output_dir, exist_ok=True)

for idx, prompt_text in enumerate(PROMPTS, 1):
    print(f"\n=== Janus Prompt {idx}: {prompt_text[:50]}... ===")
    prompt = f"User: {prompt_text}\n\nAssistant:<begin_of_image>"
    t0 = time.time()
    try:
        img_arr = janus_generate(model, tokenizer, prompt, pad_id, parallel_size=4, seed=42)
        result = Image.fromarray(img_arr)
        save_path = os.path.join(output_dir, f"janus_prompt{idx}.png")
        result.save(save_path)
        print(f"  Saved: {save_path}, mean={img_arr.mean():.1f}, std={img_arr.std():.1f}, Time: {time.time()-t0:.1f}s")
    except Exception as e:
        import traceback
        print(f"  FAILED: {e}")
        traceback.print_exc()

shutil.rmtree(tmp_dir, ignore_errors=True)
print("\n=== Done ===")
