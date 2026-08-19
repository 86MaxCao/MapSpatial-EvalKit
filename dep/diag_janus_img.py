"""Diagnose Janus image understanding path — why does it output 'Hello' for everything?"""
import os, sys
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "2")
os.environ.setdefault("PYTHONNOUSERSITE", "1")

import torch
PROJECT = "/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit"
sys.path.insert(0, PROJECT)

from mapspatial.config import load_model_config
from mapspatial.backends.veomni.janus import JanusBackend
from mapspatial.messages import Message
from mapspatial.media import load_image
from PIL import Image

# Load backend via config
bcfg = load_model_config("configs/models/janus-pro-7b.yaml")
print("Building JanusBackend...")
backend = JanusBackend(bcfg)
print("Loaded.")

# Build a sample message from a real benchmark image
DATA_ROOT = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data"
img_rel = "benchmark_images_t1/B000A07C0B_from_B000A8XLYF_to_B0FFFCQM37/推荐方案/B000A07C0B_from_B000A8XLYF_to_B0FFFCQM37_T1_angular_order_q0/base/direct/wprd01_direct.png"
img_path = os.path.join(DATA_ROOT, img_rel)
print("Image:", img_path, "exists:", os.path.exists(img_path))

img = load_image(img_path)
question = (
    "Look at the map image. A person stands at the black dot facing the blue dot. "
    "As they walk straight toward the blue dot, which colored point do they encounter first? "
    "Answer with a single letter: A, B, C, or D."
)
msg = Message([
    {"type": "text", "value": question},
    {"type": "image", "value": img_path},
])

# Run the backend's understand path
print("\n--- Running backend.understand ---")
preds = backend.understand([msg], max_new_tokens=128)
print("Prediction:", repr(preds[0].text[:200]) if preds[0].text else "ERROR:", preds[0].error)

# Now debug the processor path manually
print("\n--- Manual debug ---")
from mapspatial.messages import to_interleave_list
from mapspatial.messages import strip_placeholders

input_list = to_interleave_list(msg)
text_parts = [item for item in input_list if isinstance(item, str)]
images = [item for item in input_list if not isinstance(item, str)]
prompt = "\n".join(text_parts)
prompt = strip_placeholders(prompt)
print("Prompt:", repr(prompt[:120]))

processor = backend._processor
tokenizer = backend._tokenizer
model = backend._model

conversation = [
    {"role": "User", "content": f"<image_placeholder>\n{prompt}"},
    {"role": "Assistant", "content": ""},
]
chat_text = processor.apply_chat_template(conversation, task="und")
print("\nChat text:", repr(chat_text[:300]))
print("Chat text end:", repr(chat_text[-100:]))

inputs = processor(prompt=chat_text, images=[images[0]])
inputs = {k: v.to("cuda") if torch.is_tensor(v) else v for k, v in inputs.items()}
print("\ninput_ids shape:", inputs["input_ids"].shape)
print("pixel_values shape:", inputs["pixel_values"].shape)
print("image_mask sum:", inputs["image_mask"].sum().item())
print("input_ids[:20]:", inputs["input_ids"][0][:20].tolist())
print("input_ids[-10:]:", inputs["input_ids"][0][-10:].tolist())

# Check prepare_inputs_embeds
with torch.no_grad():
    inputs_embeds = model.prepare_inputs_embeds(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        image_mask=inputs["image_mask"],
    )
print("\ninputs_embeds shape:", inputs_embeds.shape)
print("inputs_embeds nan:", torch.isnan(inputs_embeds).any().item())
print("inputs_embeds[0, -5:]:", inputs_embeds[0, -5:, :3].tolist())

# Generate
with torch.no_grad():
    output_ids = model.language_model.generate(
        inputs_embeds=inputs_embeds,
        attention_mask=inputs["attention_mask"],
        max_new_tokens=64,
        do_sample=False,
        use_cache=True,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
print("\nGenerated ids:", output_ids[0].tolist())
print("Decoded:", repr(tokenizer.decode(output_ids[0].cpu().tolist(), skip_special_tokens=True)))
