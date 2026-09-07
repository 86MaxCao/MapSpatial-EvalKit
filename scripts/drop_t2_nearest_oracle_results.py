#!/usr/bin/env python3
"""Drop T2 nearest-point oracle records from MapSpatial results.

Targets nearest_point and directional_nearest_point in both base and
transform oracle JSONL. Transform eval reuses the same base oracle PNGs
(rotated/mirrored at inference time), so those scores are also stale.

Rewrites only:
    results/<model>/<strategy>/<tile>/t2/base/oracle.jsonl
    results/<model>/<strategy>/<tile>/t2/transform/<variant>/oracle.jsonl

Does not touch Direct, world, other T2 subtasks, T1/T3/T4, summary.json,
or results_tmp_* directories.

Default is dry-run. Pass --apply to write.
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from collections import defaultdict
from pathlib import Path

QUESTION_TYPES = ("nearest_point", "directional_nearest_point")
SKIP_MODEL_MARKERS = (".broken", ".old")
SKIP_TOP_DIRS = {"docs", "logs"}


def collect_target_ids(jsonl_root: Path) -> set[str]:
    ids: set[str] = set()
    by_file: dict[str, int] = {}
    by_type: dict[str, int] = defaultdict(int)
    oracle_files = sorted(jsonl_root.glob("*/t2/base/oracle.jsonl"))
    oracle_files += sorted(jsonl_root.glob("*/t2/transform/*/oracle.jsonl"))
    if not oracle_files:
        raise FileNotFoundError(f"no T2 oracle jsonl under {jsonl_root}")
    for path in oracle_files:
        n = 0
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            if rec.get("question_type") not in QUESTION_TYPES:
                continue
            sid = rec.get("id")
            if not sid:
                raise RuntimeError(f"missing id in {path}")
            if sid in ids:
                raise RuntimeError(f"duplicate id {sid} in {path}")
            ids.add(str(sid))
            n += 1
            by_type[str(rec["question_type"])] += 1
        rel = str(path.relative_to(jsonl_root))
        by_file[rel] = n
        print(f"input {rel}: {n}")
    print(f"target_ids={len(ids)} by_type={dict(by_type)}")
    return ids


def should_skip_model_dir(name: str) -> bool:
    if name in SKIP_TOP_DIRS:
        return True
    return any(marker in name for marker in SKIP_MODEL_MARKERS)


def iter_oracle_jsonl(results_root: Path) -> list[Path]:
    paths: list[Path] = []
    for model_dir in sorted(p for p in results_root.iterdir() if p.is_dir()):
        if should_skip_model_dir(model_dir.name):
            continue
        for path in sorted(model_dir.rglob("oracle.jsonl")):
            parts = path.parts
            if "t2" not in parts:
                continue
            if "world" in parts:
                continue
            if "base" not in parts and "transform" not in parts:
                continue
            paths.append(path)
    return paths


def is_target_record(rec: dict, target_ids: set[str]) -> bool:
    if rec.get("id") not in target_ids:
        return False
    if rec.get("question_type") not in QUESTION_TYPES:
        return False
    if rec.get("oracle") is False:
        return False
    return True


def filter_file(path: Path, target_ids: set[str], apply: bool) -> tuple[int, int, int]:
    """Return (kept, dropped, warnings)."""
    kept_lines: list[str] = []
    dropped = 0
    warnings = 0
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        rec = json.loads(raw)
        sid = rec.get("id")
        if sid in target_ids and rec.get("question_type") not in QUESTION_TYPES:
            warnings += 1
            kept_lines.append(raw)
            continue
        if is_target_record(rec, target_ids):
            dropped += 1
            continue
        kept_lines.append(raw)

    if apply and dropped:
        text = "".join(line + "\n" for line in kept_lines)
        fd, tmp_name = tempfile.mkstemp(
            prefix=path.name + ".",
            suffix=".tmp",
            dir=str(path.parent),
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(text)
            os.replace(tmp_name, path)
        except Exception:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)
            raise
    return len(kept_lines), dropped, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--jsonl-root",
        type=Path,
        default=Path(
            "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/"
            "SpatialIntelligence-gate2building/data/benchmark_jsonl"
        ),
    )
    parser.add_argument(
        "--results-root",
        type=Path,
        default=Path(
            "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/"
            "MapSpatial-EvalKit/results"
        ),
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Rewrite jsonl files. Without this flag, only print the plan.",
    )
    args = parser.parse_args()

    target_ids = collect_target_ids(args.jsonl_root)
    files = iter_oracle_jsonl(args.results_root)
    print(f"target_ids={len(target_ids)}")
    print(f"oracle_jsonl_files={len(files)}")
    print(f"mode={'APPLY' if args.apply else 'DRY-RUN'}")

    total_dropped = 0
    total_warnings = 0
    by_model: dict[str, int] = defaultdict(int)
    for path in files:
        kept, dropped, warnings = filter_file(path, target_ids, args.apply)
        rel = path.relative_to(args.results_root)
        model = rel.parts[0]
        by_model[model] += dropped
        total_dropped += dropped
        total_warnings += warnings
        print(f"{rel}: dropped={dropped} kept={kept} warnings={warnings}")

    print("---")
    for model, n in sorted(by_model.items()):
        print(f"{model}: dropped={n}")
    print(f"total_dropped={total_dropped}")
    print(f"total_warnings={total_warnings}")
    if not args.apply:
        print("dry-run only; re-run with --apply to rewrite files")


if __name__ == "__main__":
    main()
