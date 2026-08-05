# 05 · 统一模型接入

> 6 个多模态生成+理解统一模型（Bagel / ThinkMorph / BLIP3o / SenseNova-U1 / LatentUM / Janus-Pro）的接入方案。

---

## 1. 现状：可复用的比想象中少

### 1.1 VeOmni 侧的真实状态

VeOmni README 描述的能力与代码实际状态有落差。核实结果：

| README 声称 | 代码实际 |
|---|---|
| `infer_unified.py --mode generate` 支持生成 | **是 stub**，只打印 "use model-specific inference scripts"（`tasks/infer/infer_unified.py:405-408`） |
| 6 个模型都适配 | **Janus 不在 CLI**（`MODEL_TYPE_TO_CHECKPOINT` 只有 5 个，`:42-48`），`UNDERSTAND_DISPATCH` 也没有它 |
| 统一推理接口 | 5 个理解函数是**互不相干的手写代码**，参数形状完全不同 |
| — | U1 / LatentUM / BLIP3o 用**手写逐 token 贪心循环**，连 `.generate()` 都没用（`:236-262` 等） |
| — | checkpoint 路径**硬编码**在 dict 里（`:42-48`） |

唯一像样的共享层是加载链：

```python
config = get_model_config(model_path, trust_remote_code=True)   # veomni/models/loader.py
model_cls = get_model_class(config)                             # registry 查表
with init_empty_weights():
    model = model_cls._from_config(config=config)
model = model.to_empty(device=device).to(torch.bfloat16)
load_model_weights(model, model_path)
model.eval()
```

这条链可复用。

### 1.2 `draw_to_understand` 不存在

README 的示例：

```python
from draw_to_understand.models.veomni_bagel import VeOmniBagelGenerationBackend
```

**该模块在磁盘上找不到。** `generative-spatial-drafts/` 下只有 `ablation_experiment/`。测试脚本靠 `sys.path.insert` 指向 `VeOmni/../..`，但那里没有 `draw_to_understand/`。

只能从测试脚本的调用点反推出接口：

| 类 | 调用点 | 签名（反推） |
|---|---|---|
| `VeOmniBagelGenerationBackend` | `tasks/test_bagel_gen_inference.py:38-45` | `(model_path, device, dtype, num_steps, cfg_text_scale, cfg_img_scale)`；`draw(input_image, prompt, seed)` |
| `VeOmniThinkMorphGenerationBackend` | `test_it2i_bagel.py:151` | 同上 |
| `VeOmniBlip3oGenerationBackend` | `tasks/test_blip3o_gen_inference.py:30-38` | `(model_path, device, dtype, guidance_scale, dit_guidance_scale, dit_num_steps, unet_num_steps)` |
| `VeOmniU1GenerationBackend` | `test_it2i_u1.py:97` | `draw(input_image, prompt, seed)` |
| `VeOmniLatentUMGenerationBackend` | `test_it2i_latentum.py:101-109` | `(model_path, decoder_path, device)`；`draw(..., context_images, actions, seed, temperature, top_k, top_p)` |
| （无 Janus 生成 backend） | — | — |

**决策：在本项目内重写**，直接包装各模型原生生成方法。理由：源码不可得，无法 vendor；而原生方法在 VeOmni 的 modeling 文件里是齐全的。

---

## 2. 接入策略：vendor modeling，不装 veomni 包

### 2.1 不装 veomni 包的理由

| 理由 | 依据 |
|---|---|
| 它是**训练框架** | `build_foundation_model`（`veomni/models/auto.py:106-273`）需要 `OpsImplementationConfig` |
| 带一堆无关重依赖 | FSDP2、专家并行、Ulysses 序列并行、`liger-kernel`、`quack-kernels`… |
| **transformers 硬 pin `==5.9.0`** | `pyproject.toml:170-172`。与我们统一环境的其他约束（尤其 vLLM）直接冲突 |
| 我们只要 modeling 代码 | 6 个模型的 `modeling_*.py` + `configuration_*.py` |

