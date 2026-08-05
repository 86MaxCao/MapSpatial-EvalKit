"""Patch: torch.Tensor.item() on meta device crashes.

InternVL's InternVisionEncoder calls linspace(...).item() during meta-init,
which is illegal for meta tensors. Return 0.0 instead.
"""

from __future__ import annotations

from ..registry import patch


@patch(
    name="meta_tensor_item",
    reason="meta tensor has no real value; .item() crashes InternVisionEncoder linspace",
    affects=("internvl-custom",),
)
def meta_tensor_item() -> bool:
    import torch

    if getattr(torch.Tensor, "_patched_meta_item", False):
        return False  # already patched

    original_item = torch.Tensor.item

    def patched_item(self):
        if self.is_meta:
            return 0.0
        return original_item(self)

    torch.Tensor.item = patched_item
    torch.Tensor._patched_meta_item = True
    return True
