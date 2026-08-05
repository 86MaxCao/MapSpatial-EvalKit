# 01 · 核心架构

> 本文定义 MapSpatial-EvalKit 的地基：数据契约、Backend × Strategy 正交模型、目录结构。
> 实现前必读。

---

## 1. 全局数据流

```
data-jsonl/{view}/{task}/{variant}.jsonl
        │
        ▼
   TaskSample            数据层产物（含 gold / meta，backend 看不到 gold）
        │
        ▼
   Message[]             交错的 text/image 列表（借鉴 VLMEvalKit 格式）
        │
        ▼
   Strategy              direct / native_interleave / external_draw
        │  ├─ 调 backend.understand()
        │  └─ 调 backend.draw()          （仅 caps.draw）
        ▼
   Prediction            结构化：text + generated_images + trace + meta
        │
        ▼
   answer extraction  →  metrics  →  results/{...}.jsonl + summary.json
```

两条硬性边界：

| 边界 | 规则 |
|---|---|
| **Backend 不碰路径解析** | `Message` 里的 image 值必须是已解析的绝对路径或 PIL 对象。`data_root` 拼接由数据层完成 |
| **Backend 不碰 gold** | `gold` 只存在于 `TaskSample.meta`，不进 `Message`。防止实现时意外泄漏答案 |

---

## 2. 数据契约

### 2.1 Message —— 交错的多模态输入

采用 VLMEvalKit 的交错格式（`vlmeval/vlm/base.py:64-99`），但**加类型约束**。

```python
from typing import Literal, TypedDict, Union
from pathlib import Path
from PIL import Image

class TextItem(TypedDict):
    type: Literal["text"]
    value: str

class ImageItem(TypedDict):
    type: Literal["image"]
    value: Union[Path, Image.Image]   # 绝对路径或已加载的 PIL

class VideoItem(TypedDict):
    type: Literal["video"]
    value: Path

MessageItem = Union[TextItem, ImageItem, VideoItem]
Message = list[MessageItem]
```

**为什么用交错列表而不是「图片一坨 + prompt 一坨」**：

T4 `route_validity` 每题带 4 张候选路线图。交错格式能表达：

```python
[
  {"type": "text",  "value": "Which route is valid from green to purple?\n\nOption A:"},
  {"type": "image", "value": Path(".../option_A_direct.png")},
  {"type": "text",  "value": "Option B:"},
  {"type": "image", "value": Path(".../option_B_direct.png")},
  ...
  {"type": "text",  "value": "Answer with only the option letter."},
]
```

而「4 张图 + 一段文字」的结构丢掉了图与选项标签的对应关系，模型只能靠图片顺序猜。

**为什么加 TypedDict**：VLMEvalKit 全靠运行时 `assert`（`base.py:90,93,95,111-115`）。纯 duck-typed dict 的调试成本我们不必付。

### 2.2 Prediction —— 结构化返回值

这是与 VLMEvalKit 最重要的分歧点。理由见 [00-overview.md 决策 2](./00-overview.md)。

```python
@dataclass
class TraceStep:
    round: int
    kind: Literal["text", "image"]        # 这一步产出文本还是图像
    text: str | None = None
    image: Path | None = None
    triggered_by: str | None = None       # "model_marker" | "forced" | None
    elapsed_s: float = 0.0

@dataclass
class Prediction:
    text: str                             # 最终文本输出（用于答案抽取）
    generated_images: list[Path] = field(default_factory=list)
    trace: list[TraceStep] = field(default_factory=list)
    error: str | None = None
    meta: dict = field(default_factory=dict)
    #   strategy: str        实际使用的策略
    #   rounds: int          实际轮数
    #   draw_triggered: bool 是否真的生成了图
    #   backend: str
```

**`draw_triggered` 为什么必须单独记**：模型自触发模式下，`"<image_start>" in gen_text` 是子串匹配（`inferencer.py:325`）。若模型换个措辞，生成被静默跳过，此时结果与 `direct` 无异。不记录这个字段，就无法区分「模型判断不需要画」和「标记没匹配上」——而这两者对实验结论的意义完全不同。

**`generated_images` 的命名规则**（修正 ThinkMorph 的缺陷）：

```
{output_dir}/generated/{view}/{task}/{variant}/{sample_id}_r{round}.png
```

必须含 `sample_id`。ThinkMorph 用 `uuid8 + idx`（`ThinkMorph.py:429`），部分重跑后无法把图对回样本。

### 2.3 TaskSample —— 数据层产物

```python
@dataclass
class TaskSample:
    id: str                    # 全局唯一，来自 JSONL 的 id 字段
    message: Message           # 已构造好的交错输入
    gold: str                  # A-D。仅评测使用，不传给 backend
    meta: dict                 # view/variant/task_id/question_type/images(相对路径)/…
```

---

## 3. Backend：能力提供方

### 3.1 能力声明

```python
class Capabilities(NamedTuple):
    batch: bool                  # 能否真批推理（一次提交多条）
    draw: bool                   # 能否生成图像
    native_interleave: bool      # 是否有原生交错推理循环（单一 KV-cache 跨轮）
    max_images: int              # 单次输入最大图片数
    video: bool
```

