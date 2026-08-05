# 03 · Backends

> 20 个模型如何映射到 backend、能力矩阵、以及 vLLM 真批量的实现要点。

---

## 1. Backend 清单

不是「一模型一 backend」。同一推理引擎/模型族共享一个 backend，靠 config 区分。

| backend | 覆盖模型 | 参考实现 |
|---|---|---|
| `api` | qwen3.5-plus、qwen3.6-plus、qwen3.7-plus、gemini-3-flash-preview | gate2building `backends.py:187-356` |
| `vllm` | Qwen3-VL-2B/8B、Qwen2.5-VL-7B、Qwen2-VL-7B、InternVL3-8B、InternVL3_5-8B、GLM-4.6V、Step3-VL-10B、MiMo-Embodied-7B | gate2building `backends.py:360-521`（**真批量**） |
| `transformers` | 上述模型的非 vLLM 回退路径 | gate2building `backends.py:579-1117` |
| `sensenova_si` | SenseNova-SI-1.3-Qwen3-VL-8B、SenseNova-SI-1.5-InternVL3-8B | gate2building `backends.py:1121-1248` |
| `cambrian` | Cambrian-S-7B-LFP | gate2building `:1344-1456`；VLMEvalKit `vlm/cambrian_s.py`（更干净） |
| `vilasr` | ViLaSR | gate2building `:1252-1340`；VLMEvalKit 用 `Qwen2VLChat` |
| `spatial_mllm` | Spatial-MLLM | gate2building `:1475-1658`；VLMEvalKit `vlm/spatial_mllm.py` |
| `veomni_bagel` | Bagel-7B-MoT | VeOmni + vendor ThinkMorph inferencer |
| `veomni_thinkmorph` | ThinkMorph-7B | 同上（复用 Bagel 类） |
| `veomni_blip3o` | BLIP3o-8B | VeOmni `modeling_blip3o.py` |
| `veomni_u1` | SenseNova-U1-8B-MoT | VeOmni `modeling_neo_chat.py` |
| `veomni_latentum` | LatentUM-Base | VeOmni `modeling_latentum.py` |
| `veomni_janus` | Janus-Pro-7B | VeOmni `modeling_janus.py` |
| `sensenova_u1_official` | SenseNova-U1-8B-MoT（官方 `sensenova_u1` 包路径） | gate2building `:1662-1798` |

注：`sensenova_u1_official` 与 `veomni_u1` 是同一权重的两条代码路径。保留两条用于交叉验证 VeOmni 实现的正确性（VeOmni README 声称 100% 对齐，值得独立验证）。

---

## 2. 能力矩阵

| backend | batch | draw | native_interleave | max_images | video | 需要的 compat |
|---|---|---|---|---|---|---|
| `api` | ✗ (靠 worker 并发) | ✗ | ✗ | 大 | ✗ | — |
| `vllm` | **✓ 真批量** | ✗ | ✗ | 24 (config) | ✗ | — |
| `transformers` | ✗ | ✗ | ✗ | 按模型 | 部分 | `tied_weights_keys`, `meta_tensor_item` |
| `sensenova_si` | ✗ | ✗ | ✗ | 多图 | ✓ | 待确认 |
| `cambrian` | ✗ | ✗ | ✗ | 多图 | ✗ | 可能需 vendor |
| `vilasr` | ✗ | ✗ | ✗ | 多图 | ✓ | — |
| `spatial_mllm` | ✗ | ✗ | ✗ | 多图 | ✓ | — |
| `veomni_bagel` | ✓ (vendor 批量) | **✓** | **✓** | 待确认 | ✗ | — |
| `veomni_thinkmorph` | ✓ | **✓** | **✓** | 待确认 | ✗ | — |
| `veomni_blip3o` | ✗ | **✓** | ✗ | 待确认 | ✗ | 待确认 |
| `veomni_u1` | ✗ | **✓** | 待确认 | 多图 | ✗ | 待确认 |
| `veomni_latentum` | ✗ | **✓** | ✗ | 待确认 | ✗ | 需 decoder ckpt |
| `veomni_janus` | ✗ | **✓** | ✗ | 待确认 | ✗ | v4 API 适配 |

