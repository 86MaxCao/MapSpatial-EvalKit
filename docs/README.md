# MapSpatial-EvalKit 设计文档

MapSpatial-EvalKit 是一个面向**户外地图空间理解**的多模态推理与评测项目。它需要在同一套数据、同一套评测口径下，同时跑通两类模型：

- **纯多模态理解模型**（14 个，如 Qwen3-VL / InternVL3 / GLM-4.6V / Cambrian-S / Spatial-MLLM）
- **多模态生成+理解统一模型**（6 个，Bagel / ThinkMorph / BLIP3o / SenseNova-U1 / LatentUM / Janus-Pro）

后者能在推理过程中**生成中间图像**（视觉思维链），这是本项目要验证的核心假设：*让模型画出中间草图，是否真的提升空间理解准确率？*

---

## 文档索引

| 文档 | 内容 | 读者 |
|---|---|---|
| [00-overview.md](./00-overview.md) | 背景、目标、5 个关键设计决策及其依据 | 所有人先读这个 |
| [01-architecture.md](./01-architecture.md) | 数据契约（Message/Prediction）、Backend × Strategy 正交模型、目录结构 | 实现者必读 |
| [02-data-pipeline.md](./02-data-pipeline.md) | 数据 schema、加载、prompt 构造、preflight 校验 | 实现者 |
| [03-backends.md](./03-backends.md) | 20 个模型的 backend 设计、能力矩阵、vLLM 真批量方案 | 实现者 |
| [04-strategies.md](./04-strategies.md) | direct / native-interleave / external-draw 三种推理策略 | 实现者、实验设计者 |
| [05-veomni-integration.md](./05-veomni-integration.md) | 6 个统一模型的接入方式与生成路径重写 | 实现者 |
| [06-runner-eval.md](./06-runner-eval.md) | runner、断点续跑、多卡并行、答案抽取与指标 | 实现者 |
| [07-environment.md](./07-environment.md) | 统一环境构建方案、依赖冲突与风险 | 实现者、运维 |
| [08-roadmap.md](./08-roadmap.md) | 分阶段实施计划、参考代码清单、已知 bug 修复清单 | 项目管理 |

---

## 一句话架构

```
数据 (data-jsonl)  →  Message[]  →  Strategy  →  Backend  →  Prediction  →  评测
                       ↑ 交错的                  ↑ 决定怎么     ↑ 提供能力    ↑ 结构化，
                       text/image 列表            用能力        (understand/  含中间图
                                                                draw/batch)   与 trace
```

**Backend 提供能力，Strategy 决定如何编排能力。** 这两个维度正交，因此「Qwen3-VL + direct」和「Bagel + native-interleave」产出的结果 schema 完全一致，准确率天然可比。

---

## 关键约束（务必先了解）

1. **`Prediction` 不是字符串。** 它必须携带 `generated_images` 和 `trace`，否则视觉思维链无法审计——这是本项目的核心科学目标，见 [00-overview.md#决策2](./00-overview.md)。

2. **单一 Python 环境。** 所有 20 个模型跑在一个基于 micromamba `latest` 派生的新环境里。跨环境 RPC 方案已被否决，见 [07-environment.md](./07-environment.md)。

3. **vLLM 必须真批量。** 参考项目（VLMEvalKit）每次只提交 1 条请求还在循环里清 CUDA 缓存，等于白装 vLLM。见 [03-backends.md#vllm](./03-backends.md)。

4. **视觉 CoT 有两种触发方式，都要实现且可配置。** 模型自触发（`<image_start>` 标记）和策略强制触发，用于三向消融对比。见 [04-strategies.md](./04-strategies.md)。

---

## 参考代码位置

本项目大量借鉴以下已有实现。**这些是参考源，不是依赖**：

| 路径 | 用途 |
|---|---|
| `SpatialIntelligence-gate2building/eval/` | 8 个 backend 的可用实现、真批量 vLLM、数据/结果 schema |
| `outdoor-spatial-intelligence-scripts/VLMEvalKit` | 上游 v0.2rc1。message 格式、续跑、条带切分；Cambrian-S / Spatial-MLLM / SenseNova-SI / ViLaSR 模型类 |
| `generative-spatial-drafts/ablation_experiment/VLMEvalKit_Thinkmorph` | ThinkMorph fork。`vlm/thinkmorph/inferencer.py` 与 `batch_inferencer.py` 是交错推理的可用实现，值得 vendor |
| `generative-spatial-drafts/ablation_experiment/VeOmni` | 6 个统一模型的 modeling 代码与加载链 |

数据：
- 标签 `SpatialIntelligence-gate2building/data-jsonl`（24 个 JSONL，3 视图 × 4 任务 × 2 变体）
- 图像 `SpatialIntelligence-gate2building/data`（`benchmark_images_t{1..4}/`）
