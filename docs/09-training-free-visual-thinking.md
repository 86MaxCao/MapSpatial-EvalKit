# Training-Free Visual Thinking：协议、实现与实验计划

> 本文档记录 MapSpatial 中“使用多模态生成辅助多模态理解”的完整设计。
> 目标不是把所有统一多模态模型强行包装成 `native_interleave`，而是把视觉证据的
> **生成方式、触发策略、重新消费方式和内部状态是否连续**拆开评测，并保证代码语义、
> 论文 Track 定义和结果表完全一致。

---

## 1. 核心结论

MapSpatial 当前已经能够运行如下两阶段流程：

```text
输入地图 + 问题
    -> 同一模型的 draw() 生成中间图
    -> 清空本次生成调用的内部状态
    -> 同一模型的 understand() 重新读取原图、问题和中间图
    -> 最终答案
```

当前策略名为 `external_draw`。这里的 `external` 表示**编排器位于模型调用之外**，
并不表示中间图由另一个外部生成模型产生。它实际上是“同一模型自生成证据，然后在
新上下文中重新读取”，更准确的科学名称是：

- `self_draw_restart`；或
- stateless/restart generation-to-understanding。

它仍然是有价值的 G2U 条件，但不能等同于共享 KV-cache 的 stateful visual thinking。

下一阶段应形成四级推理条件：

| 条件 | 图像来源 | 触发方式 | 生成后状态 | 科学问题 |
|---|---|---|---|---|
| `direct` | 无 | 无 | fresh | 不借助视觉证据时能否答对？ |
| `self_draw_restart` | 同一模型 | 外部强制 | reset | 仅中间图本身是否有帮助？ |
| `stateful_forced` | 同一模型 | 外部强制 | shared | 保留内部推理状态是否产生额外收益？ |
| `native_autonomous` | 同一模型 | 模型自主 | shared | 模型能否自主判断何时需要视觉工作区？ |

Oracle supportive evidence 和 deterministic GIS/tool evidence 是独立的 evidence source，
不应与上述 trigger/state 维度混为一谈。

最重要的实验不是笼统比较 `external_draw` 和 `native_interleave`，而是尽可能让
restart 与 shared-state 分支消费**同一次生成得到的相同中间图**，从而隔离状态连续性：

```text
                             +-> 保留生成前后的 context/cache -> 最终答案
同一次生成的中间图 ---------|
                             +-> 新建 context，重新输入同一张图 -> 最终答案
```

定义：

```text
Delta_state = Acc(shared-state, same artifact)
              - Acc(restart, same artifact)
```

如果不控制中间图，两个策略的差异同时混入了图像质量、采样随机性、prompt 和状态保持，
无法将提升归因给 shared state。

---

## 2. 当前仓库事实与需要纠正的旧判断

### 2.1 当前能力状态

| 模型 | `draw()` | 当前 `native_interleave` | 当前 G2U | 目标状态 |
|---|---:|---:|---|---|
| ThinkMorph | 是 | 是 | marker-driven shared-state | 保留为 native reference |
| Bagel | 是 | 代码中为是 | 套用 ThinkMorph inferencer | 重分类并补 forced paired prototype |
| SenseNova-U1 | 是 | 否 | `external_draw` / restart | port 上游 `interleave_gen()` |
| LatentUM | 是 | 否 | `external_draw` / restart | 适配上游 planner 的 save-rewind-reinject |
| BLIP3o | 是 | 否 | `external_draw` / restart | 暂不宣称 stateful |
| Janus-Pro | 是 | 否 | `external_draw` / restart | 暂不宣称 stateful |
| Show-o2 | 是 | 否 | `external_draw` / restart | 暂不宣称 stateful |
| JoyAI-Image | 是 | 否 | `external_draw` / restart | 暂不宣称 stateful |

旧版文档称“当前只有 ThinkMorph 支持 `native_interleave`”，但当前仓库中 Bagel 已经：

- `caps.native_interleave=True`；
- config 包含 `native_interleave`；
- 调用 vendored ThinkMorph `InterleaveInferencer`。

因此真正的问题不是“Bagel 没有 interleave 代码”，而是：

1. Bagel 的基础权重是否学习过自主发出 `<image_start>`；
2. 当前套用 ThinkMorph system prompt 后的 marker 触发能否称为模型原生策略；
3. inferencer 能运行，与模型具有可靠的 autonomous visual-thinking policy，是两件不同的事。

在证明 Bagel 基础模型确实训练过该 marker policy 之前，应将其描述为
`stateful_forced` 或 `prompted_marker_interleave`，而不是与 ThinkMorph 的
`native_autonomous` 混为一类。

### 2.2 当前 `external_draw` 已经重新消费生成图

`mapspatial/strategies/external_draw.py` 当前执行：

1. `backend.draw(sample.message, instruction)`；
2. 保存生成图；
3. 将生成图追加到原始 message；
4. 调用同一 `backend.understand()`；
5. 返回最终答案和中间图路径。

所以它不是 artifact-only 的 Track G。它同时产生：

- 一个可以单独评分的生成 artifact；
- 一个 restart G2U 最终答案。

