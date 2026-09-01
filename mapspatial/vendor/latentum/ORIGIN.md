# latentum — Vendored from official LatentUM

## Origin

- **Repository**: `https://github.com/SJTU-DENG-Lab/LatentUM` (local checkout: `generative-spatial-drafts/ablation_experiment/LatentUM`)
- **Path**: `model/latentum/` and `model/decoder/`
- **Date**: 2026-08-31
- **Commit**: `25ed1b46c1f93f11f7c2650c4912a5ad6a2cbd17`

## Layout

This directory is registered as the `model` package:

- `latentum/` — official `model/latentum/`
- `decoder/` — official `model/decoder/`

Upstream imports (`from model.latentum import LatentUMModel`, `from model.decoder...`)
resolve here via `mapspatial/vendor/__init__.py`. Do not `sys.path.insert` an
external LatentUM checkout.

## What is NOT vendored

Training scripts, `uv.lock`, smoke tests, and assets from the official repo.
Weights stay in the HuggingFace checkpoint directory (`CKPT_DIR`).
