import os
os.environ.setdefault("VLLM_WORKER_MULTIPROC_METHOD", "spawn")


def main():
    from vllm import LLM, SamplingParams
    from PIL import Image
    from transformers import AutoProcessor

    mp = "/mnt/nas-tbt/tbt/checkpoint/hf_cache/InternVL3-8B-hf"
    img = "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data/benchmark_images_t1/B000A07C0B_from_B000A8XLYF_to_B0FFFCQM37/推荐方案/B000A07C0B_from_B000A8XLYF_to_B0FFFCQM37_T1_angular_order_q0/base/direct/sat_direct.png"
    pil = Image.open(img).convert("RGB")
    llm = LLM(model=mp, max_model_len=8192, gpu_memory_utilization=0.7,
              trust_remote_code=True, dtype="bfloat16",
              limit_mm_per_prompt={"image": 1}, enforce_eager=True)
    proc = AutoProcessor.from_pretrained(mp, trust_remote_code=True)
    print("PROC:", type(proc).__name__)
    prompt_text = "<image>\nWhich direction is north on this map? Answer briefly."
    rendered = proc.apply_chat_template([{"role": "user", "content": prompt_text}],
                                       tokenize=False, add_generation_prompt=True)
    print("RENDERED:", repr(rendered[:160]))
    sp = SamplingParams(temperature=0, max_tokens=64)
    for label, mm in [("PIL", {"image": [pil]}), ("path", {"image": [img]})]:
        try:
            out = llm.generate({"prompt": rendered, "multi_modal_data": mm}, sp, use_tqdm=False)
            print(label, "OUT:", repr(out[0].outputs[0].text[:150]),
                  "FINISH:", out[0].outputs[0].finish_reason)
        except Exception as e:
            print(label, "ERR:", repr(e)[:200])


if __name__ == "__main__":
    main()
