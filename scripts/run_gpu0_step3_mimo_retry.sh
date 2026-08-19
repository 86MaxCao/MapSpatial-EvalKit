#!/usr/bin/env bash
# Auto-retry wrapper: GPU 0 on this shared machine keeps killing vLLM
# EngineCore mid-run. Resume logic skips already-finished combos, so each
# retry picks up where it left off.
set -uo pipefail   # no -e: we want to retry on failure
MODELS=(step3-vl-10b mimo-embodied-7b)
VIEWS="sat,wprd01"; TASKS="t1,t2"; VARIANTS="base/direct,base/oracle"
RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"
MAX_TRIES=10
for MODEL in "${MODELS[@]}"; do
    echo "===== [gpu0] Starting ${MODEL} (retry up to ${MAX_TRIES}) ====="
    for try in $(seq 1 ${MAX_TRIES}); do
        echo "----- ${MODEL} attempt ${try} @ $(date +%T) -----"
        # Kill any leftover EngineCore/orphans before retry
        pkill -9 -f "VLLM::EngineCore" 2>/dev/null || true
        pkill -9 -f "mapspatial.cli.*${MODEL}" 2>/dev/null || true
        sleep 3
        if bash "${RUN_BENCH}" "$MODEL" --gpu 0 --views "$VIEWS" --tasks "$TASKS" --variants "$VARIANTS"; then
            echo "===== ${MODEL} completed cleanly on attempt ${try} ====="
            break
        else
            echo "===== ${MODEL} attempt ${try} failed/killed, will retry ====="
            sleep 5
        fi
    done
done
echo "=== ALL DONE ==="
