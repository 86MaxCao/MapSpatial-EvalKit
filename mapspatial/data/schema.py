"""JSONL record → TaskSample conversion.

Fields we use: id, question, answer, images, task_id, question_type, view, variant, oracle.
Fields we don't put in Message: answer (gold only), input_images/image (redundant with images),
conversations (ShareGPT training format, not needed for inference).
"""

from __future__ import annotations

import json
from pathlib import Path

from ..types import TaskSample, Message
from ..messages import strip_placeholders


def parse_record(record: dict, data_root: Path) -> TaskSample:
    """Convert a single JSONL record to a TaskSample.

    Path resolution happens here — backends always see absolute paths.
    gold is isolated in TaskSample.gold, never in Message.
    """
    sample_id = record.get("id", "")
    question = record.get("question", "")
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

    message = _build_message(question, image_abs, task_id, question_type, multiple_choice)

    gold = record.get("answer", "")

    meta = {
        "view": record.get("view", ""),
        "variant": record.get("variant", ""),
        "task_id": task_id,
        "question_type": question_type,
        "oracle": record.get("oracle", False),
        "images": image_rels,
        "sample_id": record.get("sample_id", ""),
        "case_id": record.get("case_id", ""),
        "scheme": record.get("scheme", ""),
        "multiple_choice": multiple_choice,
    }

    return TaskSample(id=sample_id, message=message, gold=gold, meta=meta)


def _build_message(
    question: str,
    image_paths: list[Path],
    task_id: str,
    question_type: str,
    multiple_choice: dict | None,
) -> Message:
    """Construct interleaved Message from question + image paths.

    Single image (t1/t2/t3/t4-waypoint_ordering): [image, text]
    Multi image (t4 route_validity, 4 images): [text, image, text, image, ...]
    """
    if question_type == "route_validity" and len(image_paths) > 1:
        return _build_multi_image_message(question, image_paths, multiple_choice)

    # Default: image(s) first, then text (image-initial for Bagel compatibility)
    msg: Message = []
    for p in image_paths:
        msg.append({"type": "image", "value": p})
    msg.append({"type": "text", "value": question})
    return msg


def _build_multi_image_message(
    question: str,
    image_paths: list[Path],
    multiple_choice: dict | None,
) -> Message:
    """Build interleaved text+image message for T4 route_validity.

    Format:
      [text "Which route is valid... Option A:", image A, text "Option B:", image B, ...]
    """
    msg: Message = []
    # Extract option labels from multiple_choice if available
    choices = multiple_choice.get("choices", []) if multiple_choice else []
    if choices and len(choices) == len(image_paths):
        # Prepend the question (without the options part, since we interleave)
        # The question field already contains the full question including options
        # We need to reconstruct the interleave format
        prompt = multiple_choice.get("prompt", question)
        # Split: put prompt first, then interleaved options
        # For route_validity, the prompt is like "Which route...?\n\nOption A: ...\nOption B: ..."
        # We'll just use the question as-is before the first option
        msg.append({"type": "text", "value": prompt})
        for i, (choice, img) in enumerate(zip(choices, image_paths)):
            key = choice.get("key", chr(ord("A") + i))
            msg.append({"type": "image", "value": img})
            if i < len(choices) - 1:
                msg.append({"type": "text", "value": f"Option {chr(ord('A') + i + 1)}:"})
    else:
        # Fallback: text first, then images
        msg.append({"type": "text", "value": question})
        for p in image_paths:
            msg.append({"type": "image", "value": p})

    return msg


def iter_jsonl(path: Path):
    """Yield parsed JSON objects from a JSONL file."""
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)
