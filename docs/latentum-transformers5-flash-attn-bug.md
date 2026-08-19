# LatentUM Transformers 5.x Flash Attention 2 退化问题分析

## 问题现象

在 `transformers 5.8.0`（main 环境）下加载 LatentUM-Base 模型进行多模态理解（VQA），输出严重退化：

```
输入: asset/blue_apple.png + "Describe this image."
输出(5.x): "The!!!!!!!!!!!!!!!!!!!"   (token 0 重复)
输出(4.x): "The image features a single, vibrant blue apple placed on a wooden surface..."
```

模型加载正常、不报错，但生成结果仅首 token 正确，后续全部退化为 token ID 0。

## 环境对比

| 项目 | main (5.x, 异常) | sensenova_u1 (4.x, 正常) |
|------|------------------|--------------------------|
| transformers | 5.8.0 | 4.57.1 |
| torch | 2.11.0 | 2.8.0 |
| flash_attn | 2.8.4 (**可导入**) | 2.8.4 (**导入失败**) |
| Python | 3.10.15 | 3.11.15 |
| `_attn_implementation` | `flash_attention_2` | `eager` |

## 排查过程

### 1. 排除 tokenizer 问题

两个环境使用不同 tokenizer 类型（`TokenizersBackend` vs `PreTrainedTokenizerFast`），但编码结果完全一致：

- `input_ids` 长度：均为 308
- 首 30 / 末 30 token ID：完全相同
- 特殊 token 映射：完全相同

**结论：tokenizer 不是根因。**

### 2. 排除 generation_config 问题

5.x 中 `GenerationConfig` 默认值全部改为 `None`（4.x 有具体值如 `max_length=20, do_sample=False`），但 `_prepare_generation_config` 通过 `_get_default_generation_params()` 填充了旧默认值。最终 generation_config 的 `use_cache=True, max_new_tokens=20, do_sample=False` 等关键参数均正确。

**结论：generation_config 不是根因。**

### 3. 定位 attention 实现

通过强制切换 `_attn_implementation` 测试：

| attention | 5.x 输出 | 状态 |
|-----------|---------|------|
| `flash_attention_2` | `The!!!...` | 异常 |
| `sdpa` | 正常描述 | 正常 |
| `eager` | 正常描述 | 正常 |

**根因锁定：仅 `flash_attention_2` 实现有问题。**

### 4. 深入 flash_attention_2 路径

#### 4a. causal mask 差异

5.x 中 `create_causal_mask` 对 `flash_attention_2` 返回 `None`（注释标注 "not used anymore but kept for BC"），依赖 flash_attn 自带的 `is_causal` 标志。SDPA/eager 则会创建显式 4D causal mask。

#### 4b. `is_causal` → `causal` 参数转换

`flash_attn_func` 接受的参数名是 `causal`（默认 `False`），不是 `is_causal`。转换由 `_process_flash_attention_kwargs` 完成：

```python
flash_kwargs = {
    "causal": is_causal and not (use_top_left_mask and query_length == 1),
    ...
}
```

关键逻辑：当 `use_top_left_mask=True` 且 `query_length == 1`（decoding 阶段）时，`causal` 被设为 `False`。

#### 4c. forward 调用链对比

**4.x Qwen3Attention.forward:**
```python
cache_kwargs = {"sin": sin, "cos": cos, "cache_position": cache_position}
key_states, value_states = past_key_values.update(
    key_states, value_states, self.layer_idx, cache_kwargs
)
```

**5.x Qwen3Attention.forward:**
```python
key_states, value_states = past_key_values.update(
    key_states, value_states, self.layer_idx
)  # 不传 cache_kwargs
```

5.x 完全移除了 `cache_position`，不再传给 `create_causal_mask`、decoder layer 和 cache update。

#### 4d. KV cache 调试

通过 patch LLM forward 检查每步输入：

| 步骤 | 4.x `cache_position` | 5.x `cache_position` |
|------|---------------------|---------------------|
| Step 1 (prefill) | `[0,1,...,307]` | `None` |
| Step 2 (decode) | `[308]` | `None` |
| Step 3 (decode) | `[309]` | `None` |

生成的 token IDs（5.x flash_attention_2）：
```
[785, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ↑   └── token 0 重复，退化为 "!" ──────────────────────────┘
  └── "The" 正确
```

## 根因总结

问题由 transformers 5.x 的多个 breaking change 叠加导致，**仅在 `flash_attention_2` 实现下触发**：

1. **`create_causal_mask` 对 flash_attention_2 返回 `None`** — 不再创建显式 4D causal mask，改为依赖 flash_attn 的 `is_causal`/`causal` 参数。

2. **`_process_flash_attention_kwargs` 中的 `use_top_left_mask` 逻辑** — 当 `use_top_left_mask=True` 且 `query_length==1`（decoding 阶段）时，`causal=False`。这可能导致 decoding 阶段 flash attention 不应用因果约束，query token 错误地（或不正确地）attend 到所有 key positions。

3. **`cache_position` 被完全移除** — 4.x 中 `cache_position` 贯穿 `prepare_inputs_for_generation` → `Qwen3Model.forward` → `Qwen3DecoderLayer.forward` → `Qwen3Attention.forward` → `past_key_values.update(cache_kwargs)`。5.x 中这条链路完全断开。

4. **cache update 不传 `cache_kwargs`** — 4.x 传 `{"sin": sin, "cos": cos, "cache_position": cache_position}` 给 `past_key_values.update()`，5.x 只调 `update(key_states, value_states, layer_idx)`。

**根因链条**：`flash_attention_2` + `create_causal_mask` 返回 `None` + `causal` 参数在 decoding 阶段被置为 `False` → prefill 阶段首 token 正确（query_length == key_length）但 cache 中存入的中间层 hidden states 可能有误 → decoding 阶段 cache + 错误 causal 设置 → 输出全部退化为 token 0。

SDPA/eager 不受影响，因为它们使用显式 4D causal mask，不依赖 `is_causal`/`causal` 参数。

## 修复方案

### 方案 A：强制 eager/SDPA attention（即时可用）

```python
llm = model.internvl.language_model
llm.config._attn_implementation = 'sdpa'
for layer in llm.model.layers:
    layer.self_attn.config._attn_implementation = 'sdpa'
```

### 方案 B：使用 sensenova_u1 环境（推荐）

```bash
micromamba activate sensenova_u1
# transformers 4.57.1 + torch 2.8.0 + flash_attn 2.8.4(导入失败，自动用 eager)
```

### 方案 C：适配 transformers 5.x（长期）

修改 InternVL 的 `modeling_internvl_chat.py`，在 `generate()` 中显式传递 `cache_position` 或在模型层面补充 `flash_attention_2` 所需的 causal mask。

## 复现脚本

```python
import torch
from model.latentum import LatentUMModel

model = LatentUMModel.from_pretrained(
    "/mnt/nas-tbt/tbt/checkpoint/hf_cache/LatentUM-Base",
    device="cuda:0",
    dtype=torch.bfloat16,
)

# 默认 flash_attention_2 → 退化
answer = model.answer("asset/blue_apple.png", "Describe this image.")
print(answer)  # "The!!!..."

# 修复：强制 SDPA
llm = model.internvl.language_model
llm.config._attn_implementation = "sdpa"
for layer in llm.model.layers:
    layer.self_attn.config._attn_implementation = "sdpa"

answer = model.answer("asset/blue_apple.png", "Describe this image.")
print(answer)  # 正常输出
```
