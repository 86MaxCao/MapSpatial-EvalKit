#!/usr/bin/env bash
# Inference on GPU 2 — visual thinking (generation-to-understanding) strategies.
# Each model entry uses "model_name:strategy" format.
set -euo pipefail

# ── Edit these before each run ─────────────────────────────────────────
MODELS=(                         # model:strategy pairs (pre-flight verified)
  "bagel-7b:forced_interleave"        # PASS — stateful forced, shared KV cache
  "bagel-7b:external_draw"            # PASS — restart baseline for comparison
  "thinkmorph-7b:native_interleave"   # PASS — autonomous, marker-driven
  "thinkmorph-7b:external_draw"       # PASS — restart baseline for comparison
  "latentum-base:external_draw"       # PASS — restart with I2I generation
  # "janus-pro-7b:external_draw"      # FAIL — multi-image processor shape mismatch
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
    echo "===== [gpu2] Running model: ${MODEL} | strategy: ${STRATEGY} ====="
    bash "${RUN_BENCH}" \
        "$MODEL" \
        --gpu 2 \
        --strategy "$STRATEGY" \
        --output-dir "$OUTPUT_DIR" \
        --views "$VIEWS" \
        --tasks "$TASKS" \
        --variants "$VARIANTS" \
        "$@"
done
