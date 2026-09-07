#!/usr/bin/env bash
# Inference on GPU 3 for the numbered-marker parallel of paper-v8.
# Images and prompts come from bench_with_number; do not point this at
# the original benchmark_jsonl or mix results into results/.
set -euo pipefail

# ── Edit these before each run ─────────────────────────────────────────
MODELS=(                         # model configs: yaml name (configs/models/<name>.yaml) or full path
  "sensenova-u1-8b"                # VeOmni unified
  "blip3o-8b"                      # VeOmni unified
  "show-o2-7b"                     # VeOmni unified
  "joyai-image"                    # VeOmni unified
  "cambrian-s-7b"                  # cambrian backend
  "spatial-mllm"                   # spatial_mllm backend
  "sensenova-si-1.3-qwen3-vl-8b"   # sensenova_si backend
  "sensenova-si-1.5-internvl3-8b"  # sensenova_si backend
  "internvl3-8b"                     # vLLM
  "internvl3-5-8b"                   # vLLM
)
DATA_ROOT="/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data"
INPUT_DIR="${DATA_ROOT}/bench_with_number/jsonl"
# Keep data-dir at gate2building/data — jsonl image paths are
# bench_with_number/t{1,2,3,4}/..., resolved as ${DATA_ROOT}/<rel>.
OUTPUT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/results_number"
VIEWS="blank,sat,webrd04,wprd01"
TASKS="t1,t2,t3,t4"
# Numbered export is base + world only (no transform jsonl / images).
VARIANTS=(
  "base/direct"
  "base/oracle"
  "world/intervention_001/direct"
  "world/intervention_001/oracle"
  "world/sham_001/direct"
  "world/sham_001/oracle"
)
VARIANTS="$(IFS=,; echo "${VARIANTS[*]}")"
# ────────────────────────────────────────────────────────────────────────

RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
for MODEL in "${MODELS[@]}"; do
    echo "===== [gpu3-number] Running model: ${MODEL} ====="
    bash "${RUN_BENCH}" \
        "$MODEL" \
        --gpu 3 \
        --data-dir "$DATA_ROOT" \
        --input-dir "$INPUT_DIR" \
        --output-dir "$OUTPUT_DIR" \
        --views "$VIEWS" \
        --tasks "$TASKS" \
        --variants "$VARIANTS" \
        "$@"
done
