# 04 · 推理策略

> 三种策略的语义、参数、以及它们如何支撑核心消融实验。

---

## 1. 为什么需要策略层

核心问题是：**让模型生成中间图像，是否提升空间理解准确率？**

要回答它必须做三向对比，而这三个条件跑的是**同一个模型、同一份数据**，只有推理编排方式不同：

| 条件 | 策略 | 含义 |
|---|---|---|
| 不画 | `direct` | 统一模型退化成普通 VLM |
| 模型自主画 | `native_interleave` | 模型在思维链里自行决定何时生成 |
| 强制画 | `external_draw` | 每题都先产出一张中间图 |

策略层的存在，使得这三个条件产出**完全一致的 `Prediction` schema**，因此可以进同一张结果表、用同一套指标聚合。这正是消融实验需要的形状。

---

## 2. 策略接口

```python
class Strategy(ABC):
    name: ClassVar[str]

    @abstractmethod
    def required_caps(self) -> dict[str, Any]:
        """声明对 backend 能力的要求。启动时校验，fail-fast。"""

    @abstractmethod
    def run(self, backend: Backend, samples: list[TaskSample],
            ctx: RunContext) -> list[Prediction]: ...
```

每个策略必须在返回的 `Prediction.meta` 里写入：

```python
meta = {
    "strategy": self.name,
    "rounds": <实际轮数>,
    "draw_triggered": <bool>,     # 是否真的生成了图
    "backend": backend.model_name,
}
```

`draw_triggered` 是**必填**，理由见 §4.4。

---

## 3. `direct`

### 语义

不做任何编排，直接把 `Message` 交给 backend。

```python
class DirectStrategy(Strategy):
    name = "direct"

    def required_caps(self) -> dict:
        return {}                     # 无要求，全部 20 个模型可用

    def run(self, backend, samples, ctx):
        messages = [s.message for s in samples]
        preds = backend.understand(messages, **ctx.gen_kw)
        for p in preds:
            p.meta.update(strategy="direct", rounds=1, draw_triggered=False)
        return preds
```

### 用途

1. **14 个纯理解模型的唯一策略**
2. **6 个统一模型的基线条件**——回答「不画的时候它们表现如何」

第 2 点容易被忽略但很重要：如果 Bagel 在 `direct` 下就已经比 Qwen3-VL 强，那么「生成能力带来提升」的结论需要更小心的归因（可能只是模型本身更强，与画图无关）。

### 批量

`caps.batch=True` 的 backend（vLLM、vendor 后的 Bagel 系）在这里享受真批量：整批一次提交。

---

## 4. `native_interleave`

### 4.1 语义

委托给模型**原生的**交错推理循环。模型自主决定是否、何时生成中间图。

```python
class NativeInterleaveStrategy(Strategy):
    name = "native_interleave"

    def required_caps(self) -> dict:
        return {"native_interleave": True}

    def run(self, backend, samples, ctx):
        # 逐条委托（或批量，若 vendor 的 batch inferencer 可用）
        return [backend.interleave(s.message,
                                   max_rounds=ctx.max_rounds,
                                   marker=ctx.marker) for s in samples]
```

### 4.2 为什么不能用外部编排代替

参考 ThinkMorph 的原生循环（`VLMEvalKit_Thinkmorph/vlmeval/vlm/thinkmorph/inferencer.py:260-348`）：

```python
rounds = 0
while rounds < max_rounds:
    gen_text = self.gen_text(gen_context, do_sample=..., temperature=..., max_length=...)
    output_list.append(gen_text)
    gen_context = self.update_context_text(gen_text, gen_context)

    if "<image_start>" in gen_text:                    # ← 模型自己触发
        img = self.gen_image(image_shapes, gen_context,
                             cfg_text_precontext=cfg_text_context,
                             cfg_img_precontext=cfg_img_context,
                             cfg_text_scale=..., cfg_img_scale=...,
                             cfg_interval=..., timestep_shift=...,
                             num_timesteps=..., cfg_renorm_min=...,
                             cfg_renorm_type=..., noise_seed=...)
        output_list.append(img)
        img_input = self.vae_transform.resize_transform(pil_img2rgb(img))
        gen_context = self.update_context_image(img_input, gen_context, vae=not understanding_output)
        rounds += 1
    else:
        break
```

