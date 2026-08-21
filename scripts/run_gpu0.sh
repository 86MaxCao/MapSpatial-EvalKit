#!/usr/bin/env bash
# Inference on GPU 0. Edit the config below before each run.
set -euo pipefail

# ── Edit these before each run ─────────────────────────────────────────
MODELS=(                         # model configs: yaml name (configs/models/<name>.yaml) or full path
  "qwen3-vl-8b"                  # vLLM
  "qwen2.5-vl-7b"                # vLLM
  "qwen2-vl-7b"                  # vLLM
  "glm-4-6v"                     # vLLM (glm url-style, new)
  "step3-vl-10b"                 # vLLM (glm url-style, new)
  "mimo-embodied-7b"             # transformers
)
VIEWS="blank,sat,webrd04,wprd01"               # comma-separated tile types, e.g. sat,wprd01
TASKS="t1,t2"                    # comma-separated tasks, e.g. t1,t2
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
)
VARIANTS="$(IFS=,; echo "${VARIANTS[*]}")"  # join array into comma-string
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
