# 00 · 概览：目标与关键设计决策

---

## 1. 项目目标

MapSpatial-EvalKit 在一套统一的数据与评测口径下，跑通并对比两类模型在**户外地图空间理解**任务上的表现：

| 类别 | 数量 | 代表 |
|---|---|---|
| 纯多模态理解模型 | 14 | Qwen3-VL、Qwen2.5-VL、InternVL3、GLM-4.6V、Step3-VL、MiMo-Embodied、SenseNova-SI、Cambrian-S、ViLaSR、Spatial-MLLM |
| 多模态生成+理解统一模型 | 6 | Bagel、ThinkMorph、BLIP3o、SenseNova-U1、LatentUM、Janus-Pro |

### 核心科学问题

> **让模型生成中间图像（视觉思维链），是否真的提升空间理解准确率？**

这决定了整个架构。要回答它，必须能做三向对比：

| 条件 | 含义 |
|---|---|
| **不画** | 统一模型退化成普通 VLM，直接作答 |
| **模型自主画** | 模型在思维链里自行决定何时生成中间图 |
| **强制画** | 策略层要求每题都先产出一张中间图 |

而且必须能**审计画出来的图**——否则「画得对不对」和「答得对不对」哪个是瓶颈，无从判断。这一条直接否决了「返回值是字符串」的设计。

---

## 2. 任务与数据

数据来自 `/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building`：

- 标签：`data-jsonl/{view}/{task}/{variant}.jsonl` —— 3 视图 × 4 任务 × 2 变体 = 24 个文件
- 图像：`data/benchmark_images_t{1..4}/<case_id>/<scheme>/*.png`

| 任务 | 类型 | question_type | 样本数 |
|---|---|---|---|
| T1 | spatial_relation | `direction` | 3029 |
| T2 | distance_aware_measurement | `nearest_point`、`composite_route_distance` | 5760 |
| T3 | region_counting | `segment_building_count` | 6665 |
| T4 | path_reasoning | `route_validity`、`waypoint_ordering` | 2096（blank 视图缺失） |

- 视图：`sat`（卫星）/ `webrd04`（路网）/ `blank`（空白底图）
- 变体：`direct`（仅原图）/ `oracle`（带标注辅助图）
- 全部为 A–D 四选一，指标 `exact_match`

**注意**：T4 `route_validity` 每条样本带 **4 张图**（4 个候选路线选项各一张）。这是多图支持的硬需求，不是可选项。详见 [02-data-pipeline.md](./02-data-pipeline.md)。

---

## 3. 五个关键设计决策

每个决策都附了依据（来自现有代码的实证），便于后续 review 时判断是否仍然成立。

---

### 决策 1：独立项目，借鉴 VLMEvalKit 的约定而非 fork 它

**结论**：新建 MapSpatial-EvalKit，采用 VLMEvalKit 的 message 格式、`build_prompt` hook、增量续跑、条带切分等约定；但**不 fork 框架本体**。

**依据**：

VLMEvalKit（v0.2rc1）的约定确实成熟，值得借鉴：

| 借鉴项 | 来源 |
|---|---|
| `message = list[{"type","value"}]` 交错格式 | `vlmeval/vlm/base.py:64-99` |
| `use_custom_prompt` / `build_prompt` 覆盖 hook | `base.py:14-37` |
| 增量 pickle 续跑（每 10 条 dump） | `inference.py:167-189` |
| torchrun 条带切分 `range(rank, N, world_size)` | `inference.py:102` |
| 构造模型前 unset `WORLD_SIZE` 阻止 HF 自动 TP | `inference.py:134` |

但框架本体有三个不适合直接继承的问题：

1. **eager import 全部模型。** `vlmeval/vlm/__init__.py` 无条件 `from .<file> import <Class>` 导入 80+ 模型文件，`config.py` 组装 ~551 个 `partial`。我们只要 20 个模型，不该背这个导入成本和依赖面。

2. **无批量推理抽象。** `generate_inner_batch` 和 `supports_batch` 在整个仓库 **0 匹配**。

3. **judge 选择是 15 个 `listinstr` 的 if/elif**（`run.py:362-404`），加数据集要改主流程。

框架本体约 10k LOC，其中我们真正需要的约定不到 500 行。重写比继承干净。

---

### 决策 2：`Prediction` 是结构化对象，不是字符串

**结论**：推理返回值必须携带 `generated_images` 和 `trace`。

**依据**——这是 ThinkMorph fork 的实证教训。

VLMEvalKit 基类契约是 `generate_inner(...) -> str`。ThinkMorph 生成了中间图之后，只能存盘并把路径编码进字符串（`vlmeval/vlm/ThinkMorph.py:417-434`）：

```python
out_img_path = os.path.join(self.save_dir, f"thinkmorph_out_{uuid.uuid4().hex[:8]}_{idx}.jpg")
out_item.save(out_img_path)
results.append(f"[Image: {out_img_path}]")
return "\n".join(results)
```