`native_interleave` 与 `draw` 必须分开。理由：

- Bagel/ThinkMorph 两者皆有 → 可用 `native_interleave` 策略（保持 context）
- 某些模型可能只有独立的 t2i/it2i 接口而无交错循环 → 只能用 `external_draw`

这个区分决定了策略可用性，不能合并成一个 `draw` 标志。

### 3.2 接口

```python
class Backend(ABC):
    caps: ClassVar[Capabilities]
    COMPAT: ClassVar[tuple[str, ...]] = ()     # 需要的兼容补丁，见 07 文档

    @abstractmethod
    def __init__(self, cfg: BackendConfig): ...

    @property
    @abstractmethod
    def model_name(self) -> str: ...

    # ── 理解：唯一必须实现的方法 ──
    @abstractmethod
    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        """始终接受 list 并返回等长 list。

        caps.batch=False 的实现内部串行循环即可；
        caps.batch=True 的实现必须一次性提交（如 vLLM 的 llm.generate(所有条)）。
        """

    # ── 生成：caps.draw=True 才实现 ──
    def draw(self, context: Message, instruction: str, **kw) -> Image.Image:
        raise NotImplementedError

    # ── 原生交错：caps.native_interleave=True 才实现 ──
    def interleave(self, message: Message, *, max_rounds: int, **kw) -> Prediction:
        raise NotImplementedError
```

**为什么 `understand` 统一收发 list（而非 VLMEvalKit 的单条 `generate_inner`）**：

VLMEvalKit 的批量支持是事后 bolt-on —— `generate_inner_batch` / `supports_batch` 在整个仓库 0 匹配，vLLM 每次只提交 1 条（`qwen3_vl/model.py:403`）还在循环里 `torch.cuda.empty_cache()`（`inference.py:190`）冲掉 KV cache。批量能力必须在基类契约里，不能后补。

单条只是 `len==1` 的特例，不需要单独 API。

### 3.3 注册：装饰器 + 惰性导入

```python
# mapspatial/backends/registry.py
_REGISTRY: dict[str, Callable[[], type[Backend]]] = {}

def register(name: str):
    """注册一个惰性加载器。装饰的是返回类的函数，不是类本身。"""
    def deco(loader):
        _REGISTRY[name] = loader
        return loader
    return deco

def get_backend_cls(name: str) -> type[Backend]:
    if name not in _REGISTRY:
        raise KeyError(f"unknown backend {name!r}; available: {sorted(_REGISTRY)}")
    return _REGISTRY[name]()      # 此刻才真正 import 重依赖
```

```python
# mapspatial/backends/__init__.py —— 只注册加载器，不 import 实现
@register("vllm")
def _vllm():
    from .vllm import VllmBackend      # vllm 在这一刻才被 import
    return VllmBackend

@register("veomni_bagel")
def _bagel():
    from .veomni.bagel import BagelBackend
    return BagelBackend
```

对比 VLMEvalKit：`vlmeval/vlm/__init__.py` 无条件导入 80+ 模型文件，`config.py` 组装 ~551 个 `partial`。跑一个 Qwen3-VL 要付全部模型的导入成本。惰性加载器是解法。

（gate2building 的 `try/except` + `*_AVAILABLE` 标志方向对，但仍在模块加载期执行；装饰器方案更彻底。）

---

## 4. Strategy：能力编排方

### 4.1 接口

```python
class Strategy(ABC):
    name: ClassVar[str]

    @abstractmethod
    def required_caps(self) -> dict[str, Any]:
        """声明对 backend 能力的要求，供启动时校验。"""

    @abstractmethod
    def run(self, backend: Backend, samples: list[TaskSample],
            ctx: RunContext) -> list[Prediction]: ...
```

### 4.2 三种策略

| Strategy | 要求能力 | 行为 |
|---|---|---|
| `direct` | 无 | 直接 `backend.understand(messages)`。全部 20 个模型可用 |
| `native_interleave` | `native_interleave=True` | 委托 `backend.interleave()`，模型自主决定是否生成中间图 |
| `external_draw` | `draw=True` | 外部编排：`draw()` 产出中间图 → 追加到 message → `understand()` |

详细语义与参数见 [04-strategies.md](./04-strategies.md)。

### 4.3 启动时能力校验（fail-fast）

```python
def validate(strategy: Strategy, backend: Backend) -> None:
    caps = backend.caps
    for cap, expected in strategy.required_caps().items():
        actual = getattr(caps, cap)
        if actual != expected:
            raise ConfigError(
                f"strategy {strategy.name!r} 要求 {cap}={expected}，"
                f"但 backend {backend.model_name!r} 是 {actual}。"
                f"该 backend 可用策略：{available_strategies(caps)}"
            )
```

必须在**加载模型之前**校验。等 7B 权重加载完 3 分钟才报「不支持该策略」是不可接受的。

---

## 5. 为什么这两个维度必须正交

反例：把生成建模成一种 backend 类型。

```
UnderstandingBackend  →  返回 str
GenerationBackend     →  返回 str + images
```

