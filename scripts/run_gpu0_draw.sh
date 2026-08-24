#!/usr/bin/env bash
# GPU 0 — external_draw models (prioritized)
set -euo pipefail
MODELS=( "bagel-7b:external_draw" )
VIEWS="blank,sat,webrd04,wprd01"
TASKS="t1,t2"
VARIANTS="base/direct"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-${PROJECT_DIR}/results_draw}"
RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
for ENTRY in "${MODELS[@]}"; do
    MODEL="${ENTRY%%:*}"; STRATEGY="${ENTRY##*:}"
    echo "===== [gpu0] ${MODEL} | ${STRATEGY} ====="
    bash "${RUN_BENCH}" "$MODEL" --gpu 0 --strategy "$STRATEGY" --output-dir "$OUTPUT_DIR" --views "$VIEWS" --tasks "$TASKS" --variants "$VARIANTS" "$@"
done
