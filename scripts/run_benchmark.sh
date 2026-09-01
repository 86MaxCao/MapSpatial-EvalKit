#!/usr/bin/env bash
# Local inference runner for MapSpatial-EvalKit.
#
# Usage:
#   bash scripts/run_benchmark.sh configs/models/qwen3-vl-8b.yaml
#   bash scripts/run_benchmark.sh configs/models/qwen3-vl-8b.yaml --gpu 0 --views sat --tasks t1 --variants base/direct
#
# Extra args after the options below are passed through to `mapspatial run`
# (e.g. --store-question --batch-size 8 --skip-preflight).

set -euo pipefail

# ── Environment ────────────────────────────────────────────────────────
MAMBA_ROOT_PREFIX="${MAMBA_ROOT_PREFIX:-/mnt/nas-tbt/caoziqi/micromamba}"
MICROMAMBA_BIN="${MICROMAMBA_BIN:-${MAMBA_ROOT_PREFIX}/bin/micromamba}"
eval "$("${MICROMAMBA_BIN}" shell hook -s bash --root-prefix "${MAMBA_ROOT_PREFIX}")"
micromamba activate mapspatial

# Checkpoint root for ${CKPT_DIR} references in configs/models/*.yaml
export CKPT_DIR="${CKPT_DIR:-/mnt/nas-tbt/tbt/checkpoint/hf_cache}"

# Force spawn for vLLM EngineCore: fork deadlocks for models that init CUDA in
# the parent (e.g. GLM-4.6V-Flash via trust_remote_code), hanging at
# InputBatch torch.zeros. Safe for all models; only slightly slower startup.
export VLLM_WORKER_MULTIPROC_METHOD="${VLLM_WORKER_MULTIPROC_METHOD:-spawn}"

# ── Defaults (override via env or flags) ───────────────────────────────
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODEL="${MODEL:-}"
STRATEGY="${STRATEGY:-direct}"
GPU="${GPU:-0}"
DATA_ROOT="${DATA_ROOT:-/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data}"
INPUT_DIR="${INPUT_DIR:-${DATA_ROOT}/benchmark_jsonl}"
OUTPUT_DIR="${OUTPUT_DIR:-${PROJECT_DIR}/results}"
VIEWS="${VIEWS:-blank,sat,webrd04,wprd01}"
TASKS="${TASKS:-t1,t2}"
# All 16 variant combos of the paper-v8 layout (base + 7 transforms × direct/oracle)
VARIANTS="${VARIANTS:-base/direct,base/oracle,transform/rot90/direct,transform/rot90/oracle,transform/rot180/direct,transform/rot180/oracle,transform/rot270/direct,transform/rot270/oracle,transform/mirror_h/direct,transform/mirror_h/oracle,transform/mirror_h_rot90/direct,transform/mirror_h_rot90/oracle,transform/mirror_h_rot180/direct,transform/mirror_h_rot180/oracle,transform/mirror_h_rot270/direct,transform/mirror_h_rot270/oracle}"

# ── Parse args ─────────────────────────────────────────────────────────
EXTRA=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --gpu)        GPU="$2"; shift 2 ;;
        --strategy)   STRATEGY="$2"; shift 2 ;;
        --input-dir)  INPUT_DIR="$2"; shift 2 ;;
        --data-dir)   DATA_ROOT="$2"; shift 2 ;;
        --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
        --views)      VIEWS="$2"; shift 2 ;;
        --tasks)      TASKS="$2"; shift 2 ;;
        --variants)   VARIANTS="$2"; shift 2 ;;
        --replay-i0-from) EXTRA+=("$1" "$2"); shift 2 ;;
        -*)           EXTRA+=("$1"); shift ;;
        *)
            if [[ -z "$MODEL" ]]; then
                MODEL="$1"
            elif [[ "$1" != "$MODEL" && "$1" != "configs/models/${MODEL}.yaml" ]]; then
                EXTRA+=("$1")
            fi
            shift
            ;;
    esac
done

if [[ -z "$MODEL" ]]; then
    echo "Usage: $0 <model-config.yaml> [--gpu N|N,N,...] [--strategy direct] ..." >&2
    exit 1
fi

MODEL_PATH="$MODEL"
[[ "$MODEL" = /* || "$MODEL" = configs/* ]] || MODEL_PATH="configs/models/${MODEL}.yaml"

echo "Model:      ${MODEL_PATH}"
echo "Strategy:   ${STRATEGY}"
echo "GPUs:       ${GPU}"
echo "Input:      ${INPUT_DIR}"
echo "Data root:  ${DATA_ROOT}"
echo "Output:     ${OUTPUT_DIR}"
echo "Views:      ${VIEWS}"
echo "Tasks:      ${TASKS}"
echo "Variants:   ${VARIANTS}"

RUN_ARGS=(
    run
    --model "${MODEL_PATH}"
    --strategy "${STRATEGY}"
    --input-dir "${INPUT_DIR}"
    --data-dir "${DATA_ROOT}"
    --output-dir "${OUTPUT_DIR}"
    --views "${VIEWS}"
    --tasks "${TASKS}"
    --variants "${VARIANTS}"
)
[[ ${#EXTRA[@]} -gt 0 ]] && RUN_ARGS+=("${EXTRA[@]}")

cd "${PROJECT_DIR}"

NGPU=$(awk -F',' '{print NF}' <<< "${GPU}")
if [[ "${NGPU}" -gt 1 ]]; then
    echo "ERROR: only single-GPU is supported, got --gpu ${GPU}" >&2
    exit 1
fi

CUDA_VISIBLE_DEVICES="${GPU}" python -m mapspatial.cli "${RUN_ARGS[@]}"
