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
    forced_interleave: bool = False  # same-call modality switch + reconsume + continue


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
    draw_followup_text: str = (
        "The last image is a generated visual scratchpad, not an original map "
        "and not an answer option. Use it together with the original map "
        "image(s) to answer the original question."
    )
    generation_system_prompt: str = ""
    g2u_seed: int = 42
    scratchpad_policy: str = "typed"
    view: str = ""
    task: str = ""
    variant: str = ""

    @property
    def understand_followup(self) -> str:
        if self.scratchpad_policy == "autonomous":
            text = str(
                _load_g2u_config().get("autonomous_understand_followup") or ""
            ).strip()
            if text:
                return text
        return self.draw_followup_text

    def draw_instruction(self, sample: TaskSample) -> str:
        """Per-question_type draw instruction (shared by C-R and C-F)."""
        qt = sample.meta.get("question_type", "")
        yaml_instructions = _load_g2u_config().get("draw_instruction") or {}
        if qt in yaml_instructions:
            return yaml_instructions[qt]
        return _DRAW_INSTRUCTIONS.get(qt, "Draw a helpful intermediate diagram.")

    def visual_generation_instruction(self, sample: TaskSample) -> str:
        """G-stage instruction.

        typed: shared system prompt + question-type draw text (default).
        autonomous: one generic prompt; no per-type draw_instruction.
        """
        if self.scratchpad_policy == "autonomous":
            text = str(
                _load_g2u_config().get("autonomous_generation_prompt") or ""
            ).strip()
            if text:
                return text
            return (
                self.generation_system_prompt
                or _load_g2u_config().get("generation_system_prompt")
                or ""
            ).strip()
        parts = []
        sys_p = (self.generation_system_prompt or _load_g2u_config().get("generation_system_prompt") or "").strip()
        if sys_p:
            parts.append(sys_p)
        task = self.draw_instruction(sample).strip()
        if task:
            parts.append(task)
        return "\n\n".join(parts)


def _load_g2u_config() -> dict:
    """Load configs/strategies/g2u.yaml, falling back to external_draw.yaml."""
    global _G2U_CONFIG
    if _G2U_CONFIG is not None:
        return _G2U_CONFIG
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    g2u_path = os.path.join(root, "configs", "strategies", "g2u.yaml")
    legacy_path = os.path.join(root, "configs", "strategies", "external_draw.yaml")
    cfg: dict = {}
    try:
        import yaml
        path = g2u_path if os.path.isfile(g2u_path) else legacy_path
        with open(path) as f:
            cfg = yaml.safe_load(f) or {}
    except Exception:
        cfg = {}
    _G2U_CONFIG = cfg
    return _G2U_CONFIG


def load_g2u_defaults() -> dict:
    """Public helper for runner/strategy setup."""
    return dict(_load_g2u_config())


_G2U_CONFIG: dict | None = None


_DRAW_INSTRUCTIONS: dict[str, str] = {
    "direction": "Draw an arrow from the green dot to the purple dot to indicate the direction.",
    "nearest_point": "Mark lines from the reference point to each candidate point.",
    "composite_route_distance": "Trace the two routes being compared.",
    "segment_building_count": "Highlight the specified segment and the side with buildings to count.",
    "route_validity": "Annotate each candidate route's direction of travel.",
    "waypoint_ordering": "Connect the waypoints in order.",
}
