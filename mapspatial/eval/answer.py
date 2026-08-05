"""Answer extraction — rewritten from gate2building.

Fixes two bugs in gate2building's answer_extraction.py:
  1. allow_multi parameter was declared but never used in the function body
  2. Hardcoded A-D only — should use multiple_choice.choices for valid letters

Also handles thinking/CoT output: extract from <answer>...</answer> tags first,
don't extract from within <think>...</think> blocks.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class ExtractResult:
    answer: str           # normalized answer (multi-select: comma-separated, sorted)
    method: str           # which rule matched, for extraction quality stats
    confident: bool       # True = explicit pattern, False = fallback "last letter"


# Patterns in priority order (borrowed from gate2building, improved)
_ANSWER_TAG_RE = re.compile(r"<answer>\s*([A-Z](?:\s*,\s*[A-Z])*)\s*</answer>", re.IGNORECASE)

_EXPLICIT_RE = re.compile(
    r"(?:ANSWER|THE\s+ANSWER|FINAL\s+ANSWER|CONCLUSION)\s*(?:IS|=|:)?\s*[:：]?\s*"
    r"([A-Z](?:\s*,\s*[A-Z])*)\b",
    re.IGNORECASE,
)

_CHINESE_RE = re.compile(
    r"(?:答案|选择|选|是)\s*[:：]?\s*([A-Z](?:\s*,\s*[A-Z])*)\b",
    re.IGNORECASE,
)

_IS_RE = re.compile(
    r"(?:IS|=)\s*[:：]?\s*([A-Z])\b[^A-Z]*$",
    re.IGNORECASE,
)

_SHORT_SINGLE_RE = re.compile(r"^([A-Z])\.?\s*$", re.IGNORECASE)
_SHORT_PREFIX_RE = re.compile(r"^([A-Z])[.\s]", re.IGNORECASE)

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)


def _normalize_letters(match_str: str) -> str:
    """Sort and deduplicate letters from a comma-separated match."""
    letters = [c.strip().upper() for c in match_str.split(",") if c.strip()]
    return ",".join(sorted(set(letters)))


def _strip_think(text: str) -> str:
    """Remove <think>...</think> blocks from text."""
    return _THINK_RE.sub("", text)


def _get_valid_letters(sample_meta: dict | None = None) -> str | None:
    """Extract valid option letters from sample's multiple_choice.choices."""
    if sample_meta is None:
        return None
    mc = sample_meta.get("multiple_choice") if sample_meta else None
    if not mc:
        return None
    choices = mc.get("choices", [])
    if not choices:
        return None
    letters = [c.get("key", "").strip().upper() for c in choices if c.get("key")]
    return "".join(sorted(letters)) if letters else None


def extract_answer(
    response: str,
    *,
    sample_meta: dict | None = None,
    allow_multi: bool = True,
) -> ExtractResult:
    """Extract answer letter(s) from model response.

    Priority:
      1. <answer>X</answer> tags
      2. Explicit "ANSWER IS X" / "FINAL ANSWER: X" patterns
      3. Chinese "答案：X" pattern
      4. "is X" / "= X" near end
      5. Single letter at start of response (short response)
      6. Last valid letter in text (fallback, not confident)

    For thinking/CoT output, <think>...</think> is stripped before extraction.
    """
    if not response or not response.strip():
        return ExtractResult(answer="", method="empty", confident=False)

    text = response.strip()
    # Strip thinking blocks (don't extract answers from reasoning)
    clean_text = _strip_think(text)

    # Determine valid letters from sample metadata
    valid_letters_str = _get_valid_letters(sample_meta)
    if valid_letters_str:
        valid_set = set(valid_letters_str)
    else:
        # Default A-D (our data is all 4-choice, but don't hardcode silently)
        valid_set = {"A", "B", "C", "D"}

    def _filter_letters(match_str: str) -> str:
        """Filter matched letters to only valid ones."""
        letters = [c.strip().upper() for c in match_str.split(",") if c.strip()]
        filtered = [l for l in letters if l in valid_set]
        if not filtered:
            return ""
        if not allow_multi:
            return filtered[0]
        return ",".join(sorted(set(filtered)))

    # 1. <answer> tags
    m = _ANSWER_TAG_RE.search(clean_text)
    if m:
        filtered = _filter_letters(m.group(1))
        if filtered:
            return ExtractResult(answer=filtered, method="answer_tag", confident=True)

    # 2. Explicit answer patterns
    m = _EXPLICIT_RE.search(clean_text)
    if m:
        filtered = _filter_letters(m.group(1))
        if filtered:
            return ExtractResult(answer=filtered, method="explicit", confident=True)

    # 3. Chinese pattern
    m = _CHINESE_RE.search(clean_text)
    if m:
        filtered = _filter_letters(m.group(1))
        if filtered:
            return ExtractResult(answer=filtered, method="chinese", confident=True)

    # 4. "is X" near end
    m = _IS_RE.search(clean_text)
    if m:
        letter = m.group(1).upper()
        if letter in valid_set:
            return ExtractResult(answer=letter, method="is_end", confident=True)

    # 5. Short response — single letter
    if len(clean_text) < 50:
        m = _SHORT_SINGLE_RE.match(clean_text)
        if m:
            letter = m.group(1).upper()
            if letter in valid_set:
                return ExtractResult(answer=letter, method="short_single", confident=True)

        m = _SHORT_PREFIX_RE.match(clean_text)
        if m and len(clean_text) < 20:
            letter = m.group(1).upper()
            if letter in valid_set:
                return ExtractResult(answer=letter, method="short_prefix", confident=True)

    # 6. Fallback: last valid letter in text
    all_letters = re.findall(r"\b([A-Z])\b", clean_text)
    valid_found = [l for l in all_letters if l.upper() in valid_set]
    if valid_found:
        return ExtractResult(
            answer=valid_found[-1].upper(), method="last_letter", confident=False
        )

    return ExtractResult(answer="", method="no_match", confident=False)


def is_correct(predicted: str, gold: str) -> bool:
    """Check if predicted answer matches gold (supports multi-select)."""
    if not gold:
        return bool(predicted)

    def _normalize(s: str) -> str:
        return ",".join(sorted(p.strip().upper() for p in s.split(",") if p.strip()))

    return _normalize(predicted) == _normalize(gold)