后果全部是我们无法接受的：

| 问题 | 后果 |
|---|---|
| 文件名是 `uuid8 + idx`，**不含 sample id** | 部分重跑后无法把图对回样本 |
| 评测端只看到路径字符串 | 无法审计中间图质量 —— **直接否决核心科学目标** |
| 多进程写同一 `save_dir` | 产物无法合并 |
| 无清理逻辑（只有 `assert save_dir is not None`） | 重跑漏产物 |

所以：

```python
@dataclass
class Prediction:
    text: str
    generated_images: list[Path] = ()   # 命名含 sample_id，可追溯
    trace: list[TraceStep] = ()         # 每轮的输入/输出/耗时
    error: str | None = None
    meta: dict = ...                    # 策略名、轮数、是否触发生成
```

**好消息**：VLMEvalKit 里有半成品逃生门。`inference.py:258-259` 的 `_is_structured_record` 已支持返回 `{"prediction":..., "extra_records":...}`。我们把这个 seam 扶正成一等契约，而不是学 ThinkMorph 编码字符串。

---

### 决策 3：Backend × Strategy 正交

**结论**：Backend 声明**能力**，Strategy 决定**如何编排能力**。两者正交组合。

**依据**：如果做成 `UnderstandingBackend` / `GenerationBackend` 两套并列的类型，runner 和结果 schema 会分叉，跨模型的准确率就不可比了。而正交之后，`Qwen3-VL + direct` 和 `Bagel + native-interleave` 产出完全一致的 `Prediction` schema。

```python
class Capabilities(NamedTuple):
    batch: bool              # 能否真批推理
    draw: bool               # 能否生成图像
    native_interleave: bool  # 是否有原生交错推理循环
    max_images: int
    video: bool
```

三种策略：

| Strategy | 适用 | 说明 |
|---|---|---|
| `direct` | 全部 20 个模型 | 直接作答 |
| `native_interleave` | `caps.native_interleave` | 委托模型原生的交错循环（单一 KV-cache 跨轮） |
| `external_draw` | `caps.draw` | 外部编排 draw → understand |

能力检查在**启动时** fail-fast，不允许跑到一半才报错。

详见 [01-architecture.md](./01-architecture.md) 与 [04-strategies.md](./04-strategies.md)。

---

### 决策 4：视觉 CoT 两种触发方式都实现

**结论**：模型自触发与策略强制触发都要实现，且可配置。

**依据**：这是消融实验的完整形式，能回答「模型自主判断」vs「强制」vs「不画」三者的差异。

同时要认识到：**这两者不是同一种机制的参数差异，而是两种不同的实现路径。**

ThinkMorph 的原生循环（`vlmeval/vlm/thinkmorph/inferencer.py:260-348`）：

```python
while rounds < max_rounds:
    gen_text = self.gen_text(gen_context, ...)
    gen_context = self.update_context_text(gen_text, gen_context)
    if "<image_start>" in gen_text:                 # ← 模型自己触发
        img = self.gen_image(image_shapes, gen_context, cfg_text_scale=..., ...)
        img_input = self.vae_transform.resize_transform(pil_img2rgb(img))
        gen_context = self.update_context_image(img_input, gen_context, vae=...)
        rounds += 1
    else:
        break
```

关键：**单一 KV-cache 跨轮保持**。这与「外部调 draw() 再调 understand()」不等价——后者丢失 context。

所以结果里必须记录用了哪条路径（`Prediction.meta.strategy`），否则数字不可比。

注意 `"<image_start>" in gen_text` 是**子串匹配**，很脆：模型换个措辞就静默跳过生成。我们的实现要把标记做成 per-model 可配置，并**记录是否实际触发**，这样才能区分「模型选择不画」和「标记没匹配上」。

---

### 决策 5：单一环境 + monkey-patch 兼容层

**结论**：所有 20 个模型跑在同一个 Python 环境；依赖冲突用配置调参 → monkey-patch → vendor → shim 四级手段解决。

**依据**：多环境的成本不会消失，只会转嫁给使用者，实际结果是没人用。

而且这个模式在你们代码库里已有先例。`gate2building/eval/backends.py:524-575` 的 `_patch_custom_model_compat()` 就是用 3 个补丁换取「InternVL-custom / MiniCPM-V 与其他模型共存」：

```
1. transformers.PreTrainedModel._finalize_model_loading  → 补 all_tied_weights_keys
2. transformers.integrations.accelerate._init_infer_auto_device_map → 同上
3. torch.Tensor.item → meta device 返回 0.0（绕开 InternVisionEncoder.linspace().item()）
```

我们把它从 backend 私有 hack 提升为一等组件 `mapspatial/compat/`，要求补丁**幂等、自失效、窄、声明式**。

详见 [07-environment.md](./07-environment.md)。

---

## 4. 从 gate2building 继承什么，修正什么

