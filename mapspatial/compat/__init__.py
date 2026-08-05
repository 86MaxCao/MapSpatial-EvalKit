"""Compat layer — centralized monkey-patches for dependency conflicts.

Usage:
    from mapspatial.compat import apply, applied, describe
    apply("tied_weights_keys", "meta_tensor_item")
"""

from .registry import apply, applied, describe, patch  # noqa: F401
