# 08 · 实施计划

> 分阶段路线、参考代码清单、必修 bug、待确认项。

---

## 1. 分阶段路线

每个阶段有明确的**可验证产出**。不允许「大爆炸式」一次实现全部再调试。

### 阶段 0：骨架 + 一个模型跑通

**目标**：端到端最小闭环，验证契约设计是否成立。

| 项 | 内容 |
|---|---|
| 环境 | 从 micromamba `latest` 克隆出 `mapspatial` |
| 类型层 | `types.py`：`Message` / `Prediction` / `TaskSample` / `Capabilities` |
| 共享模块 | `media.py`、`messages.py`、`compat/`（先只放已知的 2 个补丁） |
| 数据层 | `data/`：schema、loader、prompt、preflight |
| backend | 只做 `vllm`，**真批量** |
| 策略 | 只做 `direct` |
| runner | 续跑、原子写、单卡 |
| 评测 | `eval/answer.py` 重写、`eval/metrics.py` |

**验收**：`Qwen3-VL-8B × direct × sat/t1/direct` 的准确率与 gate2building 已有结果一致（1264/3029 附近）。

> 数字对不上就是契约或 prompt 构造有问题，此时发现代价最小。

### 阶段 1：铺开纯理解模型

| 项 | 内容 |
|---|---|
| backend | `transformers`（拆成子模块）、`api`、`cambrian`、`vilasr`、`spatial_mllm`、`sensenova_si` |
| 并行 | torchrun 条带切分 + 分片合并 |
| API 并发 | 样本级 worker pool，key 轮转加锁 |
| CLI | `doctor`、`preflight`、`report` |

**验收**：14 个纯理解模型全部 `doctor` 绿；至少 4 个模型的全量结果与 gate2building 对齐。

### 阶段 2：接入 Bagel 系（生成能力首次落地）

选 Bagel + ThinkMorph 先做，因为它们是**唯一有成熟交错推理实现**的（可 vendor）。

| 项 | 内容 |
|---|---|
| vendor | `bagel_interleave/`（inferencer + batch_inferencer）、`veomni_modeling/bagel/` |
| backend | `veomni_bagel`、`veomni_thinkmorph` |
| 策略 | `native_interleave`、`external_draw` |
| 落盘 | 中间图命名含 `sample_id`；`trace` 记录 |

**验收**：
- Bagel × 三种策略在 sat/t1 小样本（200 条）上跑通
- **人工检查 20 张生成的中间图是否合理** ← 这一步不能省。若生成图是噪声，后续全量跑是浪费

### 阶段 3：其余 4 个统一模型

BLIP3o / SenseNova-U1 / LatentUM / Janus。这 4 个没有成熟的交错实现，工作量最大、不确定性最高。

| 项 | 内容 |
|---|---|
| vendor | 对应的 `veomni_modeling/*` |
| 理解路径 | 用 `inputs_embeds` + `.generate()` 替代 VeOmni 的手写贪心循环 |
| 生成路径 | 包装各自原生方法（`it2i_generate` / DIT+VAE / `intern_gen` / VQ-16 采样） |
| 交叉验证 | `veomni_u1` vs `sensenova_u1_official` 输出比对 |

**验收**：`doctor` 20/20 全绿。

### 阶段 4：全量实验

| 项 | 内容 |
|---|---|
| 全量跑 | 14 × direct + 6 × 各自策略 |
| 汇总 | `mapspatial report` 产出对比表 |
| 归因 | 检查 `draw_rate`、`unconfident_extract`、`coverage` 三个健康指标 |

---

## 2. 参考代码清单

按「从哪抄什么」组织，避免实施时重新调研。

### 2.1 `SpatialIntelligence-gate2building/eval/`

| 借鉴内容 | 位置 |
|---|---|
| **真批量 vLLM**（整批一次 `generate`） | `backends.py:484` |
| vLLM 输入构造（qwen vs internvl/minicpm 两种风格） | `backends.py:418` |
| 惰性导入 + `*_AVAILABLE` 模式 | `backends.py:17-134` |
| transformers 兼容补丁（3 个，提升为 compat 层） | `backends.py:524-575` |
| API backend：多 key 轮转、按模型调图像压缩、退避重试 | `backends.py:187-356` |
| 各专用 backend 加载逻辑 | `sensenova_si:1121` `vilasr:1252` `cambrian:1344` `spatial_mllm:1475` `sensenova_u1:1662` |
| preflight 图像校验 | `run_vlm_jsonl_inference_v5.py:97-127` |
| 答案抽取的规则优先级（顺序对，实现要重写） | `answer_extraction.py:11-55` |