当前 runner 将 `external_draw` 直接标记为 `G`，会丢失第二层语义。后续需要将
“artifact 生成阶段”和“artifact 被谁、以什么状态读取”分别记录。

### 2.3 当前 marker 配置没有真正贯通

`RunContext.marker` 默认是 `<image_start>`，runner 创建 `RunContext` 时没有从
`backend_args` 读取 per-model marker。U1 和 LatentUM 上游代码使用 `<img>`，不能依赖
全局默认值。

正确做法是由 runner 显式构造模型级 interleave config，并将实际生效值写入输出 meta；
不建议让 backend 静默忽略 strategy 传入的 marker，因为那会导致配置与运行 provenance
不一致。

### 2.4 当前 native 生成图存在 schema/落盘缺口

`Prediction.generated_images` 的契约是 `list[Path]`，但 Bagel `interleave()` 当前放入的是
PIL Image；`NativeInterleaveStrategy` 又没有真正负责将这些 PIL 图按 sample id 落盘。
在运行正式实验前必须修复，否则会影响：

- Track-G 几何评分；
- 中间证据人工审计；
- 部分重跑后的样本对齐；
- 论文 qualitative case 的可复现性。

---

## 3. 术语与能力模型

### 3.1 不再用一个布尔值表达全部 interleave 能力

当前 `Capabilities.native_interleave: bool` 同时混合了三个问题：

1. backend 能否生成图；
2. backend 能否在生成后保持或恢复内部状态；
3. 模型是否学习过自主触发视觉生成。

建议逐步扩展为：

```python
@dataclass(frozen=True)
class Capabilities:
    batch: bool
    draw: bool
    max_images: int
    video: bool

    # Generation-to-understanding capabilities
    reconsume_generated: bool = False
    stateful_interleave: bool = False
    autonomous_visual_trigger: bool = False
```

兼容迁移期间可保留 `native_interleave`，但只作为 deprecated alias；新的 strategy
必须校验更精确的 capability：

| Strategy | Required capabilities |
|---|---|
| `self_draw_restart` | `draw=True`, `reconsume_generated=True` |
| `stateful_forced` | `draw=True`, `stateful_interleave=True` |
| `native_autonomous` | `stateful_interleave=True`, `autonomous_visual_trigger=True` |

`draw=True` 不能自动推出 `stateful_forced` 可用。拥有独立的生成接口并不代表 backend
暴露了可以更新、复制、回滚或继续使用的 cache/context。

### 3.2 三个相互正交的记录维度

每条 Prediction 至少记录：

```python
meta = {
    "strategy": "stateful_forced",
    "evidence_source": "same_model",       # none/gold/same_model/tool/other_model
    "trigger_policy": "forced",            # none/forced/autonomous
    "state_policy": "shared",              # fresh/reset/shared/rewind_reinject
    "reader_relation": "same_model",       # same_model/separate_model/tool
    "draw_triggered": True,
    "rounds": 1,
    "marker": None,
    "artifact_id": "<sample_id>_r0",
    "cache_protocol": "continuous_append",
}
```

这样论文聚合时不必从容易变化的 strategy 名称反推科学条件。

### 3.3 shared-state 的严格定义

shared-state 不等于“生成和理解使用同一组模型权重”。必须满足以下之一：

- 生成前后的 KV-cache/context 连续更新；或
- 保存生成前 cache，在生成视觉 token 后 rewind，并以理解路径重新注入视觉 embedding；
- 上游官方实现声明并实际执行等价的内部状态传递。

以下情况都属于 restart，而不是 shared-state：

- 保存 PNG 后重新调用 `understand()`；
- 同一 checkpoint 的两个独立进程先后调用；
- generation backend 与 understanding backend 权重相同但 cache 不共享。

---

## 4. 论文 Track 与代码策略的统一

### 4.1 建议保留 U/O/G/C，但细分 C

| Track | 含义 | 是否要求最终答案 |
|---|---|---:|
| U | Direct understanding | 是 |
| O | Reader consumes gold supportive evidence | 是 |
| G | Evidence artifact generation and quality | 否 |
| C-R | Same-model restart G2U | 是 |
| C-F | Stateful forced G2U | 是 |
| C-A | Stateful autonomous G2U | 是 |
| C-X | Separate-reader/agentic decoupled G2U | 是 |

同一次 `self_draw_restart` run 可以同时产生：

- 一个 Track-G artifact record；
- 一个 Track-C-R answer record。

不要再用一个 `track: "G"` 覆盖整个 run 的所有输出。可以采用：

```python
meta = {
    "tracks": ["G", "C-R"],
    "primary_track": "C-R",
}
```

或者在评测阶段分别从同一个 Prediction 派生 artifact metric row 和 answer metric row。

### 4.2 论文 RQ4 的推荐表述

当前 RQ4 可以细化为：

> Can unified multimodal models construct valid, non-leaking visual evidence,
> benefit from that evidence after a context restart, and obtain additional
> gains through stateful or autonomous visual thinking?

它对应三个子问题：

