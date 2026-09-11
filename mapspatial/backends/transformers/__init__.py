"""Transformers backend subpackage.

Splits the predecessor's 539-line monolithic TransformersBackend into:
  - backend.py: TransformersBackend (shared base with dispatch)
  - (future: qwen_vl.py, internvl.py, glm.py, minicpm.py, generic.py)

Model family is selected by config's load.model_family, not by
guessing from model_id prefix (fixes the predecessor's fragile detection).
"""

from .backend import TransformersBackend  # noqa: F401