`gate2building/eval/` 是可用的实现，14 个纯理解模型已跑出结果。但有若干问题，迁移时必须一并修掉（完整清单见 [08-roadmap.md](./08-roadmap.md)）。

### 4.1 值得继承

| 项 | 位置 |
|---|---|
| **真批量 vLLM** —— 一次 `llm.generate(32条)` | `backends.py:484` |
| 惰性导入 + `*_AVAILABLE` 标志（20 个 backend 解耦的正确姿势） | `backends.py:17-134` |
| 8 个 backend 的可用加载逻辑 | `backends.py` 全文 |
| 数据/结果 schema、preflight 图像校验 | `run_vlm_jsonl_inference_v5.py:97-127` |

**注意**：这里 gate2building 反而**强于** VLMEvalKit。后者每次只提交 1 条请求（`qwen3_vl/model.py:403` 的 `[req]`），且在循环里 `torch.cuda.empty_cache()`（`inference.py:190`）直接冲掉 KV cache —— `max_num_seqs=8` 永远跑不满，等于白装 vLLM。

### 4.2 必须修正

| 问题 | 位置 | 影响 |
|---|---|---|
| `<image>`/`<video>` 占位符处理在 8 个 backend 各写一遍，行为不一致 | 全文 | 收敛到统一 `messages` 模块 |
| URL 下载 5 处重复 3 种策略；`SenseNovaU1Backend` 完全没有 → 传 URL 直接崩 | 全文 | 收敛到统一 `media` 模块 |
| 视频抽帧 4 处重复，帧数上限不一致（U1 是 8，其他 16），读取器 cv2/decord/imageio 三种 | 全文 | 同上 |
| `_load_gemma4` 引用从未 import 的 `GEMMA4_AVAILABLE` → `NameError` | `backends.py:792` | 修掉 |
| `extract_answer(allow_multi=True)` 参数**函数体完全没用**，多选实际是坏的；硬编码只认 A–D | `answer_extraction.py:11-55` | 重写 |
| 续跑靠 `id` 集合 + append 模式，**无写入去重** → 输入顺序一变就产生重复行 | `run_vlm_jsonl_inference_v5.py:78-94` | 改为原子写 + 去重 |
| `summary.json` 不聚合 `skipped`，只反映本次运行量 | `:449-451` | 重新设计指标输出 |
| `RunConfig.num_workers` / `batch_size` 在 backends 里是死字段 | `config.py` | 清理 |
| per-backend 配置污染顶层（`bagel_mode`、`vilasr_max_steps`、`spatial_mllm_model_type`…） | `config.py` | 改嵌套配置 |
| **`run_api_inference_v5.sh` 硬编码 3 个 API key** | `run_api_inference_v5.sh:18-20` | 全部改环境变量 |

### 4.3 单模型只吃一张卡的问题

gate2building 的并行策略是「模型轮询分配到 GPU」（`run_inference_v5.sh`），14 个模型分 4 卡串行跑完。单个模型只用 1 张卡。

VLMEvalKit 的条带切分（`inference.py:102`）更好：

```python
sheet_indices = list(range(rank, len(dataset), world_size))
```

让单模型吃满 8 卡。这是要借鉴的。

---

## 5. 参考代码定位

| 路径 | 借鉴内容 |
|---|---|
| `SpatialIntelligence-gate2building/eval/` | 真批量 vLLM、惰性导入、8 个 backend 加载逻辑、数据/结果 schema、preflight |
| `outdoor-spatial-intelligence-scripts/VLMEvalKit`（v0.2rc1，25M，无 ThinkMorph） | message 格式、`build_prompt` hook、续跑、条带切分、unset WORLD_SIZE；**以及 Cambrian-S / Spatial-MLLM / SenseNova-SI / ViLaSR 的模型类**（比 gate2building 那份干净） |
| `VLMEvalKit_Thinkmorph` | `vlm/thinkmorph/inferencer.py`（374 行，交错循环）与 `batch_inferencer.py`（1072 行，批量 + packed KV cache + CFG 并行）—— **值得 vendor，重写不划算** |
| `generative-spatial-drafts/ablation_experiment/VeOmni` | 6 个统一模型的 modeling 代码与加载链（`get_model_config` → `get_model_class` → `init_empty_weights` → `load_model_weights`） |

**已知缺口**：README 提到的 `draw_to_understand` 模块（`VeOmniBagelGenerationBackend` 等 5 个生成 backend）**在磁盘上不存在**。已决定在本项目内重写，直接包装各模型原生生成方法。详见 [05-veomni-integration.md](./05-veomni-integration.md)。

---

## 6. 下一步

阅读顺序建议：

1. [01-architecture.md](./01-architecture.md) —— 数据契约与正交模型（实现的地基）
2. [07-environment.md](./07-environment.md) —— 单一环境约束（影响每个 backend）
3. [08-roadmap.md](./08-roadmap.md) —— 分阶段计划
