import pytest

from llm_tokenization_lab import simple_tokenize, token_count


def test_empty_string_returns_empty_list() -> None:
    assert simple_tokenize("") == []


def test_sentence_tokenizes_into_non_empty_list() -> None:
    assert simple_tokenize("Tokenization comes before reasoning.")


def test_punctuation_becomes_separate_token() -> None:
    assert "," in simple_tokenize("hello, world")


def test_numbers_are_captured() -> None:
    assert "2026" in simple_tokenize("The year is 2026.")


def test_invalid_non_string_input_raises_type_error() -> None:
    with pytest.raises(TypeError):
        simple_tokenize(123)  # type: ignore[arg-type]


def test_token_count_matches_token_list_length() -> None:
    text = "JSON, SQL, and logs can be token-heavy."
    assert token_count(text) == len(simple_tokenize(text))

