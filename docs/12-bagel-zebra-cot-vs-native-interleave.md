# 12 · Bagel-Zebra-CoT 解读，及其与 `native_interleave` 的差异

> 日期：2026-08-26
>
> 来源：对仓库
> `/mnt/nas-tbt/caoziqi/code/SpatialIntelligence/generative-spatial-drafts/ablation_experiment/Bagel-Zebra-CoT`
> 的阅读，以及与本评测套件 `native_interleave` 策略的对照。
>
> 相关文档：[04-strategies.md](./04-strategies.md)、[09-training-free-visual-thinking.md](./09-training-free-visual-thinking.md)、[11-interleave-status-and-handoff.md](./11-interleave-status-and-handoff.md)

---

## 0. 结论先行

**Bagel-Zebra-CoT** 是 ICLR 2026 论文 *Zebra-CoT: A Dataset for Interleaved Vision-Language Reasoning* 的 BAGEL 训练/推理仓库：在 ByteDance 统一多模态模型 BAGEL-7B-MoT 上，用交错图文推理数据微调，让模型学会「边想边画」的 Visual Chain-of-Thought。

它放在 `generative-spatial-drafts/ablation_experiment/` 下，适合作为 generative spatial drafts 方向的对照基线：同样是「生成中间视觉草稿来辅助推理」，实现栈是 BAGEL。

MapSpatial-EvalKit 的 **`native_interleave`** 是评测策略（Track C-A：stateful autonomous G2U），不是训练配方。两者都叫 interleave，但：

| | Bagel-Zebra-CoT 推理 | MapSpatial `native_interleave` |
|---|---|---|
| 角色 | 训练好的 visual CoT **演示/能力本身** | 评测里的 **C-A：stateful autonomous G2U** |
| 谁决定画 | **协议强制**：每段文字后必画，直到 Final Answer | **模型自主**：文本里出现 `<image_start>` 才画 |
| 最接近的 EvalKit 策略 | `forced_interleave`（C-F） | 自身（C-A）；ThinkMorph 才真正匹配 |
| 权重 | `Bagel-Zebra-CoT` 微调 ckpt | 默认 **基座 BAGEL-7B-MoT**；EvalKit **没有** Zebra-CoT 权重 |
| KV | 每轮 **整段历史重编码** | **同一份 KV-cache 增量续写** |

**不宜互相代替。** 对基座 Bagel，`native_interleave` 经常画不出来；对 Zebra-CoT，推理协议几乎每步都画。

---

## 1. Zebra-CoT 在解决什么问题