关键在 `gen_context`：**单一 KV-cache 跨轮保持**（`NaiveCache`，见 `modeling/bagel/qwen2_navit.py`）。文本生成、图像生成、图像回填共享同一份注意力上下文。

外部编排（`draw()` 然后 `understand()`）是两次独立的前向，中间 context 丢失。这不是「等价但慢一点」，而是**语义不同**——而且原生形态更贴近模型的训练分布。

所以这两条路径必须都实现，且结果里要记录用了哪条，否则数字不可比。

### 4.3 触发标记的脆弱性

`"<image_start>" in gen_text` 是**子串匹配**（`inferencer.py:325`）。风险：

- 模型换个措辞（"I'll draw a diagram"）→ 生成被静默跳过
- 不同模型的标记不同（Bagel 系用 `<image_start>`，其他模型未必）
- 标记出现在引号内或思维链的讨论中 → 误触发

对策：

```python
@dataclass
class MarkerConfig:
    start: str = "<image_start>"
    end: str | None = "<image_end>"
    mode: Literal["substring", "regex"] = "substring"
```

per-model 可配置，写在 `configs/models/*.yaml` 的 `backend_args` 下。

### 4.4 `draw_triggered` 为什么必填

模型自触发模式下有三种结果：

| 情况 | `rounds` | `draw_triggered` |
|---|---|---|
| 模型判断需要画，画了 | ≥1 | `True` |
| 模型判断不需要画 | 0 | `False` |
| 模型想画但标记没匹配上 | 0 | `False` |

后两种在结果文本上可能难以区分，但对实验结论意义完全不同：前者是模型的**主动选择**，后者是**实现缺陷**。

因此除了 `draw_triggered`，还要在 `trace` 里保留每轮原始文本，以便事后统计「有多少条疑似想画但没触发」。

### 4.5 系统提示词

ThinkMorph 用系统提示词教模型使用标记（`inferencer.py:15-21`）：

```
Let's think step by step to answer the question. For text-based thinking, enclose
the process within <think> </think>. For visual thinking, enclose the content
within <image_start> </image_end>. Finally conclude with the final answer wrapped
in <answer></answer> tags.
```

**注意该文件里 `VLM_THINK_SYSTEM_PROMPT` 与 `GEN_THINK_SYSTEM_PROMPT` 内容逐字相同**——上游的复制粘贴 bug。我们不要照搬这个结构，只保留一份，并做成 per-model 可配置（不同模型的训练时提示词不同，用错会显著降低触发率）。

### 4.6 vendor 而非重写

`inferencer.py`（374 行）+ `batch_inferencer.py`（1072 行）已实现：

- 交错循环 + KV-cache 跨轮维护
- 批量交错（packed KV cache）
- CFG 并行（`ThreadPoolExecutor` 起 worker 模型副本）
- `select_batch_context` 抽取（某些样本在某轮不请求生成时的上下文处理，`batch_inferencer.py:716-781`）

这是真 engineering，不是玩具。重写不划算，vendor 进来按 [07-environment.md §2.3](./07-environment.md) 的纪律管理。

已知约束：`validate_batch_inputs`（`batch_inferencer.py:787-826`）要求 **image-initial** 输入列表。t4 route_validity 是 text-initial，需要适配——列入待验证清单。

---

## 5. `external_draw`

### 5.1 语义

策略层显式编排：先要一张中间图，再基于它作答。

