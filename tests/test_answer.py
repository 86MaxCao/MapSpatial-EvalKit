"""Test answer extraction — all priority levels and edge cases."""

from mapspatial.eval.answer import extract_answer, is_correct, ExtractResult


def test_answer_tag():
    result = extract_answer("The answer is <answer>B</answer>")
    assert result.answer == "B"
    assert result.confident
    assert result.method == "answer_tag"


def test_answer_tag_multi():
    result = extract_answer("Result: <answer>A,C</answer>")
    assert result.answer == "A,C"
    assert result.confident


def test_explicit_pattern():
    result = extract_answer("After analysis, THE ANSWER IS D.")
    assert result.answer == "D"
    assert result.confident
    assert result.method == "explicit"


def test_chinese_pattern():
    result = extract_answer("经过分析，答案：C")
    assert result.answer == "C"
    assert result.confident
    assert result.method == "chinese"


def test_short_single():
    result = extract_answer("A")
    assert result.answer == "A"
    assert result.confident
    assert result.method == "short_single"


def test_think_block_stripped():
    """Answers should not be extracted from within  <|im_start|>... blocks."""
    text = """Let me think about this.
<identally, the answer might be B
</im_start|> answer is D
<answer>D</answer>"""
    # Wait, let me use proper think tags
    text = "Let me think.\nI think it might be B.\nActually, I'm not sure if it's A or B.\n\nThe answer is C."
    result = extract_answer(text)
    assert result.answer == "C"
    assert result.confident


def test_think_tags_no_extraction():
    """Don't extract from thinking content."""
    text = "Let me think... it could be A or B.\n\nLet me think more...\n\nWait, let me reconsider B.\n\nThe answer is D."
    result = extract_answer(text)
    assert result.answer == "D"
    assert result.method == "explicit"


def test_fallback_last_letter():
    result = extract_answer("I looked at the map and determined the direction is northeast so the answer should be B")
    # No explicit pattern, but last letter B is in text
    assert result.answer == "B"
    assert not result.confident
    assert result.method == "last_letter"


def test_empty_response():
    result = extract_answer("")
    assert result.answer == ""
    assert not result.confident


def test_no_match():
    result = extract_answer("I don't know the answer to this question.")
    assert result.answer == ""
    assert result.method == "no_match"


def test_think_only_explicit_after_image_start():
    """ThinkMorph C-F: letter is inside </think> then <image_start>."""
    text = (
        "<think>From the green point clockwise the order is red, yellow. "
        "Therefore, the correct answer is: B.</think><image_start>"
    )
    result = extract_answer(text)
    assert result.answer == "B"
    assert result.confident
    assert result.method == "think_explicit"


def test_think_only_without_explicit_stays_empty():
    """Do not last-letter harvest from a think-only leftover."""
    text = "<think>Maybe A or C. Not sure about D.</think><image_start>"
    result = extract_answer(text)
    assert result.answer == ""
    assert result.method == "no_match"


def test_with_sample_meta():
    """Test using multiple_choice from sample metadata for valid letters."""
    meta = {
        "multiple_choice": {
            "choices": [
                {"key": "A", "text": "option A"},
                {"key": "B", "text": "option B"},
                {"key": "C", "text": "option C"},
                {"key": "D", "text": "option D"},
                {"key": "E", "text": "option E"},
            ]
        }
    }
    result = extract_answer("The answer is E", sample_meta=meta)
    assert result.answer == "E"
    assert result.confident


def test_is_correct_single():
    assert is_correct("B", "B")
    assert not is_correct("B", "C")


def test_is_correct_multi():
    assert is_correct("A,C", "C,A")
    assert not is_correct("A,B", "A,C")
