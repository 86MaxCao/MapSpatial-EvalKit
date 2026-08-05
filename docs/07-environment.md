# 07 · 统一环境与兼容层

> **本文档描述 MapSpatial-EvalKit 最重要的硬约束：所有 20 个模型必须跑在同一个 Python 环境里。**

---

## 1. 决策：单一环境，不可协商

### 1.1 约束

```
一个 micromamba 环境 → 20 个模型全部可跑
```

不允许出现「模型 A 用 env1，模型 B 用 env2」。不允许出现「先 activate X 再跑这批」。

### 1.2 理由

多环境方案的成本不是消失了，而是**转嫁给使用者**：

- 使用者要维护 N 个环境，每个几十 GB
- 新增一个模型要先搞清楚它属于哪个环境
- 跨环境的结果需要手工合并，`summary.json` 无法一次生成
- CI 无法在单个容器里验证
- 「跑通全部模型」不再是一条命令

结论：**多环境的项目没有人用。** 宁可花时间写兼容层，也不要把复杂度推给下游。

### 1.3 被否决的替代方案

| 方案 | 否决理由 |
|---|---|
| 每个模型一个 env，脚本按 config 里的 `env` 字段 activate | 上述全部问题。使用者心智负担过重 |
| runner 在 env A，spawn env B 的 worker，JSONL over stdio | 复杂度高一个量级；调试时堆栈跨进程断裂；两边依赖漂移后极难排查 |
| 用 Docker 封装多环境 | 只是把问题藏进镜像；开发迭代（改一行代码要重建镜像）不可接受 |

---

## 2. 冲突的四类来源与对应手段

单一环境要付的代价是**处理依赖冲突**。手段按成本从低到高排序，**永远先试低成本的**：

```
① 配置层调参       ← 最优先
② 运行时 monkey-patch
③ vendor 模型代码
④ sys.modules 注入 shim   ← 最后手段
```

### 2.1 手段 ①：配置层调参

很多「冲突」其实只是参数默认值不同。例如 `attn_implementation`（`flash_attention_2` / `sdpa` / `eager`）、`dtype`、`device_map`、`trust_remote_code`。

这些应该在 `configs/models/*.yaml` 里显式声明，而不是靠环境差异掩盖：

```yaml
name: InternVL3-8B-Instruct
backend: transformers
model_path: ${CKPT_DIR}/InternVL3-8B-Instruct
load:
  attn_implementation: sdpa      # flash_attn 与该模型自定义代码不兼容 → 显式降级
  trust_remote_code: true
```

**原则**：任何「换个参数就能跑」的问题，都不该动到 patch 层。

### 2.2 手段 ②：运行时 monkey-patch

适用于 **transformers / torch 的 API 漂移**：模型的自定义代码（`trust_remote_code`）写死了某个旧版 API，而当前版本已改名或改签名。

这是 `gate2building` 已经在用的手段。三个真实案例（`backends.py:524-575`）：

| 症状 | 根因 | 补丁 |
|---|---|---|
| 加载自定义代码模型时 `AttributeError: all_tied_weights_keys` | transformers 新版在 `_finalize_model_loading` 里期望该属性存在，旧版自定义代码没设 | wrap `PreTrainedModel._finalize_model_loading`，缺失时补空集合 |
| `_init_infer_auto_device_map` 同类报错 | 同上，accelerate 集成路径 | 同样 wrap |
| `InternVisionEncoder` 在 meta device 上 `linspace().item()` 崩溃 | meta tensor 没有真实值，`.item()` 非法 | wrap `torch.Tensor.item`，meta device 返回 `0.0` |

**这类补丁的特征**：改动面极小（一个方法/一个属性），且**上游修好后补丁自动变成 no-op**。

### 2.3 手段 ③：vendor 模型代码

适用于**模型自带大量自定义 modeling 代码，且冻结在旧 transformers 上**。典型：Cambrian-S（LLaVA 衍生）、Bagel/ThinkMorph 系列。

与其在运行时打十几个补丁去迎合别人的代码，不如把代码复制进本仓库直接改。这样：

- 改动可见、可 review、可 diff
- 不依赖运行时 patch 顺序
- 版本固定，不会被上游更新打断

先例：`VLMEvalKit_Thinkmorph` 的 `vlmeval/vlm/thinkmorph/modeling/{bagel,qwen2,siglip}/` + `autoencoder.py` 就是 vendor 的产物。

