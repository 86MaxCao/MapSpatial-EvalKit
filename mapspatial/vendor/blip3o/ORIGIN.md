# blip3o — Origin

## Source

**Original implementation by the MapSpatial-EvalKit authors**, written in the
integration style of the [VeOmni](https://github.com/ByteDance-Seed/VeOmni)
framework (Apache-2.0). No VeOmni code is copied.

The model architecture follows the official
[JiuhaiChen/BLIP3o](https://github.com/JiuhaiChen/BLIP3o) repository
(license not stated in the source checkout — verify upstream before
redistribution).

## Notes

The image-generation pipeline in `mapspatial/backends/veomni/blip3o.py`
(LLM → DiT → UNet → VAE) was implemented following the official BLIP3o
inference approach; no code was copied directly from the official repo.