后果：runner 要分叉，结果 schema 要分叉，`summary.json` 要分叉。最终 `Qwen3-VL` 的准确率和 `Bagel` 的准确率**存在不同的表里，口径不同，无法比较**。而项目的核心目标恰恰是比较它们。

正交之后：

```
Qwen3-VL  × direct              →  Prediction
Bagel     × direct              →  Prediction   ← 同一 schema
Bagel     × native_interleave   →  Prediction   ← 同一 schema
Bagel     × external_draw       →  Prediction   ← 同一 schema
```

同一份评测代码、同一张结果表、同一套指标。`meta.strategy` 区分条件，这正是消融实验需要的形状。

---

## 6. 目录结构

```
MapSpatial-EvalKit/
├── docs/                        # 本文档集
├── configs/
│   ├── models/*.yaml            # 每模型一份：backend / path / load 参数 / 默认策略
│   └── strategies/*.yaml
│
├── mapspatial/                  # Python 包名（仓库名带连字符，包名不能带）
│   ├── types.py                 # Message / Prediction / TaskSample / Capabilities
│   ├── config.py                # 嵌套配置（per-backend 配置不污染顶层）
│   │
│   ├── compat/                  # ★ 兼容层，见 07 文档
│   │   ├── registry.py          #   @patch 装饰器；幂等 + 自失效
│   │   └── patches/*.py
│   │
│   ├── media.py                 # ★ 唯一的 URL 下载 / 视频抽帧 / 图像加载 / 临时文件
│   ├── messages.py              # ★ 唯一的占位符规范化 + chat message 构造
│   │
│   ├── data/
│   │   ├── schema.py            # JSONL 记录 → TaskSample
│   │   ├── loader.py            # view×task×variant 发现与遍历
│   │   ├── prompt.py            # TaskSample → Message（含 T4 多图交错）
│   │   └── preflight.py         # 图像存在性 + 可读性校验
│   │
│   ├── backends/
│   │   ├── base.py registry.py
│   │   ├── api.py vllm.py transformers.py
│   │   ├── cambrian.py vilasr.py spatial_mllm.py sensenova_si.py
│   │   └── veomni/              # 6 个统一模型
│   │       ├── _loader.py       #   共享加载链
│   │       └── bagel.py thinkmorph.py blip3o.py u1.py latentum.py janus.py
│   │
│   ├── vendor/                  # vendor 的第三方 modeling 代码
│   │   └── <name>/{ORIGIN.md, PATCHES.md, ...}
│   │
│   ├── strategies/
│   │   ├── base.py direct.py native_interleave.py external_draw.py
│   │
│   ├── eval/
│   │   ├── answer.py            # 重写答案抽取（修 allow_multi、放开 A-D 限制）
│   │   └── metrics.py           # 分 view/task/variant/strategy 聚合
│   │
│   ├── runner.py                # 续跑、批处理、条带切分、原子写
│   └── cli.py                   # run / doctor / compat / preflight
│
└── tests/
```

带 ★ 的三个模块是**去重的关键**。gate2building 里这些逻辑在 8 个 backend 各写一遍，行为不一致（见 [00-overview.md §4.2](./00-overview.md)）。收敛到单一实现后，那批不一致 bug 自然消失。

---

## 7. 配置形态

修正 gate2building 的 per-backend 配置污染顶层问题（`bagel_mode`、`vilasr_max_steps`、`spatial_mllm_model_type` 全挤在 `RunConfig` 里）。

```yaml
# configs/models/bagel-7b.yaml
name: Bagel-7B-MoT
backend: veomni_bagel
model_path: ${CKPT_DIR}/BAGEL-7B-MoT

load:
  dtype: bfloat16
  device: cuda

generate:
  temperature: 0.0
  max_new_tokens: 2048

# backend 私有配置，收在自己的命名空间下
backend_args:
  cfg_text_scale: 4.0
  cfg_img_scale: 2.0
  num_timesteps: 50

strategies: [direct, native_interleave]   # 该模型要跑的策略
```

```yaml
# configs/models/qwen3-vl-8b.yaml
name: Qwen3-VL-8B-Instruct
backend: vllm
model_path: ${CKPT_DIR}/Qwen3-VL-8B-Instruct

load:
  max_model_len: 32768
  gpu_memory_utilization: 0.7
  limit_mm_per_prompt: {image: 24}

batch_size: 32          # 真批量
strategies: [direct]
```

无 `env:` 字段——单一环境是硬约束（[07-environment.md](./07-environment.md)）。

---

## 8. 相关文档

| 主题 | 文档 |
|---|---|
| 数据 schema 与 prompt 构造细节 | [02-data-pipeline.md](./02-data-pipeline.md) |
| 20 个模型的 backend 实现与能力矩阵 | [03-backends.md](./03-backends.md) |
| 三种策略的详细语义 | [04-strategies.md](./04-strategies.md) |
| 6 个统一模型的接入 | [05-veomni-integration.md](./05-veomni-integration.md) |
| runner / 续跑 / 指标 | [06-runner-eval.md](./06-runner-eval.md) |
| 单一环境与兼容层 | [07-environment.md](./07-environment.md) |
