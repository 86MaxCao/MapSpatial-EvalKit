"""External draw strategy — image-first G2U with restart (C-R).

draw() then understand() as two independent forwards. Does not change direct.
"""

from __future__ import annotations

import hashlib
import os
import tempfile
import time
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
                pred.meta.setdefault("protocol", "image_first_single_image")
                pred.meta.setdefault("stateful", False)
                pred.meta.setdefault("draw_triggered", True)
                pred.meta.setdefault("visual_reinjected", True)
                pred.meta.setdefault("rounds", 1)
                pred.meta.setdefault("pre_image_text_tokens", 0)
                pred.meta.setdefault("seed", ctx.g2u_seed)
                results.append(pred)
            except Exception as e:
                results.append(Prediction(
                    error=str(e),
                    meta={
                        "strategy": "external_draw",
                        "backend": backend.model_name,
                        "draw_triggered": False,
                        "rounds": 0,
                        "protocol": "image_first_single_image",
                    },
                ))
        return results

    def _run_one(
        self,
        backend: Any,
        sample: TaskSample,
        ctx: RunContext,
    ) -> Prediction:
        instruction = ctx.visual_generation_instruction(sample)
        followup_text = ctx.understand_followup

        t0 = time.time()
        img = backend.draw(
            sample.message, instruction, seed=ctx.g2u_seed, **ctx.gen_kw,
        )
        elapsed_draw = time.time() - t0

        img_path = None
        img_hash = ""
        if img is not None:
            if ctx.save_generated:
                gen_dir = (
                    ctx.output_dir / backend.model_name / self.name / "generated"
                    / ctx.view / ctx.task / ctx.variant
                )
                gen_dir.mkdir(parents=True, exist_ok=True)
                img_path = gen_dir / f"{sample.id}_r0.png"
                img.save(str(img_path))
            else:
                fd, tmp = tempfile.mkstemp(suffix=".png")
                os.close(fd)
                img.save(tmp)
                img_path = Path(tmp)
            if img_path.exists():
                img_hash = _sha256(img_path)

        trace = [TraceStep(
            round=0, kind="image",
            image=img_path,
            triggered_by="forced_image_first",
            elapsed_s=elapsed_draw,
        )]

        # Original message (question + source images) already present.
        # Append G instruction (real G history), then I0, then follow-up.
        augmented_msg = list(sample.message) + [
            {"type": "text", "value": instruction},
            {"type": "image", "value": img_path},
            {"type": "text", "value": followup_text},
        ]

        t0 = time.time()
        messages = self._inject_system_prompt([augmented_msg], ctx.gen_kw)
        preds = backend.understand(messages, **ctx.gen_kw)
        elapsed_understand = time.time() - t0

        pred = preds[0] if preds else Prediction(error="understand returned empty")
        pred.trace = trace + list(pred.trace or [])
        pred.generated_images = [img_path] if img_path else []
        pred.meta["generated_image_count"] = 1 if img_path else 0
        if img_hash:
            pred.meta["generated_image_sha256"] = img_hash
        pred.meta["post_image_prompt_mode"] = "appended_user_turn"
        pred.meta.setdefault("understand_elapsed_s", elapsed_understand)
        return pred


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
