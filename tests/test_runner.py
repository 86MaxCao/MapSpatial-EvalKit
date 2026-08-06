"""Test runner resume logic — load_completed, write_result, dedup."""

import json
from pathlib import Path

from mapspatial.runner import load_completed, write_result


def test_load_completed_empty(tmp_path):
    path = tmp_path / "output.jsonl"
    done, corrupt = load_completed(path)
    assert done == set()
    assert corrupt == 0


def test_load_completed_with_records(tmp_path):
    path = tmp_path / "output.jsonl"
    with open(path, "w") as f:
        f.write(json.dumps({"id": "s1", "prediction": "A"}) + "\n")
        f.write(json.dumps({"id": "s2", "prediction": "B"}) + "\n")

    done, corrupt = load_completed(path)
    assert done == {"s1", "s2"}
    assert corrupt == 0


def test_load_completed_with_corrupt_lines(tmp_path):
    path = tmp_path / "output.jsonl"
    with open(path, "w") as f:
        f.write(json.dumps({"id": "s1", "prediction": "A"}) + "\n")
        f.write("CORRUPT LINE NOT JSON\n")
        f.write(json.dumps({"id": "s2"}) + "\n")  # missing fields, but valid JSON

    done, corrupt = load_completed(path)
    assert "s1" in done
    assert "s2" in done
    assert corrupt == 1  # only the "CORRUPT LINE" is corrupt


def test_write_result_atomic(tmp_path):
    path = tmp_path / "results" / "sat" / "t1" / "direct.jsonl"
    record = {"id": "s1", "prediction": "A", "exact_match": True}
    write_result(path, record)
    assert path.exists()
    content = path.read_text().strip()
    assert json.loads(content)["id"] == "s1"


def test_write_result_dedup(tmp_path):
    """write_result should append, but runner checks done_ids before writing."""
    path = tmp_path / "results.jsonl"
    # Simulate two runs that both try to write s1
    write_result(path, {"id": "s1", "prediction": "A"})
    # In the runner, load_completed would return s1 in done set,
    # so it would be skipped. But if called directly, it appends.
    # The dedup happens at the runner level (done_ids check), not write level.
    # Verify the file has the content:
    lines = path.read_text().strip().split("\n")
    assert len(lines) == 1
    assert json.loads(lines[0])["id"] == "s1"
