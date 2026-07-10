from llm_tokenization_lab import SimpleTokenizer, TokenizationResult


def test_train_encode_and_decode_round_trip_known_text() -> None:
    tokenizer = SimpleTokenizer.train(
        [
            "large language models tokenize text",
            "tokenization changes model cost",
            "language models use tokens",
        ],
        vocab_size=80,
    )

    text = "language models tokenize"
    ids = tokenizer.encode(text)

    assert ids
    assert tokenizer.decode(ids) == text


def test_encode_with_tokens_returns_result_object() -> None:
    tokenizer = SimpleTokenizer.train(["hello world", "hello tokens"], vocab_size=40)

    result = tokenizer.encode_with_tokens("hello")

    assert isinstance(result, TokenizationResult)
    assert len(result.ids) == len(result.tokens)
    assert result.tokens


def test_unknown_tokens_use_unknown_id() -> None:
    tokenizer = SimpleTokenizer.train(["abc"], vocab_size=8)

    ids = tokenizer.encode("z")

    assert ids == [tokenizer.vocab["<unk>"]]

