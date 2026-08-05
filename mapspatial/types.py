"""Core data types for MapSpatial-EvalKit.

Message: interleaved text/image/video input (borrowed from VLMEvalKit but typed).
Prediction: structured return value (not a plain string) — carries generated_images + trace.
TaskSample: data-layer product (gold isolated from Message).
Capabilities: backend ability declaration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, Literal, NamedTuple, TypedDict, Union

try:
    from PIL import Image
except ImportError:
    Image = None  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# Message — interleaved multimodal input
# ---------------------------------------------------------------------------

class TextItem(TypedDict):
    type: Literal["text"]
    value: str


class ImageItem(TypedDict):
    type: Literal["image"]
    value: Union[Path, str, "Image.Image"]  # absolute path or PIL


class VideoItem(TypedDict):
    type: Literal["video"]
    value: Union[Path, str]


MessageItem = Union[TextItem, ImageItem, VideoItem]
Message = list[MessageItem]


# ---------------------------------------------------------------------------
# Prediction — structured return value
# ---------------------------------------------------------------------------

@dataclass
class TraceStep:
    """One step in an interleaved reasoning trace."""
    round: int
    kind: Literal["text", "image"]
    text: str | None = None
    image: Path | None = None
    triggered_by: str | None = None       # "model_marker" | "forced" | None
    elapsed_s: float = 0.0


@dataclass
class Prediction:
    """Inference result — never a bare string.

    ``text`` is the final text output used for answer extraction.
    ``generated_images`` carries paths named with sample_id for auditability.
    ``trace`` records each round's input/output/timing.
    ``error`` is set when inference fails (single-sample failure, not fatal).
    ``meta`` stores strategy/rounds/draw_triggered/backend.
    """
    text: str = ""
    generated_images: list[Path] = field(default_factory=list)
    trace: list[TraceStep] = field(default_factory=list)
    error: str | None = None
    meta: dict = field(default_factory=dict)
    # Expected meta keys:
    #   strategy: str          — which strategy produced this
    #   rounds: int            — actual rounds executed
    #   draw_triggered: bool   — whether image generation actually happened
    #   backend: str           — which backend produced this


# ---------------------------------------------------------------------------
# TaskSample — data-layer product
# ---------------------------------------------------------------------------

@dataclass
class TaskSample:
    """One evaluation sample.

    ``gold`` is isolated from ``message`` — backends never see it.
    """
    id: str
    message: Message
    gold: str               # A-D, only for eval
    meta: dict = field(default_factory=dict)
    # Expected meta keys: view, variant, task_id, question_type, oracle,
    #   images (relative paths), sample_id, case_id, scheme, ...


# ---------------------------------------------------------------------------
# Capabilities — backend ability declaration
# ---------------------------------------------------------------------------

class Capabilities(NamedTuple):
    """What a backend can do. Strategies check these at startup (fail-fast)."""
    batch: bool                  # true batch inference (submit all at once)
    draw: bool                   # can generate images
    native_interleave: bool      # has native interleave loop (single KV-cache across rounds)
    max_images: int              # max images per single input
    video: bool


# ---------------------------------------------------------------------------
# RunContext — passed to strategies
# ---------------------------------------------------------------------------

@dataclass
class RunContext:
    """Runtime context passed to Strategy.run()."""
    output_dir: Path
    gen_kw: dict = field(default_factory=dict)
    max_rounds: int = 3
    marker: str = "<image_start>"
    save_generated: bool = True
    draw_followup_text: str = "Based on the intermediate image above, answer the question."
    view: str = ""
    task: str = ""
    variant: str = ""

    def draw_instruction(self, sample: TaskSample) -> str:
        """Per-question_type draw instruction (for external_draw strategy)."""
        qt = sample.meta.get("question_type", "")
        return _DRAW_INSTRUCTIONS.get(qt, "Draw a helpful intermediate diagram.")


_DRAW_INSTRUCTIONS: dict[str, str] = {
    "direction": "Draw an arrow from the green dot to the purple dot to indicate the direction.",
    "nearest_point": "Mark lines from the reference point to each candidate point.",
    "composite_route_distance": "Trace the two routes being compared.",
    "segment_building_count": "Highlight the specified segment and the side with buildings to count.",
    "route_validity": "Annotate each candidate route's direction of travel.",
    "waypoint_ordering": "Connect the waypoints in order.",
}
