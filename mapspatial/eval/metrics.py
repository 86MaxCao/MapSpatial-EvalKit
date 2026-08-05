"""Metrics aggregation — per (strategy, view, task, variant) cells + summary.

Fixes gate2building's summary.json issues:
  - 'written' only reflected current run, not cumulative → use 'total' from input
  - No 'accuracy' field (had to compute manually)
  - No strategy dimension (needed for 3-way ablation)
  - Nested array structure (hard to query)
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Cell:
    """One (strategy, view, task, variant) cell in the results table."""
    strategy: str
    view: str
    task: str
    variant: str
    total: int = 0           # input sample count (stable across re-runs)
    answered: int = 0        # predictions with valid text
    errors: int = 0          # predictions with error
    correct: int = 0         # exact_match=True
    draw_triggered: int = 0  # samples that actually generated images
    avg_rounds: float = 0.0
    unconfident_extract: int = 0

    @property
    def accuracy(self) -> float:
        return self.correct / self.answered if self.answered else 0.0

    @property
    def coverage(self) -> float:
        return self.answered / self.total if self.total else 0.0

    def to_dict(self) -> dict:
        return {
            "strategy": self.strategy,
            "view": self.view,
            "task": self.task,
            "variant": self.variant,
            "total": self.total,
            "answered": self.answered,
            "errors": self.errors,
            "correct": self.correct,
            "accuracy": round(self.accuracy, 4),
            "coverage": round(self.coverage, 4),
            "draw_triggered": self.draw_triggered,
            "avg_rounds": round(self.avg_rounds, 2),
            "unconfident_extract": self.unconfident_extract,
        }


def build_summary(
    cells: list[Cell],
    *,
    model: str,
    backend: str,
    env: dict | None = None,
) -> dict:
    """Build the full summary.json structure."""
    # Aggregate by strategy
    by_strategy: dict[str, dict[str, Any]] = {}
    for cell in cells:
        s = cell.strategy
        if s not in by_strategy:
            by_strategy[s] = {"total": 0, "answered": 0, "errors": 0, "correct": 0,
                              "draw_triggered": 0, "cells": 0}
        d = by_strategy[s]
        d["total"] += cell.total
        d["answered"] += cell.answered
        d["errors"] += cell.errors
        d["correct"] += cell.correct
        d["draw_triggered"] += cell.draw_triggered
        d["cells"] += 1

    for s, d in by_strategy.items():
        d["accuracy"] = round(d["correct"] / d["answered"], 4) if d["answered"] else 0.0
        d["coverage"] = round(d["answered"] / d["total"], 4) if d["total"] else 0.0

    # Aggregate by task
    by_task: dict[str, dict[str, Any]] = {}
    for cell in cells:
        t = cell.task
        if t not in by_task:
            by_task[t] = {"total": 0, "answered": 0, "correct": 0}
        by_task[t]["total"] += cell.total
        by_task[t]["answered"] += cell.answered
        by_task[t]["correct"] += cell.correct

    for t, d in by_task.items():
        d["accuracy"] = round(d["correct"] / d["answered"], 4) if d["answered"] else 0.0

    # Aggregate by view
    by_view: dict[str, dict[str, Any]] = {}
    for cell in cells:
        v = cell.view
        if v not in by_view:
            by_view[v] = {"total": 0, "answered": 0, "correct": 0}
        by_view[v]["total"] += cell.total
        by_view[v]["answered"] += cell.answered
        by_view[v]["correct"] += cell.correct

    for v, d in by_view.items():
        d["accuracy"] = round(d["correct"] / d["answered"], 4) if d["answered"] else 0.0

    return {
        "schema_version": 1,
        "model": model,
        "backend": backend,
        "env": env or {},
        "cells": [c.to_dict() for c in cells],
        "by_strategy": by_strategy,
        "by_task": by_task,
        "by_view": by_view,
    }


def save_summary(summary: dict, path: Path) -> None:
    """Write summary.json."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        f.write("\n")


def build_comparison_table(
    summaries: list[dict],
    tasks: list[str] | None = None,
) -> str:
    """Build a CSV comparison table across models/strategies."""
    import csv
    import io

    # Collect all tasks
    all_tasks = tasks or sorted(set(
        t for s in summaries for t in s.get("by_task", {})
    ))

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["model", "strategy"] + all_tasks + ["overall", "draw_rate"])

    for s in summaries:
        model = s.get("model", "?")
        for strat_name, strat_data in s.get("by_strategy", {}).items():
            row = [model, strat_name]
            for t in all_tasks:
                task_data = s.get("by_task", {}).get(t)
                if task_data and strat_name == list(s.get("by_strategy", {}).keys())[0]:
                    row.append(str(task_data.get("accuracy", "—")))
                else:
                    row.append("—")
            row.append(str(strat_data.get("accuracy", "—")))
            # draw_rate
            total = strat_data.get("answered", 0)
            drawn = strat_data.get("draw_triggered", 0)
            row.append(f"{drawn/total:.3f}" if total else "—")
            writer.writerow(row)

    return buf.getvalue()
