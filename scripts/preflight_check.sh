#!/usr/bin/env bash
# Pre-flight check: run 1 sample per model:strategy pair, verify no errors before full run.
set -euo pipefail

MAMBA_ROOT_PREFIX="${MAMBA_ROOT_PREFIX:-/mnt/nas-tbt/caoziqi/micromamba}"
MICROMAMBA_BIN="${MICROMAMBA_BIN:-${MAMBA_ROOT_PREFIX}/bin/micromamba}"
eval "$("${MICROMAMBA_BIN}" shell hook -s bash --root-prefix "${MAMBA_ROOT_PREFIX}")"
micromamba activate mapspatial
export CKPT_DIR="${CKPT_DIR:-/mnt/nas-tbt/tbt/checkpoint/hf_cache}"
export VLLM_WORKER_MULTIPROC_METHOD="${VLLM_WORKER_MULTIPROC_METHOD:-spawn}"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_DIR}"

DATA_ROOT="${DATA_ROOT:-/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data}"
INPUT_DIR="${INPUT_DIR:-${DATA_ROOT}/benchmark_jsonl}"
CHECK_DIR="/tmp/preflight_check"
RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"

check_gpu2() {
    local GPU=2
    local MODELS=(
        "bagel-7b:forced_interleave"
        "thinkmorph-7b:native_interleave"
        "latentum-base:external_draw"
        "janus-pro-7b:external_draw"
    )
    _run_checks "$GPU" "${MODELS[@]}"
}

check_gpu3() {
    local GPU=3
    local MODELS=(
        "sensenova-u1-8b:external_draw"
        "blip3o-8b:external_draw"
        "show-o2-7b:external_draw"
        "joyai-image:external_draw"
    )
    _run_checks "$GPU" "${MODELS[@]}"
}

_run_checks() {
    local GPU=$1; shift
    local MODELS=("$@")
    local ALL_PASS=true

    echo "=========================================="
    echo "  Pre-flight Check — GPU ${GPU}"
    echo "=========================================="

    for ENTRY in "${MODELS[@]}"; do
        local MODEL="${ENTRY%%:*}"
        local STRATEGY="${ENTRY##*:}"
        local CHECK_OUT="${CHECK_DIR}/gpu${GPU}/${MODEL}"

        echo ""
        echo "--- [GPU ${GPU}] ${MODEL} | ${STRATEGY} ---"

        # Clean old check results
        find "${CHECK_OUT}" -type f -delete 2>/dev/null || true

        # Run 1 sample with 300s timeout
        # run_benchmark.sh sets CUDA_VISIBLE_DEVICES via --gpu
        # stderr to file to avoid pipe blocking from tqdm output
        timeout 600 bash "${RUN_BENCH}" \
            "${MODEL}" \
            --gpu "${GPU}" \
            --strategy "${STRATEGY}" \
            --output-dir "${CHECK_OUT}" \
            --views blank \
            --tasks t1 \
            --variants base/direct \
            --batch-size 1 \
            --skip-preflight \
            2>/tmp/preflight_${GPU}_${MODEL}.err || true

        # Find JSONL (model name dir is unknown, use find)
        local JSONL=$(find "${CHECK_OUT}" -name "direct.jsonl" -path "*/blank/t1/*" 2>/dev/null | head -1)

        if [ -z "${JSONL}" ] || [ ! -f "${JSONL}" ]; then
            echo "  FAIL: no output file (timeout or crash)"
            ALL_PASS=false
            continue
        fi

        local LINES=$(wc -l < "${JSONL}")
        if [ "${LINES}" -eq 0 ]; then
            echo "  FAIL: empty output"
            ALL_PASS=false
            continue
        fi

        # Check first line for error
        local RESULT=$(python3 -c "
import json
with open('${JSONL}') as f:
    d = json.loads(f.readline())
e = d.get('error', '')
if e:
    print('ERROR:', e[:150])
else:
    print('OK:', (d.get('prediction','') or '')[:80], '| imgs:', len(d.get('generated_images',[])), '| track:', d.get('track',''))
" 2>/dev/null)

        if [[ "${RESULT}" == ERROR:* ]]; then
            echo "  FAIL: ${RESULT}"
            ALL_PASS=false
        else
            echo "  PASS: ${RESULT}"
        fi
    done

    echo ""
    if [ "${ALL_PASS}" = true ]; then
        echo ">>> GPU ${GPU}: ALL CHECKS PASSED <<<"
    else
        echo ">>> GPU ${GPU}: SOME CHECKS FAILED — review before full run <<<"
    fi
}

# ── Run checks ────────────────────────────────────────────────────────
echo "Starting pre-flight checks..."
echo "Each model:strategy pair will run 1 sample with 300s timeout."
echo ""

check_gpu2
echo ""
check_gpu3

echo ""
echo "=========================================="
echo "  Pre-flight check complete."
echo "  Only run full batch for models that PASSED above."
echo "=========================================="
