# Interleave 实现状态与交接文档

> 本文档记录所有已完成的修改、当前测试状态、以及后续 agent 需要执行的测试命令。

---

## 1. 已完成的修改（全部已 commit + push）

### 1.1 U1 native_interleave

**修改文件：**
- `mapspatial/vendor/neo_chat/modeling_neo_chat.py` — 新增 `interleave_gen()` 方法（~500行），从官方 U1 代码 port
- `mapspatial/backends/veomni/u1.py` — 新增 `interleave()` 方法，caps 改为 `native_interleave=True`
- `configs/models/sensenova-u1-8b.yaml` — strategies 增加 `native_interleave`

**关键适配：**
- `get_conv_template` 替换为 vendored 的 `_build_t2i_query()`
- attention_mask 用 raw tensor（非 dict）
- `_t2i_predict_v` 签名增加 `attn_mask=None, timestep_embeddings=None` 可选参数
- `forward_und` SDPA causal flag 修复：单 token + past cache 时用 `causal=False`
- marker 是 `<img>`（不是 `<image_start>`）
- 生成时 cast model 到 float32（避免 flash_attn bf16 NaN），生成完恢复 bfloat16

### 1.2 LatentUM native_interleave

**修改文件：**
- `mapspatial/backends/veomni/latentum.py` — 新增 `interleave()` 方法（~300行），caps 改为 `native_interleave=True`
- `configs/models/latentum-base.yaml` — strategies 增加 `native_interleave`

**关键适配：**
- 基于 `FrozenLakePlanner` 的 save-rewind-reinject 模式泛化
- AR 文本生成 → `<img>` → 保存 KV → 生成 256 VQ codes → rewind → 重注入 → 继续文本
- 多图输入支持
- 解码通过 `LatentUMDecoderModel.decode()`

### 1.3 U1 external_draw 修复（已完成，已验证）

**根因：** flash_attn 内部使用 bfloat16，即使模型权重是 float32 也会溢出 → 全 NaN → 黑图

**修复（3 个关键 fix）：**
1. `_HAS_FLASH_ATTN = False` — 禁用 flash_attn，强制用 SDPA（`mapspatial/vendor/neo_chat/modeling_neo_chat.py`）
2. `self._model.float()` — draw() 时转 float32，完成后恢复 bfloat16（`mapspatial/backends/veomni/u1.py`）
3. `timestep_shift=3.0` — 使用模型训练时的偏移调度（不是默认的 1.0）
4. `pixel_values.to(self.dtype)` — 不硬编码 bfloat16（`mapspatial/vendor/neo_chat/modeling_neo_chat.py`）

### 1.4 其他 6 个模型的 external_draw 修复（已完成）

| 模型 | 修复 | 文件 |
|---|---|---|
| LatentUM | decoder 路径 `LatentUM-Base/decoder` → `LatentUM-Decoder` + 用 `quantizer.indices_to_feature` + `decoder.decode()` | latentum.py, latentum-base.yaml |
| Janus | `get_input_embeddings()` → `language_model.get_input_embeddings()` + `.float()` before `.numpy()` | janus.py |
| BLIP3o | 重写 draw() 用 UNet+VAE pipeline + 多图尺寸统一 | blip3o.py |
| Show-o2 | 修复 `model_dtype` 未定义 | showo2.py |
| JoyAI | `image=` → `images=` 参数名 | joyai.py, modeling_joyai_image.py |
| 全部 backend | understand() 支持多图（不再只读 images[0]） | latentum/janus/showo2.py |
| 全部 backend | draw() 提取 context images 用于 I2I | 5 个 backend |
| 全部 | external_draw.yaml 加载 + Track G→C-R/C-F/C-A + marker config + 图片路径防覆盖 | types.py, runner.py, 3 个 strategy |

---

## 2. 当前测试状态

### 2.1 Pre-flight 结果（external_draw）

| 模型 | external_draw | 备注 |
|---|---|---|
| bagel-7b | ✅ PASS | ~168s/sample |
| thinkmorph-7b | ✅ PASS | ~59s/sample |
| latentum-base | ✅ PASS | ~22s/sample |
| sensenova-u1-8b | ✅ PASS | ~15s/sample（修复黑图后） |
| blip3o-8b | ✅ PASS | ~9s/sample |
| show-o2-7b | ✅ PASS | ~17s/sample |
| janus-pro-7b | ❌ FAIL | 多图 processor shape mismatch |
| joyai-image | ❌ FAIL | 多图 understand tokens 不匹配 |

### 2.2 native_interleave 测试（进行中）

测试命令（已在后台运行）：
```bash
# U1 native_interleave on GPU 3
CUDA_VISIBLE_DEVICES=3 bash scripts/run_benchmark.sh sensenova-u1-8b --gpu 3 \
  --strategy native_interleave \
  --output-dir /tmp/test_u1_interleave \
  --views blank --tasks t1 --variants base/direct \
  --batch-size 1 --skip-preflight

# LatentUM native_interleave on GPU 2
CUDA_VISIBLE_DEVICES=2 bash scripts/run_benchmark.sh latentum-base --gpu 2 \
  --strategy native_interleave \
  --output-dir /tmp/test_latentum_interleave \
  --views blank --tasks t1 --variants base/direct \
  --batch-size 1 --skip-preflight
```

**LatentUM 初步结果：**
- 无错误，但 `draw_triggered: False`（没有触发图像生成）
- 可能原因：模型未在 interleave 训练中学会主动输出 `<img>` marker
- 需要检查：是否应该用 forced_interleave 而非 native_interleave

**U1 结果：**
- 还未产出（模型加载 + 推理时间较长，float32 比 bfloat16 慢）

