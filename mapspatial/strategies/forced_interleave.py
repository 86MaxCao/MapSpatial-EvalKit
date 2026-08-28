"""Forced interleave strategy — image-first G2U with shared KV (C-F).

Does not call native_interleave. Does not change direct/understand.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .base import Strategy
from ..types import TaskSample, Prediction, TraceStep, RunContext


class ForcedInterleaveStrategy(Strategy):
    name = "forced_interleave"

    def required_caps(self) -> dict[str, Any]:
        return {"forced_interleave": True}

    def run(
        self,
        backend: Any,
        samples: list[TaskSample],
        ctx: RunContext,
    ) -> list[Prediction]:
        results = []
        followup = ctx.understand_followup
        for s in samples:
            instruction = ctx.visual_generation_instruction(s)
            try:
                pred = backend.forced_interleave(
                    s.message,
                    instruction,
                    max_images=1,
                    image_first=True,
                    followup=followup,
                    seed=ctx.g2u_seed,
                    **ctx.gen_kw,
                )
                saved_paths: list[Path] = []
                hashes: list[str] = []
                if pred.generated_images:
                    gen_dir = (
                        ctx.output_dir / backend.model_name / self.name / "generated"
                        / ctx.view / ctx.task / ctx.variant
                    )
                    gen_dir.mkdir(parents=True, exist_ok=True)
                    for i, img in enumerate(pred.generated_images):
                        if isinstance(img, Path):
                            path = img
                        else:
                            path = gen_dir / f"{s.id}_r{i}.png"
                            if ctx.save_generated:
                                img.save(str(path))
                            else:
                                import os
                                import tempfile
                                fd, tmp = tempfile.mkstemp(suffix=".png")
                                os.close(fd)
                                img.save(tmp)
                                path = Path(tmp)
                        saved_paths.append(path)
                        if path.exists():
                            hashes.append(_sha256(path))
                pred.generated_images = saved_paths
                pred.meta.setdefault("strategy", "forced_interleave")
                pred.meta.setdefault("backend", backend.model_name)
                pred.meta.setdefault("protocol", "image_first_single_image")
                pred.meta.setdefault("stateful", True)
                pred.meta.setdefault("draw_triggered", len(saved_paths) > 0)
                pred.meta.setdefault("visual_reinjected", len(saved_paths) > 0)
                pred.meta.setdefault("rounds", 1 if saved_paths else 0)
                pred.meta.setdefault("generated_image_count", len(saved_paths))
                pred.meta.setdefault("pre_image_text_tokens", 0)
                if hashes:
                    pred.meta.setdefault("generated_image_sha256", hashes[0])
                pred.meta.setdefault("seed", ctx.g2u_seed)
                results.append(pred)
            except Exception as e:
                results.append(Prediction(
                    error=str(e),
                    meta={
                        "strategy": "forced_interleave",
                        "backend": backend.model_name,
                        "draw_triggered": False,
                        "rounds": 0,
                        "protocol": "image_first_single_image",
                    },
                ))
        return results


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
