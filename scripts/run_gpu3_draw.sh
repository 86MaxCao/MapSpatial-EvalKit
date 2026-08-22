#!/usr/bin/env bash
# Inference on GPU 3 — visual thinking (generation-to-understanding) strategies.
# Each model entry uses "model_name:strategy" format.
set -euo pipefail

# ── Edit these before each run ─────────────────────────────────────────
MODELS=(                         # model:strategy pairs
  "sensenova-u1-8b:external_draw"     # stateful loop not yet ported → restart
  "blip3o-8b:external_draw"           # no shared cache → restart
  "show-o2-7b:external_draw"          # no shared cache → restart
  "joyai-image:external_draw"         # no shared cache → restart
)
VIEWS="blank,sat,webrd04,wprd01"
TASKS="t1,t2"
VARIANTS="base/direct,base/oracle"
# ────────────────────────────────────────────────────────────────────────

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-${PROJECT_DIR}/results_draw}"
RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"

for ENTRY in "${MODELS[@]}"; do
    MODEL="${ENTRY%%:*}"
    STRATEGY="${ENTRY##*:}"
    echo "===== [gpu3] Running model: ${MODEL} | strategy: ${STRATEGY} ====="
    bash "${RUN_BENCH}" \
        "$MODEL" \
        --gpu 3 \
        --strategy "$STRATEGY" \
        --output-dir "$OUTPUT_DIR" \
        --views "$VIEWS" \
        --tasks "$TASKS" \
        --variants "$VARIANTS" \
        "$@"
done