- RQ4a：模型生成的 supportive evidence 是否几何正确且不泄露答案？
- RQ4b：同一模型在 restart 后读取自己的证据，是否优于 direct？
- RQ4c：共享状态或自主触发是否带来超过 restart 的额外收益？

### 4.3 主结果表建议

主表建议使用：

| Model | Direct | Oracle | Self-draw restart | Stateful | Draw rate | EPG-Q |
|---|---:|---:|---:|---:|---:|---:|

其中：

- 不支持 stateful 的模型填写 N/A；
- 不对 heterogeneous availability 做简单八模型 macro average；
- forced 与 autonomous 的完整拆分放入附录；
- 主文明确 `Stateful` 列对每个模型采用的是 forced 还是 autonomous，并给出脚注。

---

## 5. 实现总览与优先级

### Phase 0：先修协议和基础设施

这一阶段不增加新模型能力，但必须在所有大规模实验之前完成。

#### 0.1 策略重命名与兼容

新增 `self_draw_restart`，保留 `external_draw` 作为 CLI/config legacy alias：

```python
_STRATEGY_REGISTRY = {
    "direct": DirectStrategy,
    "self_draw_restart": SelfDrawRestartStrategy,
    "external_draw": SelfDrawRestartStrategy,  # deprecated alias
    "stateful_forced": StatefulForcedStrategy,
    "native_autonomous": NativeAutonomousStrategy,
}
```

旧结果仍可读取，但所有新结果的 `meta.strategy` 必须写 canonical name，不能继续写 alias。

#### 0.2 扩展 capability

修改：

- `mapspatial/types.py`
- `mapspatial/backends/base.py`
- 各 UMM backend 的 capability 声明
- `mapspatial/strategies/base.py`
- capability/strategy 单元测试

迁移表初始值：

| Model | reconsume | stateful | autonomous |
|---|---:|---:|---:|
| ThinkMorph | 是 | 是 | 是 |
| Bagel | 是 | 是 | 暂定否 |
| U1 | 是 | 否，port 后是 | 否，验证上游后再改是 |
| LatentUM | 是 | 否，适配后是 | 否，验证 marker policy 后再改 |
| 其他 UMM | 是 | 否 | 否 |

这里的“reconsume”必须通过真实小样本测试确认模型理解接口能正确接收原图与生成图多图输入，
不能只因为代码存在 `understand()` 就默认通过。

#### 0.3 修复 per-model interleave config

建议引入：

```yaml
backend_args:
  interleave:
    marker_start: "<image_start>"
    marker_end: "<image_end>"
    trigger_mode: "token_sequence"
    system_prompt: "..."
    max_rounds: 3
```

runner 将其显式传入 `RunContext`。每条输出保存实际生效配置摘要或 config hash。

marker 检测优先使用 token id/token sequence，而不是 decode 后的裸字符串子串。若上游只能使用
substring，必须在 trace 中记录：

- 原始生成文本；
- marker 是否完整匹配；
- 是否疑似产生 draw intent 但未触发；
- 是否出现 quoted marker 误触发。

#### 0.4 统一中间图落盘

strategy 层或统一 artifact manager 负责把 PIL/latent/temporary file 归一为正式路径：

```text
results/{model}/{strategy}/generated/{view}/{task}/{variant}/{sample_id}_r{round}.png
```

要求：

- `Prediction.generated_images` 只保存 `Path`；
- `TraceStep.image` 指向同一文件；
- 文件名包含 sample id 和 round；
- 同时写入 SHA-256，支持 paired branch 验证确实消费相同 artifact；
- latent-only 结果可额外保存 `.npy`，但正式 Track-G 图像指标必须使用可解码图像。

#### 0.5 修正 Track 推断

删除 runner 中简单的：

```python
external_draw -> G
native_interleave -> C
```

改为根据 `evidence_source / trigger_policy / state_policy / reader_relation` 显式映射。

---

## 6. Phase 1：Bagel restart vs shared-state 配对原型

### 6.1 为什么先做 Bagel

Bagel 已经具备：

- vendored `InterleaveInferencer`；
- `init_gen_context()`；
- `update_context_text()`；
- `gen_image()`；
- `update_context_image()`；
- `gen_text()`。

因此不需要先移植几百行上游代码，就能验证最重要的科学问题：共享内部状态是否比
restart 更有帮助。

### 6.2 新增 backend API

建议不要让 strategy 直接操作 vendor 的 cache 细节。由 Bagel backend 暴露一个配对接口：

```python
def paired_visual_thinking(
    self,
    message: Message,
    instruction: str,
    *,
    max_rounds: int = 1,
    seed: int,
) -> PairedPrediction:
    """Generate once, then answer via shared-state and restart branches."""
```

返回：

```python
@dataclass
class PairedPrediction:
    artifact: Image.Image | Path
    shared: Prediction
    restart: Prediction
    generation_trace: list[TraceStep]
```

### 6.3 共享的生成前缀

两条分支必须共享：

- 同一原图；
- 同一问题；
- 同一 supportive-evidence instruction；
- 同一 seed、CFG 和 image resolution；
- 同一次实际生成得到的 artifact；
- 同一最终回答 decoding 参数。

生成过程：

