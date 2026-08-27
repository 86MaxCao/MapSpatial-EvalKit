#!/usr/bin/env python3
"""Read MapSpatial-EvalKit result JSONL files (read-only) and write a Markdown report.

Never writes, truncates, or otherwise mutates any JSONL / summary.json.

Usage (mapspatial env):
  python scripts/summarize_results.py
  python scripts/summarize_results.py --results-dir results --draw-dir results_draw --out docs/report0826.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Iterator


SKIP_DIR_MARKERS = (".broken", ".old_empty", ".backup", ".old", ".old_partial")
SKIP_TOP_DIRS = {"logs", "docs"}
REPO_ROOT = Path(__file__).resolve().parents[1]
RANK_RE = re.compile(r"^(?P<stem>.+)\.rank(?P<rank>\d+)-of-(?P<world>\d+)$")

VARIANT_ORDER = [
    "base",
    "rot90",
    "rot180",
    "rot270",
    "mirror_h",
    "mirror_h_rot90",
    "mirror_h_rot180",
    "mirror_h_rot270",
    "intervention_001",
    "sham_001",
]
VIEW_ORDER = ["blank", "sat", "webrd04", "wprd01"]
TASK_ORDER = ["t1", "t2", "t3", "t4"]
CONDITION_ORDER = ["direct", "oracle", "wrong_oracle", "shuffled_oracle", "masked_prompt"]
CONDITION_LEAFS = set(CONDITION_ORDER)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=REPO_ROOT / "results",
        help="Results root that contains per-model JSONL files",
    )
    parser.add_argument(
        "--draw-dir",
        type=Path,
        default=REPO_ROOT / "results_draw",
        help="external_draw results root (appended at the end of the report)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "docs" / "report0826.md",
        help="Output Markdown path (default: docs/report0826.md)",
    )
    return parser.parse_args()


def should_skip(path: Path, results_dir: Path) -> bool:
    try:
        rel = path.relative_to(results_dir)
    except ValueError:
        return True
    if rel.parts and rel.parts[0] in SKIP_TOP_DIRS:
        return True
    return any(marker in part for part in rel.parts for marker in SKIP_DIR_MARKERS)


def parse_result_path(path: Path, results_dir: Path) -> dict[str, str] | None:
    """Parse results/{model}/{strategy}/{view}/{task}/{variant...}.jsonl."""
    rel = path.relative_to(results_dir)
    if len(rel.parts) < 5:
        return None
    model, strategy, view, task = rel.parts[:4]
    if view not in VIEW_ORDER or task not in TASK_ORDER:
        return None
    stem = path.stem
    rank_m = RANK_RE.match(stem)
    leaf = rank_m.group("stem") if rank_m else stem
    variant_parts = list(rel.parts[4:-1]) + [leaf]
    variant = "/".join(variant_parts)
    return {
        "model_dir": model,
        "strategy": strategy,
        "view": view,
        "task": task,
        "variant": variant,
        "is_rank": "1" if rank_m else "0",
    }


def condition_from_variant(variant: str) -> str:
    leaf = variant.rsplit("/", 1)[-1]
    if leaf in {"wrong_oracle", "shuffled_oracle", "masked_prompt", "oracle"}:
        return leaf
    return "direct"


def parse_variant(variant: str) -> tuple[str, str, str]:
    """Split 'transform/rot90/direct' into (family, name, condition_hint)."""
    parts = [p for p in variant.split("/") if p]
    condition = parts[-1] if parts else ""
    if not parts:
        return "unknown", variant, condition
    if parts[0] == "base":
        return "base", "base", condition
    if parts[0] == "transform":
        name = parts[1] if len(parts) > 1 else "transform"
        return "transform", name, condition
    if parts[0] == "world":
        name = parts[1] if len(parts) > 1 else "world"
        return "world", name, condition
    return parts[0], "/".join(parts[:-1]) if len(parts) > 1 else parts[0], condition


def select_jsonl_files(results_dir: Path) -> list[Path]:
    """Pick merged JSONL when present; otherwise rank shards. Never writes."""
    grouped: dict[tuple[str, str, str, str, str], list[Path]] = defaultdict(list)
    for path in results_dir.rglob("*.jsonl"):
        if should_skip(path, results_dir):
            continue
        meta = parse_result_path(path, results_dir)
        if meta is None:
            continue
        key = (meta["model_dir"], meta["strategy"], meta["view"], meta["task"], meta["variant"])
        grouped[key].append(path)

    selected: list[Path] = []
    for paths in grouped.values():
        merged = [p for p in paths if RANK_RE.match(p.stem) is None]
        if merged:
            selected.extend(merged)
        else:
            selected.extend(paths)
    return sorted(selected)


def iter_jsonl_records(path: Path) -> Iterator[dict[str, Any]]:
    """Read JSONL read-only. Duplicate ids keep the last occurrence."""
    by_id: dict[str, dict[str, Any]] = {}
    anonymous: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(obj, dict):
                continue
            sid = obj.get("id")
            if sid:
                by_id[str(sid)] = obj
            else:
                anonymous.append(obj)
    yield from by_id.values()
    yield from anonymous


def empty_cell(strategy: str, view: str, task: str, variant: str, condition: str) -> dict[str, Any]:
    return {
        "strategy": strategy,
        "view": view,
        "task": task,
        "variant": variant,
        "evidence_condition": condition,
        "total": 0,
        "answered": 0,
        "errors": 0,
        "correct": 0,
        "draw_triggered": 0,
        "unconfident_extract": 0,
    }


def load_summaries_from_jsonl(results_dir: Path) -> tuple[list[dict[str, Any]], int]:
    """Aggregate JSONL into the same per-model summary shape used by the tables."""
    files = select_jsonl_files(results_dir)
    groups: dict[tuple[str, str], dict[str, Any]] = {}
    n_records = 0

    for path in files:
        meta = parse_result_path(path, results_dir)
        if meta is None:
            continue
        key = (meta["model_dir"], meta["strategy"])
        group = groups.get(key)
        if group is None:
            group = {
                "model": meta["model_dir"],
                "backend": "",
                "cells": {},
                "n_files": 0,
            }
            groups[key] = group
        group["n_files"] += 1

        cell_key = (meta["strategy"], meta["view"], meta["task"], meta["variant"])
        cells: dict[tuple[str, str, str, str], dict[str, Any]] = group["cells"]
        cell = cells.get(cell_key)
        if cell is None:
            cell = empty_cell(
                meta["strategy"],
                meta["view"],
                meta["task"],
                meta["variant"],
                condition_from_variant(meta["variant"]),
            )
            cells[cell_key] = cell

        for obj in iter_jsonl_records(path):
            n_records += 1
            if obj.get("model"):
                group["model"] = obj["model"]
            if obj.get("backend") and not group["backend"]:
                group["backend"] = obj["backend"]
            if obj.get("evidence_condition"):
                cell["evidence_condition"] = obj["evidence_condition"]
            cell["total"] += 1
            cell["answered"] += 1
            if obj.get("error"):
                cell["errors"] += 1
            elif obj.get("exact_match"):
                cell["correct"] += 1
            if obj.get("draw_triggered"):
                cell["draw_triggered"] += 1
            if obj.get("extract_confident") is False:
                cell["unconfident_extract"] += 1

    summaries: list[dict[str, Any]] = []
    for group in groups.values():
        cells = list(group["cells"].values())
        summaries.append({
            "model": group["model"],
            "backend": group["backend"] or "?",
            "cells": cells,
            "n_files": group["n_files"],
        })
    summaries.sort(key=lambda s: (s.get("model") or "", s["cells"][0]["strategy"] if s["cells"] else ""))
    return summaries, n_records


def pct(correct: int, answered: int) -> str:
    if answered <= 0:
        return "—"
    return f"{100.0 * correct / answered:.1f}"


def md_table(headers: list[str], rows: Iterable[list[str]]) -> str:
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_line, sep_line, *body]) if body else header_line + "\n" + sep_line


def aggregate(cells: Iterable[dict[str, Any]]) -> dict[str, int]:
    total = answered = correct = errors = 0
    n_cells = 0
    for cell in cells:
        n = int(cell.get("total") or 0)
        if n <= 0:
            continue
        n_cells += 1
        total += n
        answered += int(cell.get("answered") or 0)
        correct += int(cell.get("correct") or 0)
        errors += int(cell.get("errors") or 0)
    return {
        "total": total,
        "answered": answered,
        "correct": correct,
        "errors": errors,
        "n_cells": n_cells,
    }


def overall(summary: dict[str, Any]) -> dict[str, int]:
    return aggregate(summary.get("cells") or [])


def sort_key_acc(summary: dict[str, Any]) -> tuple[float, str]:
    stats = overall(summary)
    acc = stats["correct"] / stats["answered"] if stats["answered"] else -1.0
    return (-acc, summary.get("model") or "")


def unique_sorted(values: Iterable[str], preferred: list[str]) -> list[str]:
    seen = {v for v in values if v}
    ordered = [v for v in preferred if v in seen]
    rest = sorted(seen - set(ordered))
    return ordered + rest


def variant_label(name: str) -> str:
    return {
        "base": "base",
        "rot90": "rot90",
        "rot180": "rot180",
        "rot270": "rot270",
        "mirror_h": "mirror_h",
        "mirror_h_rot90": "m_r90",
        "mirror_h_rot180": "m_r180",
        "mirror_h_rot270": "m_r270",
        "intervention_001": "interv",
        "sham_001": "sham",
    }.get(name, name)


def families_present(summary: dict[str, Any]) -> set[str]:
    families: set[str] = set()
    for cell in summary.get("cells") or []:
        if int(cell.get("total") or 0) <= 0:
            continue
        family, _, _ = parse_variant(cell.get("variant") or "")
        families.add(family)
    return families


def tasks_present(summary: dict[str, Any]) -> list[str]:
    tasks = {
        cell.get("task")
        for cell in summary.get("cells") or []
        if int(cell.get("total") or 0) > 0
    }
    return unique_sorted(tasks, TASK_ORDER)


def _source_sections(
    summaries: list[dict[str, Any]],
    start: int,
) -> tuple[list[str], int]:
    ranked = sorted(summaries, key=sort_key_acc)
    n = start
    lines: list[str] = []

    def heading(title: str) -> str:
        nonlocal n
        text = f"## {n}. {title}"
        n += 1
        return text

    lines += [heading("Overall"), "", _overall_table(ranked), ""]
    lines += [heading("Completeness"), "", _completeness_table(ranked), ""]
    lines += [heading("By evidence condition"), "", _condition_table(ranked), ""]
    lines += [heading("By view"), "", _view_table(ranked), ""]
    lines += [heading("By task"), "", _task_table(ranked), ""]
    lines += [heading("By variant family"), "", _family_table(ranked), ""]

    t4_models = [
        s for s in ranked
        if "t4" in tasks_present(s) and ("base" in families_present(s) or "transform" in families_present(s))
    ]
    world_models = [s for s in ranked if "world" in families_present(s)]
    t12_models = [s for s in ranked if any(t in tasks_present(s) for t in ("t1", "t2"))]
    t3_models = [
        s for s in ranked
        if "t3" in tasks_present(s) and ("base" in families_present(s) or "transform" in families_present(s))
    ]

    lines += [
        heading("T4 · base + transform (comparable subset)"),
        "",
        "Aggregated across views with `total>0`.",
        "",
        "### Direct",
        "",
        _variant_table(t4_models, condition="direct", families=("base", "transform")),
        "",
        "### Oracle",
        "",
        _variant_table(t4_models, condition="oracle", families=("base", "transform")),
        "",
    ]

    if t12_models:
        lines += [
            heading("T1 / T2 · base + transform"),
            "",
            "### Direct",
            "",
            _variant_table(t12_models, condition="direct", families=("base", "transform"), tasks=("t1", "t2")),
            "",
            "### Oracle",
            "",
            _variant_table(t12_models, condition="oracle", families=("base", "transform"), tasks=("t1", "t2")),
            "",
        ]

    if t3_models:
        lines += [
            heading("T3 · base + transform"),
            "",
            "### Direct",
            "",
            _variant_table(t3_models, condition="direct", families=("base", "transform"), tasks=("t3",)),
            "",
            "### Oracle",
            "",
            _variant_table(t3_models, condition="oracle", families=("base", "transform"), tasks=("t3",)),
            "",
        ]

    if world_models:
        lines += [
            heading("World variants"),
            "",
            "### Direct",
            "",
            _variant_table(world_models, condition="direct", families=("world",)),
            "",
            "### Oracle",
            "",
            _variant_table(world_models, condition="oracle", families=("world",)),
            "",
        ]

    lines += [
        heading("Per-cell detail"),
        "",
        "Non-empty cells only.",
        "",
        _detail_table(ranked),
        "",
    ]
    return lines, n


def build_report(
    summaries: list[dict[str, Any]],
    results_dir: Path,
    n_records: int,
    draw_summaries: list[dict[str, Any]] | None = None,
    draw_dir: Path | None = None,
    n_draw_records: int = 0,
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines: list[str] = [
        "# MapSpatial-EvalKit Results",
        "",
        f"- Direct source: `{results_dir}` (JSONL, **read-only**)",
        f"- Generated: {now}",
        f"- Direct models: {len(summaries)} (skipped `*.broken` / `*.old*` / `logs` / `docs`)",
        f"- Direct records: {n_records}",
    ]
    if draw_summaries and draw_dir is not None:
        lines += [
            f"- Draw source: `{draw_dir}` (JSONL, **read-only**)",
            f"- Draw models: {len(draw_summaries)}",
            f"- Draw records: {n_draw_records}",
        ]
    lines += [
        "",
        "Accuracy is **correct / answered × 100**, using each JSONL record's `exact_match`.",
        "Empty files (`total=0`) are shown as —. Models were not all run on the same slice; overall scores are **not** directly comparable.",
        "",
        "## Direct (`results`)",
        "",
    ]
    direct_sections, next_n = _source_sections(summaries, start=1)
    lines += direct_sections

    if draw_summaries and draw_dir is not None:
        lines += [
            "## Draw (`results_draw`)",
            "",
            "Same table layout as above. These runs use the `external_draw` strategy.",
            "",
        ]
        draw_sections, _ = _source_sections(draw_summaries, start=next_n)
        lines += draw_sections

    return "\n".join(lines).rstrip() + "\n"


def _overall_table(summaries: list[dict[str, Any]]) -> str:
    headers = [
        "Model", "Strategy", "Backend", "Acc (%)", "Direct", "Oracle",
        "Δ (pp)", "N", "Correct", "Cells",
    ]
    rows: list[list[str]] = []
    for summary in summaries:
        stats = overall(summary)
        by_cond: dict[str, dict[str, int]] = {}
        for cond in CONDITION_ORDER:
            by_cond[cond] = aggregate(
                c for c in summary.get("cells") or []
                if (c.get("evidence_condition") or "") == cond
            )
        direct_acc = (
            by_cond["direct"]["correct"] / by_cond["direct"]["answered"]
            if by_cond["direct"]["answered"] else None
        )
        oracle_acc = (
            by_cond["oracle"]["correct"] / by_cond["oracle"]["answered"]
            if by_cond["oracle"]["answered"] else None
        )
        if direct_acc is None or oracle_acc is None:
            delta = "—"
        else:
            delta = f"{100.0 * (oracle_acc - direct_acc):+.1f}"
        strategies = sorted({
            c.get("strategy") or "?"
            for c in summary.get("cells") or []
            if int(c.get("total") or 0) > 0
        }) or ["?"]
        rows.append([
            summary.get("model") or "?",
            ",".join(strategies),
            summary.get("backend") or "?",
            pct(stats["correct"], stats["answered"]),
            pct(by_cond["direct"]["correct"], by_cond["direct"]["answered"]),
            pct(by_cond["oracle"]["correct"], by_cond["oracle"]["answered"]),
            delta,
            str(stats["total"]),
            str(stats["correct"]),
            str(stats["n_cells"]),
        ])
    return md_table(headers, rows)


def _completeness_table(summaries: list[dict[str, Any]]) -> str:
    headers = ["Model", "Tasks", "Views", "Families", "N", "Cells", "Files"]
    rows = []
    for summary in summaries:
        stats = overall(summary)
        views = unique_sorted(
            {
                c.get("view")
                for c in summary.get("cells") or []
                if int(c.get("total") or 0) > 0
            },
            VIEW_ORDER,
        )
        rows.append([
            summary.get("model") or "?",
            ",".join(tasks_present(summary)) or "—",
            ",".join(views) or "—",
            ",".join(sorted(families_present(summary))) or "—",
            str(stats["total"]),
            str(stats["n_cells"]),
            str(summary.get("n_files") or 0),
        ])
    return md_table(headers, rows)


def _condition_table(summaries: list[dict[str, Any]]) -> str:
    headers = ["Model", "Direct (%)", "N_direct", "Oracle (%)", "N_oracle", "Δ (pp)"]
    rows = []
    for summary in summaries:
        by_cond = {
            cond: aggregate(
                c for c in summary.get("cells") or []
                if (c.get("evidence_condition") or "") == cond
            )
            for cond in ("direct", "oracle")
        }
        d, o = by_cond["direct"], by_cond["oracle"]
        d_acc = d["correct"] / d["answered"] if d["answered"] else None
        o_acc = o["correct"] / o["answered"] if o["answered"] else None
        delta = "—" if d_acc is None or o_acc is None else f"{100.0 * (o_acc - d_acc):+.1f}"
        rows.append([
            summary.get("model") or "?",
            pct(d["correct"], d["answered"]),
            str(d["total"]) if d["total"] else "—",
            pct(o["correct"], o["answered"]),
            str(o["total"]) if o["total"] else "—",
            delta,
        ])
    return md_table(headers, rows)


def _view_table(summaries: list[dict[str, Any]]) -> str:
    views = unique_sorted(
        {
            c.get("view")
            for s in summaries
            for c in s.get("cells") or []
            if int(c.get("total") or 0) > 0
        },
        VIEW_ORDER,
    )
    headers = ["Model"] + views + ["Overall"]
    rows = []
    for summary in summaries:
        row = [summary.get("model") or "?"]
        for view in views:
            stats = aggregate(
                c for c in summary.get("cells") or [] if c.get("view") == view
            )
            row.append(pct(stats["correct"], stats["answered"]))
        overall_stats = overall(summary)
        row.append(pct(overall_stats["correct"], overall_stats["answered"]))
        rows.append(row)
    return md_table(headers, rows)


def _task_table(summaries: list[dict[str, Any]]) -> str:
    tasks = unique_sorted(
        {
            c.get("task")
            for s in summaries
            for c in s.get("cells") or []
            if int(c.get("total") or 0) > 0
        },
        TASK_ORDER,
    )
    headers = ["Model"] + tasks + ["Overall"]
    rows = []
    for summary in summaries:
        row = [summary.get("model") or "?"]
        for task in tasks:
            stats = aggregate(
                c for c in summary.get("cells") or [] if c.get("task") == task
            )
            row.append(pct(stats["correct"], stats["answered"]))
        overall_stats = overall(summary)
        row.append(pct(overall_stats["correct"], overall_stats["answered"]))
        rows.append(row)
    return md_table(headers, rows)


def _family_table(summaries: list[dict[str, Any]]) -> str:
    headers = ["Model", "base", "transform", "world", "Overall"]
    rows = []
    for summary in summaries:
        row = [summary.get("model") or "?"]
        for family in ("base", "transform", "world"):
            stats = aggregate(
                c for c in summary.get("cells") or []
                if parse_variant(c.get("variant") or "")[0] == family
            )
            row.append(pct(stats["correct"], stats["answered"]))
        overall_stats = overall(summary)
        row.append(pct(overall_stats["correct"], overall_stats["answered"]))
        rows.append(row)
    return md_table(headers, rows)


def _variant_table(
    summaries: list[dict[str, Any]],
    *,
    condition: str,
    families: tuple[str, ...],
    tasks: tuple[str, ...] | None = None,
) -> str:
    names: set[str] = set()
    for summary in summaries:
        for cell in summary.get("cells") or []:
            if int(cell.get("total") or 0) <= 0:
                continue
            if (cell.get("evidence_condition") or "") != condition:
                continue
            if tasks and cell.get("task") not in tasks:
                continue
            family, name, _ = parse_variant(cell.get("variant") or "")
            if family in families:
                names.add(name)
    columns = unique_sorted(names, VARIANT_ORDER)
    if not columns:
        return "_No matching cells._"
    headers = ["Model"] + [variant_label(n) for n in columns] + ["All"]
    rows = []
    for summary in summaries:
        row = [summary.get("model") or "?"]
        matched = []
        for cell in summary.get("cells") or []:
            if int(cell.get("total") or 0) <= 0:
                continue
            if (cell.get("evidence_condition") or "") != condition:
                continue
            if tasks and cell.get("task") not in tasks:
                continue
            family, name, _ = parse_variant(cell.get("variant") or "")
            if family in families:
                matched.append(cell)
        for name in columns:
            stats = aggregate(
                c for c in matched
                if parse_variant(c.get("variant") or "")[1] == name
            )
            row.append(pct(stats["correct"], stats["answered"]))
        all_stats = aggregate(matched)
        row.append(pct(all_stats["correct"], all_stats["answered"]))
        if all_stats["n_cells"]:
            rows.append(row)
    return md_table(headers, rows) if rows else "_No matching cells._"


def _detail_table(summaries: list[dict[str, Any]]) -> str:
    headers = [
        "Model", "Strategy", "View", "Task", "Variant", "Condition",
        "Acc (%)", "Correct", "Answered", "Total", "Errors",
    ]
    rows: list[list[str]] = []
    for summary in summaries:
        cells = [
            c for c in summary.get("cells") or []
            if int(c.get("total") or 0) > 0
        ]
        cells.sort(key=lambda c: (
            VIEW_ORDER.index(c.get("view")) if c.get("view") in VIEW_ORDER else 99,
            TASK_ORDER.index(c.get("task")) if c.get("task") in TASK_ORDER else 99,
            c.get("variant") or "",
            c.get("evidence_condition") or "",
        ))
        for cell in cells:
            rows.append([
                summary.get("model") or "?",
                cell.get("strategy") or "?",
                cell.get("view") or "?",
                cell.get("task") or "?",
                cell.get("variant") or "?",
                cell.get("evidence_condition") or "?",
                pct(int(cell.get("correct") or 0), int(cell.get("answered") or 0)),
                str(cell.get("correct") or 0),
                str(cell.get("answered") or 0),
                str(cell.get("total") or 0),
                str(cell.get("errors") or 0),
            ])
    return md_table(headers, rows)


def main() -> None:
    args = parse_args()
    results_dir = args.results_dir.resolve()
    if not results_dir.is_dir():
        raise SystemExit(f"Results directory not found: {results_dir}")

    out = args.out.resolve()
    if out.suffix.lower() == ".jsonl":
        raise SystemExit(f"Refusing to write over a JSONL path: {out}")

    print(f"Scanning JSONL under {results_dir} (read-only)...", file=sys.stderr)
    summaries, n_records = load_summaries_from_jsonl(results_dir)
    if not summaries:
        raise SystemExit(f"No result JSONL found under {results_dir}")

    draw_summaries: list[dict[str, Any]] = []
    n_draw_records = 0
    draw_dir = args.draw_dir.resolve() if args.draw_dir else None
    if draw_dir is not None and draw_dir.is_dir():
        print(f"Scanning JSONL under {draw_dir} (read-only)...", file=sys.stderr)
        draw_summaries, n_draw_records = load_summaries_from_jsonl(draw_dir)
    elif draw_dir is not None:
        print(f"Draw directory not found, skipping: {draw_dir}", file=sys.stderr)

    out.parent.mkdir(parents=True, exist_ok=True)
    report = build_report(
        summaries,
        results_dir,
        n_records,
        draw_summaries=draw_summaries or None,
        draw_dir=draw_dir if draw_summaries else None,
        n_draw_records=n_draw_records,
    )
    out.write_text(report, encoding="utf-8")
    extra = f", {len(draw_summaries)} draw models, {n_draw_records} draw records" if draw_summaries else ""
    print(f"Wrote {out} ({len(summaries)} models, {n_records} records{extra}, {len(report.splitlines())} lines)")


if __name__ == "__main__":
    main()
