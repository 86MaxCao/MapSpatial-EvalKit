# 06 · Runner 与评测

> 执行调度、断点续跑、多卡并行、答案抽取与指标聚合。

---

## 1. 执行结构

```
CLI (mapspatial run)
  │
  ├─ 加载 config（model + strategies）
  ├─ 校验策略与 backend 能力（fail-fast，在加载权重之前）
  ├─ preflight（可跳过，结果带缓存）
  │
  └─ for strategy in config.strategies:
        for (view, task, variant) in 组合:
             ├─ 读输入 JSONL → TaskSample[]
             ├─ 排除已完成（按 id）
             ├─ 条带切分（多卡时按 rank）
             ├─ 分批 → strategy.run(backend, batch, ctx)
             ├─ 答案抽取 + 判定
             └─ 原子追加写结果
        写 summary.json
```

---

## 2. 断点续跑

### 2.1 现状的缺陷

gate2building 的做法（`run_vlm_jsonl_inference_v5.py:78-94, 175-186`）：

```python
def _completed_ids(output_path):     # 读已有输出，收集 obj["id"]
    ...                              # JSONDecodeError 被静默吞掉（:89）

# 输出以 "a" 追加模式打开（:206），每条 flush
```

三个问题：

| 问题 | 后果 |
|---|---|
| **写入端无去重** | 输入顺序一变（或同一 id 被处理两次）就产生重复行 |
| 损坏行被静默忽略 | 上次崩在写一半，该行永远不会被重跑，也没人知道 |
| 追加模式 + 崩溃 | 半行残留在文件里 |

VLMEvalKit 用 pickle（`inference.py:167-189`，每 10 条 dump），避免了半行问题，但引入 pickle 的 schema 版本风险：模型类改了返回类型，旧 pickle 静默反序列化成错误结果。

### 2.2 MapSpatial-EvalKit 的做法

**JSONL + 原子追加 + 显式校验**：

```python
def load_completed(path: Path) -> tuple[set[str], int]:
    """返回 (已完成 id 集合, 损坏行数)。损坏行必须上报，不静默吞。"""
    done, corrupt = set(), 0
    if not path.exists():
        return done, 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            done.add(json.loads(line)["id"])
        except (json.JSONDecodeError, KeyError):
            corrupt += 1
    return done, corrupt
```

| 规则 | 实现 |
|---|---|
| 单条写入原子化 | 一行一次 `write` + `flush`；行内不换行（`json.dumps` 无 indent） |
| 写入前去重 | 内存里维护 `done` 集合，写之前查一次 |
| 损坏行显式处理 | 启动时报告数量；`--repair` 选项重写文件剔除损坏行 |
| 不依赖输入顺序 | 去重靠 id，与顺序无关 |

**为什么不用 pickle**：JSONL 可直接 `grep` / `jq` / 人眼看，出问题时排查成本低一个量级。schema 演进用显式版本字段处理。

### 2.3 结果记录 schema

```json
{
  "schema_version": 1,
  "id": "B000A07C0B_..._T1_q0_推荐方案_2c7e8053c5_sat_direct",
  "model": "Bagel-7B-MoT",
  "backend": "veomni_bagel",
  "strategy": "native_interleave",

  "view": "sat", "variant": "direct", "oracle": false,
  "task_id": "T1", "question_type": "direction",
  "images": ["benchmark_images_t1/.../sat_direct.png"],

  "gold": "D",
  "prediction": "<think>...</think><answer>B</answer>",
  "extracted_answer": "B",
  "exact_match": false,

  "generated_images": ["generated/sat/t1/direct/B000A07C0B_..._r0.png"],
  "rounds": 1,
  "draw_triggered": true,
  "trace": [
    {"round": 0, "kind": "text",  "text": "...", "elapsed_s": 2.1},
    {"round": 0, "kind": "image", "image": "generated/.../_r0.png",
     "triggered_by": "model_marker", "elapsed_s": 8.7}
  ],

  "error": null
}
```

与 gate2building 的差异：