```text
base_context = init_gen_context()
base_context <- system prompt + original map + question
base_context <- task-specific supportive-evidence instruction
optional reasoning text <- gen_text(base_context)
artifact <- gen_image(base_context)
```

注意：用于生成的 instruction 必须要求 answer-agnostic supportive primitives，禁止答案文字、
选项字母、数值答案和仅标出正确候选的 solution visualization。

### 6.4 shared-state 分支

```text
shared_context = generation context
shared_context <- update_context_image(artifact)
shared_context <- final-answer instruction
shared_answer <- gen_text(shared_context)
```

该分支记录：

- `state_policy=shared`；
- `cache_protocol=continuous_append`；
- `trigger_policy=forced`；
- artifact hash。

### 6.5 restart 分支

```text
restart_context = init_gen_context()
restart_context <- original map + question
restart_context <- exact same artifact
restart_context <- same final-answer instruction
restart_answer <- gen_text(restart_context)
```

必须确保 restart 分支看到解决任务所需的显式信息，但不看到 shared 分支独有的隐藏状态。
若 shared 分支在生成前产生了可见 reasoning text，需要预先决定：

- 主实验：两边都显式提供相同 reasoning text，以尽量只隔离 cache continuity；
- 附加实验：restart 不提供 reasoning text，评估完整端到端调用差异。

主实验优先采用第一种，否则 `Delta_state` 会混入可见文本上下文差异。

### 6.6 Bagel autonomous 条件的处理

当前 marker-driven `BagelBackend.interleave()` 不应直接作为 `native_autonomous` headline 结果。
先运行 trigger audit：

- 不注入 ThinkMorph 特定 system prompt 时的自然 marker 触发率；
- 注入 prompt 后的触发率；
- quoted-marker/无效 marker 比例；
- 触发后的图像质量；
- 与 forced 条件的准确率差异。

只有确认基础 Bagel 的训练协议支持这一 marker 后，才把 capability
`autonomous_visual_trigger` 改为 true。否则将结果命名为 `prompted_marker_interleave`，作为
附录诊断而不是 native headline。

### 6.7 Bagel 原型的成功门槛

在 50--200 个 scene-grouped 样本上要求：

- 两个分支 artifact SHA-256 完全一致；
- 所有生成图均可定位回 sample id；
- shared/restart 无新增异常；
- supportive leakage pass rate 可接受；
- 至少在 Oracle 有正增益的任务上比较 `Delta_state`；
- 报告 bootstrap CI，不因小样本点估计为正就宣称成功。

如果 Oracle evidence 本身对某个 task 不提供增益，则不应期待模型生成证据提供稳定增益；
该 task 主要用于报告 evidence construction failure，而不是 state benefit。

---

## 7. Phase 2：SenseNova-U1 上游 interleave port

### 7.1 目标与主张边界

上游 SenseNova-U1 据现有调查包含 `interleave_gen()`，实现文本生成、`<img>` 触发、
图像生成、ViT 重新编码和 cache 反馈。如果服务器端源代码确认这是随模型发布的通用推理路径，
U1 可以成为除 ThinkMorph 外最强的 native/stateful 证据。

在完成源码核验和 differential test 前：

- 当前 EvalKit capability 保持 `stateful_interleave=False`；
- 论文不把 U1 计入已完成的 Track C-A；
- 文档使用“target implementation”，不使用“已支持”。

### 7.2 源码核验清单

在服务器上记录：

- 上游 repo URL/commit hash；
- `interleave_gen()` 精确文件路径和行号；
- checkpoint 对应的代码版本；
- marker token id 是否存在于 tokenizer；
- marker 是否属于训练协议，而非 demo prompt 临时约定；
- cache 分支数量及各自语义；
- 图像反馈是像素重编码还是 generation latent 直连；
- 官方支持的输入形式、轮数、分辨率和 batch 限制。

### 7.3 vendor 原则

优先原样 vendor 上游实现，不按摘要重新写一个“看起来等价”的 loop。允许的适配仅包括：

- import/path 调整；
- 与 vendored tokenizer/chat template 的接口适配；
- 已有 `prepare_flash_kv_cache` 兼容；
- 输出转换为 `Prediction/TraceStep`；
- 显式参数传递和日志；
- 已知 transformers/flash-attention 兼容修复。

任何改变 attention mask、cache update、rewind 点、generation indicator 或 CFG branch 的修改，
都必须单独记录并测试，不能归入普通“接口适配”。

### 7.4 backend 接口

新增：

```python
def interleave(
    self,
    message: Message,
    *,
    max_rounds: int,
    marker: str = "<img>",
    trigger_policy: str = "autonomous",
    **kw,
) -> Prediction:
    ...
```

输出必须记录每轮：

- marker 前文本；
- 是否触发；
- 图像生成耗时；
- 图像路径/hash；
- 图像重新编码方式；
- cache update 类型；
- 最终回答文本。

若上游 loop 可以强制触发，应同时实现 U1 的 `stateful_forced`，从而在同一个模型上比较：

```text
restart forced vs stateful forced vs stateful autonomous
```

这比仅报告 U1 native 一个数字更有解释力。