「待确认」是诚实的状态，不是遗漏。这些格子需要在实施阶段用小样本实测填写，硬猜写进文档反而有害。清单见 [08-roadmap.md](./08-roadmap.md)。

**T4 route_validity 需要 4 图**，因此 `max_images >= 4` 是硬要求。任何 `max_images < 4` 的 backend 在 t4 上必须显式降级（拼图或跳过），并记录到 `Prediction.meta`。

---

## 3. vLLM：真批量是重点

### 3.1 参考实现的反面教材

VLMEvalKit 的 vLLM 集成基本浪费了 vLLM。证据：

```python
# vlmeval/vlm/qwen3_vl/model.py:403
outputs = self.llm.generate([req], sampling_params=sampling_params)   # 列表长度 1

# vlmeval/vlm/qwen2_vl/model.py:591 —— 连列表都没包
self.llm.generate({"prompt": ..., "multi_modal_data": {"image": images}}, ...)
```

外层是串行循环，且每条之后清缓存：

```python
# vlmeval/inference.py:167-190
for i in tqdm(range(lt), ...):
    response = model.generate(message=struct, dataset=dataset_name)
    torch.cuda.empty_cache()          # ← 每条都清，冲掉 vLLM 的 KV cache
```

后果：`max_num_seqs=8`（Qwen3-VL）、`=5`（Qwen2-VL）**永远跑不满**，continuous batching 从未被激活。且 `generate_inner_batch` / `supports_batch` 在整个仓库 **0 匹配**——框架没有批量抽象。

覆盖率也不足：14 个纯理解模型里只有 6 个有 vLLM 路径（Qwen 系 4 个 + GLM + ViLaSR），InternVL3/InternVL3_5/Cambrian-S/Spatial-MLLM 都只走 transformers，MiMo-Embodied 和 SenseNova-U1 根本没注册。CLI 也是残的：`inference.py:131-136` 只对 `'Llama-4'` / `'Qwen2-VL'` / `'Qwen2.5-VL'` 三个子串生效，其他模型传 `--use-vllm` 静默忽略。

### 3.2 gate2building 的做法是对的

```python
# gate2building/eval/backends.py:484
def batch_inference(self, batch_inputs):
    valid_inputs = [...]                                  # 过滤 prep 失败的
    outputs = self.llm.generate(valid_inputs, sampling_params)   # ← 一次提交全部
    # 再把输出按原始索引映射回去
```

`supports_batch = True`，batch_size 默认 32。这是正确姿势，直接继承。

### 3.3 MapSpatial-EvalKit 的实现要点

```python
@register("vllm")
class VllmBackend(Backend):
    caps = Capabilities(batch=True, draw=False, native_interleave=False,
                        max_images=24, video=False)

    def understand(self, messages: list[Message], **gen_kw) -> list[Prediction]:
        reqs, index_map = [], []
        for i, msg in enumerate(messages):
            try:
                reqs.append(self._to_vllm_request(msg))
                index_map.append(i)
            except Exception as e:
                ...     # 记录 error，不阻断整批
        outputs = self.llm.generate(reqs, self._sampling_params(**gen_kw))
        # 按 index_map 还原到原始位置
```

四条纪律：

| 纪律 | 原因 |
|---|---|
| **一次 `generate()` 提交整批** | 否则 continuous batching 无效 |
| **循环里不调 `torch.cuda.empty_cache()`** | 会冲掉 KV cache（VLMEvalKit 的错误） |
| **单条失败不阻断整批** | 用 index_map 映射回原位，失败位填 error |
| **`limit_mm_per_prompt` 由 config 给** | t4 需要 4 图；写死会静默截断 |

