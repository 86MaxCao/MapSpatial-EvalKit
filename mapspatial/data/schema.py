"""JSONL record → TaskSample conversion.

Fields we use: id, question, answer, images, task_id, question_type, view, variant,
oracle, evidence_condition, track.
Fields we don't put in Message: answer (gold only), input_images/image (redundant with images),
conversations (ShareGPT training format, not needed for inference).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from ..types import TaskSample, Message
from ..messages import strip_placeholders


def task_from_record(record: dict) -> str:
    """Normalize ``task_id`` (``T1`` / ``t1``) to the cell task key ``t1``."""
    raw = str(record.get("task_id") or "").strip()
    if raw.lower().startswith("t") and len(raw) >= 2:
        return raw.lower()
    return raw.lower()


def evidence_condition_from_record(record: dict) -> str:
    """direct / oracle / ... from HF ``condition`` or the tree fields."""
    return (
        record.get("evidence_condition")
        or record.get("mode")
        or record.get("condition")
        or _infer_evidence_condition(record)
    )


def cell_variant_from_record(record: dict) -> str:
    """Map a record onto the tree cell path, e.g. ``transform/rot90/direct``."""
    layer = str(record.get("layer") or "base").strip() or "base"
    name = record.get("variant")
    if name is None or str(name).strip() == "":
        name = "base"
    else:
        name = str(name).strip()
    condition = evidence_condition_from_record(record)
    if layer == "base":
        return f"base/{condition}"
    if layer == "transform":
        return f"transform/{name}/{condition}"
    if layer == "world":
        return f"world/{name}/{condition}"
    if name in {"", "base"}:
        return f"{layer}/{condition}"
    return f"{layer}/{name}/{condition}"


def _stem_question(question: str) -> str:
    """Drop trailing inline ``A. ...`` / ``Options:`` lines from the stem."""
    lines = question.rstrip().splitlines()
    while lines:
        s = lines[-1].strip()
        if not s:
            lines.pop()
            continue
        if s.lower() == "options:" or re.match(r"^[A-Z][.)]\s+\S", s):
            lines.pop()
            continue
        break
    return "\n".join(lines).rstrip()


def _question_text(record: dict) -> str:
    """Prompt shown to the model.

    Tree records already embed shuffled options in ``question_with_options``.
    HF records have a bare ``question`` plus a shuffled ``options`` list — and
    T2 sometimes also inlines *unshuffled* A/B lines in ``question``. Always
    rebuild from ``options`` when ``question_with_options`` is absent so gold
    letters stay consistent.
    """
    embedded = record.get("question_with_options")
    if embedded:
        return strip_placeholders(str(embedded))
    stem = _stem_question(strip_placeholders(str(record.get("question") or "")))
    options = record.get("options") or []
    if options:
        return stem + "\n\nOptions:\n" + "\n".join(str(o) for o in options)
    return stem


def _nested_meta(record: dict) -> dict:
    raw = record.get("meta")
    return raw if isinstance(raw, dict) else {}


def _gold_from_record(record: dict) -> tuple[str, str]:
    """(gold, gold_text) — normalize gold to an option letter when possible."""
    answer = record.get("answer", "")
    text = "" if answer is None else str(answer).strip()

    letter = record.get("answer_letter")
    if not letter:
        for opt in record.get("options", []):
            m = re.match(r"^([A-Z])[.\s]\s*(.+)$", str(opt).strip(), re.IGNORECASE)
            if m and m.group(2).strip() == text:
                letter = m.group(1).upper()
                break
    if not letter and re.fullmatch(r"[A-Z](\s*,\s*[A-Z])*", text, re.IGNORECASE):
        letter = text.upper()

    gold = str(letter).strip() if letter else text
    return gold, text


def parse_record(record: dict, data_root: Path) -> TaskSample:
    """Convert a single JSONL record to a TaskSample.

    Path resolution happens here — backends always see absolute paths.
    gold is isolated in TaskSample.gold, never in Message.
    """
    sample_id = record.get("id", "")
    question = _question_text(record)

    # Resolve image paths to absolute (tree: benchmark_images_t*/...;
    # HF pack: images/t1/... relative to the repo root).
    image_rels = record.get("images", [])
    image_abs = [(data_root / rel).resolve() for rel in image_rels]

    # Build Message: image(s) first, then text (image-initial convention)
    # T4 route_validity is special — interleave text+images
    task_id = record.get("task_id", "")
    question_type = record.get("question_type", "")
    multiple_choice = record.get("multiple_choice")
    options = record.get("options", [])
    nested = _nested_meta(record)

    # Transform-layer records carry the transform name in `variant`
    # (e.g. "mirror_h_rot90"); base records have variant=="base" or null.
    # HF transform rows still point at the *base* PNG — apply at load time
    # (see media.materialize_transforms). World rows already have their own PNG.
    variant_name = record.get("variant") or ""
    if variant_name == "":
        variant_name = "base"
    layer = record.get("layer") or ""
    transform = (
        variant_name
        if (layer == "transform" and variant_name and variant_name != "base")
        else None
    )

    message = _build_message(
        question, image_abs, task_id, question_type, multiple_choice, options, transform
    )

    gold, gold_text = _gold_from_record(record)
    condition = evidence_condition_from_record(record)
    oracle = record.get("oracle")
    if oracle is None:
        oracle = condition == "oracle"

    meta = {
        "view": record.get("view", "") or record.get("tile_type", "") or nested.get("tile_type", ""),
        "variant": variant_name,
        "task_id": task_id,
        "question_type": question_type,
        "oracle": bool(oracle),
        "evidence_condition": condition,
        "track": record.get("track", ""),
        "images": image_rels,
        "sample_id": record.get("sample_id", "") or nested.get("instance_id", ""),
        "case_id": record.get("case_id", "") or nested.get("case_id", ""),
        "scheme": record.get("scheme", "") or nested.get("scheme", ""),
        "instance_id": record.get("instance_id", "") or nested.get("instance_id", ""),
        "multiple_choice": multiple_choice,
        "system_prompt": record.get("system_prompt", ""),
        "gold_text": gold_text,
        "layer": layer,
    }

    return TaskSample(id=sample_id, message=message, gold=gold, meta=meta)


def _infer_evidence_condition(record: dict) -> str:
    """Infer the legacy condition name when new metadata is absent."""
    variant = str(record.get("variant", "")).lower()
    if variant in {"wrong_oracle", "shuffled_oracle", "masked_prompt"}:
        return variant
    if record.get("oracle", False) or variant == "oracle":
        return "oracle"
    return "direct"


def _build_message(
    question: str,
    image_paths: list[Path],
    task_id: str,
    question_type: str,
    multiple_choice: dict | None,
    options: list | None = None,
    transform: str | None = None,
) -> Message:
    """Construct interleaved Message from question + image paths.

    Single image (t1/t2/t3/t4-waypoint_ordering): [image, text]
    Multi image (t4 route_validity, 4 images): [text, image, text, image, ...]

    transform is the benchmark transform-variant name (e.g. "mirror_h_rot90")
    attached to each image item so backends apply it at load time. base/None
    means identity. This lets the JSONL `images` field point at the base
    image while the model sees the transformed view (no pre-rendered PNGs).
    """
    if question_type == "route_validity" and len(image_paths) > 1:
        return _build_multi_image_message(
            question, image_paths, multiple_choice, options or [], transform
        )

    # Default: image(s) first, then text (image-initial for Bagel compatibility)
    msg: Message = []
    for p in image_paths:
        msg.append({"type": "image", "value": p, "transform": transform})
    msg.append({"type": "text", "value": question})
    return msg


def _build_multi_image_message(
    question: str,
    image_paths: list[Path],
    multiple_choice: dict | None,
    options: list,
    transform: str | None = None,
) -> Message:
    """Build interleaved text+image message for T4 route_validity.

    Format:
      [text "Which route is valid... Option A:", image A, text "Option B:", image B, ...]

    Option keys come from multiple_choice.choices, or are parsed from the
    options strings ("A. red line" → "A") when multiple_choice is absent.
    """
    keys: list[str] = []
    if multiple_choice and multiple_choice.get("choices"):
        keys = [
            str(c.get("key", chr(ord("A") + i)))
            for i, c in enumerate(multiple_choice["choices"])
        ]
    else:
        for i, opt in enumerate(options):
            m = re.match(r"^([A-Z])[.\s]", str(opt).strip(), re.IGNORECASE)
            keys.append(m.group(1).upper() if m else chr(ord("A") + i))

    prompt = multiple_choice.get("prompt", question) if multiple_choice else question

    if keys and len(keys) == len(image_paths):
        msg: Message = [{"type": "text", "value": prompt}]
        for i, img in enumerate(image_paths):
            msg.append({"type": "image", "value": img, "transform": transform})
            if i < len(keys) - 1:
                msg.append({"type": "text", "value": f"Option {keys[i + 1]}:"})
        return msg

    # Fallback: text first, then images
    msg = [{"type": "text", "value": question}]
    for p in image_paths:
        msg.append({"type": "image", "value": p, "transform": transform})
    return msg


def iter_jsonl(path: Path):
    """Yield parsed JSON objects from a JSONL file."""
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)
