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
    # question_with_options embeds the option list; bare question hides options
    question = record.get("question_with_options") or record.get("question", "")
    # strip any placeholders that might sneak in from the question field
    question = strip_placeholders(question)

    # Resolve image paths to absolute
    image_rels = record.get("images", [])
    image_abs = [(data_root / rel).resolve() for rel in image_rels]

    # Build Message: image(s) first, then text (image-initial convention)
    # T4 route_validity is special — interleave text+images
    task_id = record.get("task_id", "")
    question_type = record.get("question_type", "")
    multiple_choice = record.get("multiple_choice")
    options = record.get("options", [])

    # Transform-layer records carry the transform name in `variant`
    # (e.g. "mirror_h_rot90"); base records have variant=="base". The runner
    # materializes transformed images from this tag (see media.materialize_transforms).
    variant_name = record.get("variant", "")
    layer = record.get("layer", "")
    transform = variant_name if (layer == "transform" and variant_name and variant_name != "base") else None

    message = _build_message(
        question, image_abs, task_id, question_type, multiple_choice, options, transform
    )

    gold, gold_text = _gold_from_record(record)

    meta = {
        "view": record.get("view", "") or record.get("tile_type", ""),
        "variant": record.get("variant", ""),
        "task_id": task_id,
        "question_type": question_type,
        "oracle": record.get("oracle", False),
        "evidence_condition": (
            record.get("evidence_condition")
            or record.get("mode")
            or _infer_evidence_condition(record)
        ),
        "track": record.get("track", ""),
        "images": image_rels,
        "sample_id": record.get("sample_id", ""),
        "case_id": record.get("case_id", ""),
        "scheme": record.get("scheme", ""),
        "multiple_choice": multiple_choice,
        "system_prompt": record.get("system_prompt", ""),
        "gold_text": gold_text,
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
