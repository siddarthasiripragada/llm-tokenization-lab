"""Educational tokenizer utilities.

This module intentionally does not claim to match OpenAI, Anthropic, Gemini,
or any production tokenizer. It is a small teaching tool for making tokenization
visible with only the Python standard library.
"""

from __future__ import annotations

import re


TOKEN_PATTERN = re.compile(r"[A-Za-z]+|\d+|[^\w\s]|\w", re.UNICODE)


def simple_tokenize(text: str) -> list[str]:
    """Split text into words, numbers, punctuation, and symbols.

    Args:
        text: Input text to tokenize.

    Returns:
        A list of educational tokens. Empty input returns an empty list.

    Raises:
        TypeError: If text is not a string.
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if text == "":
        return []

    return TOKEN_PATTERN.findall(text)


def token_count(text: str) -> int:
    """Return the number of educational tokens in text."""

    return len(simple_tokenize(text))

