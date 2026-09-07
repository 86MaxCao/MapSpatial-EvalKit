#!/usr/bin/env bash
# Inference on GPU 0 against the HuggingFace pack (--layout hf).
# Edit the config below before each run. Do not point this at benchmark_jsonl.
set -euo pipefail

# ── Edit these before each run ─────────────────────────────────────────
MODELS=(                         # model configs: yaml name (configs/models/<name>.yaml) or full path
  "qwen3-vl-8b"                  # vLLM
  # "qwen2.5-vl-7b"                # vLLM
  # "qwen2-vl-7b"                  # vLLM
  # "glm-4-6v"                     # vLLM (glm url-style, new)
  # "step3-vl-10b"                 # vLLM (glm url-style, new)
  # "mimo-embodied-7b"             # transformers
  # "vilasr"
)
# HF repo root: contains data/*.jsonl and images/
INPUT_DIR="/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data/for_upload/20260904_internal"
DATA_DIR="${INPUT_DIR}"           # image paths are images/t1/... relative to this root
OUTPUT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/results_hf"
# sat has base+transform for t1/t2 and base+transform+world for t3/t4
# (blank has no t3/t4; webrd04 has no transform; t1/t2 have no world)
VIEWS="sat"
TASKS="t1,t2,t3,t4"
VARIANTS=(
  "base/direct"
  "transform/rot90/direct"
  "world/intervention_001/direct"
)
VARIANTS="$(IFS=,; echo "${VARIANTS[*]}")"  # join array into comma-string
# ────────────────────────────────────────────────────────────────────────

RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
for MODEL in "${MODELS[@]}"; do
    echo "===== [gpu0 hf] Running model: ${MODEL} ====="
    bash "${RUN_BENCH}" \
        "$MODEL" \
        --gpu 0 \
        --layout hf \
        --input-dir "$INPUT_DIR" \
        --data-dir "$DATA_DIR" \
        --output-dir "$OUTPUT_DIR" \
        --views "$VIEWS" \
        --tasks "$TASKS" \
        --variants "$VARIANTS" \
        "$@"
done
