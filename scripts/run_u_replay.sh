#!/usr/bin/env bash
# U-only external_draw: reuse saved I0, skip G. wprd01 t1/t2/t4 + shuffled t3.
set -euo pipefail

GPU="${GPU:?set GPU}"
MS_MODEL="${MODEL:?set MODEL (configs/models stem)}"
REPLAY_FROM="${REPLAY_FROM:?set REPLAY_FROM to the previous result root}"
VIEWS="${VIEWS:-wprd01}"
VARIANTS="${VARIANTS:-base/direct}"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-${PROJECT_DIR}/results_draw_0831_u}"
DATA_ROOT="${DATA_ROOT:-${PROJECT_DIR}/../SpatialIntelligence-gate2building/data}"
INPUT_MAIN="${INPUT_DIR:-${DATA_ROOT}/benchmark_jsonl}"
INPUT_T3="${T3_INPUT_DIR:-${DATA_ROOT}/benchmark_jsonl_t3_optshuffle}"
RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
MAPSPATIAL_LIB="${MAMBA_ROOT_PREFIX:-/mnt/nas-tbt/caoziqi/micromamba}/envs/mapspatial/lib"
export LD_LIBRARY_PATH="${MAPSPATIAL_LIB}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
mkdir -p "${OUTPUT_DIR}"

run_cell() {
    local tasks="$1"
    local input="$2"
    echo "===== [gpu${GPU}] ${MS_MODEL} U-replay | views=${VIEWS} tasks=${tasks} input=${input} from=${REPLAY_FROM} ====="
    env -u MODEL bash "${RUN_BENCH}" "$MS_MODEL" \
        --gpu "${GPU}" \
        --strategy external_draw \
        --output-dir "$OUTPUT_DIR" \
        --input-dir "$input" \
        --data-dir "$DATA_ROOT" \
        --views "$VIEWS" \
        --tasks "$tasks" \
        --variants "$VARIANTS" \
        --replay-i0-from "$REPLAY_FROM" \
        --no-save-generated \
        --skip-preflight
}

run_cell "t1,t2,t4" "${INPUT_MAIN}"
run_cell "t3" "${INPUT_T3}"
