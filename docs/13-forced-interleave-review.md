# 13 · Training-Free Generate-then-Understand 设计与实现建议

> 设计基线：main@2226df2（2026-08-27）  
> 适用范围：MapSpatial-EvalKit 的 external_draw（C-R）与 forced_interleave（C-F）。  
> 目标模型：Bagel、ThinkMorph、LatentUM、SenseNova-U1；external_draw 进一步覆盖 Janus、Show-o2、BLIP3o、JoyAI 等支持生成与理解的统一多模态模型。  
> 本文替代此前“先生成文本推理再画图”的建议。主协议是 training-free、image-first、single-image 的 Generate → Understand。

## 1. 科学问题

本项目不训练新的 visual-CoT policy。核心问题不是模型是否学会自主选择画图，而是：

> 对同一个统一理解–生成模型，在不更新权重的情况下，先强制生成一张与任务有关的视觉证据，再让模型读取该视觉证据，是否能够提升空间理解准确率？

进一步拆成两个问题：

1. 视觉证据是否有帮助？
2. 保留统一模型内部的连续状态，是否优于生成后重新开始一次理解请求？

对应主比较：

~~~text
U   direct               无生成图
C-R external_draw        生成图后 restart / re-encode
C-F forced_interleave    生成图后保持同一 state / KV
~~~

在 prompt、模型、生成参数和图像数量匹配时：

~~~text
Delta_visual = C-R - U
Delta_state  = C-F - C-R
Delta_total  = C-F - U
~~~

其中 Delta_state 只有在两条路径使用相同生成目标、相同 prompt，并尽量产生相同视觉 artifact 时才可解释。

## 2. 主协议：image-first、single-image G2U

### 2.1 Generation 阶段

输入：

~~~text
原始问题
+ 原始输入图像
+ question-type-specific draw instruction
~~~

行为：

~~~text
立即生成恰好一张 answer-agnostic 中间图 I0
不先生成自由文本回答
不允许生成第二张图
~~~

### 2.2 Understand 阶段

生成 I0 后：

~~~text
原始问题 + 原始图像 + I0 + neutral follow-up
→ 生成最终文本答案
~~~

统一 follow-up：

~~~text
Use the generated visual evidence to answer the original question.
~~~

### 2.3 为什么主协议不先生成 T0

先生成文本再画图会额外引入：

- 文本 CoT 能力；
- pre-draw token budget；
- EOS 截断策略；
- 模型可能已在画图前给出答案；
- 不同模型文本长度差异；
- 通用 think prompt 与任务绘图 prompt 的差异。

image-first 能把主实验收敛为更直接的因果干预：

~~~text
question → generated visual evidence → answer
~~~

如果以后需要比较 plan-then-image，可作为独立消融，不应混入主 C-F/C-R 结果。

## 3. C-R 与 C-F 的严格定义

### 3.1 External Draw（C-R）

~~~text
G:
  用原问题、原图和 draw instruction 生成 I0

reset:
  丢弃生成阶段的 KV/cache

U:
  fresh encode(
      原问题,
      原图,
      draw instruction / generation transcript,
      I0,
      follow-up
  )
  → final answer
~~~

External draw 是通用协议，只要求 backend 能 draw 和 understand。

### 3.2 Forced Interleave（C-F）

~~~text
prefill:
  原问题 + 原图 + draw instruction

force:
  不生成 T0，立即进入 image phase
  → I0

reconsume:
  把 I0 的理解表示写回当前 state/KV

continue:
  在同一逻辑状态中进入 answer phase
  → final answer
~~~

Forced interleave 只适用于真正具备以下能力的 backend：

- 可以在同一次增量状态中切换理解/生成模态；
- 可以生成视觉表示；
- 可以把生成视觉表示重新写回后续理解路径；
- 可以在回注后继续文本生成。

## 4. Prompt 设计

### 4.1 两种策略必须共享绘图指令

当前 external_draw 使用 configs/strategies/external_draw.yaml 中的 task-specific instruction，而 forced_interleave 只使用原问题和 backend 内部通用 think prompt。这会把 prompt 差异混入 C-F 与 C-R。

建议把配置重命名或抽象为：

~~~text
configs/strategies/g2u.yaml
~~~

推荐结构：

~~~yaml
protocol: image_first_single_image
max_generated_images: 1

generation_system_prompt: >
  Generate exactly one answer-agnostic visual scratchpad that helps solve
  the spatial question. Do not write the final answer, an option letter,
  or explanatory text into the image.

understand_followup: >
  Use the generated visual evidence to answer the original question.