### 2.2 vendor 范围

```
mapspatial/vendor/
├── veomni_modeling/                 # 从 VeOmni 抽取
│   ├── ORIGIN.md                    #   repo + commit + 日期 + 抽取理由
│   ├── PATCHES.md                   #   逐条改动
│   ├── _loader.py                   #   精简版加载链（不依赖 OpsImplementationConfig）
│   ├── bagel/                       #   modeling_bagel.py + configuration_bagel.py
│   ├── thinkmorph/                  #   configuration 复用 bagel modeling
│   ├── blip3o/ neo_chat/ latentum/ janus/
│   └── movqgan/                     #   Bagel 生成路径的 VAE
│
└── bagel_interleave/                # 从 VLMEvalKit_Thinkmorph 抽取
    ├── ORIGIN.md  PATCHES.md
    ├── inferencer.py                #   374 行，交错循环
    ├── batch_inferencer.py          #   1072 行，批量 + packed KV + CFG 并行
    └── data/transforms.py
```

两个 vendor 来源，用途不同：

- `veomni_modeling` —— 模型定义与权重加载
- `bagel_interleave` —— Bagel 系的交错推理循环（真 engineering，重写不划算）

**注意可能的重复**：`VLMEvalKit_Thinkmorph/vlmeval/vlm/thinkmorph/modeling/` 里也有一份 Bagel/Qwen2/Siglip modeling。实施时需比对两份哪个更适配（VLMEvalKit 那份已经在推理场景验证过，可能更省事）。列入待确认清单。

---

## 3. 每个模型的生成路径

### 3.1 已定位的原生方法

| 模型 | 生成方法 | 位置 |
|---|---|---|
| Bagel | `generate_image(...)` | `modeling_bagel.py:2082` |
| Bagel | `chat(...)`（高层理解，带 KV cache） | `:2306-2371` |
| Bagel | `generate_text(...)` | `:1745` |
| SenseNova-U1 | `it2i_generate(...)`（像素空间 flow matching + CFG） | `modeling_neo_chat.py:1741` |
| SenseNova-U1 | `extract_feature(pixel_values, gen_model, grid_hw)` | `:1342` |
| BLIP3o | DIT + VAE 解码路径 | `modeling_blip3o.py`（待精确定位） |
| LatentUM | `intern_gen` / 需独立 decoder ckpt | `modeling_latentum.py`（待精确定位） |
| Janus | `prepare_gen_img_embeds(...)` + VQ-16 采样 | `modeling_janus.py:1235` |
| Janus | `prepare_inputs_embeds(...)`（理解路径） | 同文件 |
| ThinkMorph | **完全复用 Bagel 类** | `thinkmorph/__init__.py:11-15` 注册指向 `BagelForConditionalGeneration` |

标「待精确定位」的需要实施时读代码确认签名。文档不硬猜参数名。

### 3.2 统一到本项目的 Backend 接口

每个 veomni backend 实现 `understand` + `draw`（+ 可选 `interleave`）：

```python
@register("veomni_bagel")
class BagelBackend(Backend):
    caps = Capabilities(batch=True, draw=True, native_interleave=True,
                        max_images=..., video=False)

    def understand(self, messages, **gen_kw) -> list[Prediction]:
        # 走 vendor 的 batch_inferencer，understanding_output=True
        # （对应 ThinkMorph.py 的 understanding_output 模式）

    def draw(self, context, instruction, **kw) -> Image.Image:
        # 包装 generate_image(...)

    def interleave(self, message, *, max_rounds, marker, **kw) -> Prediction:
        # 走 vendor 的 InterleaveInferencer.interleave_inference
        # understanding_output=False → 全生成模式
```

### 3.3 `understanding_output` 开关

ThinkMorph 的实现里有个关键开关（`ThinkMorph.py:134-152`）：

