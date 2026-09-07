# 02 · 数据管线

> 从 `data-jsonl` 到 `Message[]` 的完整路径，以及三个共享基础模块（media / messages / prompt）的职责边界。

---

## 1. 数据布局

### 1.1 标签

```
data-jsonl/
├── manifest.json
├── sat/{t1,t2,t3,t4}/{direct,oracle,wrong_oracle,shuffled_oracle,masked_prompt}.jsonl
├── webrd04/{t1,t2,t3,t4}/{direct,oracle,wrong_oracle,shuffled_oracle,masked_prompt}.jsonl
└── blank/{t1,t2,t3,t4}/{direct,oracle,wrong_oracle,shuffled_oracle,masked_prompt}.jsonl
```

3 视图 × 4 任务 × 5 证据条件 = **60 个 JSONL**（T4 不适用的 blank 文件可以为空）。

### 1.2 图像

```
data/benchmark_images_t{1,2,3,4}/<case_id>/<scheme>/*.png
```

- `case_id` 形如 `B000A07C0B_from_B000A8XLYF_to_B0FFFCQM37`
- `scheme` 是中文目录名（`推荐方案`、`方案三`…）—— **路径处理必须支持非 ASCII**
- JSONL 里 `images` 字段是**相对 `data_root` 的路径**，形如 `benchmark_images_t1/<case_id>/推荐方案/sat_direct.png`

### 1.3 样本数

| 任务 | question_type | 每文件样本数 | 视图覆盖 |
|---|---|---|---|
| t1 | `direction`、`directional_nearest_point`、`dual_anchor_direction`、`egocentric_side`、`angular_order` | 以 manifest 为准 | 全部可用视图 |
| t2 | `nearest_point`、`directional_nearest_point`、`composite_euclidean_distance`、`composite_network_distance` | 以 manifest 为准 | 全部可用视图 |
| t3 | `segment_building_count`、`route_cumulative_count` | 以 manifest 为准 | 全部可用视图 |
| t4 | `route_validity`、`waypoint_ordering` | 2096 | **仅 sat / webrd04**（blank 为 0） |

`blank/t4/*.jsonl` 是空文件（`manifest.json` 的 `missing_view.blank.t4 = 2096`）。加载层必须容忍空文件，不能报错。

---

## 2. JSONL 记录 schema

单条记录字段较多，按用途分三类。

### 2.1 我们必须用的字段

| 字段 | 类型 | 用途 |
|---|---|---|
| `id` | str | 全局唯一。**续跑去重的键** |
| `question` | str | 完整问题（已含 Options 和 "Answer with only the option letter."） |
| `answer` | str | 金标准，A–D |
| `images` | list[str] | 相对路径列表。**t4 route_validity 长度为 4，其余为 1** |
| `task_id` | str | `T1`–`T4` |
| `question_type` | str | 当前 T1--T4 子任务之一，见上表 |
| `view` / `variant` / `oracle` | str/str/bool | 兼容字段 |
| `evidence_condition` | str | `direct`、`oracle`、`wrong_oracle`、`shuffled_oracle` 或 `masked_prompt` |
| `track` | str | 可选的 `U/O/G/C` 协议标签 |

`question` 示例（t1）：

```
The purple dot is in what direction from the green dot?

Options:
A. northeast
B. southeast
C. southwest
D. northwest
Answer with only the option letter.
```

### 2.2 可选用的字段

| 字段 | 用途 |
|---|---|
| `multiple_choice` | `{prompt, choices:[{key,text}], answer, answer_key, answer_index}`。**结构化选项**，若要重排选项或做选项级分析需要它 |
| `original_question` / `original_answer` | 未加选项的原始问答。做开放式评测时有用 |
| `sample_id` / `case_id` / `scheme` | 定位原始 case，调试用 |
| `label_instance` | 完整源标签，含任务特定元数据（t1 的 `bearing_deg`、t2 的 `distance_m`、t4 的 `correct_sequence` 等）。**做误差分析时很有价值** |

### 2.3 冗余字段（不要用）

`input_images`、`image`、`conversations` 与 `images` / `question` / `answer` 信息重复。

`conversations` 是 ShareGPT 格式（`[{"from":"human","value":"<image>\n..."},{"from":"gpt","value":"D"}]`）—— 训练用的形态，推理侧不需要。gate2building 的 `_build_result` 从 gpt message 取 gold，绕了一圈，我们直接用 `answer`。

---

## 3. TaskSample 与加载

### 3.1 加载器

```python
def iter_samples(
    input_dir: Path, data_root: Path,
    views: list[str], tasks: list[str], variants: list[str],
) -> Iterator[tuple[FileKey, list[TaskSample]]]:
    """按 (task, view, variant) 顺序、按 (view, task, variant) 分组产出。空文件产出空 list 而非跳过。"""
```

