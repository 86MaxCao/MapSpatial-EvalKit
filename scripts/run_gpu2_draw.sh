#!/usr/bin/env bash
# GPU 2 — ThinkMorph image-first C-R on wprd01 t4.
set -euo pipefail

GPU=2
MODELS_CSV="${MODELS_CSV:-thinkmorph-7b:external_draw}"
VIEWS="${VIEWS:-wprd01}"
TASKS="${TASKS:-t4}"
VARIANTS="${VARIANTS:-base/direct}"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-${PROJECT_DIR}/results_draw_0830}"
RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
MAPSPATIAL_LIB="${MAMBA_ROOT_PREFIX:-/mnt/nas-tbt/caoziqi/micromamba}/envs/mapspatial/lib"
export LD_LIBRARY_PATH="${MAPSPATIAL_LIB}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
mkdir -p "${OUTPUT_DIR}"

IFS=',' read -r -a ENTRIES <<< "${MODELS_CSV}"
for ENTRY in "${ENTRIES[@]}"; do
    MODEL="${ENTRY%%:*}"
    STRATEGY="${ENTRY##*:}"
    echo "===== [gpu${GPU}] ${MODEL} | ${STRATEGY} | views=${VIEWS} tasks=${TASKS} variants=${VARIANTS} ====="
    bash "${RUN_BENCH}" "$MODEL" \
        --gpu "${GPU}" \
        --strategy "$STRATEGY" \
        --output-dir "$OUTPUT_DIR" \
        --views "$VIEWS" \
        --tasks "$TASKS" \
        --variants "$VARIANTS" \
        --skip-preflight
done
