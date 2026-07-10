"""Small tokenizer utilities for learning tokenization concepts."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re


WORD_OR_SPACE = re.compile(r"\s+|[^\s]+")
END_OF_WORD = "</w>"
UNKNOWN = "<unk>"


@dataclass(frozen=True)
class TokenizationResult:
    """Encoded token ids plus their string tokens."""

    ids: list[int]
    tokens: list[str]


class SimpleTokenizer:
    """A compact BPE-style tokenizer for lab exercises.

    This implementation intentionally favors readability over production speed.
    It learns frequent adjacent symbol merges from a small corpus and can encode
    and decode new text with the learned vocabulary.
    """

    def __init__(self, vocab: dict[str, int], merges: list[tuple[str, str]]) -> None:
        if UNKNOWN not in vocab:
            raise ValueError(f"vocab must contain {UNKNOWN!r}")
        self.vocab = dict(vocab)
        self.id_to_token = {token_id: token for token, token_id in self.vocab.items()}
        self.merges = list(merges)

    @classmethod
    def train(cls, corpus: list[str], vocab_size: int = 100) -> "SimpleTokenizer":
        """Train a tiny BPE-style tokenizer from a text corpus."""

        if vocab_size < 4:
            raise ValueError("vocab_size must be at least 4")

        words = Counter()
        for text in corpus:
            for piece in WORD_OR_SPACE.findall(text):
                symbols = tuple(piece) + (END_OF_WORD,)
                words[symbols] += 1

        vocab_tokens = {UNKNOWN, END_OF_WORD}
        for symbols in words:
            vocab_tokens.update(symbols)

        merges: list[tuple[str, str]] = []
        while len(vocab_tokens) < vocab_size:
            pair_counts = cls._count_pairs(words)
            if not pair_counts:
                break

            best_pair, _ = pair_counts.most_common(1)[0]
            merged = "".join(best_pair)
            merges.append(best_pair)
            vocab_tokens.add(merged)
            words = cls._merge_pair(words, best_pair, merged)

        vocab = {token: index for index, token in enumerate(sorted(vocab_tokens))}
        return cls(vocab=vocab, merges=merges)

    def tokenize(self, text: str) -> list[str]:
        """Split text into learned tokens."""

        tokens: list[str] = []
        for piece in WORD_OR_SPACE.findall(text):
            symbols = list(piece) + [END_OF_WORD]
            for left, right in self.merges:
                symbols = self._apply_merge(symbols, left, right)
            tokens.extend(symbol for symbol in symbols if symbol != END_OF_WORD)
        return tokens

    def encode(self, text: str) -> list[int]:
        """Encode text as token ids."""

        return [self.vocab.get(token, self.vocab[UNKNOWN]) for token in self.tokenize(text)]

    def encode_with_tokens(self, text: str) -> TokenizationResult:
        """Encode text and keep both token ids and token strings."""

        tokens = self.tokenize(text)
        ids = [self.vocab.get(token, self.vocab[UNKNOWN]) for token in tokens]
        return TokenizationResult(ids=ids, tokens=tokens)

    def decode(self, ids: list[int]) -> str:
        """Decode token ids back into text when all ids are known."""

        pieces = [self.id_to_token[token_id] for token_id in ids]
        text = "".join(piece for piece in pieces if piece != UNKNOWN)
        return text.replace(END_OF_WORD, "")

    @staticmethod
    def _count_pairs(words: Counter[tuple[str, ...]]) -> Counter[tuple[str, str]]:
        pair_counts: Counter[tuple[str, str]] = Counter()
        for symbols, frequency in words.items():
            for index in range(len(symbols) - 1):
                pair_counts[(symbols[index], symbols[index + 1])] += frequency
        return pair_counts

    @staticmethod
    def _merge_pair(
        words: Counter[tuple[str, ...]],
        pair: tuple[str, str],
        merged: str,
    ) -> Counter[tuple[str, ...]]:
        merged_words: Counter[tuple[str, ...]] = Counter()
        for symbols, frequency in words.items():
            merged_words[tuple(SimpleTokenizer._apply_merge(list(symbols), *pair))] += frequency
        return merged_words

    @staticmethod
    def _apply_merge(symbols: list[str], left: str, right: str) -> list[str]:
        merged_symbols: list[str] = []
        index = 0
        while index < len(symbols):
            if index < len(symbols) - 1 and symbols[index] == left and symbols[index + 1] == right:
                merged_symbols.append(left + right)
                index += 2
            else:
                merged_symbols.append(symbols[index])
                index += 1
        return merged_symbols
