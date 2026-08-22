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

from pathlib import Path
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

                # Update trace image paths to match saved files
                if saved_paths:
                    img_idx = 0
                    for t in pred.trace:
                        if t.kind == "image" and t.image is None and img_idx < len(saved_paths):
                            t.image = saved_paths[img_idx]
                            img_idx += 1

                # Ensure meta is set
                pred.meta.setdefault("strategy", "native_interleave")
                pred.meta.setdefault("backend", backend.model_name)
                pred.meta.setdefault("draw_triggered", len(saved_paths) > 0)
                pred.meta.setdefault("rounds", len(saved_paths))
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
