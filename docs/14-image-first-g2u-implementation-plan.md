# 14 · Image-First G2U 实现计划

> 基线：main@2226df2；设计对照：[13-forced-interleave-review.md](./13-forced-interleave-review.md)、[09-training-free-visual-thinking.md](./09-training-free-visual-thinking.md)。  
> 本文是评估用实现计划，不改代码。同意后再按 P0 → P1 → P2 落地。  
> 范围：`external_draw`（C-R）与 `forced_interleave`（C-F）。`native_interleave`（C-A）与 `direct`（U）不改语义。

---

## 0. 结论

采纳文档 13 的主协议：**training-free、image-first、single-image Generate → Understand**。

当前 C-F / C-R 测的是混合干预（先写一段 T0、两套 prompt、两张可能不同的图），不能解释 `Delta_visual` / `Delta_state`。主实验应收成：

```text
同一问题 + 原图 + 同一套 task-specific 绘图指令
  → 立刻生成恰好一张 answer-agnostic 图 I0（不先生成自由文本）
  → C-R：丢弃生成 KV，fresh encode 后再答
  → C-F：同一 state/KV 回注 I0 后再答
```

相对文档 13，本计划有四处优先级调整：

| 点 | 文档 13 | 本计划 |
|---|---|---|
| 共享 G primitive | P0 隐含 | **P0 硬要求**：C-R / C-F 必须走同一套 generation helper |
| C-R-replay | P2 | **P1**：没有 matched artifact 就不要报 `Delta_state` |
| U1 position index | P1 | **P0**：错位会污染所有生成路径，后面全要重跑 |
| 跨模型统一 `image_first_inference` | 第 6 节写法偏像一个大函数 | **策略层协议统一，helper 按 backend 拆** |

乱码风险见 §3：协议本身不太会导致 tokenizer 乱码；乱码几乎一定是 KV / indexes / 特殊 token 接线错误。语义变差（答非所问、很短）是预期，算实验结果。

现有 `results_draw/` **不能**和改协议后的 C-R 比，必须换输出目录重跑。

---

## 1. 现在为什么不好用

### 1.1 科学问题被协议稀释

要回答的是：不改权重，强制生成一张任务相关视觉证据再读它，准不准会涨？进一步拆：

```text
Delta_visual = Acc(C-R) - Acc(U)          # 图本身有没有帮助
Delta_state  = Acc(C-F) - Acc(C-R)        # 仅当同一张 I0、同一套 G
Delta_total  = Acc(C-F) - Acc(U)
```

`Delta_state` 只有在 **同一生成目标、同一 prompt、尽量同一张图** 时才可解释。

当前实现把下面这些一起混进了差值：

- 是否先生成 T0（文本 CoT、EOS、token budget）
- C-R 与 C-F 的绘图指令是否相同
- 两张独立采样的图
- LatentUM：C-F 回注 VQ latent，C-R 走 pixel 重编码

### 1.2 代码事实（对照 2226df2）

**Bagel C-F**（`vendor/bagel_interleave/inferencer.py` `forced_interleave_inference`）：

```text
encode prompt → gen_text(max 500 / think tokens) → gen_image → 再 gen_text
```

这是 plan-then-image，不是 image-first。

**Bagel C-R `draw()`**（`backends/veomni/bagel.py`）：调用同一套 `forced_interleave_inference`，只把 PIL 抠出来、文本丢掉。G 阶段同样先写了一段推理。ThinkMorph 继承这条路径。

**U1 / LatentUM C-F**：`force_image_at=256/96`，prefix 后先 AR 文本，到阈值或 EOS 才进图像。模型可以在画图前就把选项说完。

**Prompt 不对齐**：

- C-R：`RunContext.draw_instruction()` ← `configs/strategies/external_draw.yaml` 的 12 类 question_type
- C-F：`backend.forced_interleave(sample.message)`，**不传 instruction**，吃的是原题 + backend 内部 think / GEN_THINK_SYSTEM_PROMPT

`draw_followup_text` 在 YAML 里有，但 `RunContext` 用的是 dataclass 默认值，loader **没有**从 YAML 读进去（`types.py` 只 load 了 `draw_instruction` 字典）。

