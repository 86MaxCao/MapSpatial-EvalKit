"""Test messages.py — placeholder stripping and format conversion."""

from pathlib import Path

from mapspatial.messages import (
    strip_placeholders, has_placeholders, to_placeholder_prompt,
    to_qwen_content, extract_image_paths,
)
from mapspatial.types import Message


def test_strip_placeholders():
    assert strip_placeholders("<image>\nWhat direction?") == "What direction?"
    assert strip_placeholders("<video><image>text") == "text"
    assert strip_placeholders("no placeholders") == "no placeholders"


def test_has_placeholders():
    assert has_placeholders("<image> some text")
    assert has_placeholders("text <video>")
    assert not has_placeholders("plain text")


def test_to_placeholder_prompt():
    msg: Message = [
        {"type": "image", "value": Path("/tmp/a.png")},
        {"type": "text", "value": "What direction?"},
        {"type": "image", "value": Path("/tmp/b.png")},
    ]
    prompt, images = to_placeholder_prompt(msg)
    assert "<image>" in prompt
    assert len(images) == 2
    assert images[0] == Path("/tmp/a.png")


def test_to_qwen_content():
    msg: Message = [
        {"type": "image", "value": "/tmp/a.png"},
        {"type": "text", "value": "What is this?"},
    ]
    content = to_qwen_content(msg)
    assert content[0] == {"type": "image", "image": "/tmp/a.png"}
    assert content[1] == {"type": "text", "text": "What is this?"}


def test_extract_image_paths():
    msg: Message = [
        {"type": "text", "value": "hello"},
        {"type": "image", "value": Path("/tmp/a.png")},
        {"type": "image", "value": Path("/tmp/b.png")},
    ]
    paths = extract_image_paths(msg)
    assert len(paths) == 2
    assert paths[0] == Path("/tmp/a.png")