### 2.2 `outdoor-spatial-intelligence-scripts/VLMEvalKit`（v0.2rc1）

| 借鉴内容 | 位置 |
|---|---|
| 交错 message 格式 | `vlm/base.py:64-99` |
| `use_custom_prompt` / `build_prompt` hook | `vlm/base.py:14-37` |
| 条带切分 | `inference.py:102` |
| unset `WORLD_SIZE` 阻止 HF 自动 TP | `inference.py:134`、`run.py:54` |
| 增量续跑 | `inference.py:167-189` |
| 思维链切分（`SPLIT_THINK`） | `inference.py:300-326` |
| **Cambrian-S 模型类**（比 gate2building 干净） | `vlm/cambrian_s.py` |
| **Spatial-MLLM 模型类** | `vlm/spatial_mllm.py` |
| SenseNova-SI 各变体的映射 | `config.py:2545-2607` |
| ViLaSR（走 `Qwen2VLChat`，比独立实现简单） | `config.py:2523` |

该 checkout 已有 `spatial_related_models` / `sensenova_si_series` / `bagel_series` 分组（`config.py:2644`，注释 "add by EASI team"）——空间类模型的适配已有人做过一轮，**动手前先读**。

### 2.3 `VLMEvalKit_Thinkmorph`

| 借鉴内容 | 位置 |
|---|---|
| **交错推理循环**（vendor） | `vlm/thinkmorph/inferencer.py:260-348` |
| **批量交错 + packed KV + CFG 并行**（vendor） | `vlm/thinkmorph/batch_inferencer.py` |
| `understanding_output` 开关（对应我们的策略切换） | `vlm/ThinkMorph.py:134-152` |
| 多卡时禁用 `use_cfg_parallel` | `vlm/ThinkMorph.py:199` |
| 系统提示词（**注意两个常量内容重复，是 bug**） | `vlm/thinkmorph/inferencer.py:15-21` |
| `validate_batch_inputs` 的 image-initial 约束 | `batch_inferencer.py:787-826` |

**反面教材**（明确不要抄）：图像存盘后把路径编码进返回字符串（`ThinkMorph.py:417-434`）。

### 2.4 `VeOmni`

| 借鉴内容 | 位置 |
|---|---|
| 加载链（精简后 vendor） | `veomni/models/loader.py` + `module_utils.py` |
| Bagel 生成 / 理解 | `modeling_bagel.py:2082` / `:2306` |
| U1 生成 / 特征抽取 | `modeling_neo_chat.py:1741` / `:1342` |
| Janus 生成 / 理解 | `modeling_janus.py:1235` / `prepare_inputs_embeds` |
| Janus 规范理解流程 | `tasks/test_janus_veomni_understanding.py:118-190` |
| 各模型图像预处理参数 | `tasks/infer/infer_unified.py:140-352` |

---

## 3. 必修 bug 清单

从 gate2building 迁移时必须一并修掉。**不修就是把已知缺陷带进新项目。**

### 3.1 安全

| # | 问题 | 位置 | 动作 |
|---|---|---|---|
| S1 | **硬编码 3 个 API key** | `run_api_inference_v5.sh:18-20` | 改环境变量 `MAPSPATIAL_API_KEYS`；**建议轮换这 3 个 key**（应视为已泄漏） |

### 3.2 功能性 bug

