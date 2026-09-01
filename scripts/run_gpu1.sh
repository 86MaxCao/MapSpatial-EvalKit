#!/usr/bin/env bash
# Inference on GPU 1. Edit the config below before each run.
set -euo pipefail

# ── Edit these before each run ─────────────────────────────────────────
MODELS=(                         # model configs: yaml name (configs/models/<name>.yaml) or full path
  # "internvl3-8b"                   # vLLM
  # "internvl3-5-8b"                 # vLLM
  "vilasr"                           # vilasr backend
  # "sensenova-si-1.3-qwen3-vl-8b"   # sensenova_si backend
  # "sensenova-si-1.5-internvl3-8b"  # sensenova_si backend
  # "cambrian-s-7b"                  # cambrian backend
  # "spatial-mllm"                   # spatial_mllm backend
)
INPUT_DIR="/home/ximeng.czq/caoziqi/code/SpatialIntelligence/SpatialIntelligence-gate2building/data/benchmark_jsonl"  # input jsonl dir
VIEWS="blank,sat,webrd04,wprd01"               # comma-separated tile types, e.g. sat,wprd01
TASKS="t3,t1,t2"                    # comma-separated tasks, e.g. t1,t2
VARIANTS=(                       # paper-v8 layout: base + 7 transforms × direct/oracle
  "base/direct"
  "base/oracle"
  "transform/rot90/direct"
  "transform/rot90/oracle"
  "transform/rot180/direct"
  "transform/rot180/oracle"
  "transform/rot270/direct"
  "transform/rot270/oracle"
  "transform/mirror_h/direct"
  "transform/mirror_h/oracle"
  "transform/mirror_h_rot90/direct"
  "transform/mirror_h_rot90/oracle"
  "transform/mirror_h_rot180/direct"
  "transform/mirror_h_rot180/oracle"
  "transform/mirror_h_rot270/direct"
  "transform/mirror_h_rot270/oracle"
  "world/intervention_001/direct"
  "world/intervention_001/oracle"
  "world/sham_001/direct"
  "world/sham_001/oracle"
)
VARIANTS="$(IFS=,; echo "${VARIANTS[*]}")"  # join array into comma-string
# ────────────────────────────────────────────────────────────────────────

RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
for MODEL in "${MODELS[@]}"; do
    echo "===== [gpu1] Running model: ${MODEL} ====="
    bash "${RUN_BENCH}" \
        "$MODEL" \
        --gpu 1 \
        --input-dir "$INPUT_DIR" \
        --views "$VIEWS" \
        --tasks "$TASKS" \
        --variants "$VARIANTS" \
        "$@"
done
