# bagel_interleave — Vendored from VLMEvalKit_Thinkmorph

## Origin

- **Repository**: `generative-spatial-drafts/ablation_experiment/VLMEvalKit_Thinkmorph`
- **Path**: `vlmeval/vlm/thinkmorph/`
- **Date**: 2026-08-03
- **Commit**: as of checkout

## What is vendored

- `inferencer.py` (374 lines) — InterleaveInferencer: single-sample interleaved reasoning loop
  with single KV-cache across text+image generation rounds.
- `batch_inferencer.py` (1072 lines) — BatchInterleaveInferencer: batched packed KV-cache,
  CFG parallel, `select_batch_context` for dynamic batch sizing.
- `data/transforms.py` — ImageTransform / MaxLongEdgeMinShortEdgeResize
- `data/data_utils.py` — pil_img2rgb, add_special_tokens, patchify, position_ids

## Why vendor (not rewrite)

These files are proven engineering (374 + 1072 lines of real interleave logic with
packed KV cache, CFG parallel, dynamic batch context selection). Rewriting is not
worth the risk — the logic is correct and battle-tested.

## What is NOT vendored (loaded by reference)

The Bagel modeling code (`modeling_bagel.py`, `configuration_bagel.py`,
`qwen2_navit.py`) is loaded from the VeOmni source tree at runtime via
`veomni_modeling/_loader.py`. This avoids duplicating 2394+ lines of model
definition code. When the modeling code needs modification, the files will be
copied here with patches documented in PATCHES.md.

## Known issues to fix

- `VLM_THINK_SYSTEM_PROMPT` and `GEN_THINK_SYSTEM_PROMPT` are character-identical
  (copy-paste bug in upstream). Our BagelBackend uses a single configurable prompt.
- `validate_batch_inputs` requires image-initial input. T4 route_validity is
  text-initial. Adaptation needed (tracked in docs/08-roadmap.md U8).