### 2.3 检查结果的命令

```bash
# 检查 U1 interleave 结果
find /tmp/test_u1_interleave/ -name "direct.jsonl" | head -1 | xargs head -1 | python3 -c "
import sys,json
d=json.loads(sys.stdin.read())
print('error:', d.get('error','')[:200] if d.get('error') else 'NONE')
print('draw_triggered:', d.get('draw_triggered'))
print('prediction:', (d.get('prediction','') or '')[:200])
print('generated_images:', len(d.get('generated_images',[])))
print('track:', d.get('track',''))
"

# 检查 LatentUM interleave 结果
find /tmp/test_latentum_interleave/ -name "direct.jsonl" | head -1 | xargs head -1 | python3 -c "
import sys,json
d=json.loads(sys.stdin.read())
print('error:', d.get('error','')[:200] if d.get('error') else 'NONE')
print('draw_triggered:', d.get('draw_triggered'))
print('prediction:', (d.get('prediction','') or '')[:200])
print('generated_images:', len(d.get('generated_images',[])))
print('track:', d.get('track',''))
"
```

---

## 3. 后续 agent 需要做的事

### 3.1 验证 native_interleave

1. 检查 U1 和 LatentUM 的 interleave 测试结果（用上面的命令）
2. 如果 U1 的 `draw_triggered: True` 且 `generated_images` 非空 → 成功
3. 如果 `draw_triggered: False` → 模型未主动输出 `<img>` marker，可能需要：
   - 检查 system_prompt 是否正确
   - 考虑实现 `forced_interleave`（强制触发图像生成，不等 marker）
4. 检查生成图像是否全黑（用 PIL 检查 min/max pixel）

### 3.2 检查生成图像质量

```bash
python3 -c "
from PIL import Image; import numpy as np, os
d='/tmp/test_u1_interleave/SenseNova-U1-8B-MoT/native_interleave/generated'
for r,_,fs in os.walk(d):
  for f in sorted(fs)[:3]:
    if f.endswith('.png'):
      a=np.array(Image.open(os.path.join(r,f)))
      print(f'{f}: min={a.min()} max={a.max()}', 'OK ✅' if a.max()>0 else 'BLACK ❌')
"
```

### 3.3 如果 interleave 有问题

**U1 可能的问题：**
- flash_attn 已禁用（`_HAS_FLASH_ATTN = False`），但 `forward_und` 的 SDPA 可能有问题
- `interleave_gen` 中的 `append_image_to_cache` 可能需要适配
- dtype 问题：确保 float32 cast 在 `interleave()` 方法中（和 `draw()` 一样）

**LatentUM 可能的问题：**
- 模型可能未训练过主动输出 `<img>` marker → 考虑 forced_interleave
- KV cache 的 `deepcopy` 可能有问题（HF DynamicCache 的 deepcopy）
- `vision_token_mask` 的构造可能不正确

### 3.4 重新启动全量 external_draw

如果只是验证 interleave，external_draw 可以继续跑：

```bash
# 4 GPU external_draw（已验证通过）
bash scripts/run_gpu0_draw.sh &  # bagel-7b:external_draw
bash scripts/run_gpu1_draw.sh &  # thinkmorph-7b:external_draw
bash scripts/run_gpu2_draw.sh &  # latentum-base + show-o2:external_draw
bash scripts/run_gpu3_draw.sh &  # sensenova-u1-8b + blip3o:external_draw
```

### 3.5 还需要实现的

- **Bagel forced_interleave**：已有 `forced_interleave_inference` 在 `mapspatial/vendor/bagel_interleave/inferencer.py`
- **ThinkMorph native_interleave**：已有，使用 vendored InterleaveInferencer
- **Janus + JoyAI external_draw 修复**：多图 processor 兼容性问题

---

## 4. 关键文件索引

| 文件 | 内容 |
|---|---|
| `mapspatial/vendor/neo_chat/modeling_neo_chat.py` | U1 vendored 模型（含 interleave_gen, it2i_generate, _t2i_predict_v） |
| `mapspatial/vendor/bagel_interleave/inferencer.py` | Bagel interleave inferencer（含 forced_interleave_inference） |
| `mapspatial/backends/veomni/u1.py` | U1 backend（understand, draw, interleave） |
| `mapspatial/backends/veomni/latentum.py` | LatentUM backend（understand, draw, interleave） |
| `mapspatial/backends/veomni/bagel.py` | Bagel backend（understand, draw, forced_interleave, interleave） |
| `mapspatial/strategies/forced_interleave.py` | ForcedInterleaveStrategy |
| `mapspatial/strategies/native_interleave.py` | NativeInterleaveStrategy（含 PIL→Path 落盘） |
| `mapspatial/strategies/external_draw.py` | ExternalDrawStrategy |
| `mapspatial/types.py` | RunContext, _DRAW_INSTRUCTIONS, YAML 加载 |
| `mapspatial/runner.py` | runner（Track C-R/C-F/C-A, marker config） |
| `configs/strategies/external_draw.yaml` | 12 种 question_type 的 draw instruction |
| `configs/models/*.yaml` | 各模型配置 |
| `scripts/preflight_check.sh` | Pre-flight 检查脚本 |
| `scripts/run_gpu[0-3]_draw.sh` | 4 GPU 运行脚本 |

---

## 5. 约束

1. **GPU 限制**：测试只用 GPU 0/1/2/3（现在四张卡都可以用了）
2. **输出目录**：external_draw 结果在 `results_draw/`，interleave 测试在 `/tmp/`
3. **不破坏现有逻辑**：direct/oracle 已跑完，代码修改不能破坏