### 7.5 differential test

在同一环境中运行上游与 EvalKit port：

1. 固定 checkpoint、输入、seed、temperature、CFG、resolution；
2. 比较 marker 触发次数；
3. 比较每轮 token 序列；
4. 比较生成图 hash；若 kernel 非确定，则比较像素/embedding 距离和语义输出；
5. 比较最终答案；
6. 对 divergence 给出可解释的兼容差异。

至少覆盖：

- 单图 T1/T2；
- 多图或候选图输入；
- marker 不触发；
- 恰好一次触发；
- 达到 `max_rounds`；
- 生成失败和 OOM 恢复。

### 7.6 capability 翻转条件

只有满足以下全部条件后才更新 config：

- 上游来源已记录；
- differential test 通过；
- marker policy 已验证；
- 生成图落盘和 trace 完整；
- 小样本 Track-G 质量评测可运行；
- restart/stateful 结果不共享错误 cache。

然后设置：

```yaml
strategies:
  - direct
  - self_draw_restart
  - stateful_forced
  - native_autonomous

backend_args:
  interleave:
    marker_start: "<img>"
    marker_end: "</img>"
```

---

## 8. Phase 3：LatentUM save-rewind-reinject 适配

### 8.1 正确的技术描述

LatentUM 上游 `FrozenLakePlanner` 据现有调查执行：

```text
1. 输入图像经过 ViT，构建理解上下文
2. 文本自回归生成，遇到 <img>
3. 保存生成图前的 past_key_values
4. 走 generation path 生成 VQ image codes
5. rewind 到生成图前的 cache
6. 将生成视觉 embeddings 以 understanding mask 重新注入
7. 继续文本推理
```

这属于 stateful visual loop，但不是 Bagel 式简单 continuous append。统一 meta 应写：

```text
state_policy = rewind_reinject
cache_protocol = save_generate_rewind_understand
```

### 8.2 主张边界

`FrozenLakePlanner` 是任务特化 planner。将它改造成 MapSpatial 通用 loop，涉及新的 prompt、
多图输入、停止条件和任务策略。因此论文应称为：

> an adapted stateful inference loop based on LatentUM's released planning implementation

不能在没有额外证据时称为 LatentUM 原生通用 visual-thinking policy。

如果 `<img>` marker 仅在 FrozenLake 数据/模板上训练或使用，则 LatentUM 只进入
`stateful_forced`，不进入 `native_autonomous`。

### 8.3 实现步骤

1. 从上游 planner 中抽取与 FrozenLake 无关的 cache state machine；
2. 保留原始 generation/understanding mask 语义；
3. 将任务特化 prompt 移出 backend，放入 strategy/config；
4. 支持 MapSpatial 的单图和多图 message；
5. 复用官方 image preprocessing；
6. 生成 256 个 VQ codes 或上游配置指定的长度；
7. 使用 `visual_projector` 重新注入；
8. 使用 decoder 输出可评分 PIL 图；
9. 返回完整 trace；
10. 实现 restart branch，消费同一 decoded artifact。

### 8.4 latent 与 decoded image 的公平性

shared 分支可能直接消费 VQ/projector embedding，而 restart 分支只能消费解码后的像素再经 ViT
编码。此时 `Delta_state` 同时包含：

- cache continuity；
- latent/embedding 通道避免 decode-encode 信息损失。

因此 LatentUM 需要明确报告两种比较：

1. **系统级比较**：官方 shared latent path vs restart pixel path；
2. **尽量匹配的表示比较**：若接口允许，让 shared 分支也消费 decoded-and-reencoded image。

如果第二种不可实现，论文不得将全部增益单独归因于 KV-cache。

### 8.5 LatentUM 成功门槛

- 上游 planner 在原 FrozenLake demo 上可复现；
- 抽取前后 demo 输出一致；
- MapSpatial 单图样本可以完成至少一轮 reinjection；
- decoder 输出与内部 VQ codes 一一对应；
- trace 能证明 rewind 点和 understanding reinjection 已执行；
- 不出现 transformers/attention mask 退化；
- 在小样本上没有系统性重复 token、空图或全黑图。

LatentUM 是三项扩展中风险最高的一项。若前两阶段已经形成完整论文证据，而 LatentUM 无法稳定
通过上述门槛，可以只保留 `self_draw_restart`，不应为了让结果表更整齐而降低 native 标准。

---

## 9. 其他统一模型的处理

BLIP3o、Janus-Pro、Show-o2 和 JoyAI-Image 当前继续使用 `self_draw_restart`。除非找到并验证
其官方 stateful loop，否则：

- 不把相同权重的两次调用称为 stateful；
- 不因模型同时具有理解头和生成头就推断它共享 cache；
- 不复制 Bagel/ThinkMorph inferencer 到架构不匹配的模型；
- 不把手写 agent loop 描述为模型原生能力。

它们仍然对 RQ4 很重要，因为 restart 条件回答了一个现实问题：即使没有原生交错接口，统一模型
能否通过标准的生成 API 和理解 API 使用自己创建的视觉证据？

---

## 10. Prompt 与 supportive-evidence 设计

