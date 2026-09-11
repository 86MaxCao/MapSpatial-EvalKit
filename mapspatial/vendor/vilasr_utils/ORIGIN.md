# ViLaSR attribution — vilasr_model.py + vilasr_utils/

## Source

- **Upstream project**: [AntResearchNLP/ViLaSR](https://github.com/AntResearchNLP/ViLaSR) (MIT)

## What derives from upstream

- `../vilasr_model.py` — the multi-turn Object Mapper / Path Tracer reasoning
  loop is rewritten for the MapSpatial backend, but the system prompts and
  prompt templates are copied from upstream `eval/infer.py`.
- `edit_image.py` — adapted from upstream `utils/edit_image.py`
  (bounding-box / marker drawing helpers, ~40 lines changed).
- `file_io.py` — minimal image-download helper written for this project;
  no upstream code.
