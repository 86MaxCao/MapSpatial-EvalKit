"""Patch: all_tied_weights_keys missing on trust_remote_code models.

transformers 5.x _finalize_model_loading expects all_tied_weights_keys to exist,
but older custom-code models (InternVL-custom, MiniCPM-V) don't set it.
"""

from __future__ import annotations

from ..registry import patch


@patch(
    name="tied_weights_keys",
    reason="transformers _finalize_model_loading expects all_tied_weights_keys; "
           "trust_remote_code models may not set it",
    affects=("internvl-custom", "minicpm-v"),
)
def tied_weights_keys() -> bool:
    import transformers

    target = transformers.PreTrainedModel
    if not hasattr(target, "_finalize_model_loading"):
        return False  # upstream removed/renamed — patch not applicable

    if getattr(target, "_patched_tied_weights", False):
        return False  # already patched (by us or upstream)

    original = target._finalize_model_loading

    def wrapped(self, *args, **kwargs):
        if not hasattr(self, "all_tied_weights_keys"):
            try:
                self.all_tied_weights_keys = self.get_expanded_tied_weights_keys(
                    all_submodels=False
                )
            except Exception:
                self.all_tied_weights_keys = set()
        return original(self, *args, **kwargs)

    target._finalize_model_loading = wrapped
    target._patched_tied_weights = True
    return True
