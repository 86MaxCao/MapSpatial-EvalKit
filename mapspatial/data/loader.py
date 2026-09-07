"""Data loader — view×task×variant discovery and traversal.

Yields (FileKey, list[TaskSample]) per file. Empty files yield empty list
(blank/t4 is legitimately empty). This lets summary.json distinguish
"didn't run" from "no data".

Layouts:
  tree — ``{view}/{task}/{variant}.jsonl`` (default; existing eval scripts).
  hf   — HuggingFace pack: ``{input_dir}/data/t1_direct.jsonl`` + ``images/``.
         Records are regrouped onto the same FileKey as the tree layout.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Iterator

from ..types import TaskSample
from .schema import (
    cell_variant_from_record,
    iter_jsonl,
    parse_record,
    task_from_record,
)

FileKey = tuple[str, str, str]  # (view, task, variant)


def iter_samples(
    input_dir: Path,
    data_root: Path,
    views: list[str],
    tasks: list[str],
    variants: list[str],
    layout: str = "tree",
) -> Iterator[tuple[FileKey, list[TaskSample]]]:
    """Iterate cells in task → view → variant order, yielding (FileKey, samples).

    FileKey stays (view, task, variant). Empty files produce an empty list,
    not a skip — so summary.json can distinguish "didn't run" from "no data".
    """
    if layout == "hf":
        yield from _iter_samples_hf(input_dir, data_root, views, tasks, variants)
        return
    if layout not in {"tree", "hf"}:
        raise ValueError(f"Unknown layout {layout!r}; expected 'tree' or 'hf'")

    for task in tasks:
        for view in views:
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


def _hf_jsonl_dir(input_dir: Path) -> Path:
    data_dir = input_dir / "data"
    if not data_dir.is_dir():
        raise FileNotFoundError(
            f"--layout hf expects {{input-dir}}/data/*.jsonl; missing {data_dir}"
        )
    return data_dir


def _iter_samples_hf(
    input_dir: Path,
    data_root: Path,
    views: list[str],
    tasks: list[str],
    variants: list[str],
) -> Iterator[tuple[FileKey, list[TaskSample]]]:
    jsonl_dir = _hf_jsonl_dir(input_dir)
    wanted_views = set(views)
    wanted_tasks = set(tasks)
    wanted_variants = set(variants)
    grouped: dict[FileKey, list[TaskSample]] = defaultdict(list)

    paths: list[Path] = []
    for task in tasks:
        paths.extend(sorted(jsonl_dir.glob(f"{task}_*.jsonl")))

    for path in paths:
        for record in iter_jsonl(path):
            try:
                view = str(record.get("view") or "")
                task = task_from_record(record)
                variant = cell_variant_from_record(record)
                if view not in wanted_views or task not in wanted_tasks:
                    continue
                if variant not in wanted_variants:
                    continue
                grouped[(view, task, variant)].append(parse_record(record, data_root))
            except Exception as e:
                import sys
                print(f"WARNING: failed to parse record in {path}: {e}", file=sys.stderr)

    for task in tasks:
        for view in views:
            for variant in variants:
                key: FileKey = (view, task, variant)
                if key not in grouped:
                    continue
                yield key, grouped[key]


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
