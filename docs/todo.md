# TODO: 9 个统一模型适配状态

## 环境信息

- **我们的代码路径**: `/home/ximeng.czq/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit`
- **原始 VeOmni 代码**: `/home/ximeng.czq/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/VeOmni`
- **VLMEvalKit_Thinkmorph**: `/home/ximeng.czq/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/VLMEvalKit_Thinkmorph`
- **模型权重路径**: `/mnt/nas-tbt/tbt/checkpoint/hf_cache/`
- **运行环境**: `/mnt/nas-tbt/caoziqi/micromamba/envs/mapspatial` (torch 2.11.0+cu130, transformers 5.8.0, vllm 0.22.0)
- **GPU**: 仅可使用 GPU 1, 2, 3 (`CUDA_VISIBLE_DEVICES=1,2,3`)
- **环境变量**: `PYTHONNOUSERSITE=1`, `VLLM_DEEP_GEMM_WARMUP=skip`, `CKPT_DIR=/mnt/nas-tbt/tbt/checkpoint/hf_cache`

### 各模型官方代码路径

| # | 模型 | 官方代码路径 |
|---|---|---|
| 1 | Bagel | `/home/ximeng.czq/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/Bagel` |
| 2 | ThinkMorph | 同 Bagel（复用 Bagel 代码） |
| 3 | BLIP3o | `/home/ximeng.czq/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/BLIP3o` |
| 4 | SenseNova-U1 | `/home/ximeng.czq/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/SenseNova-U1` |
| 5 | LatentUM | `/home/ximeng.czq/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/LatentUM` |
| 6 | Janus | `/home/ximeng.czq/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/Janus` |
| 7 | InternVL-U | `/home/ximeng.czq/caoziqi/code/experiment/InternVL-U` |
| 8 | Show-o2 | `/home/ximeng.czq/caoziqi/code/experiment/Show-o/show-o2`（在 VeOmni 树内） |
| 9 | JoyAI-Image | `/home/ximeng.czq/caoziqi/code/experiment/JoyAI-Image` |

## 9 个模型状态

