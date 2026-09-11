# latentum — Origin

## Source

- **Copied verbatim from**: [SJTU-DENG-Lab/LatentUM](https://github.com/SJTU-DENG-Lab/LatentUM)
  (Apache-2.0), commit `25ed1b46c1f93f11f7c2650c4912a5ad6a2cbd17`
- **Paths**: `model/latentum/` and `model/decoder/`

## Layout

This directory is registered as the `model` package:

- `latentum/` — official `model/latentum/`
- `decoder/` — official `model/decoder/`

Upstream imports (`from model.latentum import LatentUMModel`,
`from model.decoder ...`) resolve here via `mapspatial/vendor/__init__.py`.
Do not `sys.path.insert` an external LatentUM checkout.

## What is NOT vendored

Training scripts, `uv.lock`, smoke tests, and assets from the official repo.
Weights stay in the HuggingFace checkpoint directory (`CKPT_DIR`).

## Included third-party components

`latentum/internvl/` retains OpenGVLab InternVL code (MIT); `decoder/sd_35/`
contains Stability AI Stable Diffusion 3.5 MMDiT-X code. Original headers are
preserved in-file.