不做 `VLLMMixin` 混入各模型类。VLMEvalKit 把 `LLM(...)` 构造复制粘贴到 ~10 个文件（`qwen3_vl`、`qwen2_vl`、`llama4`、`cogvlm`、`gemma`、`nvlm`、`cosmos`、`deepseek_ocr`、`keye_vlm`、`ovis`），差异只在 `max_num_seqs` / `limit_mm_per_prompt` / `max_model_len`。这些统统是 config 参数，一个 backend 足够。

### 3.4 模型族差异的处理

vLLM 对不同模型族的输入格式要求不同（gate2building `_prepare_single_input:418` 已处理）：

| 模型族 | 输入形态 |
|---|---|
| qwen 系 | chat message + `{"type":"image","image":path}` |
| internvl / minicpm | `"\n".join(["<image>"]*n) + clean_prompt` 占位符风格 |

由 `messages.py` 的 `to_qwen_content` / `to_placeholder_prompt` 提供（见 [02-data-pipeline.md §4.4](./02-data-pipeline.md)），backend 只按 config 里的 `prompt_style` 选一个，不自己写转换逻辑。

---

## 4. transformers backend：拆分而非单体

gate2building 的 `TransformersBackend` 是 539 行单类（`:579-1117`），内部按 `_model_type` 分 9 个分支（qwen2.5-vl / qwen3-vl / qwen3.5 / qwen3.6 / glm-4.6v / step3-vl / minicpm-v / internvl / gemma-4），每个分支自己写一遍 message 构造和 generate 调用。

且藏着 bug：`_load_gemma4`（`:792`）引用 `GEMMA4_AVAILABLE` 和 `Gemma4ForConditionalGeneration`，但**两者都从未 import** → 走到该分支必然 `NameError`。

### 拆分方式

```
backends/transformers/
├── base.py          # 共享：加载、compat 应用、generate 调用、显存清理
├── qwen_vl.py       # qwen2.5-vl / qwen3-vl / qwen3.5 / qwen3.6
├── internvl.py      # native + custom 两种模式
├── glm.py           # glm-4.6v
├── minicpm.py       # minicpm-v（特殊：448x448 强制 resize、视频首帧）
└── generic.py       # AutoModelForCausalLM 兜底
```

模型类的选择由 config 显式给出，不靠 `model_id` 字符串前缀猜：

```yaml
# gate2building 靠 model_id.lower().startswith("qwen2.5-vl") 猜，
# 权重目录一改名就走错分支
load:
  model_class: Qwen2_5_VLForConditionalGeneration   # 显式
  processor_class: AutoProcessor
```

保留 `config.json` 的 `model_type` 作为**校验**而非猜测依据：config 声明与 `config.json` 不一致时报错，而不是静默采用其中一个。

---

## 5. 惰性加载

```python
# backends/__init__.py —— 只注册加载器
@register("vllm")
def _vllm():
    from .vllm import VllmBackend       # vllm 在此刻才 import
    return VllmBackend

@register("cambrian")
def _cambrian():
    from .cambrian import CambrianBackend
    return CambrianBackend
```

对比两种参考实现：

| 项目 | 做法 | 问题 |
|---|---|---|
| VLMEvalKit | `vlm/__init__.py` 无条件导入 80+ 模型文件 | 跑一个模型付全部导入成本；任一模型的重依赖缺失就影响全局 |
| gate2building | 模块加载期 `try/except` + `*_AVAILABLE` 标志 | 方向对，但仍在 import 时执行全部 try |
| MapSpatial-EvalKit | 装饰器注册加载器，`get_backend_cls()` 时才 import | 只 import 用到的 |

好处：`mapspatial run --model qwen3-vl-8b` 完全不会 import cambrian / veomni 的任何东西。

---

## 6. 共享基础设施

gate2building 里以下逻辑在 8 个 backend 各写一遍且行为不一致。收敛到共享模块（见 [02-data-pipeline.md](./02-data-pipeline.md)）：