| 字段 | 说明 |
|---|---|
| `schema_version` | 新增。schema 演进时能识别旧数据 |
| `strategy` / `backend` | 新增。**没有这两个字段，三向消融的结果无法区分** |
| `generated_images` / `rounds` / `draw_triggered` / `trace` | 新增。核心科学目标所需 |
| `input_jsonl` | 移除。gate2building 存的是绝对路径（`Path.as_posix()`），换挂载点就变，无意义。改存相对的 `view/task/variant` 三元组 |
| `question` | 可选（`--store-question`）。全量存会让结果文件大好几倍，而它可从输入 JSONL 按 id 还原 |

---

## 3. 并行

### 3.1 单模型吃满多卡

gate2building 的策略是「模型轮询分配到 GPU」（`run_inference_v5.sh` 的 `run_model_on_gpu`），14 个模型分 4 卡分轮串行。**单个模型只用 1 张卡。**

VLMEvalKit 的条带切分更好（`inference.py:102`）：

```python
sheet_indices = list(range(rank, len(dataset), world_size))
```

torchrun 起 N 个进程，每个进程加载完整模型到自己的卡，按 `rank` 取条带样本，各写自己的分片文件，rank 0 最后合并。

采用条带切分。理由：单模型跑 17550 条样本（sat 视图全任务），8 卡并行比 1 卡快 8 倍；而模型级并行在只跑 1 个模型时完全无法利用多卡。

### 3.2 unset `WORLD_SIZE`

VLMEvalKit 在构造模型前 unset `WORLD_SIZE`（`inference.py:134`, `run.py:54`），阻止 HuggingFace 自动张量并行。

必须照做。否则 `device_map="auto"` 遇到 `WORLD_SIZE>1` 会尝试跨进程切分模型，与「每进程一个完整模型」的策略冲突，症状是诡异的显存/通信错误。

### 3.3 分片文件与合并

```
results/{model}/{strategy}/{view}/{task}/
├── {variant}.rank0-of-8.jsonl
├── {variant}.rank1-of-8.jsonl
├── ...
└── {variant}.jsonl                 # rank 0 合并产出
```

合并规则：
- 按 id 去重（防止条带边界重叠）
- 合并后**保留**分片文件（便于排查某个 rank 的异常），`--clean-shards` 可清理
- 合并前校验：分片 id 并集应等于输入 id 集减去 error 集

### 3.4 API backend 的并发

gate2building 用 `ThreadPoolExecutor(max_workers=4)`，每 future 处理一个 (view, variant) 组合（`run_vlm_jsonl_inference_v5.py:425-447`）。粒度太粗：4 个组合并行，组合内串行，长尾严重（t3 有 6665 条，t1 只有 3029 条）。

改为样本级 worker pool：

```python
with ThreadPoolExecutor(max_workers=cfg.workers) as pool:
    for pred in pool.map(lambda s: strategy.run(backend, [s], ctx)[0], samples):
        writer.write(pred)
```

backend 内部对 key 轮转加锁（gate2building 的 `self._idx` 轮转在多线程下有竞态）。

### 3.5 vLLM 的批量与并行的关系

vLLM backend `caps.batch=True`，一次提交整批（默认 32）。这与条带切分正交：

```
rank 0: 样本 [0, 8, 16, ...] → 分成 32 一批提交
rank 1: 样本 [1, 9, 17, ...] → 分成 32 一批提交
```

每个 rank 独立的 vLLM 引擎。**不要在批处理循环里 `torch.cuda.empty_cache()`** —— 这是 VLMEvalKit 的错误（`inference.py:190`），会冲掉 KV cache 让 continuous batching 失效。

---

## 4. 答案抽取

### 4.1 现状必须重写

gate2building 的 `answer_extraction.py`（64 行）有两个真实缺陷：

**缺陷 1：`allow_multi` 参数函数体完全没用**（`:11-55`）

```python
def extract_answer(response, allow_multi=True) -> str:
    ...   # 函数体从头到尾没有引用 allow_multi
    return <单个字母>
```