**为什么按文件分组而不是打平**：结果按 `{view}/{task}/{variant}.jsonl` 分文件写，续跑也按文件粒度判断。打平后要额外维护「这条属于哪个输出文件」的映射，没必要。

**为什么空文件也产出**：`blank/t4` 是合法的空。若跳过，`summary.json` 里会缺这一格，读表的人无法区分「没跑」和「本来就没数据」。

### 3.2 路径解析

```python
image_paths = [ (data_root / rel).resolve() for rel in record["images"] ]
```

在数据层做完，backend 永远只见绝对路径。这修正了 gate2building 的一个隐性约定：`RunConfig.data_dir` 在 `backends.py` 里**完全没被使用**，「caller 负责解析路径」这条规则从未写下来。

---

## 4. Prompt 构造：TaskSample → Message

### 4.1 单图任务（t1 / t2 / t3 / t4-waypoint_ordering）

```python
[
  {"type": "image", "value": abs_path},
  {"type": "text",  "value": question},
]
```

图在前、文本在后。理由：Bagel 系的 `InterleaveInferencer` 只接受 image-initial 列表（`batch_inferencer.py:787-826` 的 `validate_batch_inputs`）。统一成图先文后，避免 per-backend 特例。

### 4.2 多图任务（t4 route_validity，4 张图）

这是交错格式的价值所在：

```python
[
  {"type": "text",  "value": "Which route is valid from the green dot to the purple dot?\n\nOption A:"},
  {"type": "image", "value": path_A},
  {"type": "text",  "value": "Option B:"},
  {"type": "image", "value": path_B},
  {"type": "text",  "value": "Option C:"},
  {"type": "image", "value": path_C},
  {"type": "text",  "value": "Option D:"},
  {"type": "image", "value": path_D},
  {"type": "text",  "value": "Answer with only the option letter."},
]
```

**为什么不能用「4 图 + 一段文字」**：丢掉图与选项标签的对应关系，模型只能靠顺序猜。而 `images` 列表的顺序与选项 A/B/C/D 的对应关系在 schema 里没有任何显式保证——依赖它是脆弱的。

**这里与 image-initial 约定冲突**：t4 route_validity 的自然形态是 text-initial。处理方式见 §4.4。

### 4.3 严禁静默丢图

VLMEvalKit 的 `message_to_promptimg`（`base.py:137-154`）对非 interleave 模型只取**第一张图**，其余静默丢弃（仅 BLINK 特例拼成 512px 网格），且**不打日志**。

对多图空间题这是静默错误——4 选 1 的路线判断只看到选项 A 的图，准确率会退化到接近随机，但表面上一切正常。

我们的规则：

```python
if len(images) > backend.caps.max_images:
    # 不允许静默截断。二选一：
    #   1) 显式拼图（记录到 Prediction.meta.stitched=True）
    #   2) 报错并跳过该样本（记录 error）
    # 由 config 决定，默认报错
```

任何降级都必须落到 `Prediction.meta` 里，让读结果的人能看见。

### 4.4 Backend 侧的适配

`messages.py` 提供从 `Message` 到各家 chat 格式的统一转换，这是收敛 gate2building 8 处重复的地方：

```python
def to_openai_content(msg: Message, *, image_encoder) -> list[dict]:
    """API 风格：[{"type":"image_url","image_url":{...}}, {"type":"text","text":...}]"""

def to_qwen_content(msg: Message) -> list[dict]:
    """{"type":"image","image":path} + {"type":"text","text":...}"""

def to_url_content(msg: Message) -> list[dict]:
    """{"type":"image","url":path}（InternVL native / GLM 等）"""

def to_placeholder_prompt(msg: Message, token: str = "<image>") -> tuple[str, list[Path]]:
    """占位符风格：返回 (含 N 个 token 的文本, 图片列表)。
    InternVL-custom / MiniCPM-V / SenseNova-U1 用。"""

def to_interleave_list(msg: Message) -> list[Union[Image.Image, str]]:
    """Bagel 系原生格式：[PIL, str, PIL, str, ...]。要求 image-initial。"""
```

对于 text-initial 的 t4 route_validity，`to_interleave_list` 需要处理：若首项是 text，Bagel 系要么把它并入首图之后，要么走 prompt 前置。**具体行为待实施时用小样本验证**，不在文档里硬猜——这是已知的待确认点，记录在 [08-roadmap.md](./08-roadmap.md)。

### 4.5 占位符规范化

gate2building 里 `<image>` / `<video>` 的处理在 8 个 backend 各写一遍，行为不一致：