**capability 写错**：`ForcedInterleaveStrategy.required_caps()` 只要求 `draw=True`；`_available_strategies()` 对所有 `draw=True` 的 backend 同时挂上 `forced_interleave`。Janus / Show-o2 / BLIP3o / JoyAI 能画，但不能同一次增量状态里切模态、回注、再继续生成。

**参数混用**：`ctx.max_rounds` 同时传给 native 和 forced。native 的「自主交错上限」和 forced 的「强制画几张图」不是一回事。主协议应固定 `max_images=1`。

**U1 `think_mode` 泄漏**：C-F 的 `forced_interleave()` `setdefault("think_mode", True)`；`draw()` 也可能吃到 yaml 里的 `_think_mode`。主协议 G 阶段不应默认先 think。

### 1.3 谁参加哪张表

| Backend | U `direct` | C-R `external_draw` | C-F `forced_interleave` | C-A `native_interleave` |
|---|---|---|---|---|
| Bagel | 是 | 是 | 是 | 保留，不进本轮主表 |
| ThinkMorph | 是 | 是 | 是 | 是（自主 marker，不改） |
| SenseNova-U1 | 是 | 是 | 是 | 否（caps 已关） |
| LatentUM | 是 | 是 | 是（须标 latent reconsume） | 否 |
| Janus / Show-o2 / BLIP3o / JoyAI | 是 | 是 | **否** | 否 |

只支持 T2I、不能消费原图做 G 的 backend，C-R 可跑，但报告里单独分组（`generation_conditioning=text_only`），不能和 image-conditioned G 混着解释。

---

## 2. 主协议（实现时的合同）

### 2.1 Generation

```text
输入：原始问题 + 原始图像 + visual_generation_instruction
行为：立即生成恰好一张 I0
禁止：先生成自由文本回答；禁止第二张图；图中写答案 / 选项字母
```

`visual_generation_instruction` = 共享 generation_system_prompt + question_type 的 draw_instruction（现有 12 类直接迁移）。

约束写进 system prompt：只画与问题有关的几何证据、统一蓝色为模型新增标记、不改无关原图内容、只出一张图。

### 2.2 Understand

**C-R（restart）**

```text
G:  用上面的输入生成 I0
    丢弃生成 KV
U:  fresh encode(原问题, 原图, I0, 中性 follow-up) → 答案
```

Follow-up 建议改为（与 YAML 对齐时一并改，两边共用）：

```text
Use the generated visual evidence to answer the original question.
```

不要往 U 里塞一段假的 generation transcript。C-F 没有 T0，C-R 硬塞 transcript 会制造新的 prompt 差。

**C-F（stateful）**

```text
prefill: 原问题 + 原图 + 同一套 visual_generation_instruction
force:   不生成 T0，立即进入 image phase → I0
reconsume: 把 I0 的理解表示写回当前 KV
continue: 同一逻辑状态进入 answer phase → 答案
```

答案阶段的 token 边界本来就和 C-R 不同（continuation vs 新 user turn）。**对齐的是 G，不是 U 的 token 序列。** 不要为了「两边 prompt 长得一样」去破坏 Bagel 的 CFG context。每个 backend 二选一，并写入 `post_image_prompt_mode`：

- `initial_phase_instruction`：初始 system 里声明「先画一张，回注后再答题」
- `appended_user_turn`：回注后追加合法 user turn（用同一条 follow-up）

### 2.3 明确不做（本轮主表）

- 先 T0 再画（plan-then-image）—— P2 消融，保留旧 `force_image_at` 路径为开关
- 多轮 visual CoT、`max_images>1`
- 把 Zebra-CoT / ThinkMorph 专项训练和 training-free C-F 混报
- 给 Janus 等没有 stateful 回注的模型挂 `forced_interleave`

---

## 3. 乱码担心：怎么判断、怎么拦

**协议不会 magically 打出乱码。** prefix 完立刻 `gen_image` / 注入 `img_start`，再 continuation，对三个主模型都是合法路径，接近官方 T2I 后再理解。

更可能出现的是：

| 现象 | 含义 | 处理 |
|---|---|---|
| 能抽出 A–D，但准不准差、很短、跑题 | 模型没按 image-first 训过 | **实验结果**，主表照收；P2 用 plan-then-image 解释 |
| 空白、重复特殊符、明显非文本、抽取全失败 | KV / indexes / mask / 漏特殊 token | **接线 bug**，修完再跑实验 |
| 图里写了选项字母 | prompt 没压住 | 收紧 generation_system_prompt；验收时人工看图 |