| # | 问题 | 位置 | 动作 |
|---|---|---|---|
| B1 | `_load_gemma4` 引用从未 import 的 `GEMMA4_AVAILABLE` / `Gemma4ForConditionalGeneration` → 走到必 `NameError` | `backends.py:792` | 补 import 或删分支 |
| B2 | `extract_answer(allow_multi=True)` 参数**函数体完全没用**；配合 `is_correct` 多选流程实际是坏的 | `answer_extraction.py:11-55` | 实现或删除，不留半成品 |
| B3 | 续跑**写入端无去重** + append 模式 → 输入顺序变化产生重复行 | `run_vlm_jsonl_inference_v5.py:78-94, 206` | 内存 id 集合去重 + 原子行写 |
| B4 | 续跑读取时 `JSONDecodeError` 被静默吞 | `run_vlm_jsonl_inference_v5.py:89` | 上报损坏行数，提供 `--repair` |
| B5 | `SenseNovaU1Backend` 完全无 URL 处理 → 传 URL 直接崩 | `backends.py:1698` | 统一走 `media.load_image` |
| B6 | 视频帧数上限不一致（U1 是 8，其余 16） | 4 处 | 统一由 config 决定 |
| B7 | `summary.json` 的 `written` 只反映本次运行，`skipped` 不聚合 → 续跑后分母错 | `run_vlm_jsonl_inference_v5.py:449-451` | `total` 取自输入；分 `accuracy` / `coverage` |
| B8 | `input_jsonl` 存绝对路径，换挂载点即失效 | `_build_result:130-161` | 改存 `view/task/variant` 三元组 |

### 3.3 一致性 / 重复

| # | 问题 | 位置 | 动作 |
|---|---|---|---|
| C1 | `<image>`/`<video>` 占位符处理 8 处、5 种行为 | 全文 | 收敛到 `messages.py` |
| C2 | URL 下载 5 处、3 种策略 | 全文 | 收敛到 `media.py` |
| C3 | 视频抽帧 4 处、3 种读取器 | 全文 | 收敛到 `media.py` |
| C4 | 临时文件各自 `tempfile` + 手工清理列表 | 多处 | `media.MediaCache` 上下文管理器 |
| C5 | per-backend 配置污染顶层（`bagel_mode`、`vilasr_max_steps`、`spatial_mllm_model_type`、`model_type`） | `config.py` | 嵌套到 `backend_args` |
| C6 | `RunConfig.num_workers` / `batch_size` 在 backends 里是死字段 | `config.py` | 清理或接上 |
| C7 | 模型类靠 `model_id` 字符串前缀猜（权重目录改名就走错分支） | `backends.py:605-644` | config 显式声明 + `config.json` 校验 |
| C8 | `TransformersBackend` 539 行单类、9 个内部分支 | `backends.py:579-1117` | 拆子模块 |

### 3.4 性能

| # | 问题 | 位置 | 动作 |
|---|---|---|---|
| P1 | 单模型只吃 1 张卡（模型级轮询分配） | `run_inference_v5.sh` | 条带切分 |
| P2 | API 并发粒度是 (view,variant)，长尾严重 | `run_vlm_jsonl_inference_v5.py:425-447` | 样本级 worker pool |
| P3 | API key 轮转 `self._idx` 多线程竞态 | `backends.py:198-199` | 加锁 |

### 3.5 参考项目的坑（不要引入）

| # | 坑 | 位置 |
|---|---|---|
| R1 | vLLM 每次只提交 1 条请求 | VLMEvalKit `qwen3_vl/model.py:403` |
| R2 | 推理循环里 `torch.cuda.empty_cache()` 冲掉 KV cache | VLMEvalKit `inference.py:190` |
| R3 | `message_to_promptimg` 静默丢弃除第一张外的所有图，不打日志 | VLMEvalKit `base.py:137-154` |
| R4 | eager import 全部 80+ 模型 | VLMEvalKit `vlm/__init__.py` |
| R5 | 生成图存盘后路径编码进字符串；文件名无 sample_id | ThinkMorph `ThinkMorph.py:417-434` |
| R6 | `VLM_THINK_SYSTEM_PROMPT` 与 `GEN_THINK_SYSTEM_PROMPT` 逐字相同（复制粘贴 bug） | ThinkMorph `inferencer.py:15-21` |
| R7 | judge 选择用 15 个 `listinstr` if/elif | VLMEvalKit `run.py:362-404` |

---

## 4. 待确认清单

**这些不能靠读文档确定，必须实测。** 每项确认后回填对应文档。

### 4.1 统一模型能力（阻塞阶段 2/3）

