"""Data loader — view×task×variant discovery and traversal.

Yields (FileKey, list[TaskSample]) per file. Empty files yield empty list
(blank/t4 is legitimately empty). This lets summary.json distinguish
"didn't run" from "no data".
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

from ..types import TaskSample
from .schema import parse_record, iter_jsonl

FileKey = tuple[str, str, str]  # (view, task, variant)


def iter_samples(
    input_dir: Path,
    data_root: Path,
    views: list[str],
    tasks: list[str],
    variants: list[str],
) -> Iterator[tuple[FileKey, list[TaskSample]]]:
    """Iterate over (view, task, variant) combinations, yielding (FileKey, samples).

    Empty files produce an empty list, not a skip — so summary.json can
    distinguish "didn't run" from "no data".
    """
    for view in views:
        for task in tasks:
            for variant in variants:
                key: FileKey = (view, task, variant)
                path = input_dir / view / task / f"{variant}.jsonl"
                if not path.exists():
                    continue
                samples = []
                for record in iter_jsonl(path):
                    try:
                        samples.append(parse_record(record, data_root))
                    except Exception as e:
                        import sys
                        print(f"WARNING: failed to parse record in {path}: {e}", file=sys.stderr)
                yield key, samples


def count_samples(path: Path) -> int:
    """Count lines in a JSONL file (for manifest verification)."""
    if not path.exists():
        return 0
    count = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                count += 1
    return count


def load_manifest(input_dir: Path) -> dict:
    """Load manifest.json from the data directory."""
    manifest_path = input_dir / "manifest.json"
    if not manifest_path.exists():
        return {}
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)
