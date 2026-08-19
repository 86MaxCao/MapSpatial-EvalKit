#!/usr/bin/env bash
# Inference on GPU 0. Edit the config below before each run.
set -euo pipefail

# ── Edit these before each run ─────────────────────────────────────────
MODELS=(                         # model configs: yaml name (configs/models/<name>.yaml) or full path
  "qwen3-vl-2b"                  # vLLM
  "qwen2.5-vl-7b"                # vLLM
  "qwen2-vl-7b"                  # vLLM
  "glm-4-6v"                     # vLLM (glm url-style, new)
  "step3-vl-10b"                 # vLLM (glm url-style, new)
  "mimo-embodied-7b"             # transformers
)
VIEWS="sat,wprd01"               # comma-separated tile types, e.g. sat,wprd01
TASKS="t1,t2"                    # comma-separated tasks, e.g. t1,t2
VARIANTS="base/direct,base/oracle"  # comma-separated variants, e.g. base/direct,transform/rot90/direct
# ────────────────────────────────────────────────────────────────────────

RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
for MODEL in "${MODELS[@]}"; do
    echo "===== [gpu0] Running model: ${MODEL} ====="
    bash "${RUN_BENCH}" \
        "$MODEL" \
        --gpu 0 \
        --views "$VIEWS" \
        --tasks "$TASKS" \
        --variants "$VARIANTS" \
        "$@"
done
