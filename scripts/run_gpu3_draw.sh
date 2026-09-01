#!/usr/bin/env bash
# GPU 3 — Bagel T3 option-shuffle check (gold no longer pinned to A).
# Runs U-direct first, then image-first C-R, both on the derived jsonl.
# Does not write into results_draw_0827 or the original benchmark_jsonl.
set -euo pipefail

GPU=3
MODELS_CSV="${MODELS_CSV:-bagel-7b:direct,bagel-7b:external_draw}"
VIEWS="${VIEWS:-wprd01}"
TASKS="${TASKS:-t3}"
VARIANTS="${VARIANTS:-base/direct}"
DATA_ROOT="${DATA_ROOT:-/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data}"
INPUT_DIR="${INPUT_DIR:-${DATA_ROOT}/benchmark_jsonl_t3_optshuffle}"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-${PROJECT_DIR}/results_draw_0830_t3optshuffle}"
RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
MAPSPATIAL_LIB="${MAMBA_ROOT_PREFIX:-/mnt/nas-tbt/caoziqi/micromamba}/envs/mapspatial/lib"
export LD_LIBRARY_PATH="${MAPSPATIAL_LIB}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
mkdir -p "${OUTPUT_DIR}"

if [[ ! -f "${INPUT_DIR}/${VIEWS%%,*}/${TASKS%%,*}/${VARIANTS%%,*}.jsonl" ]]; then
    echo "===== [gpu${GPU}] building option-shuffled T3 jsonl → ${INPUT_DIR} ====="
    python "${PROJECT_DIR}/scripts/shuffle_t3_route_options.py" \
        --src-root "${DATA_ROOT}/benchmark_jsonl" \
        --dst-root "${INPUT_DIR}" \
        --views "${VIEWS}"
fi

IFS=',' read -r -a ENTRIES <<< "${MODELS_CSV}"
for ENTRY in "${ENTRIES[@]}"; do
    MODEL="${ENTRY%%:*}"
    STRATEGY="${ENTRY##*:}"
    echo "===== [gpu${GPU}] ${MODEL} | ${STRATEGY} | input=${INPUT_DIR} views=${VIEWS} tasks=${TASKS} ====="
    bash "${RUN_BENCH}" "$MODEL" \
        --gpu "${GPU}" \
        --strategy "$STRATEGY" \
        --input-dir "${INPUT_DIR}" \
        --data-dir "${DATA_ROOT}" \
        --output-dir "$OUTPUT_DIR" \
        --views "$VIEWS" \
        --tasks "$TASKS" \
        --variants "$VARIANTS" \
        --skip-preflight
done
