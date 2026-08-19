"""Check Janus weight loading: missing/unexpected keys, param count, and text-only generation."""
import os, sys
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "2")
os.environ.setdefault("PYTHONNOUSERSITE", "1")

import torch
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

from mapspatial.loader import load_model, load_tokenizer, _load_safetensors

JANUS_PATH = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/Janus-Pro-7B"
from mapspatial.vendor.janus.modeling_janus import Janus

model, config = load_model(JANUS_PATH, Janus, device="cuda", dtype="bfloat16")
tokenizer = load_tokenizer(JANUS_PATH)

# Re-check weight loading
state_dict = _load_safetensors(JANUS_PATH)
model_params = dict(model.named_parameters())
missing = [k for k in model_params if k not in state_dict]
unexpected = [k for k in state_dict if k not in model_params]
print(f"Params: {sum(p.numel() for p in model.parameters())/1e9:.2f}B, Missing: {len(missing)}, Unexpected: {len(unexpected)}")
if missing: print(f"  Missing first 10: {sorted(missing)[:10]}")
if unexpected: print(f"  Unexpected first 10: {sorted(unexpected)[:10]}")

# Check if loaded weights differ from meta (empty) values
print("\nChecking if weights are actually loaded (not meta):")
for name, p in model.named_parameters():
    if p.device.type == "meta":
        print(f"  META device param: {name}")
    break

# Check a sample weight
for name, p in model.named_parameters():
    if "lm_head" in name or "embed_tokens" in name:
        print(f"  {name}: shape={p.shape}, device={p.device}, dtype={p.dtype}, mean={p.float().mean().item():.6f}, std={p.float().std().item():.6f}")
        break

# Test 1: Text-only with DeepSeek chat template
print("\n--- Test 1: DeepSeek chat template (correct for Janus) ---")
prompt = "What is 2+2? Answer with just the number."
chat = f"You are a helpful assistant.\n\nUser: {prompt}\n\nAssistant:"
input_ids = tokenizer.encode(chat, return_tensors="pt").to("cuda")
print(f"  Input shape: {input_ids.shape}, first tokens: {input_ids[0][:5].tolist()}")
with torch.no_grad():
    outputs = model.language_model.generate(
        input_ids=input_ids,
        attention_mask=torch.ones_like(input_ids),
        max_new_tokens=20, do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
print(f"  Output: '{tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)}'")

# Test 2: With image using processor
print("\n--- Test 2: Image understanding via processor ---")
from mapspatial.vendor.janus.image_processing_janus import JanusImageProcessor
from mapspatial.vendor.janus.processing_janus import JanusProcessor

image_processor = JanusImageProcessor(
    image_size=384, min_size=14,
    image_mean=[0.5, 0.5, 0.5], image_std=[0.5, 0.5, 0.5],
)
processor = JanusProcessor(
    image_processor=image_processor,
    tokenizer=tokenizer,
    image_tag="<image_placeholder>",
    num_image_tokens=576,
    add_special_token=False,
)

from PIL import Image
img_path = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data/benchmark_images_t1/B000A07C0B_from_B000A8XLYF_to_B0FFFCQM37/推荐方案/B000A07C0B_from_B000A8XLYF_to_B0FFFCQM37_T1_angular_order_q0/base/direct/wprd01_direct.png"
img = Image.open(img_path).convert("RGB")

conversation = [
    {"role": "User", "content": f"<image_placeholder>\nWhat do you see in this image? Describe briefly."},
    {"role": "Assistant", "content": ""},
]
chat_text = processor.apply_chat_template(conversation, task="und")
print(f"  Chat text (end): ...{chat_text[-80:]}")

inputs = processor(prompt=chat_text, images=[img])
inputs = {k: v.to("cuda") if torch.is_tensor(v) else v for k, v in inputs.items()}
print(f"  input_ids: {inputs['input_ids'].shape}, pixel_values: {inputs['pixel_values'].shape}, image_mask: {inputs['image_mask'].sum().item()}")

with torch.no_grad():
    inputs_embeds = model.prepare_inputs_embeds(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        image_mask=inputs["image_mask"],
    )
    print(f"  inputs_embeds: {inputs_embeds.shape}, nan={torch.isnan(inputs_embeds).any().item()}")
    output_ids = model.language_model.generate(
        inputs_embeds=inputs_embeds,
        attention_mask=inputs["attention_mask"],
        max_new_tokens=50, do_sample=False, use_cache=True,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
print(f"  Output: '{tokenizer.decode(output_ids[0].cpu().tolist(), skip_special_tokens=True)}'")

# Test 3: Official Janus generation approach (if model has .generate)
print("\n--- Test 3: Check if model has its own generate method ---")
print(f"  model.generate: {hasattr(model, 'generate')}")
print(f"  model._supports_cache_class: {getattr(model, '_supports_cache_class', 'N/A')}")

del model
torch.cuda.empty_cache()
print("\n=== Done ===")
