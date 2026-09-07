"""Autonomous C-R agent steps: gate → optional G → judge → U."""

from pathlib import Path

from PIL import Image

from mapspatial.strategies.external_draw import ExternalDrawStrategy, parse_yes_no
from mapspatial.types import Prediction, RunContext, TaskSample


class _MockBackend:
    model_name = "mock"

    def __init__(self, replies: list[str]):
        self.replies = list(replies)
        self.draw_calls = 0
        self.understand_msgs: list = []

    def understand(self, messages, **kw):
        self.understand_msgs.append(messages[0])
        text = self.replies.pop(0) if self.replies else "B"
        return [Prediction(text=text)]

    def draw(self, context, instruction, **kw):
        self.draw_calls += 1
        return Image.new("RGB", (8, 8), color=(0, 0, 255))


def _sample() -> TaskSample:
    return TaskSample(
        id="s1",
        message=[
            {"type": "image", "value": Path("/tmp/orig.png")},
            {"type": "text", "value": "Which direction?"},
        ],
        gold="A",
        meta={"question_type": "direction"},
    )


def test_parse_yes_no():
    assert parse_yes_no("YES") is True
    assert parse_yes_no("NO") is False
    assert parse_yes_no("No, skip drawing.") is False
    assert parse_yes_no("B") is True  # unparseable defaults to True
    assert parse_yes_no("B", default=False) is False


def test_typed_always_draws(tmp_path: Path):
    backend = _MockBackend(["B"])
    ctx = RunContext(output_dir=tmp_path, scratchpad_policy="typed", view="wprd01", task="t1", variant="base")
    pred = ExternalDrawStrategy().run(backend, [_sample()], ctx)[0]
    assert backend.draw_calls == 1
    assert len(backend.understand_msgs) == 1
    assert pred.meta["draw_triggered"] is True
    assert pred.meta["visual_reinjected"] is True
    assert pred.generated_images


def test_judge_compares_original_and_generated(tmp_path: Path):
    backend = _MockBackend(["YES", "NO", "B"])
    ctx = RunContext(output_dir=tmp_path, scratchpad_policy="autonomous", view="wprd01", task="t1", variant="base")
    ExternalDrawStrategy().run(backend, [_sample()], ctx)
    judge_msg = backend.understand_msgs[1]
    images = [x for x in judge_msg if x.get("type") == "image"]
    assert len(images) == 2
    assert images[0]["value"] == Path("/tmp/orig.png")
    blob = " ".join(str(x.get("value") or "") for x in judge_msg).lower()
    assert "original" in blob and "generated" in blob
    assert "scratchpad" in blob or "compare" in blob


def test_autonomous_skip_draw(tmp_path: Path):
    backend = _MockBackend(["NO", "B"])
    ctx = RunContext(output_dir=tmp_path, scratchpad_policy="autonomous", view="wprd01", task="t1", variant="base")
    pred = ExternalDrawStrategy().run(backend, [_sample()], ctx)[0]
    assert backend.draw_calls == 0
    assert len(backend.understand_msgs) == 2  # gate + answer
    assert pred.meta["scratchpad_gate"] == "skip"
    assert pred.meta["draw_triggered"] is False
    assert pred.meta["visual_reinjected"] is False
    assert pred.generated_images == []
    answer_msg = backend.understand_msgs[-1]
    answer_images = [x.get("value") for x in answer_msg if x.get("type") == "image"]
    assert answer_images == [Path("/tmp/orig.png")]


def test_autonomous_draw_then_discard(tmp_path: Path):
    backend = _MockBackend(["YES", "NO", "B"])
    ctx = RunContext(output_dir=tmp_path, scratchpad_policy="autonomous", view="wprd01", task="t1", variant="base")
    pred = ExternalDrawStrategy().run(backend, [_sample()], ctx)[0]
    assert backend.draw_calls == 1
    assert len(backend.understand_msgs) == 3  # gate, judge, answer
    assert pred.meta["scratchpad_gate"] == "draw"
    assert pred.meta["scratchpad_usable"] is False
    assert pred.meta["draw_triggered"] is True
    assert pred.meta["visual_reinjected"] is False
    assert pred.generated_images  # kept for audit
    answer_msg = backend.understand_msgs[-1]
    answer_images = [x.get("value") for x in answer_msg if x.get("type") == "image"]
    assert answer_images == [Path("/tmp/orig.png")]
    assert pred.generated_images[0] not in answer_images


def test_autonomous_draw_then_use(tmp_path: Path):
    backend = _MockBackend(["YES", "YES", "B"])
    ctx = RunContext(output_dir=tmp_path, scratchpad_policy="autonomous", view="wprd01", task="t1", variant="base")
    pred = ExternalDrawStrategy().run(backend, [_sample()], ctx)[0]
    assert backend.draw_calls == 1
    assert pred.meta["scratchpad_usable"] is True
    assert pred.meta["visual_reinjected"] is True
    answer_msg = backend.understand_msgs[-1]
    answer_images = [x.get("value") for x in answer_msg if x.get("type") == "image"]
    assert Path("/tmp/orig.png") in answer_images
    assert pred.generated_images[0] in answer_images