| backend | 行为 |
|---|---|
| `APIBackend` | 不剥离，原样保留 |
| `VllmBackend` | 剥离后按模型族重建 |
| `TransformersBackend` (qwen2.5-vl) | **不剥离**，依赖 `process_vision_info` 从 prompt 找 token |
| `SenseNovaSIBackend` | 只剥 `<video>`；`<image>` 数量与图片数不符时自动重建并告警 |
| `SenseNovaU1Backend` | 剥离后前置 `"\n".join(["<image>"]*n)` |

我们的规则：**数据层产出的 `Message` 一律不含占位符**。占位符是 backend 侧的表示细节，由 `to_placeholder_prompt` 在需要时生成。

本项目数据的 `question` 字段本身不含 `<image>`（占位符只在冗余的 `conversations` 字段里），所以这条规则天然成立。但 `messages.py` 仍需提供防御性剥离，以免未来数据变更时静默出错。

---

## 5. media.py —— 唯一的媒体处理入口

收敛 gate2building 的三类重复。

### 5.1 URL 下载（5 处重复 → 1 处）

gate2building 现状：

| backend | 策略 |
|---|---|
| `VllmBackend` | `vllm.multimodal.utils.fetch_image` |
| `APIBackend` | 本地转 data URL；http(s) 直接透传 |
| `TransformersBackend` / `SenseNovaSI` / `Cambrian` / `SpatialMLLM` | `utils.file_io.download_image_from_url` → 落临时文件 |
| `VilasrBackend` | 图像分支**无 URL 处理** |
| `SenseNovaU1Backend` | **完全没有 → 传 URL 直接崩** |

统一为：

```python
def load_image(src: Union[Path, str], *, cache: MediaCache) -> Image.Image:
    """本地路径 / http(s) URL / data URI 统一入口。URL 结果按 URL 哈希缓存到磁盘。"""
```

本项目数据全是本地路径，URL 支持是为了兼容性。但既然要写，就写对——`SenseNovaU1Backend` 那种「传 URL 直接崩」不该再出现。

### 5.2 视频抽帧（4 处重复 → 1 处）

gate2building 现状：帧数上限不一致（`SenseNovaU1Backend` 是 8，其余 16），读取器有 cv2 / decord / imageio 三种。

```python
def sample_frames(video: Path, *, n: int = 16, reader: str = "auto") -> list[Image.Image]:
    """均匀抽 n 帧。reader='auto' 时按可用性 decord → cv2 → imageio 降级。"""
```

帧数由 config 决定而非 backend 硬编码。当前数据集是纯图像任务，视频路径暂不启用，但接口留好。

### 5.3 临时文件生命周期

多个 backend 需要「PIL 对象 → 落盘 → 传路径给模型」。gate2building 各自 `tempfile.NamedTemporaryFile` 并手工记录待清理列表，容易泄漏。

```python
class MediaCache:
    """上下文管理器。退出时清理本次产生的临时文件。"""
    def materialize(self, img: Image.Image, *, suffix: str = ".jpg") -> Path: ...
```

---

## 6. preflight 校验

沿用 gate2building 的实现（`run_vlm_jsonl_inference_v5.py:97-127`），它是对的：

```python
def preflight(input_dir, data_root, views, tasks, variants) -> PreflightReport:
    """遍历全部记录的全部图片：
       1) data_root/rel 是否存在
       2) PIL.Image.open(...).verify() 是否通过
    """
```

输出 `{total_images, missing, unreadable}` 及明细。

**改进点**：

| gate2building | MapSpatial-EvalKit |
|---|---|
| 打印 `MISSING\t<jsonl>\t<rel>` 到 stdout | 结构化写入 `preflight.json`，便于程序消费 |
| `missing` 或 `unreadable` 非 0 就 `SystemExit(1)` | 同样默认拒绝启动，但支持 `--allow-missing N` 阈值（大规模数据里少数坏图不该阻断全部实验） |
| 无缓存，每次全量扫 | 结果按 `(input_dir, data_root)` mtime 缓存；`--force-preflight` 可强制重扫 |

保留 `--skip-preflight`。20 万张图的全量 verify 不便宜，反复实验时需要跳过。

---

## 7. 关于 gold 的纪律

```python
@dataclass
class TaskSample:
    id: str
    message: Message      # ← 不含 gold
    gold: str             # ← 只有评测层读
    meta: dict
```

`gold` 不进 `Message`，`Backend` 接口也不接收 `TaskSample`（只接收 `Message`）。这是类型层面的防泄漏。

gate2building 的 backend 签名是 `inference(image_paths, prompt)`，天然不会泄漏；但我们的 `Message` 结构更复杂，显式隔离更稳妥。

---

## 8. 相关文档

| 主题 | 文档 |
|---|---|
| `Message` / `Prediction` / `TaskSample` 完整定义 | [01-architecture.md](./01-architecture.md) |
| 各 backend 如何消费 `Message` | [03-backends.md](./03-backends.md) |
| 答案抽取与指标聚合 | [06-runner-eval.md](./06-runner-eval.md) |
