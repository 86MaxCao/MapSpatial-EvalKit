#!/usr/bin/env bash
# GPU 1 — U-replay into results_draw (reuse I0, skip G).
# Resume-by-id: already-written rows are skipped. Use after deleting a subset
# of direct.jsonl (e.g. the 7 shuffled types, or the complementary types).
set -euo pipefail

GPU="${GPU:-1}"
MODELS_CSV="${MODELS_CSV:-bagel-7b:external_draw,thinkmorph-7b:external_draw,latentum-base:external_draw,sensenova-u1-8b:external_draw}"
VIEWS="${VIEWS:-wprd01}"
TASKS="${TASKS:-t1,t2,t3,t4}"
VARIANTS="${VARIANTS:-base/direct}"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-${PROJECT_DIR}/results_draw}"
REPLAY_FROM="${REPLAY_FROM:-${OUTPUT_DIR}}"
DATA_ROOT="${DATA_ROOT:-${PROJECT_DIR}/../SpatialIntelligence-gate2building/data}"
INPUT_DIR="${INPUT_DIR:-${DATA_ROOT}/benchmark_jsonl}"
RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
MAPSPATIAL_LIB="${MAMBA_ROOT_PREFIX:-/mnt/nas-tbt/caoziqi/micromamba}/envs/mapspatial/lib"
export LD_LIBRARY_PATH="${MAPSPATIAL_LIB}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
mkdir -p "${OUTPUT_DIR}"

IFS=',' read -r -a ENTRIES <<< "${MODELS_CSV}"
for ENTRY in "${ENTRIES[@]}"; do
    MODEL="${ENTRY%%:*}"
    STRATEGY="${ENTRY##*:}"
    echo "===== [gpu${GPU}] ${MODEL} | ${STRATEGY} U-replay | views=${VIEWS} tasks=${TASKS} from=${REPLAY_FROM} ====="
    env -u MODEL bash "${RUN_BENCH}" "$MODEL" \
        --gpu "${GPU}" \
        --strategy "$STRATEGY" \
        --output-dir "$OUTPUT_DIR" \
        --input-dir "$INPUT_DIR" \
        --data-dir "$DATA_ROOT" \
        --views "$VIEWS" \
        --tasks "$TASKS" \
        --variants "$VARIANTS" \
        --replay-i0-from "$REPLAY_FROM" \
        --no-save-generated \
        --skip-preflight
done
