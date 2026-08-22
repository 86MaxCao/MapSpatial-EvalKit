"""Forced interleave strategy — force image generation with shared KV cache.

Unlike native_interleave (model decides via marker), this strategy ALWAYS
generates an intermediate image after the first text reasoning round,
then feeds it back into the KV cache and continues reasoning.

Unlike external_draw (separate draw + understand calls, no shared cache),
this strategy preserves the single KV cache across text+image rounds via
the backend's forced_interleave() method.

Use case: models that have the interleave API (shared KV cache + incremental
forward) but were NOT trained to emit marker tokens (e.g. base Bagel).
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from .base import Strategy
from ..types import TaskSample, Prediction, TraceStep, RunContext


class ForcedInterleaveStrategy(Strategy):
    name = "forced_interleave"

    def required_caps(self) -> dict[str, Any]:
        return {"draw": True}

    def run(
        self,
        backend: Any,
        samples: list[TaskSample],
        ctx: RunContext,
    ) -> list[Prediction]:
        results = []
        for s in samples:
            try:
                pred = backend.forced_interleave(
                    s.message,
                    max_rounds=ctx.max_rounds,
                    **ctx.gen_kw,
                )
                # Save generated PIL images to disk as Paths
                saved_paths: list[Path] = []
                if ctx.save_generated and pred.generated_images:
                    gen_dir = ctx.output_dir / backend.model_name / self.name / "generated" / ctx.view / ctx.task / ctx.variant
                    gen_dir.mkdir(parents=True, exist_ok=True)
                    for i, img in enumerate(pred.generated_images):
                        if isinstance(img, Path):
                            saved_paths.append(img)
                        else:
                            # PIL Image — save to disk
                            img_path = gen_dir / f"{s.id}_r{i}.png"
                            img.save(str(img_path))
                            saved_paths.append(img_path)
                pred.generated_images = saved_paths

                pred.meta.setdefault("strategy", "forced_interleave")
                pred.meta.setdefault("backend", backend.model_name)
                pred.meta.setdefault("draw_triggered", len(saved_paths) > 0)
                pred.meta.setdefault("rounds", len(saved_paths))
                results.append(pred)
            except Exception as e:
                results.append(Prediction(
                    error=str(e),
                    meta={
                        "strategy": "forced_interleave",
                        "backend": backend.model_name,
                        "draw_triggered": False,
                        "rounds": 0,
                    },
                ))
        return results
