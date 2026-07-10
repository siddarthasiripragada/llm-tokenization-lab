# Tokenization Guide

Tokenization is the process of converting text into smaller units that a model can process. Those units may be characters, words, byte sequences, or learned subword chunks.

## Key Ideas

- A token is not always a word.
- Common words or word fragments often become single tokens.
- Rare words are usually split into smaller pieces.
- Whitespace and punctuation can be tokens or parts of tokens depending on the tokenizer.
- Token counts affect context length, latency, and cost.

## Lab Exercises

1. Train the tokenizer on a small corpus.
2. Encode short and long sentences.
3. Compare word count with token count.
4. Change `vocab_size` and observe how token splits change.
5. Decode token ids and check whether the original text is reconstructed.

## Discussion Questions

- What happens when the tokenizer sees a character that was not in the training corpus?
- How does increasing the vocabulary size change the encoded output?
- Why might two similar strings have different token counts?
- What tradeoffs exist between small and large vocabularies?

