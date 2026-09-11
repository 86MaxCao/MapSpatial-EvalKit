"""Unified message construction — placeholder normalization + chat format conversion.

Consolidates 8 places in the predecessor pipeline where <image>/<video> placeholder handling
was written per-backend with 5 different behaviors.

Data layer produces Messages WITHOUT placeholders. When a backend needs
placeholders, it calls to_placeholder_prompt() here.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Union

from PIL import Image

from .types import Message

_PLACEHOLDER_RE = re.compile(r"<(?:image|video)>")
_HAS_PLACEHOLDER = re.compile(r"<(?:image|video)>")


def strip_placeholders(text: str) -> str:
    """Remove <image>/<video> placeholders from text."""
    return _PLACEHOLDER_RE.sub("", text).strip()


def has_placeholders(text: str) -> bool:
    """Check if text contains image/video placeholders."""
    return bool(_HAS_PLACEHOLDER.search(text))


def to_openai_content(msg: Message) -> list[dict]:
    """API-style content: [{"type":"image_url","image_url":{...}}, {"type":"text","text":...}]"""
    out: list[dict] = []
    for item in msg:
        if item["type"] == "text":
            out.append({"type": "text", "text": item["value"]})
        elif item["type"] == "image":
            v = item["value"]
            if isinstance(v, str) and v.startswith(("http://", "https://", "data:")):
                url = v
            elif isinstance(v, Path):
                url = str(v)
            elif isinstance(v, Image.Image):
                # caller should have materialized to path for API
                raise TypeError("PIL Image in API content — materialize to path first")
            else:
                url = str(v)
            out.append({"type": "image_url", "image_url": {"url": url}})
        elif item["type"] == "video":
            # API backends don't support video directly; frames should be extracted upstream
            raise TypeError("video item in API content — extract frames first")
    return out


def to_qwen_content(msg: Message) -> list[dict]:
    """Qwen-style content: {"type":"image","image":path} + {"type":"text","text":...}"""
    out: list[dict] = []
    for item in msg:
        if item["type"] == "text":
            out.append({"type": "text", "text": item["value"]})
        elif item["type"] == "image":
            v = item["value"]
            if isinstance(v, Image.Image):
                out.append({"type": "image", "image": v})
            else:
                out.append({"type": "image", "image": str(v)})
        elif item["type"] == "video":
            raise TypeError("video not supported in qwen content")
    return out


def to_url_content(msg: Message) -> list[dict]:
    """InternVL native / GLM style: {"type":"image","url":path}"""
    out: list[dict] = []
    for item in msg:
        if item["type"] == "text":
            out.append({"type": "text", "text": item["value"]})
        elif item["type"] == "image":
            v = item["value"]
            out.append({"type": "image", "url": str(v) if not isinstance(v, Image.Image) else v})
        elif item["type"] == "video":
            raise TypeError("video not supported in url content")
    return out


def to_placeholder_prompt(msg: Message, token: str = "<image>") -> tuple[str, list[Path]]:
    """Placeholder style: returns (text_with_N_tokens, image_paths).

    Used by InternVL-custom / MiniCPM-V / SenseNova-U1.
    """
    parts: list[str] = []
    image_paths: list[Path] = []
    for item in msg:
        if item["type"] == "text":
            parts.append(item["value"])
        elif item["type"] == "image":
            v = item["value"]
            if isinstance(v, Image.Image):
                raise TypeError("PIL Image in placeholder prompt — materialize to path first")
            image_paths.append(Path(v))
            parts.append(token)
        elif item["type"] == "video":
            image_paths.append(Path(item["value"]))
            parts.append(token)
    return "\n".join(parts), image_paths


def to_interleave_list(msg: Message) -> list[Union[Image.Image, str]]:
    """Bagel-style native interleave format: [PIL, str, PIL, str, ...].

    Requires image-initial input (Bagel InterleaveInferencer constraint).
    """
    out: list[Union[Image.Image, str]] = []
    for item in msg:
        if item["type"] == "text":
            out.append(item["value"])
        elif item["type"] == "image":
            v = item["value"]
            if isinstance(v, Image.Image):
                out.append(v)
            else:
                from .media import load_image
                out.append(load_image(v))
        elif item["type"] == "video":
            raise TypeError("video not supported in interleave list")
    return out


def extract_image_paths(msg: Message) -> list[Path]:
    """Return all image paths from a Message (for preflight checks)."""
    paths = []
    for item in msg:
        if item["type"] in ("image", "video"):
            v = item["value"]
            if not isinstance(v, Image.Image):
                paths.append(Path(v))
    return paths
