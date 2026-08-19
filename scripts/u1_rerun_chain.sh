#!/usr/bin/env bash
# Wait for blip3o (PID 1284572) to finish, then rerun U1 on GPU3 with the fixed backend.
while kill -0 1284572 2>/dev/null; do sleep 30; done
echo "=== blip3o done, launching U1 rerun on GPU3 ==="
cd /home/ximeng.czq/caoziqi/code/SpatialIntelligence/MapSpatial-EvalKit
export MAMBA_ROOT_PREFIX=/mnt/nas-tbt/caoziqi/micromamba
eval "$(/mnt/nas-tbt/caoziqi/micromamba/bin/micromamba shell hook -s bash --root-prefix $MAMBA_ROOT_PREFIX)"
micromamba activate mapspatial
export CKPT_DIR=/mnt/nas-tbt/tbt/checkpoint/hf_cache
LOG=results/logs/u1_fixed_$(date +%Y%m%d_%H%M%S).log
bash scripts/run_benchmark.sh sensenova-u1-8b --gpu 3 --views wprd01 --tasks t1,t2 --variants base/direct > "$LOG" 2>&1
echo "U1 EXIT=$? LOG=$LOG"
for f in $(find results/SenseNova-U1-8B-MoT/direct/wprd01 -name '*.jsonl' 2>/dev/null); do
  echo "$(basename $(dirname $(dirname $f)))/$(basename $f): $(wc -l < $f) lines"
done
