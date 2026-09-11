# bagel_interleave — Origin

## Source

- **Copied from**: [hychaochao/VLMEvalKit_Thinkmorph](https://github.com/hychaochao/VLMEvalKit_Thinkmorph) (Apache-2.0),
  `vlmeval/vlm/thinkmorph/` — the evaluation kit accompanying
  [ThinkMorph](https://github.com/ThinkMorph/ThinkMorph) (Apache-2.0)

## What is vendored

- `inferencer.py` — InterleaveInferencer: single-sample interleaved reasoning
  loop with a single KV-cache across text+image generation rounds.
- `batch_inferencer.py` — BatchInterleaveInferencer: batched packed KV-cache,
  CFG parallel, `select_batch_context` for dynamic batch sizing.
- `data/transforms.py` — ImageTransform / MaxLongEdgeMinShortEdgeResize.
- `data/data_utils.py` — pil_img2rgb, add_special_tokens, patchify, position_ids.

## Local modifications

Adapted (~250 lines) for the MapSpatial backend layer: configurable system
prompts (the upstream VLM/GEN think prompts were character-identical) and
support for text-initial inputs.

## What is NOT vendored

The Bagel modeling code lives in `vendor/bagel/` (via VeOmni).
