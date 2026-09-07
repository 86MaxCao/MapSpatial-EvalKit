"""External draw strategy — image-first G2U with restart (C-R).

typed: draw() then understand() (previous C-R; always one I0).
autonomous: gate (draw?) → optional G → judge (usable?) → U.
Does not change direct.
"""

from __future__ import annotations

import hashlib
import os
import re
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
                pred.meta.setdefault("draw_triggered", bool(pred.generated_images))
                pred.meta.setdefault(
                    "visual_reinjected", bool(pred.meta.get("visual_reinjected"))
                )
                pred.meta.setdefault("rounds", 1 if pred.generated_images else 0)
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
        replay = sample.meta.get("replay_i0")
        img_path = None
        img_hash = ""
        elapsed_draw = 0.0
        trace: list[TraceStep] = []
        gate_raw = ""
        judge_raw = ""
        gate_decision = "typed"
        usable = True

        if replay:
            img_path = Path(replay)
            if not img_path.exists():
                raise FileNotFoundError(f"replay_i0 not found: {img_path}")
            img_hash = _sha256(img_path)
            gate_decision = "replay"
            trace.append(TraceStep(
                round=0, kind="image", image=img_path,
                triggered_by="replay_i0", elapsed_s=0.0,
            ))
        elif ctx.scratchpad_policy == "autonomous":
            gate_raw, want_draw, elapsed_gate = _yes_no_turn(
                backend, sample, ctx, ctx.draw_gate_prompt, image=None,
            )
            gate_decision = "draw" if want_draw else "skip"
            trace.append(TraceStep(
                round=0, kind="text", text=gate_raw,
                triggered_by="scratchpad_gate", elapsed_s=elapsed_gate,
            ))
            if want_draw:
                img_path, img_hash, elapsed_draw = _draw_and_save(
                    backend, sample, ctx,
                )
                trace.append(TraceStep(
                    round=1, kind="image", image=img_path,
                    triggered_by="autonomous_draw", elapsed_s=elapsed_draw,
                ))
                if img_path is not None:
                    judge_raw, usable, elapsed_judge = _yes_no_turn(
                        backend, sample, ctx, ctx.image_judge_prompt,
                        image=img_path,
                    )
                    trace.append(TraceStep(
                        round=2, kind="text", text=judge_raw,
                        triggered_by="scratchpad_judge", elapsed_s=elapsed_judge,
                    ))
                else:
                    usable = False
            else:
                usable = False
        else:
            img_path, img_hash, elapsed_draw = _draw_and_save(
                backend, sample, ctx,
            )
            trace.append(TraceStep(
                round=0, kind="image", image=img_path,
                triggered_by="forced_image_first", elapsed_s=elapsed_draw,
            ))

        use_image = img_path is not None and usable
        followup_text = ctx.understand_followup if use_image else ""
        augmented_msg = list(sample.message)
        if use_image:
            # U is original question + original maps + labeled I0 + follow-up.
            # Do not re-append the G instruction. See docs/14 §2.2.
            augmented_msg.append({
                "type": "text",
                "value": (
                    "Generated visual scratchpad "
                    "(not an original map and not an answer option):"
                ),
            })
            augmented_msg.append({"type": "image", "value": img_path})
            if followup_text:
                augmented_msg.append({"type": "text", "value": followup_text})

        t0 = time.time()
        messages = self._inject_system_prompt([augmented_msg], ctx.gen_kw)
        preds = backend.understand(messages, **ctx.gen_kw)
        elapsed_understand = time.time() - t0

        pred = preds[0] if preds else Prediction(error="understand returned empty")
        pred.trace = trace + list(pred.trace or [])
        pred.generated_images = [img_path] if img_path else []
        pred.meta["generated_image_count"] = 1 if img_path else 0
        pred.meta["draw_triggered"] = img_path is not None
        pred.meta["visual_reinjected"] = use_image
        pred.meta["scratchpad_policy"] = ctx.scratchpad_policy
        pred.meta["scratchpad_gate"] = gate_decision
        if gate_raw:
            pred.meta["scratchpad_gate_raw"] = gate_raw[:500]
        if img_path is not None and ctx.scratchpad_policy == "autonomous":
            pred.meta["scratchpad_usable"] = usable
            if judge_raw:
                pred.meta["scratchpad_judge_raw"] = judge_raw[:500]
        if img_hash:
            pred.meta["generated_image_sha256"] = img_hash
        pred.meta["post_image_prompt_mode"] = (
            "appended_user_turn" if use_image else "original_only"
        )
        pred.meta.setdefault("understand_elapsed_s", elapsed_understand)
        return pred


def parse_yes_no(text: str, *, default: bool = True) -> bool:
    """Parse a YES/NO reply. Unparseable returns ``default``."""
    raw = (text or "").strip()
    if not raw:
        return default
    cleaned = re.sub(r"<think>.*?</think>", " ", raw, flags=re.S | re.I)
    cleaned = re.sub(r"</?think>", " ", cleaned, flags=re.I)
    t = cleaned.strip().upper()
    first = re.split(r"[\s,.:;!?]+", t, maxsplit=1)[0]
    if first in {"NO", "N", "FALSE", "SKIP", "DISCARD"}:
        return False
    if first in {"YES", "Y", "TRUE", "DRAW", "USE"}:
        return True
    has_yes = bool(re.search(r"\bYES\b", t))
    has_no = bool(re.search(r"\bNO\b", t))
    if has_no and not has_yes:
        return False
    if has_yes and not has_no:
        return True
    if any(s in raw for s in ("不需要", "不用画", "无需画", "不可用", "不能用")):
        return False
    return default


def _yes_no_turn(
    backend: Any,
    sample: TaskSample,
    ctx: RunContext,
    prompt: str,
    *,
    image: Path | None,
) -> tuple[str, bool, float]:
    """One understand() that must not see the MCQ system prompt."""
    if not prompt:
        return "", True, 0.0
    msg = list(sample.message)
    if image is not None:
        msg.append({
            "type": "text",
            "value": (
                "The image(s) above are the ORIGINAL input. "
                "The NEXT image is GENERATED. Compare original vs generated:"
            ),
        })
        msg.append({"type": "image", "value": image})
    msg.append({"type": "text", "value": prompt})
    gate_kw = {k: v for k, v in ctx.gen_kw.items() if k != "system_prompt"}
    t0 = time.time()
    preds = backend.understand([msg], **gate_kw)
    elapsed = time.time() - t0
    raw = ((preds[0].text if preds else "") or "").strip()
    return raw, parse_yes_no(raw, default=True), elapsed


def _draw_and_save(
    backend: Any,
    sample: TaskSample,
    ctx: RunContext,
) -> tuple[Path | None, str, float]:
    instruction = ctx.visual_generation_instruction(sample)
    t0 = time.time()
    draw_kw = dict(ctx.gen_kw)
    draw_kw["seed"] = ctx.g2u_seed
    if ctx.scratchpad_policy == "autonomous":
        draw_kw["edit"] = True
    img = backend.draw(sample.message, instruction, **draw_kw)
    elapsed = time.time() - t0
    if img is None:
        return None, "", elapsed
    if ctx.save_generated:
        gen_dir = (
            ctx.output_dir / backend.model_name / "external_draw" / "generated"
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
    img_hash = _sha256(img_path) if img_path.exists() else ""
    return img_path, img_hash, elapsed


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