draw_instruction:
  direction: "Draw one blue arrow that represents the queried direction..."
  nearest_point: "Draw blue measurement lines..."
  ...
~~~

原 external_draw.yaml 中 12 类 question_type 指令可以直接迁移。

### 4.2 构造统一 Generation prompt

建议 RunContext 增加：

~~~python
def visual_generation_instruction(sample):
    task_instruction = instruction_by_question_type(sample)
    return generation_system_prompt + "\n\n" + task_instruction
~~~

最终 G 输入：

~~~text
[original question]
[original images]
[visual_generation_instruction]
~~~

关键约束：

- 只画与问题有关的几何证据；
- 不写答案或选项字母；
- 尽量不添加自然语言文字；
- 使用统一颜色约定，例如蓝色表示模型新增标记；
- 不修改与任务无关的原图内容；
- 只生成一张图。

### 4.3 Answer prompt

C-R 的 fresh understand 输入建议保持：

~~~text
[original question]
[original images]
[visual generation instruction]
[generated image I0]
[Use the generated visual evidence to answer the original question.]
~~~

C-F 如果模型的原生 interleave loop 会在图像回注后直接继续 assistant generation，可以把“两阶段行为”提前写进 generation system prompt：

~~~text
First generate exactly one visual scratchpad.
After the visual scratchpad has been incorporated, answer the original question.
~~~

不要为了强行追加 follow-up 而破坏模型原生 chat/token 边界。每个 backend 可以采用：

- 回注后追加合法 user turn；或
- 在初始系统提示中声明两阶段协议。

二者必须在 metadata 中记录 post_image_prompt_mode。

## 5. 公共接口修改

### 5.1 Capabilities

文件：

- mapspatial/types.py
- mapspatial/strategies/base.py
- 各 backend 的 caps

当前 forced_interleave 只要求 draw=True，这是错误的。建议短期增加：

~~~python
class Capabilities(NamedTuple):
    batch: bool
    draw: bool
    native_interleave: bool
    forced_interleave: bool
    max_images: int
    video: bool
~~~

支持情况：

| Backend | draw | forced_interleave |
|---|---:|---:|
| Bagel | true | true |
| ThinkMorph | true | true |
| SenseNova-U1 | true | true |
| LatentUM | true | true |
| Janus | true | false |
| Show-o2 | true | false |
| BLIP3o | true | false |
| JoyAI | true | false |

ForcedInterleaveStrategy.required_caps() 改为：

~~~python
return {"forced_interleave": True}
~~~

available strategies 也应分别依据 draw 和 forced_interleave 输出。

### 5.2 Backend 方法签名

在 mapspatial/backends/base.py 增加显式接口：

~~~python
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
    raise NotImplementedError
~~~

约束：

- image_first=True 时禁止先生成自由文本；
- max_images 在主协议中必须为 1；
- instruction 必须与 external_draw 相同；
- 返回的 Prediction.text 必须是图像回注后的答案；
- trace 必须能证明 image 发生在 answer text 之前。

### 5.3 Strategy 修改

文件：mapspatial/strategies/forced_interleave.py

建议：

~~~python
instruction = ctx.visual_generation_instruction(sample)
pred = backend.forced_interleave(
    sample.message,
    instruction,
    max_images=1,
    image_first=True,
    followup=ctx.understand_followup,
    **ctx.gen_kw,
)
~~~

不要再把 ctx.max_rounds 直接传给 forced_interleave。native 的 max_rounds 与 forced 的 max_images 是两个不同参数。

文件：mapspatial/strategies/external_draw.py

建议保持：

~~~python
image = backend.draw(message, instruction, **draw_kw)
answer = backend.understand(augmented_message, **understand_kw)
~~~

但 instruction 必须来自同一个 G2U 配置，并修正以下问题：

1. 从 YAML 同时加载 generation_system_prompt、understand_followup 和 draw_instruction；
2. 当前 YAML 的 draw_followup_text 实际没有被 RunContext loader 读取，应修复；
3. draw 与 understand 参数应分开，避免 temperature 等同名参数在两阶段含义不同。

建议配置字段：

~~~yaml
draw_generate:
  seed: 42
  temperature: 0.0

answer_generate:
  temperature: 0.0
  max_new_tokens: 512
~~~

## 6. Bagel / ThinkMorph 修改建议

### 6.1 当前问题

当前 BagelBackend.draw() 调用 forced_interleave_inference()：

~~~text
gen_text(max 500)
→ image
→ final text
→ 只取 image 返回
~~~