配合 `is_correct`（`:58-64`）看，多选流程实际是坏的：

```python
def is_correct(predicted, ground_truth):
    a = ",".join(sorted(p.strip() for p in predicted.split(",") if p.strip())).upper()
    b = ",".join(sorted(...for ground_truth...)).upper()
    return a == b
```

`is_correct` 支持逗号分隔的多选比对，但 `extract_answer` 永远只返回单个字母。所以 `is_correct("B", "B,C")` 恒为 `False`。

**缺陷 2：硬编码只认 A–D**

注释说「所有任务 ≤4 选项」，显式排除 E–K 以避免匹配英文单词（"is"、"it"、"key"）。当前数据确实全是 4 选一，所以不算错。但这个假设应该**显式声明并校验**，而不是埋在正则里——将来加了 5 选项任务会静默出错。

### 4.2 重写要点

```python
@dataclass
class ExtractResult:
    answer: str                    # 归一化后的答案（多选时逗号分隔且已排序）
    method: str                    # 命中哪条规则，用于统计抽取质量
    confident: bool                # 是否走了明确模式（而非"取最后一个字母"兜底）
```

| 要点 | 说明 |
|---|---|
| **选项集合从数据来** | 由 `multiple_choice.choices` 的 key 决定合法字母集，不硬编码 A–D |
| **要么实现 `allow_multi`，要么删掉** | 当前的「声明了不实现」是最坏状态 |
| **记录命中的规则** | 统计各规则占比。若「取最后一个字母」兜底占比过高，说明 prompt 或抽取有问题 |
| **`confident=False` 单独统计** | 兜底命中的样本准确率若显著异常，需要人工检查 |
| **保留优先级顺序** | gate2building 的规则顺序（显式 answer 模式 → 中文模式 → 句尾 "is X" → 短回答单字母 → 最后一个字母）是合理的，继承 |

### 4.3 思维链输出的处理

统一模型在 `native_interleave` 下输出形如：

```
Round_0:
<think>The green dot is at the lower-left...</think>
[生成图]
Round_1:
<think>Based on the arrow...</think><answer>D</answer>
```

抽取必须：
1. 优先从 `<answer>...</answer>` 取
2. 其次按常规规则从最后一轮文本取
3. **不要**从 `<think>` 内容里取（思维链里常出现「可能是 A 或 B」这类干扰）

VLMEvalKit 有个 `SPLIT_THINK` 机制（`inference.py:300-326`）做类似的事，可参考其正则。

---

## 5. 指标聚合

### 5.1 现状的问题

gate2building 的 `summary.json`（`:449-451`）是 (view, variant) × files 的嵌套数组：

```json
[{"view":"sat","variant":"direct","files":[{"input":...,"output":...,"skipped":0,"written":3029,"exact_match":1264,"errors":0}, ...]}, ...]
```

问题：

| 问题 | 后果 |
|---|---|
| `written` 只是**本次运行**写入量，`skipped` 不聚合 | 续跑后 `written` 变小，看起来像样本变少了 |
| 没有 accuracy 字段，要自己算 `exact_match/written` | 而 `written` 在续跑后是错的分母 |
| 无 strategy 维度 | 三向消融的结果无处安放 |
| 嵌套数组不便查询 | 要写代码遍历才能取某一格 |

### 5.2 重新设计

分两层：**逐格明细**与**聚合视图**。

```json
{
  "schema_version": 1,
  "model": "Bagel-7B-MoT",
  "backend": "veomni_bagel",
  "env": {
    "python": "...", "torch": "...", "transformers": "...", "vllm": "...",
    "compat_applied": ["tied_weights_keys"],
    "compat_skipped": ["flash_attn_fallback"]
  },
  "cells": [
    {
      "strategy": "native_interleave",
      "view": "sat", "task": "t1", "variant": "direct",
      "total": 3029,              // 输入样本数（不随续跑变化）
      "answered": 3010,           // 有有效预测
      "errors": 19,
      "correct": 1264,
      "accuracy": 0.4201,         // correct / answered
      "coverage": 0.9937,         // answered / total
      "draw_triggered": 2874,     // 实际生成了中间图的条数
      "avg_rounds": 1.02,
      "unconfident_extract": 87   // 抽取走了兜底规则
    }
  ],
  "by_strategy": { "direct": {...}, "native_interleave": {...} },
  "by_task":     { "t1": {...}, ... },
  "by_view":     { "sat": {...}, ... }
}
```

