"""Runner — execution scheduling, resume, striped multi-GPU, atomic write.

Key improvements over gate2building:
  - JSONL + atomic append + id dedup (no duplicate lines on re-run)
  - Striped multi-GPU (torchrun range(rank, N, world_size))
  - unset WORLD_SIZE before model construction
  - Result schema with schema_version, strategy, backend, generated_images, trace
  - Corrupt lines reported (not silently swallowed)
  - summary.json with stable 'total' from input (not 'written' from current run)
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any

from .config import RunConfig
from .types import TaskSample, Prediction, RunContext
from .data.loader import iter_samples
from .data.preflight import preflight, PreflightReport
from .media import MediaCache, materialize_transforms
from .backends.registry import get_backend_cls
from .strategies import get_strategy
from .eval.answer import extract_answer, is_correct
from .eval.metrics import Cell, build_summary, save_summary
from .compat import applied as compat_applied


def load_completed(path: Path) -> tuple[set[str], int]:
    """Return (completed id set, corrupt line count).

    Corrupt lines are reported, NOT silently swallowed (fixes gate2building bug).
    """
    done: set[str] = set()
    corrupt = 0
    if not path.exists():
        return done, 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                done.add(obj["id"])
            except (json.JSONDecodeError, KeyError):
                corrupt += 1
    return done, corrupt


def write_result(path: Path, record: dict) -> None:
    """Atomic single-line write to JSONL. No half-lines on crash."""
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, default=str)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
        f.flush()


def build_result_record(
    sample: TaskSample,
    pred: Prediction,
    *,
    model_name: str,
    backend_name: str,
    strategy: str,
    store_question: bool = False,
) -> dict:
    """Build a result record for JSONL output."""
    meta = sample.meta
    # Extract answer
    extract_result = extract_answer(
        pred.text,
        sample_meta=meta,
        allow_multi=True,
    )

    record = {
        "schema_version": 1,
        "id": sample.id,
        "model": model_name,
        "backend": backend_name,
        "strategy": strategy,
        "view": meta.get("view", ""),
        "variant": meta.get("variant", ""),
        "oracle": meta.get("oracle", False),
        "evidence_condition": meta.get("evidence_condition", "direct"),
        "track": meta.get("track", "") or _infer_track(strategy, meta),
        "task_id": meta.get("task_id", ""),
        "question_type": meta.get("question_type", ""),
        "images": meta.get("images", []),
        "gold": sample.gold,
        "prediction": pred.text,
        "extracted_answer": extract_result.answer,
        "exact_match": is_correct(extract_result.answer, sample.gold),
        "extract_method": extract_result.method,
        "extract_confident": extract_result.confident,
        "generated_images": [str(p) for p in pred.generated_images],
        "rounds": pred.meta.get("rounds", 1),
        "draw_triggered": pred.meta.get("draw_triggered", False),
        "trace": [
            {
                "round": t.round,
                "kind": t.kind,
                "text": t.text,
                "image": str(t.image) if t.image else None,
                "triggered_by": t.triggered_by,
                "elapsed_s": t.elapsed_s,
            }
            for t in pred.trace
        ],
        "error": pred.error,
    }

    if store_question:
        # Get question from the message text items
        for item in sample.message:
            if item["type"] == "text":
                record["question"] = item["value"]
                break

    return record


def _infer_track(strategy: str, meta: dict) -> str:
    """Provide a protocol label while remaining compatible with old JSONL.

    Track mapping:
      direct + non-direct condition → O (oracle)
      direct                      → U (understanding only)
      external_draw               → C-R (restart generation-to-understanding)
      forced_interleave           → C-F (stateful forced G2U)
      native_interleave           → C-A (stateful autonomous G2U)
    """
    condition = meta.get("evidence_condition", "direct")
    if strategy == "direct" and condition != "direct":
        return "O"
    if strategy == "direct":
        return "U"
    if strategy == "external_draw":
        return "C-R"
    if strategy == "forced_interleave":
        return "C-F"
    if strategy == "native_interleave":
        return "C-A"
    return ""


def _condition_from_variant_name(variant: str) -> str:
    """Normalize legacy variant names into the evidence-condition dimension.

    Variant may carry directory components for layered datasets
    (e.g. "base/oracle", "world/intervention_001/direct") — judge by the
    final path segment.
    """
    leaf = variant.rsplit("/", 1)[-1]
    if leaf in {"wrong_oracle", "shuffled_oracle", "masked_prompt"}:
        return leaf
    return "oracle" if leaf == "oracle" else "direct"


def run(
    cfg: RunConfig,
    *,
    views: list[str] | None = None,
    tasks: list[str] | None = None,
    variants: list[str] | None = None,
    strategy_name: str | None = None,
) -> None:
    """Main run loop.

    Steps:
      1. Preflight (unless --skip-preflight)
      2. For each (view, task, variant):
         a. Load samples
         b. Exclude completed (by id)
         c. Striped split (multi-GPU)
         d. Batch → strategy.run(backend, batch, ctx)
         e. Answer extraction + judgment
         f. Atomic append write
      3. Write summary.json
    """
    views = views or cfg.views
    tasks = tasks or cfg.tasks
    variants = variants or cfg.variants
    strategy_name = strategy_name or cfg.strategy

    # Preflight
    if not cfg.skip_preflight:
        report = preflight(cfg.input_dir, cfg.data_dir, views, tasks, variants)
        if report.missing > 0 or report.unreadable > 0:
            if report.missing > cfg.allow_missing:
                print(f"Preflight FAILED: {report.missing} missing, "
                      f"{report.unreadable} unreadable images", file=sys.stderr)
                # Save report for debugging
                preflight_path = cfg.output_dir / "preflight.json"
                preflight_path.parent.mkdir(parents=True, exist_ok=True)
                from .data.preflight import save_preflight
                save_preflight(report, preflight_path)
                print(f"Report saved to {preflight_path}", file=sys.stderr)
                sys.exit(1)
            else:
                print(f"Preflight: {report.missing} missing (within threshold "
                      f"{cfg.allow_missing}), {report.unreadable} unreadable")

    # Build backend
    BackendCls = get_backend_cls(cfg.model.backend)
    backend = BackendCls(cfg.model)

    # Build strategy
    strategy = get_strategy(strategy_name)
    strategy.validate(backend)

    # Build run context — populate marker/max_rounds from backend_args
    gen_kw = cfg.model.generate
    ba = cfg.model.backend_args or {}
    ctx = RunContext(
        output_dir=cfg.output_dir,
        gen_kw=gen_kw,
        max_rounds=ba.get("max_rounds", 3),
        marker=ba.get("marker", "<image_start>"),
        view="", task="", variant="",
        save_generated=not cfg.no_save_generated,
    )

    # Result output directory
    result_base = cfg.output_dir / cfg.model.name / strategy_name

    # Track cells for summary
    cells: list[Cell] = []

    for (view, task, variant), samples in iter_samples(
        cfg.input_dir, cfg.data_dir, views, tasks, variants
    ):
        # Update context
        ctx.view = view
        ctx.task = task
        ctx.variant = variant

        # Records may carry a per-cell system prompt (e.g. paper-v8 view
        # conventions); surface it to backends via gen_kw. It is constant
        # within a cell, so one lookup suffices.
        cell_system_prompt = next(
            (s.meta["system_prompt"] for s in samples if s.meta.get("system_prompt")),
            None,
        )
        if cell_system_prompt:
            ctx.gen_kw = {**gen_kw, "system_prompt": cell_system_prompt}
        else:
            ctx.gen_kw = gen_kw

        # Output path for this cell
        if cfg.world_size > 1:
            out_path = result_base / view / task / f"{variant}.rank{cfg.rank}-of-{cfg.world_size}.jsonl"
        else:
            out_path = result_base / view / task / f"{variant}.jsonl"

        # Load completed ids (resume)
        done_ids, corrupt = load_completed(out_path)
        if corrupt > 0:
            print(f"WARNING: {corrupt} corrupt lines in {out_path}, "
                  f"use --repair to clean up", file=sys.stderr)

        # Filter to pending
        pending = [s for s in samples if s.id not in done_ids]

        # Striped split for multi-GPU
        if cfg.world_size > 1:
            pending = pending[cfg.rank::cfg.world_size]

        cell = Cell(
            strategy=strategy_name,
            view=view, task=task, variant=variant,
            evidence_condition=_condition_from_variant_name(variant),
            total=len(samples),
        )

        if not pending:
            # All done or empty file
            # Still need to count for summary — load existing results
            if out_path.exists():
                existing_done, _ = load_completed(out_path)
                # Count correct from existing
                with open(out_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            obj = json.loads(line)
                            cell.answered += 1
                            cell.errors += 1 if obj.get("error") else 0
                            cell.correct += 1 if obj.get("exact_match") else 0
                            cell.draw_triggered += 1 if obj.get("draw_triggered") else 0
                        except json.JSONDecodeError:
                            pass
            cells.append(cell)
            continue

        # Process in batches
        batch_size = cfg.effective_batch_size
        batch_size = max(batch_size, 1)

        from tqdm import tqdm

        progress = tqdm(
            total=len(pending),
            desc=f"{view}/{task}/{variant}",
            disable=cfg.rank > 0,  # only rank 0 shows progress
        )

        total_rounds = 0
        total_draw_triggered = 0
        total_unconfident = 0

        for i in range(0, len(pending), batch_size):
            batch = pending[i:i + batch_size]

            # Apply benchmark transforms (mirror_h/rot90/...) by materializing
            # transformed images to temp files and rewriting message image
            # items to point at them. This is backend-agnostic — every backend
            # just loads a path — so it works for vLLM/transformers/API/...
            # No-op for base variants (items carry no transform).
            with MediaCache() as media_cache:
                materialize_transforms(
                    [s.message for s in batch], media_cache
                )
                try:
                    preds = strategy.run(backend, batch, ctx)
                except Exception as e:
                    print(f"ERROR: strategy.run failed for batch starting at {i}: {e}",
                          file=sys.stderr)
                    preds = [Prediction(error=str(e)) for _ in batch]

            for sample, pred in zip(batch, preds):
                record = build_result_record(
                    sample, pred,
                    model_name=cfg.model.name,
                    backend_name=cfg.model.backend,
                    strategy=strategy_name,
                    store_question=cfg.store_question,
                )
                write_result(out_path, record)

                # Update cell stats
                cell.answered += 1
                if pred.error:
                    cell.errors += 1
                else:
                    cell.correct += 1 if record["exact_match"] else 0
                if pred.meta.get("draw_triggered"):
                    cell.draw_triggered += 1
                    total_draw_triggered += 1
                cell.total += 0  # total is set from len(samples), not per-record
                total_rounds += pred.meta.get("rounds", 1)
                if not record["extract_confident"]:
                    total_unconfident += 1

            progress.update(len(batch))

        progress.close()

        # Merge with existing results if multi-GPU
        if cfg.world_size > 1 and cfg.rank == 0:
            # Rank 0 merges all shards
            _merge_shards(result_base / view / task, variant, cfg.world_size)

        # Update cell averages
        if cell.answered:
            cell.avg_rounds = total_rounds / cell.answered
        cell.unconfident_extract = total_unconfident

        cells.append(cell)

    # Write summary (only rank 0)
    if cfg.rank == 0:
        # If multi-GPU, merge all shards first for accurate counts
        if cfg.world_size > 1:
            for view in views:
                for task in tasks:
                    for variant in variants:
                        _merge_shards(
                            result_base / view / task, variant, cfg.world_size
                        )

        # Recompute cells from merged files for accuracy
        cells = _recompute_cells(result_base, views, tasks, variants, strategy_name,
                                 cfg.input_dir, cfg.data_dir)

        summary = build_summary(
            cells,
            model=cfg.model.name,
            backend=cfg.model.backend,
            env={
                "compat_applied": sorted(compat_applied()),
            },
        )
        summary_path = result_base / "summary.json"
        save_summary(summary, summary_path)
        print(f"\nSummary written to {summary_path}")


def _merge_shards(task_dir: Path, variant: str, world_size: int) -> None:
    """Merge rank shard files into a single output file."""
    merged_path = task_dir / f"{variant}.jsonl"
    merged_path.parent.mkdir(parents=True, exist_ok=True)

    seen_ids: set[str] = set()
    records: list[str] = []

    for rank in range(world_size):
        shard_path = task_dir / f"{variant}.rank{rank}-of-{world_size}.jsonl"
        if not shard_path.exists():
            continue
        with open(shard_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    sid = obj.get("id", "")
                    if sid not in seen_ids:
                        seen_ids.add(sid)
                        records.append(line)
                except json.JSONDecodeError:
                    pass

    with open(merged_path, "w", encoding="utf-8") as f:
        for line in records:
            f.write(line + "\n")


def _recompute_cells(
    result_base: Path,
    views: list[str],
    tasks: list[str],
    variants: list[str],
    strategy: str,
    input_dir: Path,
    data_root: Path,
) -> list[Cell]:
    """Recompute cell statistics from result files (accurate after merge)."""
    from .data.loader import count_samples

    cells = []
    for view in views:
        for task in tasks:
            for variant in variants:
                input_path = input_dir / view / task / f"{variant}.jsonl"
                total = count_samples(input_path)

                cell = Cell(
                    strategy=strategy, view=view, task=task, variant=variant,
                    evidence_condition=_condition_from_variant_name(variant),
                    total=total,
                )

                result_path = result_base / view / task / f"{variant}.jsonl"
                if result_path.exists():
                    rounds_sum = 0
                    with open(result_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                obj = json.loads(line)
                                cell.answered += 1
                                if obj.get("error"):
                                    cell.errors += 1
                                elif obj.get("exact_match"):
                                    cell.correct += 1
                                if obj.get("draw_triggered"):
                                    cell.draw_triggered += 1
                                rounds_sum += obj.get("rounds", 1)
                                if not obj.get("extract_confident", True):
                                    cell.unconfident_extract += 1
                            except json.JSONDecodeError:
                                pass
                    if cell.answered:
                        cell.avg_rounds = rounds_sum / cell.answered

                cells.append(cell)

    return cells
