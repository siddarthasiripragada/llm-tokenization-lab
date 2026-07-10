from llm_tokenization_lab import SimpleTokenizer


def main() -> None:
    corpus = [
        "large language models tokenize text",
        "tokenization changes context length and cost",
        "models process tokens instead of raw words",
    ]
    tokenizer = SimpleTokenizer.train(corpus, vocab_size=60)

    text = "language models tokenize text"
    result = tokenizer.encode_with_tokens(text)

    print(f"Input: {text}")
    print(f"Tokens: {result.tokens}")
    print(f"Token ids: {result.ids}")
    print(f"Decoded: {tokenizer.decode(result.ids)}")


if __name__ == "__main__":
    main()

