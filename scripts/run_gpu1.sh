#!/usr/bin/env bash
# Inference on GPU 1. Edit the config below before each run.
set -euo pipefail

# ── Edit these before each run ─────────────────────────────────────────
MODELS=(                         # model configs: yaml name (configs/models/<name>.yaml) or full path
  "internvl3-8b"                 # vLLM
  "internvl3-5-8b"               # vLLM
  "vilasr"                       # vilasr backend
  "sensenova-si-1.3-qwen3-vl-8b" # sensenova_si backend
  "sensenova-si-1.5-internvl3-8b"  # sensenova_si backend
  "cambrian-s-7b"                # cambrian backend
  "spatial-mllm"                 # spatial_mllm backend
)
VIEWS="sat,wprd01"               # comma-separated tile types, e.g. sat,wprd01
TASKS="t1,t2"                    # comma-separated tasks, e.g. t1,t2
VARIANTS="base/direct,base/oracle"  # comma-separated variants, e.g. base/direct,transform/rot90/direct
# ────────────────────────────────────────────────────────────────────────

RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
for MODEL in "${MODELS[@]}"; do
    echo "===== [gpu1] Running model: ${MODEL} ====="
    bash "${RUN_BENCH}" \
        "$MODEL" \
        --gpu 1 \
        --views "$VIEWS" \
        --tasks "$TASKS" \
        --variants "$VARIANTS" \
        "$@"
done
