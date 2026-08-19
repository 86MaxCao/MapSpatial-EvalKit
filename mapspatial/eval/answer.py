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

# Filler words stripped before comparing a free-text answer to option texts
# (models often answer "blue point, red point" for option "blue, red").
_TEXT_STOPWORDS = {
    "the", "a", "an", "is", "are", "to", "of", "and", "in", "on", "at",
    "it", "its", "point", "points", "marker", "markers",
}


def _norm_text(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower().rstrip(".!?"))


def _squash_text(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _tokens(s: str) -> list[str]:
    return [t for t in re.split(r"[^a-z0-9]+", s.lower()) if t]


def _match_option_text(clean_text: str, sample_meta: dict | None) -> str | None:
    """Match a free-text answer back to its option letter; None when unmappable."""
    if sample_meta is None:
        return None
    mc = sample_meta.get("multiple_choice") or {}
    choices = [(c.get("key", "").upper(), str(c.get("text", ""))) for c in mc.get("choices", [])]
    choices = [(k, t) for k, t in choices if k and t]
    if not choices:
        return None

    norm = _norm_text(clean_text)
    squashed = _squash_text(clean_text)

    # exact text match (also symbol-insensitive: "South-East" vs "southeast")
    for key, text in choices:
        if norm == _norm_text(text) or (
            len(squashed) > 2 and squashed == _squash_text(text)
        ):
            return key

    # numeric match ("4.0" vs "4")
    try:
        pred_num = float(norm)
    except ValueError:
        pred_num = None
    if pred_num is not None:
        for key, text in choices:
            try:
                if float(_norm_text(text)) == pred_num:
                    return key
            except ValueError:
                continue

    # token-sequence match after dropping filler words ("blue point, red point" → "blue, red")
    pred_seq = [t for t in _tokens(clean_text) if t not in _TEXT_STOPWORDS]
    if pred_seq:
        seq_hits = [
            key for key, text in choices
            if [t for t in _tokens(text) if t not in _TEXT_STOPWORDS] == pred_seq
        ]
        if len(set(seq_hits)) == 1:
            return seq_hits[0]

    # substring containment, most specific (longest) option first
    for key, text in sorted(choices, key=lambda kt: len(kt[1]), reverse=True):
        if len(norm) > len(_norm_text(text)) and _norm_text(text) in norm:
            return key

    return None


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
      6. Free-text answer matched back to an option letter (option_text)
      7. Last valid letter in text (fallback, not confident)

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
        valid_set = {"A", "B", "C", "D", "E", "F"}

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

    # 6. Free-text answer matched back to an option letter
    key = _match_option_text(clean_text, sample_meta)
    if key:
        return ExtractResult(answer=key, method="option_text", confident=True)

    # 7. Comma-separated multi-letter at end of response (e.g. "A, C", "A,B")
    #    Single-choice questions: model outputting multiple answers should be
    #    judged wrong. Only check the tail to avoid false positives in reasoning.
    tail = clean_text[-80:].strip()
    comma_match = re.search(r'([A-F](?:\s*,\s*[A-F])+)', tail)
    if comma_match:
        letters = sorted(set(l.strip().upper() for l in comma_match.group(1).split(",") if l.strip() in valid_set))
        if len(letters) > 1:
            return ExtractResult(answer=",".join(letters), method="comma_multi", confident=False)

    # 8. Fallback: last valid letter in text
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