因此 external_draw 的 Bagel G 阶段也不是 image-first。

当前 forced_interleave_inference()：

~~~text
T0 → I0 → I1 → I2 → T1
~~~

不符合主 G2U。

### 6.2 建议增加共享 image-first primitive

文件：mapspatial/vendor/bagel_interleave/inferencer.py

建议新增：

~~~python
def image_first_inference(
    self,
    input_lists,
    instruction,
    *,
    cfg_text_scale,
    cfg_img_scale,
    ...,
    keep_context=False,
):
    # 1. init contexts
    # 2. encode common generation prompt + source images + instruction
    # 3. DO NOT call gen_text()
    # 4. call gen_image() exactly once
    # 5. if keep_context:
    #       update_context_image(generated_image, gen_context, vae=True, vit=True)
    # 6. return image and optional state
~~~

更简单的实现方式是拆出内部 helper：

~~~python
_prepare_generation_context(input_lists, instruction, system_prompt)
_generate_one_image(prepared_context, generation_kw)
_reconsume_generated_image(image, gen_context)
_generate_answer(gen_context)
~~~

External 和 forced 共用前两个 helper：

- external：拿到 PIL image 后丢弃 state；
- forced：保留 state、回注 image、继续 answer。

### 6.3 Bagel forced image-first

建议流程：

~~~text
init gen_context / cfg contexts
→ 写入 G2U generation system prompt
→ 写入 original message
→ 写入 task-specific draw instruction
→ gen_image() exactly once
→ update_context_image(I0, vae=True, vit=True)
→ 合法地进入 answer phase
→ gen_text()
~~~

不调用 pre-image gen_text()。

注意事项：

- generated image 必须同时进入 VAE 与 ViT 路径，保持 BAGEL interleaved sequence 语义；
- final Prediction.text 只取图后文本；
- trace 应为 image round 0、text round 1；
- max_images 固定 1；
- ThinkMorph 继承同一 forced 实现；
- ThinkMorph 的 marker-driven 行为仍只属于 native_interleave，不应影响 forced 实验。

### 6.4 Bagel external image-first

BagelBackend.draw() 改为调用同一个 image_first primitive，但 keep_context=False。

不得再通过 forced_interleave_inference() 先生成 500 token 文本。

## 7. SenseNova-U1 修改建议

### 7.1 External draw

当前 U1Backend.draw() 已直接调用 it2i_generate()，总体适合 external image-first。

需要修改：

1. G2U 主协议显式传 think_mode=False；
2. full_prompt 使用统一的 original question + task instruction；
3. 不复用 backend 的 direct/think 配置来决定 draw 是否先输出规划文本；
4. 固定 seed、image size、CFG 和 num_steps；
5. understand 阶段重新编码原图与生成图。

建议：

~~~python
draw_think_mode = kw.get("draw_think_mode", False)
~~~

不要直接使用 self._think_mode。

### 7.2 Forced image-first

当前 interleave_gen() 只支持 force_image_at > 0，先生成文本 token 后才注入 img_start。

建议新增独立参数：

~~~python
force_image_first: bool = False
post_image_max_tokens: int | None = None
~~~

在 prefix forward 完成后：

~~~python
if force_image_first:
    next_token = img_start_token
    # 直接进入现有 image branch
~~~

图像生成完成后：

- 经理解 ViT 重新编码；
- 写入 img_end；
- 从图后 cache 继续生成答案；
- max_images=1 时禁止再次进入 image phase。

### 7.3 必须同时修复 position index

本地 port 将官方隐式 current_index 改为显式 indexes 时少了 +1。

统一约定：

~~~python
t_index = last_committed_temporal_position
next_index = t_index + 1
forward(indexes=[[next_index], [0], [0]])
t_index = next_index
~~~

一起审计：

- condition 文本 continuation；
- text-uncondition continuation；
- img_start；
- image temporal plane；
- img_end；
- 图后 continuation；
- _generate_think()；
- _append_text_tokens_to_cache()。

不要只修改 forced 分支，否则 U1 各生成路径的位置语义仍不一致。

## 8. LatentUM 修改建议

### 8.1 External draw

当前 LatentUMBackend.draw() 已直接调用 generate_latents_with_images() / generate_latents()，适合作为 image-first G。

保持：

~~~text
original question + original images + task instruction
→ latent generation
→ pixel decoder
→ PIL image
~~~

然后 external understand fresh encode 原问题、原图、PIL 中间图和 follow-up。

### 8.2 Forced image-first

