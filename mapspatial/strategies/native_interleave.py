"""Native interleave strategy — delegate to backend's native interleave loop.

For models with caps.native_interleave=True (Bagel/ThinkMorph), this
preserves the single KV-cache across text+image generation rounds.

The key difference from external_draw: the model decides WHEN to generate
intermediate images, not us. The marker (e.g. "<image_start>") is per-model
configurable.

draw_triggered must be recorded to distinguish:
  - Model chose to draw (rounds >= 1, draw_triggered=True)
  - Model chose not to draw (rounds=0, draw_triggered=False)
  - Model tried to draw but marker didn't match (rounds=0, draw_triggered=False, but trace text may show intent)
"""

from __future__ import annotations

from typing import Any

from .base import Strategy
from ..types import TaskSample, Prediction, RunContext


class NativeInterleaveStrategy(Strategy):
    name = "native_interleave"

    def required_caps(self) -> dict[str, Any]:
        return {"native_interleave": True}

    def run(
        self,
        backend: Any,
        samples: list[TaskSample],
        ctx: RunContext,
    ) -> list[Prediction]:
        results = []
        for s in samples:
            try:
                pred = backend.interleave(
                    s.message,
                    max_rounds=ctx.max_rounds,
                    marker=ctx.marker,
                    **ctx.gen_kw,
                )
                # Ensure meta is set
                pred.meta.setdefault("strategy", "native_interleave")
                pred.meta.setdefault("backend", backend.model_name)
                pred.meta.setdefault("draw_triggered",
                                     len(pred.generated_images) > 0)
                pred.meta.setdefault("rounds",
                                     len([t for t in pred.trace if t.kind == "image"]))
                results.append(pred)
            except Exception as e:
                results.append(Prediction(
                    error=str(e),
                    meta={
                        "strategy": "native_interleave",
                        "backend": backend.model_name,
                        "draw_triggered": False,
                        "rounds": 0,
                    },
                ))
        return results
