#!/usr/bin/env bash
set -euo pipefail
MODELS=(glm-4-6v step3-vl-10b mimo-embodied-7b)
VIEWS="sat,wprd01"; TASKS="t1,t2"; VARIANTS="base/direct,base/oracle"
RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
for MODEL in "${MODELS[@]}"; do
    echo "===== [gpu0-rem] Running ${MODEL} ====="
    bash "${RUN_BENCH}" "$MODEL" --gpu 0 --views "$VIEWS" --tasks "$TASKS" --variants "$VARIANTS"
done