当前 interleave() 在 AR text loop 中达到 force_image_at 后才进入 image phase。

建议增加：

~~~python
image_first: bool = False
~~~

prefix forward 后，在 round 1 直接执行：

~~~text
kv_before_img = deepcopy(past_key_values)
→ feed img_start with vision_token_mask=1
→ generate VQ codes
→ rewind kv_before_img
→ inject projected latent with vision_token_mask=0
→ feed img_end
→ continue final text
~~~

跳过 pre-image AR text loop。

### 8.3 Latent 与 pixel 路径必须显式标注

LatentUM C-F 直接把生成 VQ latent 回注理解路径；C-R 必须先：

~~~text
VQ latent → pixel decoder → PIL → vision encoder
~~~

因此它的 Delta_state 同时可能包含：

- state continuity；
- 避免 pixel codec；
- latent-space semantic preservation。

Prediction.meta 必须记录：

~~~python
{
    "reconsume_mode": "latent" | "pixel",
    "pixel_decoded": bool,
}
~~~

建议额外实现可选控制：

~~~text
latentum_stateful_pixel
~~~

即在保留同一逻辑会话的情况下，也把生成 latent decode 成 PIL 后重新走视觉编码。若实现代价太高，至少在论文局限中明确说明 Delta_state 不是纯 KV effect。

### 8.4 保留的 bug 修复

旧 force_image_at 路径仍可作为 plan-then-image 消融，但应：

- 用 committed_text_tokens 判断阈值，修复 96 实际变 95 的 off-by-one；
- meta.rounds 改为生成视觉步骤数，而不是文本循环数。

## 9. 其他 UMM 的 External Draw 适配

目标 backend：

- Janus
- Show-o2
- BLIP3o
- JoyAI
- 后续所有 draw=True 的统一模型

统一要求：

1. draw(context, instruction) 必须消费所有原始输入图像；
2. full prompt 必须是原问题加统一 task instruction；
3. G 阶段只返回一张图，不返回答案；
4. 不支持 I2I 的模型必须标记 generation_conditioning=text_only，不能假装使用了原图；
5. U 阶段必须消费原始图和生成图；
6. 生成图不可覆盖原始图路径；
7. 记录模型是否真正 reconsume 了生成图。

建议在 Prediction.meta 记录：

~~~python
{
    "generation_conditioning": "text_only" | "text+source_images",
    "reconsume_mode": "pixel",
    "source_image_count": N,
    "generated_image_count": 1,
}
~~~

如果某 backend 的 draw 只能 T2I，仍可参加 external_draw，但应单独分组报告，不能与真正的 image-conditioned editing 路径完全等价解释。

## 10. Artifact matching 与可归因性

### 10.1 最理想方案

C-R 与 C-F 使用同一个内部 generation primitive：

~~~text
same model
same generation prompt
same original images
same seed
same CFG
same image shape
same denoising steps
same generated image count
~~~

生成结果应尽可能逐像素一致。运行时记录：

~~~python
generation_prompt_hash
generated_image_sha256
seed
generation_params
~~~

### 10.2 如果两次生成不能保证相同

增加 artifact replay 控制：

~~~text
C-F:
  在 stateful 路径中生成 I0 并回答

C-R-replay:
  直接使用 C-F 保存的同一张 I0
  fresh encode 后回答
~~~

比较：

~~~text
C-F(I0) - C-R-replay(I0)
~~~

它比独立生成两张不同图后的 C-F - C-R 更能说明状态连续性的贡献。

## 11. Trace 与 metadata 统一

主协议 trace：

~~~python
[
    TraceStep(
        round=0,
        kind="image",
        image=generated_path,
        triggered_by="forced_image_first",
    ),
    TraceStep(
        round=1,
        kind="text",
        text=final_answer_text,
    ),
]
~~~

统一 metadata：

~~~python
{
    "strategy": "external_draw" | "forced_interleave",
    "protocol": "image_first_single_image",
    "stateful": bool,
    "draw_triggered": True,
    "visual_reinjected": True,
    "rounds": 1,
    "generated_image_count": 1,
    "pre_image_text_tokens": 0,
    "reconsume_mode": "pixel" | "latent",
    "generation_conditioning": "text_only" | "text+source_images",
    "post_image_prompt_mode": "initial_phase_instruction" | "appended_user_turn",
}
~~~

字段定义：