**vendor 的纪律**（必须遵守，否则会变成技术债）：

```
mapspatial/vendor/<name>/
├── ORIGIN.md      # 来源 repo/commit、vendor 日期、为什么 vendor
├── PATCHES.md     # 逐条列出相对原始代码的改动及原因
└── <源码树>
```

每一处本地修改加注释标记：

```python
# [MapSpatial-EvalKit] 原代码用 transformers.models.llama.LlamaAttention（已移除）。
# 改用 sdpa 等价实现。原始代码见 ORIGIN.md 指向的 commit。
```

### 2.4 手段 ④：`sys.modules` 注入 shim

最后手段。适用于模型代码 `import` 了一个**已被完全删除**的模块，且该模块在导入期就被求值（无法靠 config 或 wrap 绕开）。

做法：在模型加载前，往 `sys.modules` 塞一个提供所需符号的假模块。

**必须满足的条件**（否则不许用）：
- 有明确注释说明假的是什么、为什么、什么条件下可以删除
- 只在需要它的 backend 里激活，不得全局生效
- 假模块提供的符号必须行为等价，不能是空壳

理由：这种 patch 会污染全局导入状态，且失败时的报错离根因极远。宁可 vendor。

---

## 3. 兼容层的架构

### 3.1 为什么要做成一等组件

如果把补丁散落在各个 backend 的 `__init__` 里（现状），会出现：

- **顺序依赖**：补丁 A 必须在 B 之前，但没人知道
- **重复打补丁**：两个 backend 打同一个补丁，第二次可能把第一次的 wrap 又 wrap 一层
- **无法审计**：出问题时不知道当前进程里生效了哪些补丁
- **无法测试**：补丁和模型加载耦合，不能单独验证

所以补丁必须集中管理、显式声明、可查询。

### 3.2 结构

```
mapspatial/compat/
├── __init__.py        # apply(*names), applied(), describe()
├── registry.py        # @patch 装饰器 + 注册表
└── patches/
    ├── tied_weights.py       # all_tied_weights_keys 缺失
    ├── meta_tensor_item.py   # meta device .item()
    ├── flash_attn_fallback.py
    └── ...
```

### 3.3 补丁的契约

每个补丁是一个带元数据的函数：

```python
@patch(
    name="tied_weights_keys",
    reason="transformers 新版 _finalize_model_loading 期望 all_tied_weights_keys 存在，"
           "但 trust_remote_code 模型的旧版自定义代码未设置该属性",
    affects=["internvl-custom", "minicpm-v"],   # 仅文档用途，便于排查
)
def tied_weights_keys() -> bool:
    """返回 True 表示实际打了补丁，False 表示当前版本无需打（自动 no-op）。"""
    import transformers

    target = transformers.PreTrainedModel
    if not hasattr(target, "_finalize_model_loading"):
        return False          # 上游已改，补丁不再适用

    original = target._finalize_model_loading

    def wrapped(self, *args, **kwargs):
        if not hasattr(self, "all_tied_weights_keys"):
            self.all_tied_weights_keys = set()
        return original(self, *args, **kwargs)

    target._finalize_model_loading = wrapped
    return True
```

四条硬性要求：

| 要求 | 原因 |
|---|---|
| **幂等** —— 重复 `apply()` 只生效一次 | 避免 wrap 套 wrap。由 registry 用 applied-set 保证，补丁本身不用操心 |
| **自失效** —— 检测到上游已修则返回 `False` | 升级依赖后补丁自动消失，不会掩盖新问题 |
| **窄** —— 只碰必须碰的那一个符号 | 降低对无关模型的副作用 |
| **声明式** —— 由 backend 声明需要哪些，不隐式全局打 | 可审计；跑 Qwen3-VL 时不该激活 InternVL 的补丁 |

### 3.4 backend 侧的声明

```python
@register("transformers")
class TransformersBackend(Backend):
    # 该 backend 加载模型前需要的补丁
    COMPAT = ("tied_weights_keys", "meta_tensor_item")

    def __init__(self, cfg):
        compat.apply(*self.COMPAT)     # 幂等；registry 负责去重
        ...
```

### 3.5 可观测性

结果文件里必须记录生效的补丁，否则复现实验时无法确认环境一致：