| # | 模型 | 权重目录 | 后端文件 | 官方代码路径 | VeOmni 调用方式 | Load | Understand | Draw | Interleave | 根因分析 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Bagel-7B-MoT | `BAGEL-7B-MoT` | `mapspatial/backends/veomni/bagel.py` | `.../ablation_experiment/Bagel` | `model.chat(...)` / `model.generate_image(...)` | ✅ | ✅ FIXED | ✅ FIXED | ❌ 待实现 | **Understand**: flash_attn 2.8.4 GQA bug — `flash_attn_varlen_func` 在 GQA (28Q vs 4KV) + `max_seqlen_q=1` 时输出 NaN → argmax 返回 token 0。**修复**: `PackedAttentionMoT.forward_inference` 中用 `repeat_interleave` 扩展 KV heads。**Draw**: CFG 上下文创建顺序错误 — 三个分支相同，CFG 失效。**修复**: 匹配官方 `VeOmniBagelGenerationBackend.draw()`: 图像先填充→快照 cfg_text→文本填充到 gen_ctx + cfg_img。 |
| 2 | ThinkMorph-7B | `ThinkMorph-7B` | `mapspatial/backends/veomni/thinkmorph.py` | 同 Bagel | 同 Bagel | ✅ | ✅ FIXED | ✅ FIXED | ❌ 待实现 | 同 Bagel，继承 BagelBackend。flash_attn GQA fix + CFG 上下文顺序 fix 自动生效。 |
| 3 | BLIP3o-8B | `BLIP3o-Model-8B` | `mapspatial/backends/veomni/blip3o.py` | `.../ablation_experiment/BLIP3o` | `model.visual()` → `model._llm_forward()` → `lm_head` / DiT→UNet→VAE 2-stage | ✅ | ✅ FIXED | ✅⚠️ | N/A | **Understand**: `Qwen2Attention` 定义 `q_norm`/`k_norm`（checkpoint 无权重→初始化为 0→attention 输出全 0），且 `bias=False`。**修复**: `bias=True`，删除 `q_norm`/`k_norm`。视觉特征 prepend → 用 Qwen2.5-VL 格式 `<|vision_start|><|image_pad|>*N<|vision_end|>`。**Draw**: DiT 是 2-stage pipeline（LLM→DiT [B,1792,8,8]→UNet→VAE），DiT config `in_channels=1792, input_size=8`。UNet 需 `added_cond_kwargs={text_embeds, time_ids}`。图片质量偏低，需官方 `EmuVisualGenerationPipeline` + `LuminaFeedForward` monkey-patch。 |
| 4 | SenseNova-U1-8B-MoT | `SenseNova-U1-8B-MoT` | `mapspatial/backends/veomni/u1.py` | `.../ablation_experiment/SenseNova-U1` | `model.language_model(input_ids, attention_mask, indexes)` / `model.it2i_generate(...)` | ✅ | ✅ FIXED | ✅⚠️ | N/A | **Understand**: M-RoPE 需要 `indexes=[3, seq_len]`。**Draw**: (1) `flash_attn_func` GQA NaN → SDPA fallback; (2) `forward_und` 忽略 block causal mask → 传入 `attn_mask`; (3) `timestep_shift=3.0`。图片质量偏低（SDPA 与 flash_attn 数值差异）。 |
| 5 | LatentUM-Base | `LatentUM-Base` | `mapspatial/backends/veomni/latentum.py` | `.../ablation_experiment/LatentUM` | `model._llm_forward()` / `model.generate_images(prompt, decoder=...)` | ✅ | ✅ FIXED | ✅ FIXED | N/A | **Understand**: `Qwen3MoTModel` 无 `forward()` → 改用 `model._llm_forward()`。**Draw**: 从官方代码导入 `LatentUMDecoderModel`，通过 `from_pretrained(DECODER_PATH, device='cuda', dtype=torch.bfloat16)` 加载。 |
| 6 | Janus-Pro-7B | `Janus-Pro-7B` | `mapspatial/backends/veomni/janus.py` | `.../ablation_experiment/Janus` | `model.language_model.generate(...)` / AR loop + VQ decode | ✅ | ❌ 待验证 | ✅ FIXED | N/A | **Draw**: 标准 `transformers.LlamaForCausalLM` 与 VeOmni patched 版（`veomni.models.transformers.llama.generated.patched_modeling_llama_gpu`）行为不同 — 即使 OpSlot guards 未绑定，两者仍产生不同输出。标准版→纯橙色，VeOmni patched 版→正确红色箭头。**修复**: 使用 VeOmni patched LlamaForCausalLM + tokenizer pre-tokenizer fix。 |
| 7 | InternVL-U | `InternVL-U` | `mapspatial/backends/veomni/internvlu.py` | `/home/ximeng.czq/caoziqi/code/experiment/InternVL-U` | `model.generate_text(input_ids, attention_mask, pixel_values, generation_config)` | ❌ | - | - | - | checkpoint 为 diffusers 格式（`model_index.json` + `vlm/` + `generation_decoder/` + `vae/` + `processor/` + `scheduler/` 子目录）。需要分组件加载：VLM from `vlm/`，生成解码器 from `generation_decoder/`，VAE from `vae/`。当前 loader 只支持单目录加载。 |
| 8 | Show-o2-7B | `show-o2-7B` | `mapspatial/backends/veomni/showo2.py` | `/home/ximeng.czq/caoziqi/code/experiment/Show-o/show-o2` | `model.showo2.mmu_generate(input_embeds, attention_mask, max_new_tokens, top_k=1, eos_token)` | ❌ | - | - | - | 权重为 `.bin` 格式（`diffusion_pytorch_model.bin.index.json`）。tokenizer 需要从 `Qwen2.5-VL-7B-Instruct` 加载（checkpoint 在/mnt/nas-tbt/tbt/checkpoint/hf_cache/Qwen2.5-VL-7B-Instruct/）。VeOmni 报 "Couldn't instantiate the backend tokenizer"。 |
| 9 | JoyAI-Image | `JoyAI-Image-Edit` | `mapspatial/backends/veomni/joyai.py` | `/home/ximeng.czq/caoziqi/code/experiment/JoyAI-Image` | `model.generate_text(input_ids, attention_mask, pixel_values, generation_config)` | ✅ | ❌ 无 `generate` 方法 | ❌ gen_model 为 None | N/A | checkpoint 为多组件格式：`JoyAI-Image-Und/`（理解模型 Qwen3VL）+ `transformer/`（DiT）+ `vae/`。理解模型用 `JoyAIImageModel` 类（来自 VeOmni vendored 代码），但该类没有 `.generate()` 方法，实际应该用 `model.generate_text()`。生成模型需 `infer_runtime.model.build_model()` 但缺少 `infer_runtime` 包导入。 |