### 10.1 生成提示必须与任务相关

继续复用 `configs/strategies/external_draw.yaml` 的 task-specific instruction，但将文件重命名或
扩展为通用 visual-evidence policy，使 restart、stateful forced 使用同一模板。

每种 question type 指定允许的 supportive primitives：

| Task type | 允许的证据 |
|---|---|
| direction | reference ray/arrow，不写方向答案 |
| nearest point | 从参考点到所有候选点的测量线 |
| egocentric side | forward axis 与 queried point |
| angular order | 指向所有候选点的 rays |
| Euclidean distance | 所有待比较直线段 |
| network distance | 所有待比较路线和 via points |
| counting | 查询区域/路段与所有相关建筑，不圈出最终计数 |
| route validity | 所有候选路线、障碍和 forbidden regions |
| waypoint ordering | 显示候选 waypoints 和连接约束，不写选项 |

### 10.2 禁止 solution leakage

supportive evidence 禁止：

- 最终答案文本；
- 选项字母；
- 数值答案；
- 只高亮正确候选；
- 删除错误候选；
- 通过颜色或图例唯一编码正确答案；
- 修改与原图不一致的道路、建筑和拓扑。

自动 leakage detector 与人工审计都必须在回答准确率之前运行。生成图未通过 leakage 检查时，
对应回答不能被解释为合法 visual-thinking gain。

### 10.3 forced 和 autonomous 的 prompt 必须区分

- `stateful_forced`：明确要求模型现在生成指定 supportive evidence；
- `native_autonomous`：只说明模型可以使用视觉工作区，不强制每题生成；
- 不能给 autonomous 条件塞入逐任务“必须画什么”的答案性指导，否则触发策略已不再自主。

---

## 11. 实验设计

### 11.1 最小完整矩阵

对每个支持的模型、scene、question、view 运行：

```text
D   direct
O   gold supportive evidence
R   self_draw_restart
F   stateful_forced
A   native_autonomous（仅 capability 支持时）
```

并保留 deterministic GIS evidence 作为 calibration。

### 11.2 主要差值

```text
Delta_oracle  = Acc(O) - Acc(D)
Delta_restart = Acc(R) - Acc(D)
Delta_forced  = Acc(F) - Acc(D)
Delta_state   = Acc(F_same_artifact) - Acc(R_same_artifact)
Delta_auto    = Acc(A) - Acc(D)
```

解释：

- `Delta_oracle`：正确 supportive evidence 的可用上限；
- `Delta_restart`：模型自己构造证据后，仅靠显式图像能获得多少收益；
- `Delta_state`：在 artifact 尽量相同条件下，内部状态连续性的附加价值；
- `Delta_auto`：完整自主视觉思考的 intention-to-treat 效果。

### 11.3 autonomous 必须同时报告 ITT 和 triggered subset

模型自主选择不画时，不能只分析成功触发的样本。至少报告：

- 所有 eligible 样本上的 ITT accuracy/gain；
- `draw_rate`；
- triggered subset accuracy；
- non-triggered subset accuracy；
- 按 direct correctness 分层的 correction/regression rate。

Triggered subset 是模型自己选择出来的，存在 selection bias，只能作为诊断，不能替代 ITT 主结果。

### 11.4 证据正确性与回答收益联合分析

每个生成 artifact 分为：

- geometry-correct / incorrect；
- leakage-pass / fail；
- case-specific / generic；
- consumed / ignored。

报告四类结果：

```text
correct evidence + answer corrected
correct evidence + answer unchanged/worse
incorrect evidence + answer follows error
incorrect evidence + answer resists error
```

这比只报告平均 `Delta_gen` 更能证明模型是否真正使用了视觉证据。

### 11.5 必要控制条件

除已有 wrong/shuffled/masked oracle 外，增加或明确：

- `generated_shuffled`：读取另一场景的模型生成图；
- `generated_masked`：删除一个关键 primitive；
- `generated_wrong`：几何合理但答案不一致的生成证据；
- `extra_call_text_only`：增加等量文本推理/调用预算但不给生成图；
- `blank_generated_canvas`：相同图像 token/分辨率预算但无证据；
- `same_artifact_restart/shared`：状态效应的核心控制。

`extra_call_text_only` 很重要，用于排除提升仅来自“多调用一次、多生成一些 token”。

### 11.6 统计口径

- 以 geographic scene 为 bootstrap/resampling unit；
- paired comparison 必须在同 scene/question/view 上进行；
- 报告 95% scene-bootstrap CI；
- 多 task 汇总使用预先声明的 macro 规则；
- 同时报 correction rate 和 regression rate；
- 对不同 capability 的模型不做虚假的全模型 paired macro；
- compute/latency/image-generation rate 作为成本指标报告。

---

## 12. 评测与日志字段

### 12.1 Artifact metrics

- primitive precision/recall；
- geometry distance/angle/overlap；
- topology/path validity；
- leakage pass rate；
- edit faithfulness/background preservation；
- EPG-Q 或论文定义的 evidence quality composite；
- deterministic renderer gap。

### 12.2 Answer metrics

