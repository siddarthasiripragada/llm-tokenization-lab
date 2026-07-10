"""Educational token-aware chunking for RAG-style preprocessing."""

from __future__ import annotations

from .simple_tokenizer import simple_tokenize


def chunk_by_token_budget(
    text: str,
    max_tokens_per_chunk: int,
    overlap_tokens: int = 0,
) -> list[str]:
    """Split text into chunks using a token budget.

    This is an educational token-aware chunker, not a semantic chunker. It
    rebuilds chunks by joining tokens with spaces, which keeps the demo simple
    and makes token counts easy to inspect.
    """

    if max_tokens_per_chunk <= 0:
        raise ValueError("max_tokens_per_chunk must be greater than 0")
    if overlap_tokens < 0:
        raise ValueError("overlap_tokens must be greater than or equal to 0")
    if overlap_tokens >= max_tokens_per_chunk:
        raise ValueError("overlap_tokens must be less than max_tokens_per_chunk")

    tokens = simple_tokenize(text)
    if not tokens:
        return []

    chunks: list[str] = []
    step = max_tokens_per_chunk - overlap_tokens
    for start in range(0, len(tokens), step):
        chunk_tokens = tokens[start : start + max_tokens_per_chunk]
        if not chunk_tokens:
            break
        chunks.append(" ".join(chunk_tokens))
        if start + max_tokens_per_chunk >= len(tokens):
            break

    return chunks

