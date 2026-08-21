# AGENT.md — MapSpatial-EvalKit

## 绝对规则

1. **禁止删除或清空任何文件**，无论是否为 error 结果。需要为重跑腾位置时，用 `mv` 重命名为 `.backup` 后缀（如 `direct.jsonl` → `direct.jsonl.backup`），保留原数据可恢复。
2. **禁止绕过权限限制**：`rm` 被禁是有意为之，不得用 Python `open('w')`、`os.remove` 等方式绕过。
3. 修改任何结果文件前必须先问用户。

## 环境与运行

- Python 环境：`micromamba activate mapspatial`（`/mnt/nas-tbt/caoziqi/micromamba`）
- GPU 分配：只使用用户指定的 GPU，不碰其他卡
- 运行脚本时加 `OMP_NUM_THREADS=1`（容器 nproc/affinity 不匹配会导致 libgomp 死锁）
- 用 `setsid nohup ... < /dev/null &` 后台运行，脱离会话避免被中断杀掉
- `CKPT_DIR=/mnt/nas-tbt/tbt/checkpoint/hf_cache`

## transformers 5.8 兼容性问题

环境是 transformers 5.8.0 + torch 2.11.0，许多 vendored 模型代码是为 4.x 写的，有以下 breaking change：

| 问题 | 影响 | 修复 |
|------|------|------|
| `rope_scaling` → `rope_parameters` | cambrian (Qwen2) | 设 `config.rope_parameters = {"rope_type":"default","scaling_factor":1.0,"rope_theta":...}` |
| `embed_tokens` → `_input_embed_layer` | spatial-mllm (Qwen2_5_VL) | 用 `self.model.get_input_embeddings()` |
| `layer_types` 属性为 None | cambrian (Qwen2) | `config.layer_types = []` |
| `load_in_8bit` 参数移除 | sensenova internvl | 删掉该参数 |
| `all_tied_weights_keys` 重命名 | sensenova internvl | monkeypatch `get_total_byte_count` |
| `cache_position` 不再传给 prepare_inputs | spatial-mllm | 从 `model_inputs` 读回 |
| `mm_token_type_ids` 未消费 | spatial-mllm | generate 前 `batch.pop("mm_token_type_ids")` |
| **flash_attention_2 causal mask bug** | sensenova-1.5, latentum | **强制 LLM 用 `sdpa`**（见 `docs/latentum-transformers5-flash-attn-bug.md`） |

## vLLM 0.22 问题

- **CUDA graph 崩溃**：InternVL/ViLaSR 类模型开 CUDA graph 会让 EngineCore segfault。修复：`enforce_eager: true`（config yaml）或 `enforce_eager=True`（LLM() 调用）。
- **InternVL 路径→PIL**：vLLM 0.22 的 InternVLProcessor 不自动把文件路径转 PIL。`vllm.py` placeholder 风格里用 `load_image()` 加载 PIL。
- **ViLaSR 多轮累积**：多轮推理累积图片（最多 45 张/请求）可能超 max_model_len。三层防护：设 `max_model_len` + generate 前检查累积长度 + `try/except` 防 hang。

## 项目结构

```
configs/models/     # 模型 YAML 配置
mapspatial/backends/  # 后端（vllm, cambrian, sensenova_si, vilasr, spatial_mllm 等）
mapspatial/vendor/    # 第三方模型代码（vendored）
mapspatial/eval/       # 答案提取与判分（answer.py）
mapspatial/strategies/ # 推理策略（direct, external_draw）
scripts/              # 运行脚本（run_benchmark.sh, run_gpu{0,1,2,3}.sh）
results/              # 推理结果（JSONL + summary.json），不在 git 中
```

## 答案提取逻辑（answer.py）

- 优先级：`<answer>` tag → "ANSWER IS X" → "答案：X" → "is X" → 首字母单字母 → 选项文本匹配 → comma_multi（末尾逗号分隔多字母）→ last_letter（fallback）
- `comma_multi`：响应末尾有逗号分隔字母（如 "A, C"）→ 提取为多选 "A,C"，单选题判错
- `valid_set` 默认 A-F（选项最多到 F）
