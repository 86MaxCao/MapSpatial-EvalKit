#!/usr/bin/env bash
# GPU 2 only — image-first G2U.
# C-F: Bagel / ThinkMorph / LatentUM / U1 forced_interleave
# C-R: all UMM with draw (optional)
#
# Full C-F (blank first, then other views):
#   PHASE=cf MAX_SAMPLES= TASKS=t1,t2,t3,t4 VARIANTS=base/direct \
#     VIEW_STAGES="blank;sat,webrd04,wprd01" \
#     OUTPUT_DIR=.../results_draw_0827 \
#     bash scripts/run_gpu2_draw.sh
#
# Smoke still works with defaults (6 samples, blank/t1, g2u_verify).
set -euo pipefail

PHASE="${PHASE:-all}"   # cf | cr | all
CF_MODELS=(
    "bagel-7b:forced_interleave"
    "thinkmorph-7b:forced_interleave"
    "latentum-base:forced_interleave"
    "sensenova-u1-8b:forced_interleave"
)
CR_MODELS=(
    "bagel-7b:external_draw"
    "thinkmorph-7b:external_draw"
    "latentum-base:external_draw"
    "sensenova-u1-8b:external_draw"
    "janus-pro-7b:external_draw"
    "show-o2-7b:external_draw"
    "blip3o-8b:external_draw"
    "joyai-image:external_draw"
)
if [[ -n "${MODELS_CSV:-}" ]]; then
    IFS=',' read -r -a _MODELS <<< "${MODELS_CSV}"
    if [[ "${PHASE}" == "cr" ]]; then
        CR_MODELS=("${_MODELS[@]}")
    elif [[ "${PHASE}" == "cf" ]]; then
        CF_MODELS=("${_MODELS[@]}")
    else
        CF_MODELS=("${_MODELS[@]}")
        CR_MODELS=()
    fi
fi

VIEWS="${VIEWS:-blank}"
TASKS="${TASKS:-t1}"
VARIANTS="${VARIANTS:-base/direct}"
# Unset or empty MAX_SAMPLES → full split (no --max-samples).
# Default 6 only when MAX_SAMPLES is unset (smoke).
if [[ -z "${MAX_SAMPLES+x}" ]]; then
    MAX_SAMPLES=6
fi
# fail | warn | off
SANITY="${SANITY:-fail}"
# Semicolon-separated view groups, run in order (finish one group for all
# models before the next). Empty → use VIEWS once.
VIEW_STAGES="${VIEW_STAGES:-}"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-${PROJECT_DIR}/results_draw/g2u_verify}"
RUN_BENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_benchmark.sh"

MAPSPATIAL_LIB="${MAMBA_ROOT_PREFIX:-/mnt/nas-tbt/caoziqi/micromamba}/envs/mapspatial/lib"
export LD_LIBRARY_PATH="${MAPSPATIAL_LIB}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"

mkdir -p "${OUTPUT_DIR}"

run_one() {
    local ENTRY="$1"
    local MODEL="${ENTRY%%:*}"
    local STRATEGY="${ENTRY##*:}"
    echo "===== [gpu2] ${MODEL} | ${STRATEGY} | views=${VIEWS} tasks=${TASKS} variants=${VARIANTS} ====="
    local extra=()
    if [[ -n "${MAX_SAMPLES}" ]]; then
        extra+=(--max-samples "${MAX_SAMPLES}")
    fi
    bash "${RUN_BENCH}" "$MODEL" \
        --gpu 2 \
        --strategy "$STRATEGY" \
        --output-dir "$OUTPUT_DIR" \
        --views "$VIEWS" \
        --tasks "$TASKS" \
        --variants "$VARIANTS" \
        --skip-preflight \
        "${extra[@]}"
}

