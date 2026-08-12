# MapSpatial-EvalKit 设计文档

MapSpatial-EvalKit 是一个面向**户外地图空间理解**的多模态推理与评测工具包。它在统一的数据格式、推理接口和评测口径下，支持运行和比较多种视觉语言模型及视觉生成模型。

- **多模态理解模型**（17 个）：Qwen2-VL、Qwen2.5-VL、Qwen3-VL、InternVL3、GLM-4.6V、Step3-VL、MiMo-Embodied、Cambrian-S、ViLaSR、Spatial-MLLM、SenseNova-SI，以及 Gemini 3 Flash、Qwen3.5 Plus、Qwen3.6 Plus API 模型。
- **多模态生成+理解统一模型**（10 个）：Bagel、ThinkMorph、BLIP3o、SenseNova-U1、LatentUM、Janus-Pro、InternVL-U、JoyAI-Image、Ming-UniVision、Show-o2。

当前仓库包含 **27 个模型配置**。配置文件位于 `configs/models/`，实际运行还取决于对应模型权重、API 凭据和可选依赖是否已准备好。

后者能在推理过程中**生成中间图像**（视觉思维链），这是本项目要验证的核心假设：*让模型画出中间草图，是否真的提升空间理解准确率？*

---

## 文档索引

| 文档 | 内容 | 读者 |
|---|---|---|
| [00-overview.md](./docs/00-overview.md) | 背景、目标、5 个关键设计决策及其依据 | 所有人先读这个 |
| [01-architecture.md](./docs/01-architecture.md) | 数据契约（Message/Prediction）、Backend × Strategy 正交模型、目录结构 | 实现者必读 |
| [02-data-pipeline.md](./docs/02-data-pipeline.md) | 数据 schema、加载、prompt 构造、preflight 校验 | 实现者 |
| [03-backends.md](./docs/03-backends.md) | backend 设计、能力矩阵、vLLM 真批量方案 | 实现者 |
| [04-strategies.md](./docs/04-strategies.md) | direct / native-interleave / external-draw 三种推理策略 | 实现者、实验设计者 |
| [05-veomni-integration.md](./docs/05-veomni-integration.md) | 统一模型的接入方式与生成路径重写 | 实现者 |
| [06-runner-eval.md](./docs/06-runner-eval.md) | runner、断点续跑、多卡并行、答案抽取与指标 | 实现者 |
| [07-environment.md](./docs/07-environment.md) | 统一环境构建方案、依赖冲突与风险 | 实现者、运维 |
| [08-roadmap.md](./docs/08-roadmap.md) | 分阶段实施计划与已知问题 | 项目管理 |

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

1. **`Prediction` 不是字符串。** 它必须携带 `generated_images` 和 `trace`，否则视觉思维链无法审计——这是本项目的核心科学目标，见 [00-overview.md#决策2](./docs/00-overview.md)。

2. **统一运行环境。** 本地模型和 API 模型通过统一的 runner 接口接入；本地模型建议使用同一 Python/micromamba 环境，并按需安装 vLLM、视频等可选依赖，见 [07-environment.md](./docs/07-environment.md)。

3. **vLLM 必须真批量。** vLLM backend 一次提交整批请求，不在推理循环中清空 CUDA cache，见 [03-backends.md#vllm](./docs/03-backends.md)。

4. **视觉 CoT 可配置。** 支持模型自触发和策略强制触发两种方式，用于消融对比，见 [04-strategies.md](./docs/04-strategies.md)。