```python
class ExternalDrawStrategy(Strategy):
    name = "external_draw"

    def required_caps(self) -> dict:
        return {"draw": True}

    def run(self, backend, samples, ctx):
        out = []
        for s in samples:
            trace = []
            # 1) 强制生成中间图
            instr = ctx.draw_instruction(s)         # 按 question_type 定制
            img = backend.draw(s.context_message, instr)
            path = ctx.save_generated(s.id, round=0, img=img)
            trace.append(TraceStep(round=0, kind="image", image=path,
                                   triggered_by="forced"))

            # 2) 把中间图追加进 message 后作答
            msg = s.message + [
                {"type": "text",  "value": ctx.draw_followup_text},
                {"type": "image", "value": path},
            ]
            pred = backend.understand([msg], **ctx.gen_kw)[0]
            pred.generated_images = [path]
            pred.trace = trace + pred.trace
            pred.meta.update(strategy="external_draw", rounds=1, draw_triggered=True)
            out.append(pred)
        return out
```

### 5.2 用途

| 用途 | 说明 |
|---|---|
| **强制条件的消融** | 保证每题都有视觉 CoT，与「模型自主」形成对照 |
| **无原生循环模型的生成路径** | BLIP3o / LatentUM / Janus 若无交错循环，只能走这条 |

### 5.3 绘图指令按任务定制

不同 `question_type` 需要画的东西不同。通用指令（"draw something helpful"）大概率无效。

| question_type | 绘图指令方向 |
|---|---|
| `direction` | 画出从绿点到紫点的方向箭头 |
| `nearest_point` | 标出参考点到各候选点的连线 |
| `composite_route_distance` | 描出两条待比较路线 |
| `segment_building_count` | 高亮指定路段的指定一侧 |
| `route_validity` | 标注每个候选路线的走向 |
| `waypoint_ordering` | 按序连接途经点 |

这些指令模板放 `configs/strategies/external_draw.yaml`，可迭代调整。**指令质量直接决定这个条件的实验结论**，需要先在小样本上人工检查生成图是否合理，再跑全量。

### 5.4 与 `native_interleave` 的结果差异要归因

同一模型（如 Bagel）跑两种策略若差异明显，可能原因：

- context 丢失（外部编排的固有劣势）
- 绘图指令与模型训练时的提示分布不匹配
- 强制画在本不需要画的题上引入噪声

因此 `trace` 里必须留住中间图路径和每轮文本，否则无法归因。

---

## 6. 实验矩阵

```
14 个纯理解模型  × direct                                    = 14 组
6 个统一模型     × {direct, native_interleave, external_draw} ≤ 18 组
```

实际组数取决于每个统一模型的能力（`native_interleave` 需 `caps.native_interleave=True`）。config 里逐模型声明：

```yaml
# configs/models/bagel-7b.yaml
strategies: [direct, native_interleave, external_draw]

# configs/models/blip3o-8b.yaml
strategies: [direct, external_draw]        # 无原生交错循环
```

结果目录按策略分层，避免覆盖：

```
results/{model}/{strategy}/{view}/{task}/{variant}.jsonl
results/{model}/{strategy}/generated/{view}/{task}/{variant}/{sample_id}_r{n}.png
results/{model}/{strategy}/summary.json
```

---

## 7. 中间图的落盘规则

修正 ThinkMorph 的缺陷（`ThinkMorph.py:429` 用 `uuid8 + idx`，不含 sample_id）：

```
{results}/{model}/{strategy}/generated/{view}/{task}/{variant}/{sample_id}_r{round}.png
```

| 规则 | 原因 |
|---|---|
| 含 `sample_id` | 部分重跑后能对回样本 |
| 含 `round` | 多轮生成时可区分 |
| 按 view/task/variant 分目录 | 避免单目录几万文件 |
| 路径写入 `Prediction.generated_images` | 评测/审计层能定位 |

`--no-save-generated` 选项用于只关心准确率的快速跑（几万张中间图占空间不小），但**默认必须保存**——否则核心科学目标无法达成。

---

## 8. 相关文档

| 主题 | 文档 |
|---|---|
| `Prediction` / `TraceStep` 定义 | [01-architecture.md](./01-architecture.md) |
| 各 backend 的 `draw` / `interleave` 实现 | [05-veomni-integration.md](./05-veomni-integration.md) |
| 指标如何按策略聚合 | [06-runner-eval.md](./06-runner-eval.md) |
| vendor 纪律 | [07-environment.md](./07-environment.md) |
