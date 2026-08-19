#!/usr/bin/env bash
# Inference on GPU 3. Edit the config below before each run.
set -euo pipefail

# ── Edit these before each run ─────────────────────────────────────────
MODELS=(                         # model configs: yaml name (configs/models/<name>.yaml) or full path
  "sensenova-u1-8b"              # VeOmni unified
  "blip3o-8b"                    # VeOmni unified
  "show-o2-7b"                   # VeOmni unified
  "joyai-image"                  # VeOmni unified
)
# VIEWS="sat,wprd01"                  # comma-separated tile types, e.g. sat,wprd01
# TASKS="t1,t2"                       # comma-separated tasks, e.g. t1,t2
# VARIANTS="base/direct,base/oracle"  # comma-separated variants, e.g. base/direct,transform/rot90/direct
VIEWS="wprd01"                        # comma-separated tile types, e.g. sat,wprd01
TASKS="t1,t2"                         # comma-separated tasks, e.g. t1,t2
VARIANTS="base/direct"                # comma-separated variants, e.g. base/direct,transform/rot90/direct
# ────────────────────────────────────────────────────────────────────────

RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
for MODEL in "${MODELS[@]}"; do
    echo "===== [gpu3] Running model: ${MODEL} ====="
    bash "${RUN_BENCH}" \
        "$MODEL" \
        --gpu 3 \
        --views "$VIEWS" \
        --tasks "$TASKS" \
        --variants "$VARIANTS" \
        "$@"
done