| 逻辑 | gate2building 现状 | 归属 |
|---|---|---|
| `<image>` / `<video>` 占位符 | 8 处，5 种行为 | `messages.py` |
| URL 下载 | 5 处，3 种策略；`SenseNovaU1Backend` 完全没有（传 URL 直接崩） | `media.py` |
| 视频抽帧 | 4 处；帧数上限不一致（U1 是 8，其余 16）；读取器 cv2/decord/imageio 三种 | `media.py` |
| 临时文件清理 | 各自 `tempfile` + 手工列表 | `media.MediaCache` |
| transformers 兼容补丁 | `_patch_custom_model_compat()` 私有函数 | `compat/`（见 [07](./07-environment.md)） |
| system prompt 前置 | `BaseBackend._system_messages`（唯一已共享的） | 保留 |

**backend 不允许自己写这些。** code review 时这是硬门槛。

---

## 7. API backend

### 7.1 保留的设计

gate2building 的 `APIBackend`（`:187-356`）有几点做得好，保留：

- 多 key 轮转，遇限流切换
- 按模型名调整图像压缩：gemini 512/75、qwen/gpt 768/80、其他 1024/85
- 指数退避 + jitter 重试；超时 `(180, 600)`

### 7.2 必须修正

**硬编码 API key。** `run_api_inference_v5.sh:18-20`：

```bash
KEY1="QUIdDuW3oC7bQ0Ym8iLeZZf0"
KEY2="xXFHJUtmV9rTXKSr1ob6Ba2D"
KEY3="OzNqIm7Wrhc8YpxidE621SjB"
```

全部改为环境变量（`MAPSPATIAL_API_KEYS`，逗号分隔）。这三个 key 应视为已泄漏，建议轮换。

**并发模型。** gate2building 用 `ThreadPoolExecutor(max_workers=4)`，每个 future 处理一个 (view, variant) 组合，共享同一 backend 实例。粒度太粗——4 个组合跑完才收工，长尾明显。

改为按样本粒度的 worker pool，backend 内部对 key 轮转加锁：

```python
caps = Capabilities(batch=False, ...)   # 不是引擎级批量
# runner 用 worker pool 并发调 understand([单条])
```

---

## 8. 从 VLMEvalKit 移植哪些模型类

新 checkout（`outdoor-spatial-intelligence-scripts/VLMEvalKit`，v0.2rc1）的实现比 gate2building 干净，优先从这里移植：

| 模型 | VLMEvalKit 路径 | 备注 |
|---|---|---|
| Cambrian-S | `vlm/cambrian_s.py` | 比 gate2building 的 `CambrianBackend` 干净；后者需把 `models/` 插进 `sys.path` 才能 `import cambrian` |
| Spatial-MLLM | `vlm/spatial_mllm.py` | `class SpatialMLLM(Qwen2VLPromptMixin, BaseModel)` |
| SenseNova-SI 系列 | `config.py:2545-2607` | 多个变体，分别映射到 InternVLChat / Qwen2VLChat / Qwen3VLChat |
| ViLaSR | `config.py:2523` | 走 `Qwen2VLChat`，比 gate2building 的独立 `VilasrModel` 简单 |

注意该 checkout 已有 `spatial_related_models` / `sensenova_si_series` / `bagel_series` 分组（`config.py:2644`，注释 "add by EASI team"），说明空间类模型的适配工作已有人做过一轮，值得先读再动手。

---

## 9. 相关文档

| 主题 | 文档 |
|---|---|
| Backend 接口与能力声明 | [01-architecture.md](./01-architecture.md) |
| `messages.py` / `media.py` 的 API | [02-data-pipeline.md](./02-data-pipeline.md) |
| 6 个统一模型的 backend 细节 | [05-veomni-integration.md](./05-veomni-integration.md) |
| compat 补丁机制 | [07-environment.md](./07-environment.md) |
| 「待确认」格子的验证计划 | [08-roadmap.md](./08-roadmap.md) |