各 backend 的高危接线（P0 smoke 必须盯）：

- **Bagel**：回注必须 `update_context_image(..., vae=True, vit=True)`；少一边 context 会漂，不一定乱码但答案会漂。
- **U1**：显式 `indexes` 相对官方隐式 `current_index` 少 +1 的话，图后文本最容易花。所有 continuation（condition / uncond / img_start / img_end / 图后）按同一约定修，不要只改 forced 分支。
- **LatentUM**：`kv_before_img` rewind、`vision_token_mask`、img_start/end 与 token 列表必须对齐；错了会脏 cache。

每个 backend 先 5–10 条样本再放大：

1. `pre_image_text_tokens == 0`
2. `generated_image_count == 1`，图能打开
3. trace 第一项是 image，之后才是 answer text
4. `Prediction.text` 非空，抽取器能拿到 A–D（对错不论）
5. C-F 的 `visual_reinjected==true`；C-R 确认是两次独立前向

过不了第 4 条，停止该 backend 的全量跑。

---

## 4. 公共接口与配置

### 4.1 Capabilities

文件：`mapspatial/types.py`、`strategies/base.py`、各 backend `caps`。

```python
class Capabilities(NamedTuple):
    batch: bool
    draw: bool
    native_interleave: bool
    forced_interleave: bool   # 新增：同一次增量状态切模态 + 回注 + 续写
    max_images: int
    video: bool
```

`ForcedInterleaveStrategy.required_caps()` → `{"forced_interleave": True}`。  
`_available_strategies`：`draw` 只开 `external_draw`；`forced_interleave` cap 才开 C-F。

建议 cap：

| Backend | draw | forced_interleave | native_interleave |
|---|---|---|---|
| Bagel | true | true | true（C-A 另测） |
| ThinkMorph | true | true | true |
| U1 | true | true | false |
| LatentUM | true | true | false |
| Janus / Show-o2 / BLIP3o / JoyAI | true | false | false |

`Backend.forced_interleave` 在基类显式声明（现在只有 bagel/u1/latentum 各写一份，签名还不统一）。

### 4.2 Backend 方法

```python
def draw(self, context: Message, instruction: str, **kw) -> Image:
    """G-only。必须走与 C-F 相同的 image-first primitive，返回一张 PIL，不返回答案。"""

def forced_interleave(
    self,
    message: Message,
    instruction: str,
    *,
    max_images: int = 1,
    image_first: bool = True,
    followup: str = "",
    **kw,
) -> Prediction:
    """image_first=True 时禁止先生成自由文本。text 必须是回注后的答案。"""
```

约束：

- 主协议 `image_first=True`、`max_images=1`
- `instruction` 与 `draw()` 完全相同
- 不要把 `ctx.max_rounds` 传进 forced
- `Prediction.text` 只取图后文本；trace 能证明 image 在 answer 之前

每个 stateful backend 拆四个内部 helper（名字可不同，职责必须分开）：

```text
_prepare_generation_context(message, instruction)
_generate_one_image(prepared, gen_kw) → (PIL or latent, state)
_reconsume_generated(image_or_latent, state)
_generate_answer(state, followup) → text
```

- C-R `draw()`：前两步，丢 state，返回 PIL
- C-F：四步都走，保留 state

禁止 C-R 再调用「先 gen_text 再画」的 forced 循环再丢文本。

### 4.3 Strategy

`forced_interleave.py`：

```python
instruction = ctx.visual_generation_instruction(sample)
pred = backend.forced_interleave(
    sample.message,
    instruction,
    max_images=1,
    image_first=True,
    followup=ctx.understand_followup,
    **answer_kw,          # 与 draw_kw 分开
)
```

`external_draw.py` 保持 `draw()` + `understand()`，但：

1. instruction 来自同一 G2U 配置
2. 真正加载 `understand_followup` / `generation_system_prompt`
3. `draw_generate` 与 `answer_generate` 分套参数，避免 temperature 等同名串台
4. U 阶段消费 **全部原图 + I0**（生成图追加，不覆盖原图路径）

### 4.4 配置拆分

新建 `configs/strategies/g2u.yaml`（或把 `external_draw.yaml` 升格，保留文件名 alias）。建议结构：