关键设计：

| 字段 | 为什么必要 |
|---|---|
| `total` 来自输入而非本次写入 | 续跑后分母稳定 |
| `accuracy` 与 `coverage` 分开 | 区分「答错」和「没答上」。gate2building 混在一起会高估失败模型 |
| `draw_triggered` 计数 | 消融实验的核心观测量。若某模型 `native_interleave` 下触发率只有 30%，其平均准确率的解释完全不同 |
| `unconfident_extract` | 抽取质量的健康指标 |
| `env` 快照 + `compat_applied` | 换机器复现时能确认环境一致（见 [07-environment.md §3.5](./07-environment.md)） |

### 5.3 跨模型对比表

单独命令产出，不混在 `summary.json` 里：

```bash
mapspatial report --models "*" --out results/comparison.csv
```

```csv
model,strategy,t1,t2,t3,t4,overall,draw_rate
Qwen3-VL-8B-Instruct,direct,0.4180,0.4074,0.2564,0.4065,0.3607,—
Bagel-7B-MoT,direct,...,...,...,...,...,—
Bagel-7B-MoT,native_interleave,...,...,...,...,...,0.949
Bagel-7B-MoT,external_draw,...,...,...,...,...,1.000
```

这张表是最终要看的东西。`draw_rate` 一列让「生成是否被真正使用」一目了然。

---

## 6. CLI

```bash
# 单模型单策略
mapspatial run --model configs/models/bagel-7b.yaml --strategy native_interleave

# 模型 config 里声明的全部策略
mapspatial run --model configs/models/bagel-7b.yaml --all-strategies

# 多卡（条带切分）
torchrun --nproc_per_node 8 -m mapspatial.cli run --model ... --strategy direct

# 环境自检：逐 backend 检查 import / load / infer(1)
mapspatial doctor

# 查看兼容补丁状态
mapspatial compat --describe

# 数据校验
mapspatial preflight --input-dir ... --data-root ...

# 跨模型汇总
mapspatial report --models "*" --out comparison.csv
```

`doctor` 是发布门槛（20/20 全绿），见 [07-environment.md §5](./07-environment.md)。

---

## 7. 错误处理原则

| 场景 | 处理 |
|---|---|
| 单样本推理失败 | 记 `error` 字段写入结果，继续下一条。**不重试**（重试逻辑放 backend 内部，如 API 限流退避） |
| 图片缺失 | preflight 阶段就该发现。运行时遇到则记 `error: "missing images"` |
| 批量中单条 prep 失败 | 用 index_map 映射，失败位填 error，**不阻断整批**（gate2building 的 vLLM 已这样做） |
| 模型加载失败 | 直接终止。不允许「加载失败但继续跑其他组合」——那会产出误导性的部分结果 |
| 策略与能力不匹配 | 启动时 fail-fast，加载权重之前 |
| 损坏的续跑文件行 | 启动时报数量，不静默吞（修正 gate2building `:89` 的 `except JSONDecodeError: pass`） |

---

## 8. 相关文档

| 主题 | 文档 |
|---|---|
| `Prediction` / `TraceStep` 定义 | [01-architecture.md](./01-architecture.md) |
| preflight 细节 | [02-data-pipeline.md](./02-data-pipeline.md) |
| vLLM 真批量要点 | [03-backends.md](./03-backends.md) |
| `draw_triggered` 的语义 | [04-strategies.md](./04-strategies.md) |
| `doctor` 与环境快照 | [07-environment.md](./07-environment.md) |
