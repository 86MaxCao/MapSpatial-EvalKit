import os
os.environ.setdefault("VLLM_WORKER_MULTIPROC_METHOD", "spawn")


def main():
    import json
    import traceback
    import torch
    from PIL import Image
    from mapspatial.vendor.spatial_mllm.spatial_mllm import (
        SpatialMLLMConfig,
        SpatialMLLMForConditionalGeneration,
    )
    from mapspatial.vendor.spatial_mllm.processing import prepare_spatial_mllm_inputs
    from transformers import Qwen2_5_VLProcessor
    from qwen_vl_utils import process_vision_info

    mp = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/Spatial-MLLM-v1.1-Instruct-820K"
    img = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data/benchmark_images_t1/B000A07C0B_from_B000A8XLYF_to_B0FFFCQM37/推荐方案/B000A07C0B_from_B000A8XLYF_to_B0FFFCQM37_T1_angular_order_q0/base/direct/sat_direct.png"

    config = SpatialMLLMConfig.from_pretrained(mp)
    if not getattr(config, "hidden_size", None):
        config.hidden_size = json.load(open(mp + "/config.json"))["hidden_size"]
    print("config hidden_size:", config.hidden_size)

    model = SpatialMLLMForConditionalGeneration.from_pretrained(
        mp, config=config, torch_dtype="bfloat16", device_map="cuda",
        attn_implementation="eager",
    )
    model.eval()
    processor = Qwen2_5_VLProcessor.from_pretrained(mp)
    pil = Image.open(img).convert("RGB")

    prompt_text = "<image>\nWhich direction is north on this map? Answer briefly."
    messages_payload = [{"role": "user", "content": [
        {"type": "image", "image": img},
        {"type": "text", "text": prompt_text},
    ]}]
    rendered = processor.apply_chat_template(
        messages_payload, tokenize=False, add_generation_prompt=True
    )
    image_inputs, video_inputs = process_vision_info(messages_payload)
    print("DEBUG image_inputs:", len(image_inputs) if image_inputs else 0)
    batch = processor(
        text=[rendered], images=image_inputs or None, return_tensors="pt", padding=True, padding_side="left"
    )
    batch = prepare_spatial_mllm_inputs(batch, video_inputs, image_inputs)
    batch.pop("mm_token_type_ids", None)
    device = next(model.parameters()).device
    batch = batch.to(device)
    if batch.get("image_tchw"):
        batch["image_tchw"] = [t.to(device) for t in batch["image_tchw"]]
    print("batch keys:", list(batch.keys()))
    print("DEBUG image_tchw in batch:", batch.get("image_tchw") is not None, type(batch.get("image_tchw")))

    model._gen_image_tchw = batch.get("image_tchw")
    model._gen_video_tchw = batch.get("video_tchw")
    print("DEBUG model._gen_image_tchw set:", getattr(model, "_gen_image_tchw", "MISSING") is not None)

    try:
        with torch.no_grad():
            out = model.generate(**batch, max_new_tokens=64, use_cache=True, do_sample=False)
        input_len = batch["input_ids"].shape[1]
        text = processor.batch_decode(out[:, input_len:], skip_special_tokens=True)[0]
        print("OUTPUT:", repr(text[:200]))
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()
