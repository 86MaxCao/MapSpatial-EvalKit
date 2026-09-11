"""Preflight: image existence + readability check.

Borrowed from the predecessor internal pipeline (the correct implementation).
Improvements: structured output, --allow-missing threshold, mtime cache.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from .loader import iter_samples


@dataclass
class PreflightReport:
    total_images: int = 0
    missing: int = 0
    unreadable: int = 0
    missing_details: list[dict] = field(default_factory=list)
    unreadable_details: list[dict] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.missing == 0 and self.unreadable == 0

    def to_dict(self) -> dict:
        return {
            "total_images": self.total_images,
            "missing": self.missing,
            "unreadable": self.unreadable,
            "missing_details": self.missing_details[:100],  # cap for readability
            "unreadable_details": self.unreadable_details[:100],
        }


def preflight(
    input_dir: Path,
    data_root: Path,
    views: list[str],
    tasks: list[str],
    variants: list[str],
    layout: str = "tree",
) -> PreflightReport:
    """Verify all images exist and are readable.

    Walks every record in every JSONL file, checks each image path.
    """
    report = PreflightReport()

    for (view, task, variant), samples in iter_samples(
        input_dir, data_root, views, tasks, variants, layout=layout,
    ):
        for sample in samples:
            for item in sample.message:
                if item["type"] not in ("image", "video"):
                    continue
                report.total_images += 1
                v = item["value"]
                if hasattr(v, "exists"):
                    p = v
                else:
                    p = Path(v)

                if not p.exists():
                    report.missing += 1
                    report.missing_details.append({
                        "view": view, "task": task, "variant": variant,
                        "sample_id": sample.id, "path": str(p),
                    })
                    continue

                try:
                    from PIL import Image
                    Image.open(p).verify()
                except Exception as e:
                    report.unreadable += 1
                    report.unreadable_details.append({
                        "view": view, "task": task, "variant": variant,
                        "sample_id": sample.id, "path": str(p), "error": str(e),
                    })

    return report


def save_preflight(report: PreflightReport, path: Path) -> None:
    """Write preflight report to JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
        f.write("\n")