```python
if understanding_output:
    inference_hyper = dict(max_think_token_n=..., do_sample=..., text_temperature=..., max_rounds=...)
else:
    inference_hyper = dict(   # 全生成：加 CFG 与扩散参数
        ..., cfg_text_scale=..., cfg_img_scale=..., cfg_interval=...,
        timestep_shift=..., num_timesteps=..., cfg_renorm_min=...,
        cfg_renorm_type=..., enable_taylorseer=..., noise_seed=...,
    )
```

`understanding_output=True` 绕过图像生成，只跑语言头 —— 这正好对应我们的 `direct` 策略。
`understanding_output=False` 跑完整交错 —— 对应 `native_interleave`。

映射关系：

| 本项目策略 | `understanding_output` |
|---|---|
| `direct` | `True` |
| `native_interleave` | `False` |
| `external_draw` | `True`（作答阶段）+ 单独调 `draw()` |

---

## 4. 理解路径：修正 VeOmni 的手写贪心循环

### 4.1 问题

`infer_unified.py` 里 U1 / LatentUM / BLIP3o 的理解路径是**手写逐 token 循环**（`:236-262` 等）：

```python
outputs = model.language_model(input_ids=input_ids, attention_mask=attention_mask)
logits = outputs.logits if hasattr(outputs, "logits") else model.language_model.lm_head(outputs.last_hidden_state)
next_token = torch.argmax(logits[0, -1], dim=-1).item()
generated = [next_token]
# … 逐 token 反馈
```

这是变通做法，代价：

- 慢（无 KV cache 复用）
- 只支持贪心（不支持 temperature/top-p，我们的 config 需要）
- 无法批量

而 `model.language_model` 是标准的 `Qwen3ForCausalLM` 之类，本身支持 `.generate()`。VeOmni 之所以手写，很可能是 `inputs_embeds` 的视觉 token 注入没打通。

### 4.2 正确路径

Janus 的规范做法已在测试脚本里（`tasks/test_janus_veomni_understanding.py:118-190`）：

```python
inputs_embeds = model.prepare_inputs_embeds(
    input_ids=inputs["input_ids"],
    pixel_values=inputs["pixel_values"],
    image_mask=inputs["image_mask"],
)
outputs = model.language_model.generate(
    inputs_embeds=inputs_embeds, attention_mask=..., max_new_tokens=512
)
```

对 U1，对应零件是 `extract_feature(...)`（`modeling_neo_chat.py:1342`）+ 手工拼 `inputs_embeds`。

**实施要求**：每个模型都走 `.generate()`，不用手写循环。若某模型确实打不通 `inputs_embeds` 注入，必须在 `PATCHES.md` 里记录尝试过什么、为什么退回，不允许默默用贪心循环（那会让 temperature 配置静默失效）。

### 4.3 多图支持是硬要求

T4 route_validity 每题 4 图。各模型的多图能力需实测确认：

| 模型 | 已知线索 |
|---|---|
| Bagel | `chat(images=[...])` 接受列表；`InterleaveInferencer` 支持多图但要求 image-initial |
| U1 | `pixel_values` 拼接 + `grid_hw`，看似支持多图 |
| BLIP3o / LatentUM / Janus | 未知，需实测 |

若某模型上限 < 4，按 [02-data-pipeline.md §4.3](./02-data-pipeline.md) 的规则处理（显式拼图或跳过，记录到 meta），**不允许静默截断**。

---

## 5. 各模型的图像预处理差异

这是 6 个模型无法共享代码的主因。已知：

| 模型 | 预处理 |
|---|---|
| Bagel | `ImageTransform(max=980, min=224, patch_size=14)`；resize 后归一化到 `[-1,1]`（`(x-0.5)/0.5`）；BICUBIC。生成路径另有 `_vae_resize(max=1024, min=512, stride=16)` |
| U1 | `load_image_native(p) → (pixel_values, grid_hw)` |
| LatentUM | resize 到 448×448 |
| Janus | `JanusImageProcessor(image_size=384, min_size=14, mean=[0.5]*3, std=[0.5]*3)` + `JanusProcessor(image_tag="<image_placeholder>", num_image_tokens=576)` |
| BLIP3o | `model.visual` + `model.visual_projector`（细节待确认） |
| ThinkMorph | 同 Bagel |