- rounds：实际生成并回注的视觉步骤数；
- pre_image_text_tokens：主协议必须为 0；
- draw_triggered：是否真正进入生成阶段，与是否保存 PNG 无关；
- visual_reinjected：生成视觉表示是否进入最终答案路径；
- artifacts_saved：可另外记录，不影响 draw_triggered；
- generated_images 与 image TraceStep.image 必须一一对应。

## 12. 配置建议

模型配置只保留 backend 固有参数：

~~~yaml
backend_args:
  cfg_text_scale: 4.0
  cfg_img_scale: 2.0
  num_timesteps: 50
  image_shapes: [1024, 1024]
~~~

策略协议参数放到 G2U 配置：

~~~yaml
protocol: image_first_single_image
max_generated_images: 1
image_first: true
seed: 42
save_generated: true
~~~

不要再让：

~~~text
backend_args.max_rounds
~~~

同时控制 native_interleave、forced_interleave 和 external_draw。三者含义不同：

- native_max_rounds：模型自主交错上限；
- forced_max_images：框架强制视觉步骤数，主协议为 1；
- external_max_images：restart G2U 图像数，主协议为 1。

## 13. 建议实现顺序

### P0：先跑通主实验

1. 抽出共享 G2U prompt 与 task instruction。
2. ExternalDrawStrategy 和 ForcedInterleaveStrategy 使用同一 instruction。
3. forced_interleave 固定 image_first=True、max_images=1。
4. Bagel/ThinkMorph 实现无 pre-image gen_text 的 image-first。
5. U1 实现 prefix 后立即注入 img_start。
6. LatentUM 实现 prefix 后立即进入 VQ image phase。
7. 增加 forced_interleave capability。

### P1：保证结果可解释

8. 修复 U1 position index。
9. 修复 LatentUM rounds 与旧 force_image_at off-by-one。
10. 统一 trace / metadata。
11. 确认 external draw 的 U 阶段消费所有原图和生成图。
12. 固定并记录 seed / CFG / resolution / steps。

### P2：增强论文消融

13. 增加 C-R-replay。
14. 增加 LatentUM pixel-vs-latent reconsume 控制。
15. 增加 image-first 与 plan-then-image 的次要消融。
16. 增加 blank/random visual placebo 小规模控制。

## 14. 服务器验收清单

每个 backend 先跑 5–10 个样本，逐条检查：

### 协议

- pre_image_text_tokens == 0；
- generated_image_count == 1；
- trace 第一项是 image，之后才是 answer text；
- 最终答案来自图像回注后的路径；
- C-R 确实 fresh encode；
- C-F 确实复用同一 state/KV。

### Prompt

- C-R 与 C-F 的 draw instruction 完全一致；
- 图片中没有答案字母或最终答案文本；
- direction / route / count 等任务使用正确 question_type 指令；
- follow-up 不引入新的空间信息。

### 图像

- 所有原始输入图都被 G 阶段消费；
- 所有生成图都被 U 阶段消费；
- 生成图片可正常打开且尺寸正确；
- C-R/C-F seed 和 generation 参数一致；
- 保存 generated image hash。

### 输出

- Prediction.text 非空；
- answer extractor 能正常提取；
- rounds == 1；
- draw_triggered == true；
- visual_reinjected == true；
- generated_images 与 trace image path 一致；
- --no-save-generated 时 draw_triggered 仍为 true。

## 15. 最终实验矩阵

主表建议：

| 条件 | 训练 | 图像触发 | 状态 | 图像数 |
|---|---|---|---|---:|
| Direct U | 无额外训练 | 无 | fresh | 0 |
| External C-R | training-free | 强制 image-first | restart | 1 |
| Forced C-F | training-free | 强制 image-first | shared state | 1 |
| Native C-A | checkpoint-dependent | 模型自主 | shared state | 0–N |

说明：

- Zebra-CoT / ThinkMorph 的专项训练能力不能与 training-free C-F 混为一谈；
- ThinkMorph forced 仍是框架强制条件，native 才测自主触发；
- 其他只支持 draw+understand 的 UMM 参加 U 与 C-R，不参加 C-F；
- LatentUM 的 C-F 使用 latent reconsume，需单独标注。

## 16. 一句话方案

主协议统一为：

~~~text
同一个问题、原图和 task-specific instruction
→ 立即生成一张 answer-agnostic visual evidence
→ C-R 丢弃状态后重新理解
→ C-F 在同一状态中回注后理解
~~~

先把 prompt、artifact 数量和 generation 参数对齐，再用 C-F 与 C-R 的差异讨论 stateful G2U。plan-then-image、多轮 visual CoT 和 autonomous marker 都属于后续独立问题，不进入本轮 training-free 主设计。
