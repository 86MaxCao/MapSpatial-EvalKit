#!/usr/bin/env bash
# GPU 3 — external_draw models
set -euo pipefail
MODELS=( "sensenova-u1-8b:external_draw" "blip3o-8b:external_draw" )
VIEWS="blank,sat,webrd04,wprd01"
TASKS="t1,t2"d d
VARIANTS="base/direct"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-${PROJECT_DIR}/results_draw}"
RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
for ENTRY in "${MODELS[@]}"; do
    MODEL="${ENTRY%%:*}"; STRATEGY="${ENTRY##*:}"
    echo "===== [gpu3] ${MODEL} | ${STRATEGY} ====="
    bash "${RUN_BENCH}" "$MODEL" --gpu 3 --strategy "$STRATEGY" --output-dir "$OUTPUT_DIR" --views "$VIEWS" --tasks "$TASKS" --variants "$VARIANTS" "$@"
done