因此每个 veomni backend 有自己的 `_preprocess`，共享的只有加载链和 `media.py` 的图像读取。**不要试图抽象统一的预处理器**——差异是本质的，强行统一会引入错误。

---

## 6. Tokenizer / Processor

| 模型 | 需要 |
|---|---|
| Bagel / ThinkMorph | `AutoTokenizer` + 手工添加特殊 token（`<\|im_start\|>`、`<\|im_end\|>`、`<\|vision_start\|>`、`<\|vision_end\|>`），构造 `new_token_ids` dict（`infer_unified.py:142-161`） |
| U1 | `AutoProcessor`（VeOmni 里 fallback 到 `"Qwen/Qwen3-VL-8B"`，**可疑，需核实正确的 processor 来源**） |
| Janus | `LlamaTokenizerFast` + `JanusProcessor` |
| 其余 | 待确认 |

U1 那个 fallback 特别值得警惕：`infer_unified.py:218-230` 用 `config._name_or_path if hasattr(...) else "Qwen/Qwen3-VL-8B"`。若实际走了 fallback，chat template 可能与训练时不一致，静默降低准确率。实施时必须确认。

---

## 7. 交叉验证

VeOmni README 声称 6 个模型的理解输出与官方实现 100% 对齐（如 Bagel 20/20 exact match）。这个声明值得独立验证，因为：

- 我们要 vendor 它的 modeling 代码，正确性直接影响结论
- 我们会改动加载链（去掉 `OpsImplementationConfig` 依赖）
- 我们会把手写贪心循环换成 `.generate()`

验证手段：对 SenseNova-U1，同时接入两条路径

- `veomni_u1` —— vendor 的 VeOmni modeling
- `sensenova_u1_official` —— 官方 `sensenova_u1` 包（gate2building `backends.py:1662-1798` 已有实现）

在小样本上比对输出。若不一致，以官方为准并记录差异。

---

## 8. 待确认清单

诚实记录不能靠读文档确定的点，实施阶段逐项实测：

| # | 待确认 | 影响 |
|---|---|---|
| 1 | BLIP3o / LatentUM 生成方法的精确签名 | `draw()` 实现 |
| 2 | 6 个模型各自的 `max_images` | t4 是否需降级 |
| 3 | U1 / BLIP3o / LatentUM 是否有原生交错循环 | `caps.native_interleave` |
| 4 | `inputs_embeds` + `.generate()` 能否替代手写贪心循环 | 速度与采样参数是否生效 |
| 5 | LatentUM 的 `decoder_path` 从哪来、是否已下载 | 能否跑 |
| 6 | Janus 的 v4 风格 API（`LlamaForCausalLM._from_config`，`modeling_janus.py:1219`）在当前 transformers 下是否可用 | 需要哪个 compat 补丁 |
| 7 | `VLMEvalKit_Thinkmorph/vlmeval/vlm/thinkmorph/modeling/` vs VeOmni 的 Bagel modeling，用哪份 | vendor 来源 |
| 8 | `batch_inferencer.validate_batch_inputs` 的 image-initial 约束如何适配 t4 的 text-initial | t4 route_validity 能否跑 |
| 9 | U1 的正确 processor 来源（非 Qwen3-VL fallback） | 准确率 |
| 10 | 各模型是否需要 compat 补丁 | 单一环境可行性 |

每项确认后回填 [03-backends.md](./03-backends.md) 的能力矩阵。

---

## 9. 相关文档

| 主题 | 文档 |
|---|---|
| Backend 接口定义 | [01-architecture.md](./01-architecture.md) |
| 能力矩阵 | [03-backends.md](./03-backends.md) |
| 三种策略如何使用 `draw` / `interleave` | [04-strategies.md](./04-strategies.md) |
| vendor 纪律与 compat 补丁 | [07-environment.md](./07-environment.md) |
| 实施顺序 | [08-roadmap.md](./08-roadmap.md) |