- accuracy；
- `Delta_oracle/restart/state/auto`；
- correction/regression；
- support-gain ratio；
- representation/view breakdown；
- task/difficulty breakdown。

### 12.3 Trace/provenance

每轮保存：

```json
{
  "round": 0,
  "kind": "image",
  "path": ".../sample_r0.png",
  "sha256": "...",
  "triggered_by": "forced",
  "marker": null,
  "state_policy": "shared",
  "cache_protocol": "continuous_append",
  "elapsed_s": 12.3
}
```

模型级 meta 还应包含：

- checkpoint/config hash；
- upstream repo commit；
- strategy canonical name；
- prompt template version；
- seed；
- resolution/CFG/steps；
- marker token ids；
- artifact hash；
- decoding budget。

---

## 13. 测试与验证计划

### 13.1 单元测试

- strategy 注册和 legacy alias；
- capability fail-fast；
- per-model marker 进入 RunContext；
- canonical meta 字段完整；
- PIL 自动落盘为 Path；
- sample id/round 命名；
- artifact hash 稳定；
- Track 映射；
- unsupported strategy 明确报错；
- `draw_triggered` 与实际 artifact 数量一致。

### 13.2 backend contract test

每个 UMM 测试：

- direct 单图；
- restart 原图 + 生成图多图输入；
- draw 返回可解码图像；
- failure 不污染下一样本 cache；
- seed 是否可复现；
- max image count；
- OOM 后清理。

### 13.3 stateful 专项测试

- cache 在生成前后是否真实变化；
- shared 分支没有意外重建模型/context；
- restart 分支没有复用 shared cache；
- paired artifact hash 完全一致；
- 分支执行顺序不改变结果；
- max-round termination；
- marker false positive/false negative；
- image feedback 走 understanding path 而不是再次走 generation path。

### 13.4 小样本人工审计

每个 task/view/strategy 至少抽取若干：

- 中间图是否与输入场景一致；
- 是否包含要求的 supportive primitive；
- 是否泄露答案；
- 是否修改背景或拓扑；
- 最终回答是否引用/遵循图中证据；
- restart/shared 对相同 artifact 的行为差异。

---

## 14. 文件修改计划

### Phase 0

| 文件 | 修改 |
|---|---|
| `mapspatial/types.py` | 扩展 capability、meta/trace 契约和 interleave config |
| `mapspatial/runner.py` | 显式加载 marker/config；修正 Track 映射 |
| `mapspatial/strategies/base.py` | 精确 capability validation |
| `mapspatial/strategies/external_draw.py` | 迁移为 canonical `self_draw_restart` |
| `mapspatial/strategies/self_draw_restart.py` | 新 canonical strategy，或重命名现文件 |
| `mapspatial/strategies/stateful_forced.py` | 新 strategy |
| `mapspatial/strategies/native_interleave.py` | 迁移为 `native_autonomous` 语义 |
| `mapspatial/strategies/__init__.py` | 注册 canonical names 和 legacy alias |
| `mapspatial/artifacts.py` | 可选：统一图像落盘/hash/provenance |
| `mapspatial/eval/metrics.py` | G 与 C-R/C-F/C-A 分开聚合 |
| `configs/strategies/*.yaml` | 共用 supportive-evidence 模板和版本号 |
| `tests/` | 补 capability、artifact、track、paired tests |

### Phase 1：Bagel

| 文件 | 修改 |
|---|---|
| `mapspatial/vendor/bagel_interleave/inferencer.py` | 增加受控的 forced/shared 分支 seam，尽量少改 vendor |
| `mapspatial/backends/veomni/bagel.py` | `paired_visual_thinking()` / `stateful_forced()` |
| `configs/models/bagel-7b.yaml` | 声明 stateful=true、autonomous 暂定 false |
| `tests/test_bagel_stateful.py` | same-artifact 与 cache isolation 测试 |

优先在 backend 外写 wrapper；只有 vendor API 无法暴露必要 context 时才修改 vendor，并同步更新
`ORIGIN.md` 记录 patch。

### Phase 2：U1

| 文件 | 修改 |
|---|---|
| `mapspatial/vendor/neo_chat/modeling_neo_chat.py` | vendor/port 上游 `interleave_gen()` |
| `mapspatial/vendor/neo_chat/ORIGIN.md` | 记录来源 commit 和本地 patch |
| `mapspatial/backends/veomni/u1.py` | stateful forced/autonomous wrapper 与 trace |
| `configs/models/sensenova-u1-8b.yaml` | marker 和 capability |
| `tests/test_u1_interleave.py` | contract 与 differential fixtures |

### Phase 3：LatentUM

| 文件 | 修改 |
|---|---|
| `mapspatial/backends/veomni/latentum.py` | 通用 save-rewind-reinject wrapper |
| `mapspatial/vendor/latentum/` | 若决定 vendor 上游 state machine，则记录来源 |
| `configs/models/latentum-base.yaml` | marker/cache protocol/capability |
| `tests/test_latentum_interleave.py` | rewind、mask、decoder 和 trace 测试 |

---

## 15. 实施顺序与决策门