sanity() {
    local FILTER="${1:-}"
    if [[ "${SANITY}" == "off" ]]; then
        echo "===== [gpu2] sanity skipped (SANITY=off) ====="
        return 0
    fi
    echo "===== [gpu2] sanity check filter=${FILTER:-all} mode=${SANITY} ====="
    set +e
    python - "${OUTPUT_DIR}" "${FILTER}" <<'PY'
import json, sys, statistics
from pathlib import Path
from PIL import Image

root = Path(sys.argv[1])
filt = (sys.argv[2] or "").strip()
jsonls = sorted(root.rglob("*.jsonl"))
if filt:
    jsonls = [p for p in jsonls if filt in str(p)]
if not jsonls:
    print(f"FAIL: no jsonl under {root} filter={filt!r}", file=sys.stderr)
    sys.exit(1)

errors = []
n_ok = n_img = 0
for path in jsonls:
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not lines:
        errors.append(f"{path}: empty jsonl")
        continue
    for i, ln in enumerate(lines, 1):
        try:
            rec = json.loads(ln)
        except json.JSONDecodeError as e:
            errors.append(f"{path}:{i}: bad json ({e})")
            continue
        ident = f"{path.parts[-6]}/{rec.get('strategy')} {rec.get('id')}"
        if rec.get("error"):
            errors.append(f"{ident}: error={rec['error']!r}")
            continue
        text = rec.get("prediction") or ""
        strategy = rec.get("strategy") or ""
        if strategy == "forced_interleave" and not str(text).strip():
            errors.append(f"{ident}: empty prediction")
        if "\ufffd" in text:
            errors.append(f"{ident}: replacement char in text")
        imgs = rec.get("generated_images") or []
        if not imgs:
            errors.append(f"{ident}: no generated_images")
        for img_path in imgs:
            p = Path(img_path)
            if not p.is_file():
                errors.append(f"{ident}: missing image {p}")
                continue
            if p.stat().st_size < 256:
                errors.append(f"{ident}: tiny image {p.stat().st_size}B")
                continue
            try:
                im = Image.open(p)
                im.load()
            except Exception as e:
                errors.append(f"{ident}: cannot open {p}: {e}")
                continue
            w, h = im.size
            if w < 16 or h < 16:
                errors.append(f"{ident}: image too small {w}x{h}")
            pix = list(im.convert("L").getdata())
            std = statistics.pstdev(pix)
            mean = sum(pix) / len(pix)
            if std < 5 and mean > 240:
                errors.append(f"{ident}: near-blank image std={std:.1f} mean={mean:.1f}")
            n_img += 1
        if strategy == "forced_interleave":
            kinds = [t.get("kind") for t in (rec.get("trace") or [])]
            if "image" not in kinds:
                errors.append(f"{ident}: C-F trace missing image")
            elif kinds and kinds[0] != "image":
                errors.append(f"{ident}: C-F not image-first {kinds}")
        n_ok += 1

print(f"checked jsonl={len(jsonls)} records_ok={n_ok} images_ok={n_img} root={root}")
if errors:
    print("FAIL:", file=sys.stderr)
    for e in errors:
        print(f"  {e}", file=sys.stderr)
    sys.exit(1)
print("PASS: generated images and text look normal")
PY
    local rc=$?
    set -e
    if [[ $rc -ne 0 && "${SANITY}" == "warn" ]]; then
        echo "===== [gpu2] sanity WARN (continuing) =====" >&2
        return 0
    fi
    return $rc
}

run_cf_stage() {
    local STAGE_VIEWS="$1"
    VIEWS="${STAGE_VIEWS}"
    echo "===== [gpu2] C-F stage views=${VIEWS} tasks=${TASKS} variants=${VARIANTS} out=${OUTPUT_DIR} ====="
    for ENTRY in "${CF_MODELS[@]}"; do
        run_one "$ENTRY"
    done
}

echo "GPU=2 PHASE=${PHASE} OUTPUT_DIR=${OUTPUT_DIR}"
echo "TASKS=${TASKS} VARIANTS=${VARIANTS} MAX_SAMPLES=${MAX_SAMPLES:-<all>} SANITY=${SANITY}"

if [[ "${PHASE}" == "cf" || "${PHASE}" == "all" ]]; then
    if [[ -n "${VIEW_STAGES}" ]]; then
        IFS=';' read -r -a _STAGES <<< "${VIEW_STAGES}"
        for STAGE_VIEWS in "${_STAGES[@]}"; do
            run_cf_stage "${STAGE_VIEWS}"
            sanity "forced_interleave"
        done
    else
        for ENTRY in "${CF_MODELS[@]}"; do
            run_one "$ENTRY"
        done
        sanity "forced_interleave"
    fi
fi

if [[ "${PHASE}" == "cr" || "${PHASE}" == "all" ]]; then
    for ENTRY in "${CR_MODELS[@]}"; do
        run_one "$ENTRY"
    done
    sanity "external_draw"
fi