```yaml
protocol: image_first_single_image
max_generated_images: 1
image_first: true
seed: 42
save_generated: true

generation_system_prompt: |
  Generate exactly one answer-agnostic visual scratchpad that helps solve
  the spatial question. Do not write the final answer, an option letter,
  or explanatory text into the image.
  First generate exactly one visual scratchpad.
  After the visual scratchpad has been incorporated, answer the original question.

understand_followup: >
  Use the generated visual evidence to answer the original question.

draw_instruction:
  direction: "Draw one blue arrow ..."
  # ... 现有 12 类原样迁移

draw_generate:
  seed: 42
  temperature: 0.0

answer_generate:
  temperature: 0.0
  max_new_tokens: 512
```

模型 yaml **只留** backend 固有参数（CFG、步数、分辨率、decoder 路径）。不要再用 `backend_args.max_rounds` 同时管 native / forced / external。

`RunContext` 增加：`visual_generation_instruction(sample)`、`understand_followup`、`draw_kw` / `answer_kw`、`g2u_seed`。YAML 的 follow-up 必须真正读进来。

### 4.5 Trace / meta（主协议）

```text
trace:
  round=0 kind=image  triggered_by=forced_image_first
  round=1 kind=text   text=final_answer
```

统一 meta（写入 JSONL，方便验收脚本扫）：

```python
{
    "strategy": "external_draw" | "forced_interleave",
    "protocol": "image_first_single_image",
    "stateful": bool,
    "draw_triggered": True,          # 是否真正进了生成，与是否落盘 PNG 无关
    "visual_reinjected": True,
    "rounds": 1,                     # 实际生成并回注的视觉步数，不是文本循环数
    "generated_image_count": 1,
    "pre_image_text_tokens": 0,
    "reconsume_mode": "pixel" | "latent",
    "generation_conditioning": "text_only" | "text+source_images",
    "post_image_prompt_mode": "initial_phase_instruction" | "appended_user_turn",
    "generation_prompt_hash": "...",
    "generated_image_sha256": "...",
    "seed": 42,
}
```

`generated_images` 与 image TraceStep.path 必须一一对应。`--no-save-generated` 时 `draw_triggered` 仍为 true。

---

## 5. 分 backend 改什么

### 5.1 Bagel / ThinkMorph（P0 第一刀，收益最大）

现状：C-R 和 C-F 都在先写最多 500 token。

在 `vendor/bagel_interleave/inferencer.py` 增加 image-first 路径（或把现有 `forced_interleave_inference` 拆 helper），**不要**再走 pre-image `gen_text()`：

```text
init gen_context / cfg contexts
→ 写入 G2U generation_system_prompt
→ 写入 original message
→ 写入 task-specific instruction
→ gen_image() exactly once
→ C-F: update_context_image(I0, vae=True, vit=True) → 合法进入 answer → gen_text()
→ C-R: 返回 PIL，丢 context
```

注意：

- ThinkMorph 继承同一 forced / draw 实现；它的 marker-driven 只留在 `native_interleave`
- `draw()` 改为 `keep_context=False` 的同一 primitive
- `Prediction.text` 只取图后文本；禁止再把 pre-image think 拼进答案
- `max_images=1` 后禁止再进 image 循环
- smoke：确认 CFG 的 `cfg_text_context` / `cfg_img_context` 在「没有 T0」时仍按官方 T2I 方式初始化（这是 Bagel 最可能「图很差」而不是「乱码」的点）

### 5.2 SenseNova-U1（P0：image-first + indexes）

**C-R `draw()`**：已经直接 `it2i_generate()`，方向对。改动：

- G 显式 `think_mode=False`，**不要**用 `self._think_mode`
- full_prompt = 原问题 + 同一套 task instruction
- seed / size / CFG / steps 固定并记入 meta
- understand 重新编码原图 + I0

**C-F**：现在只有 `force_image_at > 0`（先文本再注入）。增加：

```python
force_image_first: bool = False
post_image_max_tokens: int | None = None
```

prefix forward 完成后：

```text
if force_image_first:
    next_token = img_start
    直接进现有 image branch
图像生成 → ViT 重编码 → img_end → 从图后 cache 答
max_images=1 时禁止再进 image phase
```

旧 `force_image_at` 保留为 plan-then-image 开关，默认主协议不用。

**indexes（P0，全路径）** 统一约定：

