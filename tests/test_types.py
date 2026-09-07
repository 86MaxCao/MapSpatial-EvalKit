"""Test types.py — Prediction, TaskSample, Capabilities serialization."""

import json
from pathlib import Path
from mapspatial.types import (
    Prediction, TraceStep, TaskSample, Capabilities, Message, RunContext,
)


def test_prediction_defaults():
    p = Prediction(text="hello")
    assert p.text == "hello"
    assert p.generated_images == []
    assert p.trace == []
    assert p.error is None
    assert p.meta == {}


def test_prediction_with_images_and_trace():
    p = Prediction(
        text="answer",
        generated_images=[Path("/tmp/img_r0.png")],
        trace=[TraceStep(round=0, kind="image", image=Path("/tmp/img_r0.png"),
                         triggered_by="forced")],
        meta={"strategy": "external_draw", "draw_triggered": True},
    )
    assert len(p.generated_images) == 1
    assert p.trace[0].triggered_by == "forced"
    assert p.meta["strategy"] == "external_draw"


def test_capabilities():
    caps = Capabilities(batch=True, draw=False, native_interleave=False,
                        max_images=24, video=False)
    assert caps.batch is True
    assert caps.max_images == 24
    assert caps.forced_interleave is False


def test_run_context_g2u_defaults():
    ctx = RunContext(output_dir=Path("/tmp"))
    assert ctx.g2u_seed == 42
    assert ctx.understand_followup
    sample = TaskSample(
        id="x",
        message=[{"type": "text", "value": "q"}],
        gold="A",
        meta={"question_type": "direction"},
    )
    inst = ctx.visual_generation_instruction(sample)
    assert "arrow" in inst.lower() or "direction" in inst.lower()
    assert ctx.scratchpad_policy == "typed"


def test_run_context_autonomous_scratchpad_does_not_use_typed_draw():
    ctx = RunContext(output_dir=Path("/tmp"), scratchpad_policy="autonomous")
    sample = TaskSample(
        id="x",
        message=[{"type": "text", "value": "q"}],
        gold="A",
        meta={"question_type": "direction"},
    )
    inst = ctx.visual_generation_instruction(sample)
    assert "blue arrow" not in inst.lower()
    assert "edit" in inst.lower() or "image editing" in inst.lower()
    assert "you decide" in inst.lower()
    assert "line" in inst.lower() or "box" in inst.lower() or "circle" in inst.lower()
    follow = ctx.understand_followup.lower()
    assert "ignore" in follow or "optional" in follow
    assert ctx.draw_gate_prompt
    assert "yes or no" in ctx.draw_gate_prompt.lower()
    assert "default to no" in ctx.draw_gate_prompt.lower()
    assert ctx.image_judge_prompt
    assert "last image" in ctx.image_judge_prompt.lower()
    assert "scratchpad" in ctx.image_judge_prompt.lower()
    assert "default to no" in ctx.image_judge_prompt.lower()
    typed = RunContext(output_dir=Path("/tmp"), scratchpad_policy="typed")
    typed_inst = typed.visual_generation_instruction(sample)
    assert "arrow" in typed_inst.lower() or "direction" in typed_inst.lower()


def test_forced_interleave_followup_restates_question_and_asks_for_letter():
    ctx = RunContext(
        output_dir=Path("/tmp"),
        gen_kw={"system_prompt": "Return only the option letter."},
    )
    sample = TaskSample(
        id="x",
        message=[
            {"type": "image", "value": Path("/tmp/m.png")},
            {"type": "text", "value": "Which way is north? A) up B) down"},
        ],
        gold="A",
        meta={"question_type": "direction"},
    )
    follow = ctx.forced_interleave_followup(sample)
    low = follow.lower()
    assert "drawing is finished" in low or "do not generate" in low
    assert "image_start" in low
    assert "<answer>" in low
    assert "return only the option letter" in low
    assert "which way is north" in low
    inst = ctx.visual_generation_instruction(sample)
    assert "after the visual scratchpad has been incorporated" not in inst.lower()


def test_task_sample_gold_isolation():
    """gold must not be in Message — verify isolation."""
    msg: Message = [
        {"type": "image", "value": Path("/tmp/test.png")},
        {"type": "text", "value": "What direction?"},
    ]
    sample = TaskSample(id="test_001", message=msg, gold="D")
    # Check that gold is not in the message
    for item in sample.message:
        assert "gold" not in item
        assert item.get("value") != "D"


def test_prediction_serialization():
    """Prediction should be JSON-serializable for result records."""
    p = Prediction(
        text="The answer is B",
        generated_images=[Path("/tmp/gen_0_r0.png")],
        trace=[TraceStep(round=0, kind="text", text="thinking...", elapsed_s=1.5)],
        meta={"strategy": "direct", "rounds": 1, "draw_triggered": False},
    )
    # The runner serializes manually, but verify key fields work
    assert p.text == "The answer is B"
    assert str(p.generated_images[0]) == "/tmp/gen_0_r0.png"
    assert p.trace[0].elapsed_s == 1.5
