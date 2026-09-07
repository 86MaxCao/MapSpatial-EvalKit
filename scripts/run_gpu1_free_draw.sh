#!/usr/bin/env bash
# GPU 1 — autonomous G2U C-R (model chooses what to draw; U may ignore).
# Does not replay typed I0. Writes a new G image per sample.
# Default protocol matches previous C-R comparison: wprd01 t1-t4 base/direct.
set -euo pipefail

GPU="${GPU:-1}"
MODELS_CSV="${MODELS_CSV:-bagel-7b:external_draw,thinkmorph-7b:external_draw,latentum-base:external_draw,sensenova-u1-8b:external_draw}"
VIEWS="${VIEWS:-wprd01}"
TASKS="${TASKS:-t1,t2,t3,t4}"
VARIANTS="${VARIANTS:-base/direct}"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-${PROJECT_DIR}/results_free_draw}"
DATA_ROOT="${DATA_ROOT:-${PROJECT_DIR}/../SpatialIntelligence-gate2building/data}"
INPUT_DIR="${INPUT_DIR:-${DATA_ROOT}/benchmark_jsonl}"
RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
MAPSPATIAL_LIB="${MAMBA_ROOT_PREFIX:-/mnt/nas-tbt/caoziqi/micromamba}/envs/mapspatial/lib"
export LD_LIBRARY_PATH="${MAPSPATIAL_LIB}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
mkdir -p "${OUTPUT_DIR}/logs"

IFS=',' read -r -a ENTRIES <<< "${MODELS_CSV}"
for ENTRY in "${ENTRIES[@]}"; do
    MODEL="${ENTRY%%:*}"
    STRATEGY="${ENTRY##*:}"
    echo "===== [gpu${GPU}] ${MODEL} | ${STRATEGY} autonomous | views=${VIEWS} tasks=${TASKS} ====="
    env -u MODEL bash "${RUN_BENCH}" "$MODEL" \
        --gpu "${GPU}" \
        --strategy "$STRATEGY" \
        --output-dir "$OUTPUT_DIR" \
        --input-dir "$INPUT_DIR" \
        --data-dir "$DATA_ROOT" \
        --views "$VIEWS" \
        --tasks "$TASKS" \
        --variants "$VARIANTS" \
        --g2u-scratchpad autonomous \
        --skip-preflight
done