```text
t_index = last_committed_temporal_position
next_index = t_index + 1
forward(indexes=[[next_index], [0], [0]])
t_index = next_index
```

一起审计：condition 续写、text-uncond 续写、img_start、image temporal plane、img_end、图后续写、`_generate_think()`、`_append_text_tokens_to_cache()`。只改 forced 分支会留下不一致。

### 5.3 LatentUM

**C-R `draw()`**：已是 `generate_latents(_with_images)` → pixel decoder → PIL，方向对。G prompt 换成统一 instruction；U 为 fresh encode（原图 + PIL I0 + follow-up）。

**C-F**：增加 `image_first=True`。prefix 后 round 1 **跳过** pre-image AR loop，直接：

```text
kv_before_img = deepcopy(past_key_values)
→ feed img_start (vision_token_mask=1)
→ generate VQ codes
→ rewind kv_before_img
→ inject projected latent (vision_token_mask=0)
→ feed img_end
→ continue final text
```

**必须标注**：C-F 默认 `reconsume_mode=latent`；C-R 是 `pixel`。因此 LatentUM 的 `Delta_state` 同时可能包含 KV 连续、避开 pixel codec、latent 语义。主表单独一列/脚注。P2 再做 `latentum_stateful_pixel`（同会话但 decode 成 PIL 再视觉编码）；若代价大，论文局限里写明。

旧 `force_image_at` 留作消融；修 off-by-one（用 committed_text_tokens 判断阈值，避免 96 变成 95）；`meta.rounds` 改为视觉步数。

### 5.4 仅 C-R 的 UMM（Janus / Show-o2 / BLIP3o / JoyAI）

不实现 C-F。统一要求：

1. `draw(context, instruction)` 消费所有原始输入图；做不到则 `generation_conditioning=text_only` 并分组报告
2. G prompt = 原问题 + 统一 task instruction；只返回一张图，不返回答案
3. U 消费原图 + I0；生成图不覆盖原图路径
4. meta 记 `source_image_count` / `generated_image_count` / `reconsume_mode=pixel`

文档 10 里提过的多图 processor、路径覆盖问题，C-R 重跑前再核对一遍。

---

## 6. Artifact 对齐与 C-R-replay

### 6.1 理想

C-R 与 C-F 同一内部 G primitive：同模型、同 G prompt、同原图、同 seed、同 CFG、同分辨率、同步数、同图数。运行时记 `generation_prompt_hash`、`generated_image_sha256`、seed、params。

### 6.2 P1 必做：C-R-replay

两次独立 G 很难逐像素一致（即使 seed 相同，stateful 与 restart 的 RNG / 数值路径也可能分叉）。增加：

```text
C-F:           stateful 路径生成 I0 并回答（保存 I0）
C-R-replay:    不重新生成，直接 fresh encode 同一张 I0 再答
比较:          Acc(C-F, I0) - Acc(C-R-replay, I0)
```

这才是可发表的 `Delta_state`。独立 G 的 C-F vs C-R 只能当探索，不能当主归因。

实现上可以是 `external_draw` 的 `--replay-from <c-f-run-dir>`，按 sample_id 读已存 PNG，跳过 `draw()`。

---

## 7. 实现顺序

### P0 — 主实验能跑、能过 smoke（建议按此序）

1. **G2U 配置与 RunContext**：抽出共享 prompt；修 YAML follow-up 未加载；draw / answer 参数分开。
2. **capability + 基类签名**：`forced_interleave` cap；strategy 不再把 C-F 挂到仅能 draw 的模型上。
3. **U1 indexes 全路径审计**（确认少 +1 就修；不确认也要在 smoke 里盯图后文本）。
4. **Bagel/ThinkMorph image-first primitive**：C-R / C-F 共用；去掉 pre-image `gen_text`。这是对现有逻辑伤害最大、也最值的一刀。
5. **U1 image-first**：prefix 后立刻 `img_start`；G 阶段 `think_mode=False`。
6. **LatentUM image-first**：prefix 后立刻 VQ image phase；meta 标 `reconsume_mode`。
7. **strategy 接线**：instruction 传入 C-F；`max_images=1`；trace/meta 按 §4.5。
8. **每 backend 5–10 条验收**（§3 + 文档 13 §14 清单）。不过关不大跑。

### P1 — 结果可解释