```text
Gate 0: 协议、命名、artifact schema、Track 映射正确
    |
Gate 1: Bagel same-artifact paired prototype 跑通
    |
Gate 2: 小样本证明生成图具有足够质量，Oracle 对应任务存在可用空间
    |
Gate 3: U1 上游 port 通过 differential test
    |
Gate 4: 决定是否投入 LatentUM 通用化
    |
Gate 5: 扩大到完整数据并修改论文结果表
```

具体优先级：

1. 修复当前事实不一致和落盘 bug；
2. Bagel restart/shared paired prototype；
3. U1 官方 loop port；
4. ThinkMorph 作为 autonomous reference 做同口径重跑；
5. LatentUM 适配；
6. 其他四个模型保持 restart baseline；
7. 完整 benchmark 批量运行。

不建议先改 GPU 批量脚本。大规模运行脚本应在策略语义和输出 schema 稳定之后更新，否则会生成
一批难以重新归类的结果。

---

## 16. 风险与缓解

| 风险 | 后果 | 缓解 |
|---|---|---|
| 把同权重两次调用误称 shared-state | 方法主张不成立 | 以 cache/context 是否跨生成连续为准 |
| 把 forced loop 称为 native | 模型能力被夸大 | 分开 forced/autonomous |
| Bagel marker 未训练 | native 触发率和结果不可解释 | trigger audit；headline 使用 forced |
| U1 port 偏离上游 | 结论建立在错误实现上 | 原样 vendor + differential test |
| LatentUM planner 过度任务特化 | 通用化后行为不再代表原模型 | 标注 adapted；先复现原 demo |
| LatentUM shared/restart 表示不匹配 | `Delta_state` 混入 latent 通道优势 | 报告系统级与表示匹配两种比较 |
| generated image 未落盘 | 无法评分和审计 | 统一 artifact manager |
| marker 配置未生效 | 静默不触发 | runner 显式传参 + token-level audit |
| 强制生成泄露答案 | 虚假 accuracy gain | supportive schema + leakage gate |
| 多一次调用带来文本预算优势 | 将 compute gain 误当 visual gain | `extra_call_text_only` 控制 |
| autonomous triggered subset 偏差 | 高估视觉思考效果 | ITT 为主，subset 仅诊断 |
| 全部八个模型硬塞进 C | heterogeneous interface 不可比 | C-R/C-F/C-A 分列，unsupported=N/A |
| 生成质量太差 | stateful 结果无解释力 | 先看 Oracle 和 Track-G，再扩规模 |

---

## 17. 论文修改计划

实现稳定后同步修改论文：

1. RQ4 拆成 evidence construction、restart consumption、stateful/autonomous gain；
2. Evaluation Protocol 中定义 C-R/C-F/C-A；
3. 明确 `self_draw_restart` 仍由同一 UMM 生成和读取，不是 external generator；
4. 将 deterministic GIS renderer 保留为 external-tool calibration；
5. 主表增加 restart/stateful/draw-rate 列；
6. 不支持 stateful 的模型填 N/A；
7. 附录记录 checkpoint、上游 commit、marker、cache protocol 和 re-consumption 路径；
8. Discussion 明确不同模型可能使用 pixel re-encode、continuous cache 或 rewind-reinject；
9. 对 Bagel 使用 “training-free stateful forced inference”，不轻率使用 native；
10. 对 LatentUM 使用 “adapted stateful inference loop”；
11. 只有通过上游协议核验的 ThinkMorph/U1 才使用 native/autonomous；
12. 报告 negative results：生成图错误、共享状态无增益同样是 benchmark 结论。

推荐的论文主张是：

> MapSpatial factorizes visual evidence generation-to-understanding into
> evidence construction, restart consumption, stateful integration, and
> autonomous triggering, enabling capability-aware and causally cleaner
> comparisons across heterogeneous unified multimodal models.

这仍然是 benchmark/evaluation contribution，而不是新的训练方法。

---

## 18. 完成标准

只有满足下列条件，training-free visual-thinking 部分才算完成：

- [ ] `external_draw` 已迁移为语义明确的 `self_draw_restart`；
- [ ] legacy config/result 仍可读取；
- [ ] capability 能区分 draw、reconsume、stateful、autonomous；
- [ ] Track G 与 C-R/C-F/C-A 不再混淆；
- [ ] 所有生成图按 sample id 落盘并带 hash；
- [ ] marker 配置真实生效且进入 provenance；
- [ ] Bagel same-artifact restart/shared prototype 通过；
- [ ] ThinkMorph native reference 按新 schema 输出；
- [ ] U1 上游来源和 differential test 完成；
- [ ] LatentUM 被正确标记为 adapted，或明确保持 restart-only；
- [ ] forced/autonomous prompt 不泄露答案；
- [ ] Oracle、text-only extra-call、wrong/shuffled/masked controls 齐全；
- [ ] ITT、trigger rate、correction/regression 和 artifact quality 均可聚合；
- [ ] 论文 RQ4、Track、主表和附录与代码完全一致。

在这些条件满足前，不应仅通过把 `native_interleave=False` 翻成 `True` 来宣称模型获得了
training-free visual thinking 能力。
