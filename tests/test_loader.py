"""Tree vs HuggingFace dataset layouts."""

import json
from pathlib import Path

import pytest
from PIL import Image

from mapspatial.config import resolve_data_paths
from mapspatial.data.loader import iter_samples
from mapspatial.data.schema import (
    cell_variant_from_record,
    parse_record,
    task_from_record,
)


def _write_png(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (4, 4), (255, 0, 0)).save(path)


def test_resolve_data_paths_tree_requires_data_dir(tmp_path):
    with pytest.raises(ValueError, match="data-dir"):
        resolve_data_paths("tree", tmp_path, None)


def test_resolve_data_paths_hf_defaults_data_dir(tmp_path):
    input_dir, data_dir = resolve_data_paths("hf", tmp_path, None)
    assert input_dir == tmp_path
    assert data_dir == tmp_path


def test_cell_variant_from_hf_fields():
    assert cell_variant_from_record({
        "layer": "base", "variant": None, "condition": "direct",
    }) == "base/direct"
    assert cell_variant_from_record({
        "layer": "transform", "variant": "rot90", "condition": "oracle",
    }) == "transform/rot90/oracle"
    assert cell_variant_from_record({
        "layer": "world", "variant": "intervention_001", "condition": "direct",
    }) == "world/intervention_001/direct"
    assert task_from_record({"task_id": "T1"}) == "t1"


def test_tree_layout_still_reads_nested_jsonl(tmp_path):
    img = tmp_path / "benchmark_images_t1" / "x.png"
    _write_png(img)
    jsonl = tmp_path / "jsonl" / "blank" / "t1" / "base" / "direct.jsonl"
    jsonl.parent.mkdir(parents=True)
    rec = {
        "id": "tree-1",
        "task_id": "T1",
        "layer": "base",
        "variant": "base",
        "view": "blank",
        "oracle": False,
        "question": "Which way?",
        "question_with_options": "Which way?\n\nOptions:\nA. north\nB. south",
        "options": ["A. north", "B. south"],
        "answer": "A",
        "answer_letter": "A",
        "question_type": "direction",
        "images": ["benchmark_images_t1/x.png"],
        "system_prompt": "sys",
    }
    jsonl.write_text(json.dumps(rec) + "\n")

    cells = list(iter_samples(
        tmp_path / "jsonl", tmp_path,
        views=["blank"], tasks=["t1"], variants=["base/direct"],
        layout="tree",
    ))
    assert len(cells) == 1
    key, samples = cells[0]
    assert key == ("blank", "t1", "base/direct")
    assert samples[0].gold == "A"
    text = next(i["value"] for i in samples[0].message if i["type"] == "text")
    assert "Options:" in text
    assert samples[0].message[0]["transform"] is None


def test_hf_layout_groups_by_tree_cell(tmp_path):
    img = tmp_path / "images" / "t1" / "c_x" / "base.png"
    _write_png(img)
    jsonl = tmp_path / "data" / "t1_direct.jsonl"
    jsonl.parent.mkdir(parents=True)
    records = [
        {
            "id": "hf-base",
            "task_id": "T1",
            "layer": "base",
            "variant": None,
            "view": "blank",
            "condition": "direct",
            "question_type": "direction",
            "question": "Which way?",
            "options": ["A. north", "B. south"],
            "answer": "A",
            "answer_letter": "A",
            "images": ["images/t1/c_x/base.png"],
            "system_prompt": "sys",
            "meta": {"case_id": "c_x", "instance_id": "q_1"},
        },
        {
            "id": "hf-rot90",
            "task_id": "T1",
            "layer": "transform",
            "variant": "rot90",
            "view": "blank",
            "condition": "direct",
            "question_type": "direction",
            "question": "Which way?",
            "options": ["A. north", "B. south"],
            "answer": "B",
            "answer_letter": "B",
            "images": ["images/t1/c_x/base.png"],
            "system_prompt": "sys",
            "meta": {"case_id": "c_x"},
        },
    ]
    jsonl.write_text("".join(json.dumps(r) + "\n" for r in records))

    cells = {
        key: samples
        for key, samples in iter_samples(
            tmp_path, tmp_path,
            views=["blank"], tasks=["t1"],
            variants=["base/direct", "transform/rot90/direct"],
            layout="hf",
        )
    }
    assert set(cells) == {("blank", "t1", "base/direct"), ("blank", "t1", "transform/rot90/direct")}
    base = cells[("blank", "t1", "base/direct")][0]
    rot = cells[("blank", "t1", "transform/rot90/direct")][0]
    assert base.meta["case_id"] == "c_x"
    assert base.message[0]["transform"] is None
    assert rot.message[0]["transform"] == "rot90"
    assert rot.message[0]["value"] == img.resolve()


def test_hf_rebuilds_options_when_question_letters_diverge(tmp_path):
    rec = {
        "id": "t2-mismatch",
        "task_id": "T2",
        "layer": "base",
        "variant": None,
        "view": "blank",
        "condition": "direct",
        "question_type": "composite_euclidean_distance",
        "question": "Which route is shorter?\nA. gray to yellow\nB. gray to blue to black",
        "options": ["A. gray to blue to black", "B. gray to yellow"],
        "answer": "B",
        "answer_letter": "B",
        "images": ["images/t2/x.png"],
    }
    sample = parse_record(rec, tmp_path)
    text = next(i["value"] for i in sample.message if i["type"] == "text")
    assert sample.gold == "B"
    assert "Options:\nA. gray to blue to black\nB. gray to yellow" in text
    assert text.startswith("Which route is shorter?")
    # Unshuffled inline letters must not survive.
    assert "A. gray to yellow" not in text.split("Options:", 1)[1]


def test_hf_missing_data_dir_errors(tmp_path):
    with pytest.raises(FileNotFoundError, match="data/"):
        list(iter_samples(
            tmp_path, tmp_path,
            views=["blank"], tasks=["t1"], variants=["base/direct"],
            layout="hf",
        ))
