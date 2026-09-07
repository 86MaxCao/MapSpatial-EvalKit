#!/usr/bin/env python3
"""Derive a T3 jsonl with shuffled route_cumulative_count option letters.

Does not read or write the original benchmark_jsonl in place. Images and
source labels are unchanged. segment_building_count rows are copied as-is.

Usage:
  python scripts/shuffle_t3_route_options.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SRC = Path(
    "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/"
    "SpatialIntelligence-gate2building/data/benchmark_jsonl"
)
DEFAULT_DST = Path(
    "/home/ximeng.czq/caoziqi/code/SpatialIntelligence/"
    "SpatialIntelligence-gate2building/data/benchmark_jsonl_t3_optshuffle"
)

OPTION_RE = re.compile(r"^([A-Z])[.\s]\s*(.+)$", re.IGNORECASE)


def _option_text(option: str, index: int) -> str:
    m = OPTION_RE.match(str(option).strip())
    if m:
        return m.group(2).strip()
    return str(option).strip()


def _seed_for(record: dict, salt: int) -> int:
    key = str(record.get("instance_id") or record.get("id") or "")
    digest = hashlib.sha256(f"{key}|{salt}".encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def _rewrite_human(text: str, options: list[str]) -> str:
    if "Options:" not in text:
        return text
    prefix, rest = text.split("Options:", 1)
    after_opts = rest
    answer_tail = ""
    if "\nAnswer with" in rest:
        after_opts, answer_part = rest.split("\nAnswer with", 1)
        answer_tail = "\nAnswer with" + answer_part
    return prefix + "Options:\n" + "\n".join(options) + answer_tail


def shuffle_route(record: dict, salt: int) -> dict:
    rec = json.loads(json.dumps(record))
    options = list(rec.get("options") or [])
    if len(options) < 2:
        return rec
    texts = [_option_text(opt, i) for i, opt in enumerate(options)]
    old_letter = str(rec.get("answer_letter") or rec.get("answer") or "A").strip().upper()
    if not re.fullmatch(r"[A-Z]", old_letter):
        old_letter = "A"
    old_idx = ord(old_letter) - ord("A")
    correct = texts[old_idx] if 0 <= old_idx < len(texts) else texts[0]

    rng = random.Random(_seed_for(rec, salt))
    order = list(range(len(texts)))
    rng.shuffle(order)
    new_texts = [texts[i] for i in order]
    new_options = [f"{chr(ord('A') + i)}. {text}" for i, text in enumerate(new_texts)]
    new_letter = chr(ord("A") + new_texts.index(correct))

    rec["source_id"] = rec.get("id")
    rec["id"] = f"{rec.get('id')}_optsh"
    rec["options"] = new_options
    rec["answer"] = new_letter
    rec["answer_letter"] = new_letter
    rec["option_shuffle"] = {
        "salt": salt,
        "source_gold": old_letter,
        "gold": new_letter,
        "order": order,
    }

    q = rec.get("question") or ""
    rec["question_with_options"] = f"{q.rstrip()}\n\nOptions:\n" + "\n".join(new_options)

    mc = rec.get("multiple_choice")
    if isinstance(mc, dict):
        rec["multiple_choice"] = {
            **mc,
            "choices": [
                {"key": chr(ord("A") + i), "text": text} for i, text in enumerate(new_texts)
            ],
        }

    convs = rec.get("conversations")
    if isinstance(convs, list):
        new_convs = []
        for turn in convs:
            turn = dict(turn)
            if turn.get("from") == "human":
                turn["value"] = _rewrite_human(str(turn.get("value") or ""), new_options)
            elif turn.get("from") == "gpt":
                turn["value"] = new_letter
            new_convs.append(turn)
        rec["conversations"] = new_convs
    return rec


def convert_file(src: Path, dst: Path, salt: int) -> dict:
    rows = [json.loads(ln) for ln in src.read_text(encoding="utf-8").splitlines() if ln.strip()]
    out: list[dict] = []
    golds: Counter[str] = Counter()
    n_route = n_seg = 0
    for rec in rows:
        qt = rec.get("question_type")
        if qt == "route_cumulative_count":
            rec = shuffle_route(rec, salt)
            n_route += 1
            golds[str(rec["answer_letter"])] += 1
        else:
            n_seg += 1
        out.append(rec)
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8") as f:
        for rec in out:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return {"n": len(out), "route": n_route, "seg": n_seg, "gold": dict(golds), "dst": str(dst)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src-root", type=Path, default=DEFAULT_SRC)
    parser.add_argument("--dst-root", type=Path, default=DEFAULT_DST)
    parser.add_argument("--views", default="wprd01")
    parser.add_argument("--relpath", default="t3/base/direct.jsonl")
    parser.add_argument("--salt", type=int, default=17)
    args = parser.parse_args()
    if args.dst_root.resolve() == args.src_root.resolve():
        raise SystemExit("dst-root must be a new directory; refusing to write in place")
    stats = []
    for view in args.views.split(","):
        src = args.src_root / view / args.relpath
        dst = args.dst_root / view / args.relpath
        if not src.is_file():
            raise SystemExit(f"missing source jsonl: {src}")
        stats.append(convert_file(src, dst, args.salt))
    for item in stats:
        print(json.dumps(item, ensure_ascii=False))


if __name__ == "__main__":
    main()
