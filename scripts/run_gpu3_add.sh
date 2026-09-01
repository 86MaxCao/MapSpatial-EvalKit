#!/usr/bin/env bash
# GPU 3: resume T2 oracle for nearest_point / directional_nearest_point.
# Writes into results/. Euclidean/network oracle ids are already present, so
# the runner skips them and only fills the two deleted subtasks.
set -euo pipefail

# ── Edit these before each run ─────────────────────────────────────────
MODELS=(                           # model configs: yaml name (configs/models/<name>.yaml) or full path
  "qwen3-vl-8b"                    # vLLM
  "qwen2.5-vl-7b"                  # vLLM
  "qwen2-vl-7b"                    # vLLM
  "glm-4-6v"                       # vLLM (glm url-style, new)
  "step3-vl-10b"                   # vLLM (glm url-style, new)
  "mimo-embodied-7b"               # transformers
  "sensenova-si-1.3-qwen3-vl-8b"   # sensenova_si backend
  "sensenova-si-1.5-internvl3-8b"  # sensenova_si backend
  "cambrian-s-7b"                  # cambrian backend
  "spatial-mllm"                   # spatial_mllm backend
  "bagel-7b"                       # VeOmni unified
  "thinkmorph-7b"                  # VeOmni unified
  "latentum-base"                  # VeOmni unified
  "janus-pro-7b"                   # VeOmni unified
  "sensenova-u1-8b"                # VeOmni unified
  "blip3o-8b"                      # VeOmni unified
  "show-o2-7b"                     # VeOmni unified
  "joyai-image"                    # VeOmni unified
  "internvl3-8b"                   # vLLM
  "internvl3-5-8b"                 # vLLM
  "vilasr"                         # vilasr backend
)
INPUT_DIR="/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data/benchmark_jsonl"  # input jsonl dir
VIEWS="blank,sat,webrd04,wprd01"                        # comma-separated tile types, e.g. sat,wprd01
TASKS="t2"                         # comma-separated tasks, e.g. t1,t2
VARIANTS=(                       # T2 oracle only; Direct unchanged
  "base/oracle"
  "transform/rot90/oracle"
  "transform/rot180/oracle"
  "transform/rot270/oracle"
  "transform/mirror_h/oracle"
  "transform/mirror_h_rot90/oracle"
  "transform/mirror_h_rot180/oracle"
  "transform/mirror_h_rot270/oracle"
)
VARIANTS="$(IFS=,; echo "${VARIANTS[*]}")"  # join array into comma-string
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-${PROJECT_DIR}/results}"
# Bagel/transformers import scipy HiGHS, which needs conda's newer libstdc++.
MAPSPATIAL_LIB="${MAMBA_ROOT_PREFIX:-/mnt/nas-tbt/caoziqi/micromamba}/envs/mapspatial/lib"
export LD_LIBRARY_PATH="${MAPSPATIAL_LIB}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
# ────────────────────────────────────────────────────────────────────────

RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
for MODEL in "${MODELS[@]}"; do
    echo "===== [gpu3] Running model: ${MODEL} ====="
    echo "===== [gpu3] Output: ${OUTPUT_DIR} ====="
    bash "${RUN_BENCH}" \
        "$MODEL" \
        --gpu 3 \
        --input-dir "$INPUT_DIR" \
        --output-dir "$OUTPUT_DIR" \
        --views "$VIEWS" \
        --tasks "$TASKS" \
        --variants "$VARIANTS" \
        "$@"
done
