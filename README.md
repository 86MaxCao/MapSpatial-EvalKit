# MapSpatial-EvalKit

MapSpatial-EvalKit is a multimodal reasoning and evaluation toolkit for **outdoor map spatial understanding**. It runs and compares vision-language models and unified (generate + understand) models under a unified data format, inference interface, and evaluation protocol.

- **Understanding models**: Qwen2-VL, Qwen2.5-VL, Qwen3-VL, InternVL3, InternVL3.5, GLM-4.6V, Step3-VL, MiMo-Embodied, Cambrian-S, ViLaSR, Spatial-MLLM, SenseNova-SI, plus API models (Gemini 3 Flash, Qwen3.5 Plus, Qwen3.6 Plus).
- **Unified models** (generate + understand): Bagel, ThinkMorph, SenseNova-U1, LatentUM, JoyAI-Image, Show-o2.

Unified models can **generate intermediate images** during reasoning (visual chain-of-thought). This is the core hypothesis the toolkit is built to verify: *does letting a model draw intermediate sketches actually improve spatial understanding accuracy?*

## Architecture in one sentence

```
data (JSONL)  →  Message[]  →  Strategy  →  Backend  →  Prediction  →  evaluation
                  interleaved               orchestrates   provides        structured,
                  text/image list           capabilities   understand/     with generated
                                                           draw/batch      images + trace
```

**Backends provide capabilities; strategies decide how to orchestrate them.** The two dimensions are orthogonal, so `Qwen3-VL + direct` and `Bagel + native-interleave` produce results with an identical schema, making accuracy directly comparable.

Key constraints:

1. **`Prediction` is not a string.** It carries `generated_images` and `trace` so the visual chain-of-thought remains auditable.
2. **Strategies**: `direct` (no intermediate images), `native-interleave` (model decides when to draw), `external-draw` / `forced-interleave` (strategy forces drawing, for ablation).
3. **vLLM batches for real.** The vLLM backend submits the whole batch at once and never clears the CUDA cache inside the inference loop.

## Installation

Requires Python ≥ 3.10.

```bash
git clone <repo-url>
cd MapSpatial-EvalKit
pip install -e .
```

Optional extras:

```bash
pip install -e ".[vllm]"   # vLLM backend for batched local inference
pip install -e ".[api]"    # API backends (DashScope, Gemini, ...)
pip install -e ".[video]"  # video input support
pip install -e ".[dev]"    # pytest for development
```

Unified models run through PyTorch/Transformers with vendored integration code under `mapspatial/vendor/`; some models need extra dependencies (e.g. `diffusers`, `safetensors`).

## Model checkpoints

Model configs live in `configs/models/` (27 configs). Local checkpoints are referenced via the `CKPT_DIR` environment variable:

```bash
export CKPT_DIR=/path/to/your/checkpoints
# configs/models/bagel-7b.yaml → model_path: ${CKPT_DIR}/BAGEL-7B-MoT
```

API models use environment placeholders as well:

```bash
export DASHSCOPE_API_URL=...   # for Qwen API models
export GOOGLE_API_URL=...      # for Gemini
export MAPSPATIAL_API_KEYS=... # API key(s), comma-separated for rotation
```

## Dataset

First, download the MapSpatial benchmark data from HuggingFace:
[mapspatial/map-spatial-benchmark](https://huggingface.co/datasets/mapspatial/map-spatial-benchmark)

```bash
huggingface-cli download mapspatial/map-spatial-benchmark --repo-type dataset --local-dir /path/to/map-spatial-benchmark
```

The benchmark pack follows the HuggingFace layout (`data/*.jsonl` + `images/`);
pass `--layout hf --input-dir /path/to/map-spatial-benchmark` to the CLI
commands below.

## Quick start

All functionality is exposed through the `mapspatial` CLI (equivalently `python -m mapspatial.cli`).

### Environment self-check

```bash
mapspatial doctor                    # verify configs, imports, capabilities
mapspatial doctor --check-load       # additionally try loading each model (slow)
```

### Preflight: check dataset image availability

```bash
mapspatial preflight --layout hf --input-dir /path/to/map-spatial-benchmark
```

### Run inference

```bash
CUDA_VISIBLE_DEVICES=0 mapspatial run \
  --model configs/models/qwen3-vl-8b.yaml \
  --strategy direct \
  --layout hf \
  --input-dir /path/to/map-spatial-benchmark \
  --output-dir results \
  --views blank,sat,webrd04,wprd01 \
  --tasks t1,t2 \
  --variants base/direct,base/oracle
```

Useful flags: `--max-samples N` (smoke test), `--batch-size N`, `--skip-preflight`, `--store-question`. See `mapspatial run --help` for the full list.

### Cross-model report

```bash
mapspatial report --output-dir results --models '*' --out report.csv
```

### Compatibility patches

```bash
mapspatial compat --describe
```

## Repository layout

```
mapspatial/          # core package: data pipeline, backends, strategies, runner, eval
  vendor/            # vendored third-party model integration code
configs/models/      # per-model YAML configs (local via ${CKPT_DIR}, API via env vars)
```

## License

MapSpatial-EvalKit is released under the [Apache-2.0 License](./LICENSE).
Third-party vendored code and attributions are listed in [NOTICE](./NOTICE)
and in the `ORIGIN.md` file of each `mapspatial/vendor/` subdirectory.