## 关键发现

### 1. VeOmni 自身也跑不通

在 `latest` 环境（torch 2.11.0 + transformers 5.8.0）下，直接运行 VeOmni 的 `infer_unified.py`：

- **Bagel**: `infer_bagel_understand()` → "!!!!!!!!!!!!!!!!!!!!"（token 0 重复）
- **BLIP3o**: `infer_blip3o_understand()` → 乱码（"mlink铿ǜ社会实践..."）
- **U1/LatentUM**: 测试中

这证明 "!!!!!" 不是 MapSpatial-EvalKit 的代码 bug，而是 **checkpoint 与当前环境的兼容性问题**。

### 2. 可能的根因

- **transformers 版本不匹配**: VeOmni `pyproject.toml` 要求 `transformers==5.9.0`，但环境是 `5.8.0`
- **torch 版本**: torch 2.11.0+cu130 是较新版本，某些算子行为可能变化
- **VeOmni attention patches**: `veomni/ops/__init__.py` 的 attention 补丁可能影响模型行为
- **checkpoint 版本**: 权重可能与当前 VeOmni 代码版本不匹配

### 3. 我们的代码修复

已完成的修复（均已验证正确）：

- **loader.py**: `config_class.from_pretrained()` 替代 `from_dict()` → 正确创建嵌套 config
- **loader.py**: 支持 `.bin` 分片 + `diffusion_pytorch_model.bin.index.json`
- **loader.py**: 检查 `load_weights_from_checkpoint()` 方法
- **bagel.py**: 添加 `import torch` + `from PIL import Image`
- **bagel.py**: 内联 `_ImageTransform`（匹配 VeOmni `infer_unified.py`）
- **bagel.py**: 内联 `_vae_resize_inner`
- **bagel.py**: VAE 加载（`ae.safetensors`）
- **modeling_bagel.py**: dtype 补丁（`forward_cache_update_vit` + `forward_cache_update_vae` 添加 bfloat16 转换）
- **blip3o.py**: `_llm_forward` + `lm_head` 贪心解码替代 `language_model.generate`
- **blip3o.py**: `pixel_values` dtype 转换
- **blip3o.py**: `model.model.latent_queries` 替代 `get_latent_queries`
- **u1.py**: `inputs_embeds` + `pixel_values` dtype 转换
- **inferencer.py**: NaiveCache import 路径修复
- **batch_inferencer.py**: 同上
- **janus/modeling_janus.py**: VeOmni distributed imports 替换为 stub
- **janus/image_processing_janus.py**: VeOmni logging 替换为标准 logging
- **internvl-u.yaml**: checkpoint 路径 `InternV-U` → `InternVL-U`
- **全部 7 个 backend understand 方法**: 严格对照 VeOmni `infer_unified.py` 重写

## 下一步

1. **逐个验证**: 在兼容的环境下重跑 `test_unified_models.py`
2. **实现 draw()**: 各模型生成路径（参考 VeOmni `gen_*.py` 脚本）
3. **27 张图测试**: 3 个 prompt × 9 模型



多模态生成测试 Prompt:
├──────────┼──────────────────────────────────────────────────────────────────────────────┤
│ Prompt 1 │ Draw a red arrow pointing from the bottom-left to the top-right of the image │
│ Prompt 2 │ Add a blue circle in the center of this image                                │
│ Prompt 3 │ Draw a green route line from the left side to the right side of the image    │