9. C-R-replay。
10. 确认 C-R 的 U 消费全部原图 + I0；生成图不覆盖原图。
11. 固定并记录 seed / CFG / 分辨率 / steps / image hash。
12. 仅 C-R 的 UMM：标 `generation_conditioning`；T2I-only 分组。
13. LatentUM 主表脚注；旧 `force_image_at` off-by-one 与 `rounds` 定义。

### P2 — 论文消融（主表稳定后再做）

14. LatentUM `stateful_pixel`。
15. plan-then-image（旧 `force_image_at` / Bagel 先 think 再画）作次要条件，**另目录**，不进主表。
16. blank / random visual placebo。
17. 小规模人工看图：有没有答案字母、箭头是否对应 question_type。

---

## 8. 实验矩阵与输出目录

主表：

| 条件 | 训练 | 图像触发 | 状态 | 图像数 |
|---|---|---|---|---:|
| Direct U | 无额外训练 | 无 | fresh | 0 |
| External C-R | training-free | 强制 image-first | restart | 1 |
| Forced C-F | training-free | 强制 image-first | shared state | 1 |
| C-R-replay | training-free | 复用 C-F 的 I0 | restart | 1 |
| Native C-A | checkpoint-dependent | 模型自主 | shared state | 0–N |

输出不要覆盖现有 `results/`、`results_draw/`：

```text
results_g2u/          # 新协议 U / C-R / C-F
results_g2u_replay/   # C-R-replay
results_g2u_ablation/ # plan-then-image 等 P2
```

GPU 脚本新开一组，或给现有 `run_gpu*_draw.sh` 加 `OUTPUT_DIR` + `--strategy`，避免和旧 draw 混在一个 summary 里。

ThinkMorph forced 仍是框架强制（C-F），native 才测自主触发。Zebra-CoT 权重若以后要跑，单独策略名，不要标成 training-free C-F。

---

## 9. 验收清单（每个 backend 过了再放量）

**协议**

- `pre_image_text_tokens == 0`
- `generated_image_count == 1`
- trace：image 在前，answer text 在后
- 最终答案来自图像回注之后（C-F）或 fresh understand（C-R）
- C-R 两次前向；C-F 复用同一 state（可用一次 debug 标志或 cache 对象 id 抽查）

**Prompt**

- C-R 与 C-F 的 G instruction 字节级一致（hash 相同）
- follow-up 不引入新的空间信息
- 图中原则上无答案字母（抽检）

**图像**

- G 消费了所有原图（或显式 `text_only`）
- U 消费了原图 + I0
- PNG 可开、尺寸符合配置
- 保存 sha256

**输出**

- `Prediction.text` 非空，抽取器工作
- `rounds == 1`，`draw_triggered == true`，`visual_reinjected == true`
- `--no-save-generated` 时仍 `draw_triggered == true`

**乱码闸门**：5–10 条里若抽取失败率异常高（相对该模型 `direct`），先当接线 bug 查 U1 indexes / Bagel VAE+ViT / LatentUM rewind，不解释成「image-first 不行」。

---

## 10. 风险与不做什么

**风险**

- Image-first 图画得很差：生成头可能依赖一段 plan。这是主协议允许的失败模式，用 P2 消融解释，不改回主表。
- Bagel 无 T0 时 CFG context 若初始化错，图会差而不是乱码。
- LatentUM `Delta_state` 被误读成纯 KV 效应。
- 旧 `results_draw` 数字被拿来和新 C-R 比。

**本轮不做**

- 不把 C-A 改成 image-first。
- 不强制所有 UMM 实现 C-F。
- 不把 think_mode 从模型 yaml 泄漏进 G。
- 不为了对齐 U prompt 去破坏各模型原生 chat/token 边界。
- 不在修协议的同一 PR 里顺手大改 answer extractor / direct。

---

## 11. 建议的第一张 PR 切分（若同意落地）

评完这份计划后，第一刀建议只含：

1. `g2u.yaml` + RunContext 加载修复（follow-up、分套 generate 参数）
2. `Capabilities.forced_interleave` + strategy 校验
3. Bagel/ThinkMorph 共享 image-first helper，C-R `draw()` 与 C-F 同时切过去

U1 indexes + image-first、LatentUM image-first 各跟一刀，便于 smoke 出问题时归因。C-R-replay 单独一刀，放在三条 stateful 路径都过 5–10 条之后。