人解几何、拼图、3D 规划、棋类时会在纸上画草图。普通 VLM 只会写文字 CoT，**不会原生生成中间图**。论文（[arXiv:2507.16746](https://arxiv.org/abs/2507.16746)，ICLR 2026）认为卡点有两个：

1. 现成 visual CoT 太弱，不好做 RL
2. 缺少高质量「文本–图像交错推理轨迹」数据

数据集约 **18.2 万条** 交错推理轨迹（18 个领域、50+ 任务），四类任务尤其依赖画图：

| 类别 | 例子 |
|------|------|
| 科学推理 | 几何、物理、算法 |
| 2D 视觉 | 视觉搜索、拼图 |
| 3D / 具身 | 多跳 3D、机器人规划 |
| 视觉逻辑与博弈 | 棋类等策略游戏 |

微调 Anole-7B 后，自测集约 +12%，标准 VLM bench 最高约 +13%。BAGEL-7B 微调后能产出质量更高的交错视觉推理链。本仓库就是后者。

开源：

- 数据：`multimodal-reasoning-lab/Zebra-CoT`
- 模型：`multimodal-reasoning-lab/Bagel-Zebra-CoT`
- 代码：<https://github.com/multimodal-reasoning-lab/Bagel-Zebra-CoT>
- 改编自：[ByteDance-Seed/Bagel](https://github.com/ByteDance-Seed/Bagel)

---

## 2. 基座 BAGEL：为什么能「又看又画」

BAGEL 不是纯 VLM，而是 **理解 + 生成共用一个 LLM backbone** 的统一模型：

```
文本 token  → Qwen2 embed
图像理解   → SigLIP ViT → MLP connector → 同一 hidden space
图像生成   → FLUX VAE latent → vae2llm，再经 flow matching 预测速度场
```

核心在 `modeling/bagel/bagel.py`：

- **理解支路** `visual_und`：ViT 特征进序列，文本侧用 CE loss
- **生成支路** `visual_gen`：VAE latent 加噪后进序列，`llm2vae` 预测 `v = noise - clean`（flow matching 的 MSE）
- **MoT（Mixture of Transformers）**：`Qwen2MoTDecoderLayer` 给 understanding token 和 generation token **两套 QKV / MLP / LayerNorm**，注意力仍共享，避免「看图」和「画图」互相冲

训练时一个 packed sequence 里可以同时有：

- 问题文本（无 loss）
- 问题图（只走 ViT，不生成）
- 推理文本（CE）
- 推理草稿图（VAE 生成 MSE + 再走一遍 ViT，让后续步骤能「看见」自己画的图）

这正是 visual CoT 需要的能力：**生成的中间图立刻变成下一步的视觉条件**。

---

## 3. Zebra-CoT 仓库相对原版 BAGEL 改了什么

主干训练/评测几乎原样搬自 ByteDance-Seed/Bagel。增量主要在数据与推理循环。

### 3.1 数据：`ThinkTraceJSONLIterableDataset`

`data/interleave_datasets/think_trace_dataset.py` 把每条 JSONL 编成交错序列。字段大致是：

- `Question`：可含 `<image_start>[problem_image_1]<image_end>`
- `Text Reasoning Trace`：文字步骤 + 中间图引用
- `Final Answer`

拼出来的训练样本是：

```
[system prompt]          # 无 loss，开 CFG
Question: ... + 题目图   # 题目图 need_vit=True, need_loss=False
<think>步骤1</think>     # CE；若后面有图，让 im_end 预测 vision_start
  中间图                  # need_loss + need_vae + need_vit
<think>步骤2</think>
  ...
<answer>Final Answer: …</answer>   # CE
```

要点：

- 题目图只理解、不生成
- 推理图既当生成目标，又当后续 ViT 条件
- `THOUGHT 1:` 这类标记会被剥掉，统一包进 `<think></think>`
- JSONL 里的 `<image_start>[key]<image_end>` 只是 **数据占位符**，解析时换成真图；模型并不被要求把这串字写出来
- 训练里「该画了」对应的是 special token `<|vision_start|>`（前一段文字的 `im_end` 去预测它）

当前配置只开了 think_trace，T2I / editing / VLM SFT 都注释掉了：这是 **纯 visual CoT 微调**，不是 BAGEL 原配方的混合预训练。

路径写死在 `/dev/shm/`：

- 数据：`/dev/shm/data/Zebra-CoT/zebra_cot.jsonl`
- 基座：`/dev/shm/models/BAGEL-7B-MoT`

`data/configs/example.yaml` 只启用 `think_trace`；`data/dataset_info.py` 注册 `think_trace` → `ThinkTraceJSONLIterableDataset`。

### 3.2 训练：`scripts/train.sh`

从 HuggingFace 的 BAGEL-7B-MoT 微调，而不是从 Qwen/SigLIP 从头训：

- 8 GPU、FSDP `HYBRID_SHARD`
- lr `2e-5`，cosine，warmup 50，共 **5000 step**，每 50 step 存盘
- packed 长度拉到 60k token（交错图文很长）
- wandb 项目名 `zebra-cot`

### 3.3 推理：文本–图像交替循环

`infz_bf16.py` 不是一次生成整段。外层循环是：

```text
写一段文字
  → 若出现 Final Answer / <answer>  → 停
  → 否则无条件生成一张图，append 进历史
  → 再写下一段
```

不看 `<image_start>`，也不看 `<|vision_start|>`。训练时每步推理后面本来就可以接图，推理协议把这一点写成了硬规则。

系统提示大意：你会交错文字和视觉 CoT，最后写成 `Final Answer: …`。

典型题是空间操作，例如：*Subtract all cylinders. Add 1 red sphere. How many objects are left?* —— 模型被期望先画出变换后的场景，再数物体。

CFG 默认：`cfg_text_scale=4.0`，`cfg_img_scale=2.0`，`cfg_renorm_type=text_channel`，`cfg_interval=[0.0, 1.0]`。

### 3.4 Inferencer API：单次原语 + Python 外层循环

Zebra-CoT 的 `InterleaveInferencer.interleave_inference` 是 **单次原语**：要么出字（`understanding_output=True`），要么出一张图。交错由 `infz_bf16.py` 的 Python 外层循环拼出来。

每一轮调用都会 `init_gen_context()`，把 `[prompt, 题图, 已写文字, 已画的图, …]` **整段重编码**。内容连续，但不是增量 KV。

图怎么喂回去：

- 写字时 `understanding_output=True` → 历史上的图 **只走 ViT**（`vae=False`）
- 画图时 `understanding_output=False` → 历史上的图走 VAE（`update_context_image` 默认 `vit=True`，故 VAE + ViT）

### 3.5 目录怎么读

| 路径 | 作用 |
|------|------|
| `modeling/bagel/` | BAGEL + MoT + NaViT 式变长视觉 |
| `modeling/qwen2/`、`modeling/siglip/` | backbone |
| `data/interleave_datasets/think_trace_dataset.py` | **Zebra-CoT 特有数据** |
| `data/t2i_dataset.py`、`vlm_dataset.py`、`edit_dataset.py` | 原版 BAGEL 任务（本实验基本关掉） |
| `train/pretrain_unified_navit.py` | FSDP 统一训练入口 |
| `infz_bf16.py` / `inferencer.py` | 交错推理 |
| `EVAL.md` + `scripts/eval/` | 原版评测：MMMU、GenEval、WISE、KRIS、RISE 等；KRIS/RISE 的 spatial 子集和空间课题更相关 |

### 3.6 和 generative spatial drafts 的关系

BAGEL-Zebra-CoT 的主张：

> **把中间视觉草稿当作一等公民的推理 token**：不是事后解释图，而是推理过程中必须生成、再被自己读回去的状态。

这和 generative spatial drafts 高度同构。做消融时，这个仓库适合当：

1. **强基线**：统一理解–生成模型 + 大规模交错 CoT 数据
2. **数据格式参考**：`Question` / `Text Reasoning Trace` / 图像占位符 / `<think>`–`<answer>`
3. **推理协议参考**：停在 final answer；每步「写一段 → 画一张 → 看自己的图」

和本课题可能不同的地方：BAGEL 的草稿是 **通用 RGB 图 + flow matching**，没有显式 3D/空间结构（深度、相机、物体状态）；MoT 把 und/gen 参数拆开，不一定适合结构化空间表征。若消融目标是「要不要生成中间草稿」，这里是现成的 yes 对照；若目标是「草稿要不要结构化」，这里是 unstructured raster 对照。

---

## 4. MapSpatial `native_interleave` 是什么

### 4.1 在评测体系里的位置

核心科学问题（见 [00-overview.md](./00-overview.md)、[04-strategies.md](./04-strategies.md)）：

> **让模型生成中间图像，是否提升空间理解准确率？**

四级推理条件（见 [09-training-free-visual-thinking.md](./09-training-free-visual-thinking.md) 与 `runner.py` 的 Track 标签）：

| 条件 / 策略 | Track | 图像来源 | 触发方式 | 生成后状态 |
|---|---|---|---|---|
| `direct` | U | 无 | 无 | fresh |
| `external_draw` | C-R | 同一模型 | 外部强制 | **reset**（两次独立前向） |
| `forced_interleave` | C-F | 同一模型 | 外部强制 | **shared KV** |
| `native_interleave` | C-A | 同一模型 | **模型自主 marker** | **shared KV** |

`native_interleave` 要求 `caps.native_interleave=True`。策略本身几乎只做委托：调用 `backend.interleave()`，把 PIL 图落盘，写入 `draw_triggered` / `rounds`。

### 4.2 实现：ThinkMorph 式 inner loop

Bagel backend（`mapspatial/backends/veomni/bagel.py`）把 `native_interleave` 映射到 vendored `InterleaveInferencer`，且：

- `think=True`
- `understanding_output=False`
- 一次调用跑完整条链

Vendored inferencer（`mapspatial/vendor/bagel_interleave/inferencer.py`）把 **while + marker** 收进内部：

```text
while rounds < max_rounds:
    gen_text(...)
    把文字写入同一份 KV
    if "<image_start>" in gen_text:     # 子串匹配
        gen_image(...)
        update_context_image(..., vae=True)   # 默认 vit=True，VAE+ViT 都进 cache
        rounds += 1
    else:
        break
```

停条件：这轮文字里 **没有** `"<image_start>"`，或达到 `max_rounds`（Bagel 默认 3，ThinkMorph 默认 5）。

关键在 `gen_context`：**单一 KV-cache 跨轮保持**（`NaiveCache`）。文本生成、图像生成、图像回填共享同一份注意力上下文。这是相对 `external_draw` 的核心语义差异——后者 `draw()` 再 `understand()` 是两次独立前向，中间 context 丢失。

### 4.3 系统提示与 marker

native 用的是 ThinkMorph 提示（`VLM_THINK_SYSTEM_PROMPT` / `GEN_THINK_SYSTEM_PROMPT` 内容相同）：

```text
Let's think step by step to answer the question.
For text-based thinking, enclose the process within <think> </think>.
For visual thinking, enclose the content within <image_start> </image_end>.
Finally conclude with the final answer wrapped in <answer></answer> tags.
```

触发靠 **解码文本里的子串** `"<image_start>"`，不是 BAGEL 的 `<|vision_start|>` token。

[04-strategies.md](./04-strategies.md) §4.3 已指出脆弱性：措辞一变就静默跳过；不同模型标记不同；出现在引号或讨论中会误触发。`draw_triggered` 必须记录，否则三种结果混在一起：

| 情况 | `rounds` | `draw_triggered` |
|---|---|---|
| 模型判断需要画，画了 | ≥1 | `True` |
| 模型判断不需要画 | 0 | `False` |
| 模型想画但标记没匹配上 | 0 | `False` |

### 4.4 当前权重配置

EvalKit **搜不到** Zebra-CoT。相关 config：

| 配置 | 权重 | 是否学过自主画图 |
|---|---|---|
| `configs/models/bagel-7b.yaml` | 基座 `BAGEL-7B-MoT` | 文档明确：**没学过** 发 `<image_start>` |
| `configs/models/bagel-7b-think.yaml` | 同一基座，`think_mode=true` | 同上；只影响 `direct` 的 understand 路径 |
| `configs/models/thinkmorph-7b.yaml` | ThinkMorph-7B | 是，和 native 的 marker 协议对齐 |

[09-training-free-visual-thinking.md](./09-training-free-visual-thinking.md) §2.1 已写明：给基座 Bagel 套 ThinkMorph inferencer，真正的问题不是「没有 interleave 代码」，而是：

1. 基础权重是否学习过自主发出 `<image_start>`
2. 套用 ThinkMorph system prompt 后的 marker 触发，能否称为模型原生策略
3. inferencer 能运行 ≠ 模型具有可靠的 autonomous visual-thinking policy

在证明基座 Bagel 确实训练过该 marker policy 之前，应将其描述为 `stateful_forced` 或 `prompted_marker_interleave`，而不是与 ThinkMorph 的 `native_autonomous` 混为一类。

EvalKit Bagel 的 CFG：`cfg_renorm_type=global`，`cfg_interval=[0.4, 1.0]`，`cfg_text_scale=4.0`，`cfg_img_scale=2.0`。

---

## 5. 逐项对比

### 5.1 控制流：强制画 vs 等 marker

| | Zebra-CoT `infz_bf16.py` | EvalKit `native_interleave` | EvalKit `forced_interleave` |
|---|---|---|---|
| 写完一段后 | **无条件画一张** | 仅当文本含 `<image_start>` | 无条件画 |
| 停止 | `Final Answer:` / `<answer>` | 无 marker 或 `max_rounds` | 先写 → 画 N 张 → 再写最终答案 |
| 多步 | 直到给出答案，每步都画 | 模型决定画几次（常为 0） | 固定 `max_rounds` 张图，然后作答 |

Zebra-CoT 训练时每步推理后面就可以接图；推理协议把这一点写成硬规则。基座 Bagel 若从不吐 `<image_start>`，native 会退化成一轮纯文本，和 `direct` 几乎一样。

### 5.2 Inferencer 不是同一个 API

| | Zebra-CoT | EvalKit native |
|---|---|---|
| `interleave_inference` | 单次：出字 **或** 出一张图 | 内部 while：完整交错链 |
| 交错由谁拼 | `infz_bf16.py` 外层循环 | inferencer 内部 |
| KV | 每轮 `init_gen_context()`，整段历史重编码 | 同一 `NaiveCache` 增量 `update_context_*` |
| 生成图回填 | 下一轮写字时 **只走 ViT** | 全程 `understanding_output=False`，**VAE + ViT** |

内容可以看起来连续，但 Zebra-CoT 的「重编码」和 native 的「增量 cache」不是同一套位置编码 / CFG context 更新方式。EvalKit 把单 KV 增量当作 native 相对 `external_draw` 的科学差异；Zebra-CoT demo 实际上更接近 **带着累积 artifact 的 restart**。

### 5.3 提示词和「开始画」的符号不是一套

| | Zebra-CoT | native_interleave |
|---|---|---|
| 系统提示 | 交错文字与视觉 CoT，结尾 `Final Answer:` | ThinkMorph：`<think>` / `<image_start>` / `<answer>` |
| 数据里的 `<image_start>[key]<image_end>` | JSONL **占位符**，换成真图 | 不使用这套数据格式 |
| 训练时「该画了」 | special token `<\|vision_start\|>` | 模型在正文里 **写出字符串** `<image_start>` |
| 推理时触发 | 协议强制，不看 token/字符串 | 子串 `"<image_start>" in gen_text` |

因此：即使用 Zebra-CoT 权重去跑 EvalKit 的 `native_interleave`，也很可能 **几乎不触发画图**——它学的是「后面接图像 token」，不是「在正文里写出 `<image_start>`」。这和文档里对基座 Bagel 的警告是同一类问题。

### 5.4 权重与 CFG

| | Zebra-CoT 仓库 | EvalKit `bagel-7b` native |
|---|---|---|
| ckpt | `multimodal-reasoning-lab/Bagel-Zebra-CoT` | `${CKPT_DIR}/BAGEL-7B-MoT` |
| 是否微调过交错 CoT | 是 | 否 |
| `cfg_renorm_type` | `text_channel` | `global` |
| `cfg_interval` | `[0.0, 1.0]` | `[0.4, 1.0]` |

ThinkMorph 才是 `native_interleave` 的参考实现（`cfg_text_scale=3.0`，`cfg_img_scale=1.5`，`max_rounds=5`）。

### 5.5 科学问题不同

Zebra-CoT 问的是：用 18 万条交错轨迹微调后，统一模型能不能原生 visual CoT。

`native_interleave` 问的是：在 **同一模型、同一份 MapSpatial 数据** 上，

> 模型自己决定要不要画，且 KV 不断，是否比 `direct` / `external_draw` / `forced_interleave` 更能提升空间题准确率？

`draw_triggered` 必须记，否则「模型选择不画」和「marker 没匹配上」会混在一起。

### 5.6 和 EvalKit 其他策略的相对位置

```
                    触发：模型自主          触发：协议/外部强制
                 ┌──────────────────┐   ┌──────────────────────────┐
shared KV        │ native_interleave│   │ forced_interleave        │
                 │ (C-A, ThinkMorph │   │ (C-F)                    │
                 │  才真正匹配)      │   │ Zebra-CoT 推理更像这里    │
                 └──────────────────┘   └──────────────────────────┘
reset / 重编码   │ （无对应）        │   │ external_draw (C-R)      │
                 │                  │   │ Zebra-CoT 每轮重编码      │
                 │                  │   │ 在「状态」上更像 C-R      │
                 └──────────────────┘   │ 在「必画」上更像 C-F      │
                                        └──────────────────────────┘
```

Zebra-CoT demo 同时具备：

- **必画**（像 C-F）
- **每轮整段重编码**（状态连续性上更像 C-R，而不是 native 的单 KV）
- **微调过的交错权重**（能力本身强于基座 Bagel 的 native）

这三件事不能折叠进现有某一个 strategy 名。

---

## 6. 若要把 Zebra-CoT 接到 MapSpatial 消融

不宜直接丢进现在的 `native_interleave`。更干净的做法：

1. **新 backend / 新 config**：权重换成 Bagel-Zebra-CoT，推理循环按 `infz_bf16.py`（每步必画直到 Final Answer）。策略标签用 `forced_interleave` 或单独的 `zebra_cot`，不要标成 C-A。
2. 若坚持测「自主触发」，要改 marker：去看 `<|vision_start|>` / 模型是否真的要切到图像模式，而不是搜字符串 `<image_start>`。
3. 和 EvalKit 的 `forced_interleave` 比时，还要控制 **同一张中间图**，才能把「协议强制多步」和「共享 KV」拆开——[09](./09-training-free-visual-thinking.md) 里的 `Delta_state` 就是这个意思。

Capability 也不应继续用一个布尔 `native_interleave` 表达全部能力（[09](./09-training-free-visual-thinking.md) §3.1 已建议拆开）：

| 能力 | Zebra-CoT | 基座 Bagel + 当前 native | ThinkMorph + native |
|---|---|---|---|
| `draw` | 是 | 是 | 是 |
| `reconsume_generated` | 是（外层把图 append 进历史） | 是 | 是 |
| `stateful_interleave`（单 KV 增量） | **否**（每轮重编码） | 是（代码路径） | 是 |
| `autonomous_visual_trigger` | **否**（协议强制画） | **否**（没学过 marker） | **是** |

---

## 7. 关键代码锚点

### Zebra-CoT 仓库

```
ablation_experiment/Bagel-Zebra-CoT/
  README.md
  data/interleave_datasets/think_trace_dataset.py   # 交错 JSONL → sequence_plan
  data/dataset_info.py / data/configs/example.yaml  # 只开 think_trace
  scripts/train.sh                                  # BAGEL-7B-MoT 微调 5000 step
  inferencer.py                                     # 单次：出字 XOR 出图
  infz_bf16.py                                      # 外层：写 → 必画 → 直到 Final Answer
  modeling/bagel/bagel.py                           # und/gen + flow matching
  modeling/bagel/qwen2_navit.py                     # Qwen2MoTDecoderLayer
```

### MapSpatial-EvalKit

```
mapspatial/strategies/native_interleave.py          # 委托 backend.interleave + 落盘
mapspatial/strategies/forced_interleave.py          # 必画 + 共享 KV
mapspatial/strategies/external_draw.py              # 必画 + 两次独立前向
mapspatial/backends/veomni/bagel.py                 # interleave() / forced_interleave()
mapspatial/vendor/bagel_interleave/inferencer.py    # ThinkMorph 式 while + <image_start>
mapspatial/runner.py                                # native_interleave → Track C-A
configs/models/bagel-7b.yaml
configs/models/bagel-7b-think.yaml
configs/models/thinkmorph-7b.yaml
```

---

## 8. 一句话收束

名字都叫 interleave。**Zebra-CoT 是「微调过的、协议强制的、多步画图直到作答」（且 demo 每轮重编码历史）**；**EvalKit `native_interleave` 是「基座/ThinkMorph、marker 自主、单 KV 增量」**。对基座 Bagel，后者经常画不出来；对 Zebra-CoT，前者几乎每步都画。接到本套件时，不要标成 C-A，优先按 C-F / 独立 `zebra_cot` 条件来跑。
