"""External draw strategy — force generate an intermediate image, then answer.

Unlike native_interleave (model decides), this strategy ALWAYS generates
an intermediate image first, then feeds it back to the model for answering.

Context is lost between draw() and understand() — this is a known semantic
difference from native_interleave (which preserves single KV-cache).

The draw instruction is per-question_type, configurable via
configs/strategies/external_draw.yaml.

Intermediate image naming: {output_dir}/generated/{view}/{task}/{variant}/{sample_id}_r{round}.png
Must contain sample_id (fixes ThinkMorph's uuid8+idx problem).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import Strategy
from ..types import TaskSample, Prediction, TraceStep, RunContext


class ExternalDrawStrategy(Strategy):
    name = "external_draw"

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
                pred = self._run_one(backend, s, ctx)
                pred.meta.setdefault("strategy", "external_draw")
                pred.meta.setdefault("backend", backend.model_name)
                pred.meta.setdefault("draw_triggered", True)
                pred.meta.setdefault("rounds", 1)
                results.append(pred)
            except Exception as e:
                results.append(Prediction(
                    error=str(e),
                    meta={
                        "strategy": "external_draw",
                        "backend": backend.model_name,
                        "draw_triggered": False,
                        "rounds": 0,
                    },
                ))
        return results

    def _run_one(
        self,
        backend: Any,
        sample: TaskSample,
        ctx: RunContext,
    ) -> Prediction:
        import time

        trace: list[TraceStep] = []

        # 1) Force-generate an intermediate image
        instruction = ctx.draw_instruction(sample)
        t0 = time.time()
        img = backend.draw(sample.message, instruction, **ctx.gen_kw)
        elapsed_draw = time.time() - t0

        # Save with sample_id in filename (not uuid8!)
        img_path = None
        if ctx.save_generated and img is not None:
            gen_dir = ctx.output_dir / "generated" / ctx.view / ctx.task / ctx.variant
            gen_dir.mkdir(parents=True, exist_ok=True)
            img_path = gen_dir / f"{sample.id}_r0.png"
            img.save(str(img_path))
        elif img is not None:
            # Still need a path for the message — use temp
            import tempfile
            fd, tmp = tempfile.mkstemp(suffix=".png")
            import os
            os.close(fd)
            img.save(tmp)
            img_path = Path(tmp)

        trace.append(TraceStep(
            round=0, kind="image",
            image=img_path,
            triggered_by="forced",
            elapsed_s=elapsed_draw,
        ))

        # 2) Append intermediate image to message and answer
        followup_text = ctx.draw_followup_text
        augmented_msg = list(sample.message) + [
            {"type": "text", "value": followup_text},
            {"type": "image", "value": img_path},
        ]

        t0 = time.time()
        preds = backend.understand([augmented_msg], **ctx.gen_kw)
        elapsed_understand = time.time() - t0

        pred = preds[0] if preds else Prediction(error="understand returned empty")
        pred.trace = trace + pred.trace
        pred.generated_images = [img_path] if img_path else []
        return pred
