"""CLI entry point — mapspatial command.

Usage:
  mapspatial run --model configs/models/qwen3-vl-8b.yaml --strategy direct
  mapspatial preflight --input-dir ... --data-root ...
  mapspatial compat --describe
  mapspatial report --models "*" --out comparison.csv
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _get_rank_world_size() -> tuple[int, int]:
    """Detect torchrun environment."""
    rank = int(os.environ.get("RANK", "0"))
    world_size = int(os.environ.get("WORLD_SIZE", "1"))
    return rank, world_size


def cmd_run(args: argparse.Namespace) -> None:
    from .config import load_run_config
    from .runner import run

    rank, world_size = _get_rank_world_size()

    cfg = load_run_config(
        args.model,
        data_dir=args.data_dir,
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        strategy=args.strategy,
        views=args.views.split(",") if args.views else None,
        tasks=args.tasks.split(",") if args.tasks else None,
        variants=args.variants.split(",") if args.variants else None,
        batch_size=args.batch_size,
        skip_preflight=args.skip_preflight,
        allow_missing=args.allow_missing,
        store_question=args.store_question,
        no_save_generated=args.no_save_generated,
        no_system_prompt=args.no_system_prompt,
        max_samples=args.max_samples,
        rank=rank,
        world_size=world_size,
    )

    run(cfg)


def cmd_preflight(args: argparse.Namespace) -> None:
    from .data.preflight import preflight, save_preflight

    views = args.views.split(",") if args.views else ["sat", "webrd04", "blank"]
    tasks = args.tasks.split(",") if args.tasks else ["t1", "t2", "t3", "t4"]
    variants = args.variants.split(",") if args.variants else ["direct", "oracle"]

    report = preflight(
        Path(args.input_dir),
        Path(args.data_dir),
        views, tasks, variants,
    )

    if args.output:
        save_preflight(report, Path(args.output))

    print(f"Total images: {report.total_images}")
    print(f"Missing: {report.missing}")
    print(f"Unreadable: {report.unreadable}")

    if report.missing > 0 or report.unreadable > 0:
        print("\nDetails:")
        for d in report.missing_details[:20]:
            print(f"  MISSING: {d['view']}/{d['task']}/{d['variant']} sample={d['sample_id']} path={d['path']}")
        for d in report.unreadable_details[:20]:
            print(f"  UNREADABLE: {d['view']}/{d['task']}/{d['variant']} sample={d['sample_id']} error={d['error']}")
        if not args.allow_missing:
            sys.exit(1)


def cmd_compat(args: argparse.Namespace) -> None:
    from .compat import describe

    if args.describe:
        patches = describe()
        if not patches:
            print("No compat patches registered.")
            return
        for p in patches:
            status = "ACTIVE" if p["active"] else "inactive"
            print(f"  [{status}] {p['name']}")
            print(f"    reason: {p['reason']}")
            print(f"    affects: {', '.join(p['affects']) or '(none)'}")
            print()


def cmd_report(args: argparse.Namespace) -> None:
    from .eval.metrics import build_comparison_table

    # Find all summary.json files
    output_dir = Path(args.output_dir)
    summaries = []

    if args.models == "*":
        # Find all summary.json under output_dir
        for path in output_dir.rglob("summary.json"):
            with open(path, "r") as f:
                summaries.append(json.load(f))
    else:
        for model in args.models.split(","):
            for path in output_dir.glob(f"{model}/*/summary.json"):
                with open(path, "r") as f:
                    summaries.append(json.load(f))

    if not summaries:
        print("No summaries found.", file=sys.stderr)
        sys.exit(1)

    csv = build_comparison_table(summaries)

    if args.out:
        Path(args.out).write_text(csv)
        print(f"Comparison table written to {args.out}")
    else:
        print(csv)


def cmd_doctor(args: argparse.Namespace) -> None:
    """Check all backends: can import? can load? can infer 1 sample?

    Scans configs/models/*.yaml, for each:
      1. Can we import the backend module? (without loading weights)
      2. (Optional) Can we load the model? (--check-load)
      3. (Optional) Can we run 1 sample? (--check-infer, needs --input-dir)
    """
    from .backends.registry import available_backends, get_backend_cls
    from .config import load_model_config
    from .compat import describe as describe_compat
    import traceback
    import glob

    print("=" * 70)
    print("MapSpatial-EvalKit Doctor — Environment Self-Check")
    print("=" * 70)

    # 1. Show registered backends
    backends = available_backends()
    print(f"\nRegistered backends ({len(backends)}):")
    for b in backends:
        print(f"  {b}")

    # 2. Show compat patches
    print("\nCompatibility patches:")
    patches = describe_compat()
    if not patches:
        print("  (none registered)")
    for p in patches:
        status = "ACTIVE" if p["active"] else "inactive"
        print(f"  [{status}] {p['name']}: {p['reason']}")

    # 3. Scan model configs
    configs_dir = args.configs_dir or "configs/models"
    configs = sorted(glob.glob(f"{configs_dir}/*.yaml"))
    if not configs:
        print(f"\nNo model configs found in {configs_dir}/")
        return

    print(f"\nModel configs ({len(configs)}):")
    print(f"{'Model':<35} {'Backend':<15} {'Import':<8} {'Load':<8} {'Caps':<30}")
    print("-" * 96)

    all_ok = True
    for cfg_path in configs:
        try:
            cfg = load_model_config(cfg_path)
        except Exception as e:
            print(f"  {cfg_path}: config load error: {e}", file=sys.stderr)
            all_ok = False
            continue

        # Skip Phase 2 configs (veomni_*)
        if cfg.backend not in backends:
            print(f"  {cfg.name:<35} {cfg.backend:<15} {'SKIP':<8} {'':8} (not registered)")
            continue

        # Check import (lazy load the backend class)
        import_status = "ok"
        caps_str = ""
        try:
            BackendCls = get_backend_cls(cfg.backend)
            caps = BackendCls.caps
            caps_str = f"batch={caps.batch},draw={caps.draw},max_img={caps.max_images}"
        except ImportError as e:
            import_status = "FAIL"
            caps_str = str(e)[:50]
            all_ok = False
        except Exception as e:
            import_status = f"ERR"
            caps_str = str(e)[:50]
            all_ok = False

        # Check load (optional, requires weights on disk)
        load_status = "—"
        if args.check_load and import_status == "ok":
            try:
                BackendCls(cfg)
                load_status = "ok"
            except Exception as e:
                load_status = "FAIL"
                caps_str = str(e)[:50]
                all_ok = False

        print(f"  {cfg.name:<35} {cfg.backend:<15} {import_status:<8} {load_status:<8} {caps_str}")

    print("-" * 96)
    if all_ok:
        print("\nAll checks passed.")
    else:
        print("\nSome checks FAILED — see output above.")
        if not args.check_load:
            print("(Load checks skipped — use --check-load to verify model loading)")



def main():
    parser = argparse.ArgumentParser(
        prog="mapspatial",
        description="MapSpatial-EvalKit: multimodal evaluation for outdoor map spatial understanding",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # run
    p_run = sub.add_parser("run", help="Run inference")
    p_run.add_argument("--model", required=True, help="Path to model YAML config")
    p_run.add_argument("--strategy", default="direct", help="Strategy name")
    p_run.add_argument("--input-dir", required=True, help="Path to data-jsonl/ directory")
    p_run.add_argument("--data-dir", required=True, help="Path to data/ directory (images root)")
    p_run.add_argument("--output-dir", required=True, help="Output directory for results")
    p_run.add_argument("--views", default=None, help="Comma-separated views (e.g. sat,webrd04)")
    p_run.add_argument("--tasks", default=None, help="Comma-separated tasks (e.g. t1,t2)")
    p_run.add_argument(
        "--variants", default=None,
        help="Comma-separated evidence conditions (direct,oracle,wrong_oracle,shuffled_oracle,masked_prompt)",
    )
    p_run.add_argument("--batch-size", type=int, default=0, help="Batch size (0=auto)")
    p_run.add_argument("--skip-preflight", action="store_true", help="Skip image preflight")
    p_run.add_argument("--allow-missing", type=int, default=0, help="Allow N missing images")
    p_run.add_argument("--store-question", action="store_true", help="Store question text in results")
    p_run.add_argument("--no-save-generated", action="store_true", help="Don't save generated images")
    p_run.add_argument(
        "--no-system-prompt",
        action="store_true",
        help="Don't inject the benchmark record's system_prompt (e.g. for think runs, "
        "where 'return only the option letter, no explanation' conflicts with CoT)",
    )
    p_run.add_argument(
        "--max-samples", type=int, default=0,
        help="Cap samples per (view, task, variant) cell (0=all). For smoke tests.",
    )
    p_run.set_defaults(func=cmd_run)

    # preflight
    p_pf = sub.add_parser("preflight", help="Check image availability")
    p_pf.add_argument("--input-dir", required=True, help="Path to data-jsonl/ directory")
    p_pf.add_argument("--data-dir", required=True, help="Path to data/ directory")
    p_pf.add_argument("--views", default=None)
    p_pf.add_argument("--tasks", default=None)
    p_pf.add_argument(
        "--variants", default=None,
        help="Comma-separated evidence conditions (direct,oracle,wrong_oracle,shuffled_oracle,masked_prompt)",
    )
    p_pf.add_argument("--output", default=None, help="Write report to JSON file")
    p_pf.add_argument("--allow-missing", action="store_true", help="Don't exit non-zero on issues")
    p_pf.set_defaults(func=cmd_preflight)

    # compat
    p_compat = sub.add_parser("compat", help="Show compatibility patches")
    p_compat.add_argument("--describe", action="store_true", help="Describe all patches")
    p_compat.set_defaults(func=cmd_compat)

    # report
    p_rep = sub.add_parser("report", help="Generate cross-model comparison")
    p_rep.add_argument("--output-dir", default="results", help="Results directory")
    p_rep.add_argument("--models", default="*", help="Model name(s) or * for all")
    p_rep.add_argument("--out", default=None, help="Output CSV file path")
    p_rep.set_defaults(func=cmd_report)

    # doctor
    p_doc = sub.add_parser("doctor", help="Environment self-check")
    p_doc.add_argument("--configs-dir", default=None, help="Path to model configs dir (default: configs/models)")
    p_doc.add_argument("--check-load", action="store_true", help="Also try loading each model (slow)")
    p_doc.set_defaults(func=cmd_doctor)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
