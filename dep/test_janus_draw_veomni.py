"""Janus draw() — using VeOmni patched LlamaForCausalLM (fixes solid orange issue)."""
import os, sys, json, time, tempfile, shutil

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")
os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")

# Add VeOmni to path for patched LlamaForCausalLM
VEOMNI_DIR = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/VeOmni"
sys.path.insert(0, VEOMNI_DIR)
sys.path.insert(0, "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit")

import torch, numpy as np
from PIL import Image

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

from veomni.models.transformers.janus.configuration_janus import JanusConfig
from veomni.models.transformers.janus.modeling_janus import Janus
from veomni.models.module_utils import init_empty_weights, load_model_weights

config = JanusConfig.from_pretrained(tmp_dir)
config._attn_implementation = "eager"
print("Loading Janus with VeOmni patched Llama...")
t0 = time.time()
with init_empty_weights():
    model = Janus._from_config(config=config, attn_implementation="eager")
load_model_weights(model, tmp_dir, "cuda")
model = model.to(dtype=torch.bfloat16).eval()
print(f"  Loaded in {time.time()-t0:.1f}s")

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
    tokens = torch.zeros((parallel_size*2, len(input_ids)), dtype=torch.int, device=device)
    for i in range(parallel_size*2):
        tokens[i, :] = input_ids
        if i % 2: tokens[i, 1:-1] = pad_id
    inputs_embeds = mmgpt.language_model.get_input_embeddings()(tokens)
    generated = torch.zeros((parallel_size, image_token_num), dtype=torch.int, device=device)
    outputs = None
    for i in range(image_token_num):
        outputs = mmgpt.language_model.model(inputs_embeds=inputs_embeds, use_cache=True,
            past_key_values=outputs.past_key_values if outputs else None)
        logits = mmgpt.gen_head(outputs.last_hidden_state[:, -1, :])
        lc, lu = logits[0::2, :], logits[1::2, :]
        logits = lu + cfg_weight * (lc - lu)
        probs = torch.softmax(logits, dim=-1)
        nxt = torch.multinomial(probs, num_samples=1)
        generated[:, i] = nxt.squeeze(-1)
        nxt = torch.cat([nxt.unsqueeze(1)]*2, dim=1).view(-1)
        inputs_embeds = mmgpt.prepare_gen_img_embeds(nxt).unsqueeze(1)
    dec = mmgpt.gen_vision_model.decode_code(generated.int(), shape=[parallel_size, 8, img_size//patch_size, img_size//patch_size])
    dec = dec.float().cpu().numpy().transpose(0, 2, 3, 1)
    return np.clip((dec+1)/2*255, 0, 255).astype(np.uint8)[0]

PROMPTS = [
    "Draw a red arrow pointing from the bottom-left to the top-right of the image",
    "Add a blue circle in the center of this image",
    "Draw a green route line from the left side to the right side of the image",
]
output_dir = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit/gen_results"

for idx, prompt_text in enumerate(PROMPTS, 1):
    print(f"\n  Prompt {idx}: {prompt_text[:50]}...")
    t0 = time.time()
    prompt = f"User: {prompt_text}\n\nAssistant:<begin_of_image>"
    img_arr = janus_generate(model, tokenizer, prompt, pad_id, parallel_size=4, seed=42)
    result = Image.fromarray(img_arr)
    save_path = os.path.join(output_dir, f"janus_prompt{idx}.png")
    result.save(save_path)
    print(f"    Saved: mean={img_arr.mean():.1f}, std={img_arr.std():.1f}, Time: {time.time()-t0:.1f}s")

shutil.rmtree(tmp_dir, ignore_errors=True)
print("\n=== Done ===")
