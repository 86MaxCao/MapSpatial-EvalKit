"""ThinkMorph backend — reuses Bagel modeling code.

ThinkMorph-7B is registered to use BagelForConditionalGeneration
(thinkmorph/__init__.py:11-15). The only difference is the checkpoint path.
So we subclass BagelBackend with minimal overrides.
"""

from __future__ import annotations

from typing import ClassVar

from ...types import Capabilities
from ...config import BackendConfig
from ..base import Backend
from .bagel import BagelBackend


class ThinkMorphBackend(BagelBackend):
    """ThinkMorph-7B backend.

    ThinkMorph uses the same BagelForConditionalGeneration model class.
    The checkpoint contains different weights (trained with thinking + image
    generation), but the code path is identical.

    See docs/05-veomni-integration.md §3.3 for the understanding_output mapping:
      direct             → understand() (understanding_output=True)
      native_interleave  → interleave() (understanding_output=False)
      external_draw      → understand() + draw()
    """

    caps: ClassVar[Capabilities] = Capabilities(
        batch=True,
        draw=True,
        native_interleave=True,
        max_images=24,
        video=False,
    )

    def __init__(self, cfg: BackendConfig) -> None:
        # ThinkMorph may need slightly different defaults
        if "max_rounds" not in cfg.backend_args:
            cfg.backend_args["max_rounds"] = 5  # ThinkMorph supports more rounds
        if "cfg_text_scale" not in cfg.backend_args:
            cfg.backend_args["cfg_text_scale"] = 3.0  # ThinkMorph default
        super().__init__(cfg)