| # | 待确认 | 回填到 |
|---|---|---|
| U1 | BLIP3o / LatentUM 生成方法的精确签名 | [05](./05-veomni-integration.md) |
| U2 | 6 个模型各自的 `max_images`（t4 需 ≥4） | [03](./03-backends.md) 能力矩阵 |
| U3 | U1 / BLIP3o / LatentUM 是否有原生交错循环 | [03](./03-backends.md) `native_interleave` 列 |
| U4 | `inputs_embeds` + `.generate()` 能否替代手写贪心循环 | [05](./05-veomni-integration.md) |
| U5 | LatentUM 的 `decoder_path` 来源与是否已下载 | [05](./05-veomni-integration.md) |
| U6 | Janus 的 v4 风格 API（`modeling_janus.py:1219`）在当前 transformers 下是否可用 | [07](./07-environment.md) 补丁清单 |
| U7 | Bagel modeling 用 VeOmni 那份还是 VLMEvalKit_Thinkmorph 那份 | [05](./05-veomni-integration.md) vendor 来源 |
| U8 | `validate_batch_inputs` 的 image-initial 约束如何适配 t4 的 text-initial | [02](./02-data-pipeline.md) §4.4 |
| U9 | U1 的正确 processor 来源（VeOmni fallback 到 `Qwen/Qwen3-VL-8B` **可疑**） | [05](./05-veomni-integration.md) |

### 4.2 环境（阻塞全部阶段）

| # | 待确认 | 回填到 |
|---|---|---|
| E1 | 6 个统一模型的增量依赖装完后，14 个纯理解模型是否仍全绿 | [07](./07-environment.md) |
| E2 | Cambrian-S 是否必须 vendor（gate2building 需插 `sys.path` 才能 `import cambrian`） | [07](./07-environment.md) |
| E3 | vLLM 与 diffusers（BLIP3o 需要）是否有 torch 版本冲突 | [07](./07-environment.md) |
| E4 | 各 backend 实际需要哪些 compat 补丁 | [03](./03-backends.md) 补丁列 |

### 4.3 实验设计

| # | 待确认 | 回填到 |
|---|---|---|
| X1 | `external_draw` 的绘图指令模板是否有效（**需人工检查生成图**） | [04](./04-strategies.md) §5.3 |
| X2 | 各模型 `native_interleave` 的触发标记与系统提示词 | [04](./04-strategies.md) §4.3/4.5 |
| X3 | t4 route_validity 的多图交错 prompt 是否优于「4图+文字」 | [02](./02-data-pipeline.md) §4.2 |

---

## 5. 风险与应对

| 风险 | 影响 | 应对 |
|---|---|---|
| 单一环境装不下全部 20 个模型 | 阻塞全项目 | 四级手段（config → patch → vendor → shim），见 [07](./07-environment.md)。**vendor 是主力手段**，不要指望靠调版本解决 |
| 生成的中间图是噪声 | 核心科学结论无从谈起 | 阶段 2 强制人工检查 20 张；不合理则先调绘图指令/参数，不要盲目跑全量 |
| `native_interleave` 触发率过低 | `native_interleave` 与 `direct` 无差异 | `draw_triggered` 指标会暴露；检查标记与系统提示词是否匹配模型训练形态 |
| VeOmni 的 modeling 正确性 | 结论建立在错误实现上 | `veomni_u1` vs `sensenova_u1_official` 交叉验证 |
| 4 个无交错实现的模型工作量超预期 | 阶段 3 拖长 | 阶段 3 内部按 U1 → BLIP3o → Janus → LatentUM 排序（U1 有官方实现可对照，LatentUM 需额外 decoder 最麻烦），允许部分模型只支持 `direct` + `external_draw` |

---

## 6. 文档维护

实施过程中这些文档会过时。维护约定：

| 情况 | 动作 |
|---|---|
| 待确认项得到结论 | 立即回填对应文档，并从 §4 清单移除 |
| 发现新的必修 bug | 加入 §3 |
| 环境安装的每一步 | 记录到 `docs/env-log.md`（新建），含失败尝试 |
| 设计决策变更 | 更新 [00-overview.md](./00-overview.md) 的决策及依据，说明为什么原依据不再成立 |

`docs/env-log.md` 特别重要——单一环境的搭建过程是本项目最容易出问题也最难复现的部分，失败的尝试同样有价值。
