"""Direct strategy — no orchestration, just pass Message to backend.

Applicable to all 20 models. Also serves as the baseline condition for
unified models (answering: "how well do they do without drawing?").
"""

from __future__ import annotations

from typing import Any

from .base import Strategy
from ..types import TaskSample, Prediction, RunContext


class DirectStrategy(Strategy):
    name = "direct"

    def required_caps(self) -> dict[str, Any]:
        return {}  # no requirements — all backends support this

    def run(
        self,
        backend: Any,
        samples: list[TaskSample],
        ctx: RunContext,
    ) -> list[Prediction]:
        messages = [s.message for s in samples]
        messages = self._inject_system_prompt(messages, ctx.gen_kw)
        preds = backend.understand(messages, **ctx.gen_kw)

        # Ensure meta is set on every prediction
        for p in preds:
            p.meta.setdefault("strategy", "direct")
            p.meta.setdefault("rounds", 1)
            p.meta.setdefault("draw_triggered", False)
            p.meta.setdefault("backend", backend.model_name)

        return preds