```json
{
  "env": {
    "python": "3.11.x",
    "torch": "...",
    "transformers": "...",
    "vllm": "...",
    "compat_applied": ["tied_weights_keys", "meta_tensor_item"],
    "compat_skipped": ["flash_attn_fallback"]
  }
}
```

`mapspatial compat --describe` 应能打印全部注册补丁、原因、当前是否会生效——这是排查「换机器就跑不通」的第一手工具。

---

## 4. 环境构建

### 4.1 基线

以 `gate2building` 使用的 micromamba `latest` 环境为基线派生，因为它**已经验证过 14 个纯理解模型 + vLLM**，是已知可用的最大集合。

```bash
export MAMBA_ROOT_PREFIX=/mnt/nas-tbt/caoziqi/micromamba
micromamba create -n mapspatial --clone latest
micromamba activate mapspatial
```

派生而非从零搭建的理由：从零搭建要重新踩一遍 14 个模型的依赖坑；克隆则只需处理**增量**（6 个统一模型）。

### 4.2 增量安装

6 个统一模型需要的额外依赖（VeOmni 侧证据）：

- `diffusers`（BLIP3o 的 DIT 路径）
- MoVQGAN / VAE 相关（Bagel 系生成路径，可能随 vendor 一起进来）
- 各模型 tokenizer/processor 依赖

**安装纪律**：
1. 逐个模型装、逐个模型验证，**每步记录到 `docs/env-log.md`**
2. 装完立即回归验证已通过的模型（防止装 A 打破 B）
3. 出现版本冲突时，**先走第 2 节的手段 ①→④**，不要靠升/降级全局包解决

### 4.3 冲突预案

基于现有代码证据，以下是**预期**会出问题的点。具体表现待实施时确认，此处记录判断依据：

| 风险点 | 依据 | 预案 |
|---|---|---|
| `trust_remote_code` 模型的 API 漂移 | `gate2building` 已需要 3 个 patch 才能加载 InternVL-custom / MiniCPM-V | 沿用已有 patch，纳入 compat 层 |
| Cambrian-S 依赖 LLaVA 时代的 transformers 内部 API | `backends.py:114-118` 需要把 `models/` 插入 `sys.path` 才能 `import cambrian` | 优先 vendor（手段 ③） |
| Janus 用 v4 风格 `LlamaForCausalLM._from_config` | `modeling_janus.py:1219` | vendor 或窄 patch |
| VeOmni 侧代码假定特定 transformers 版本 | VeOmni `pyproject.toml` 有硬 pin | 只 vendor 需要的 modeling 文件，**不装 veomni 包本身**（见 05 文档） |
| vLLM 与其他包争 torch 版本 | vLLM 自带 torch/flash-attn 约束 | vLLM 优先级最高（14 个模型靠它跑批量）；其他包让步 |

### 4.4 不做的事

- **不安装 `veomni` 包本身。** 它是训练框架（`build_foundation_model` 需要 `OpsImplementationConfig`），带一堆 FSDP2/EP/序列并行依赖，而我们只要 modeling 代码。见 05 文档。
- **不追求依赖版本「最新」。** 目标是全部模型可跑，不是版本好看。
- **不用 `--force-reinstall` / `--no-deps` 掩盖冲突。** 这会造成运行时才暴露的隐性破损。

---

## 5. 验收标准

单一环境是否达标，用这个矩阵判断：

```bash
mapspatial doctor          # 逐个 backend 检查：可导入？可加载？可推理 1 条？
```

输出应形如：

| backend | 模型 | import | load | infer(1) | 生效补丁 |
|---|---|---|---|---|---|
| vllm | Qwen3-VL-8B | ok | ok | ok | — |
| transformers | InternVL3-8B | ok | ok | ok | tied_weights_keys, meta_tensor_item |
| veomni_bagel | Bagel-7B-MoT | ok | ok | ok | — |
| ... | | | | | |

**20/20 全绿是发布门槛。** 任何一格红都必须在 `docs/env-log.md` 里有 issue 记录和处理计划，不允许静默跳过。

---

## 6. 与其他文档的关系

- 每个 backend 需要哪些补丁 → [03-backends.md](./03-backends.md)
- 6 个统一模型为什么 vendor 而非装包 → [05-veomni-integration.md](./05-veomni-integration.md)
- 环境搭建的分阶段计划 → [08-roadmap.md](./08-roadmap.md)
