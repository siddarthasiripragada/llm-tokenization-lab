# Tokenization: The First Thing Most People Skip

Before an LLM reasons, retrieves, summarizes, or uses tools, it does something much simpler: it turns text into tokens.

That step looks small. It is not small in the system.

Tokenization affects cost, latency, context window usage, RAG chunking, prompt design, retrieval quality, and how structured data behaves inside a prompt.

This repository explains tokenization from first principles with small Python examples. It uses only the Python standard library at runtime. No paid API key is required, and there are no external LLM API calls.

## Overview

An LLM does not directly operate on raw text.

The rough path is:

```text
text -> tokens -> token IDs -> embeddings -> transformer layers -> next-token prediction
```

This lab does not try to reproduce a production tokenizer from OpenAI, Anthropic, Gemini, or any other model provider. Instead, it provides a small educational tokenizer so the engineering ideas are visible.

## Why Tokenization Matters

Tokenization is the boundary between human-visible text and model-visible input.

Humans see words, paragraphs, JSON, SQL, logs, and tables. Models see token IDs. That difference matters when you design prompts, chunk documents, estimate cost, or decide how much retrieved context can fit.

A prompt that looks short can still use many tokens. A JSON payload can be visually compact but token-heavy. A domain-specific identifier can split into several pieces.

## Text to Tokens to Token IDs

Production tokenizers map text to integer IDs from a learned vocabulary.

This project keeps the idea simple:

```python
from llm_tokenization_lab import simple_tokenize, token_count

text = "Order ID abc_123 failed at 2026-07-09."

tokens = simple_tokenize(text)
count = token_count(text)

print(tokens)
print(count)
```

The tokenizer separates words, numbers, punctuation, and symbols. That makes it useful for learning, tests, and demos, while staying honest about what it is not.

## Why Not Split by Words?

Word splitting hides important details.

Consider:

```text
user_id = "acct_9f3a_json_export"
```

A word-based split might treat that as one unit. A tokenizer may see many units: words, underscores, digits, quotes, and punctuation.

That difference is why token counts can diverge from word counts. It is also why prompts with code, logs, SQL, or JSON often consume more context than expected.

## Tokenization as Compression

Subword tokenization is partly a compression strategy.

Common patterns can be represented with fewer tokens. Rare words, unusual identifiers, and mixed-format strings may be broken into smaller pieces.

The practical lesson is simple: the model-visible length of text depends on the tokenizer, not only on the number of characters or words.

## Cost, Latency, and Context Windows

Most hosted LLM APIs price and limit usage in tokens.

More input tokens usually means more work. More expected output tokens reserve more room. The context window is not a suggestion; it is a budget.

This project includes a small budgeting helper:

```python
from llm_tokenization_lab import TokenBudget

budget = TokenBudget(
    max_context_tokens=8192,
    system_prompt_tokens=600,
    user_query_tokens=120,
    expected_output_tokens=900,
    safety_margin_tokens=500,
    chat_history_tokens=700,
)

print(budget.used_tokens())
print(budget.available_for_retrieval())
print(budget.utilization_ratio())
```

## Tokenization and RAG Chunking

RAG systems often split documents before embedding and retrieval.

Chunking by characters alone can be misleading. A 2,000-character chunk of plain prose and a 2,000-character chunk of logs may have very different token counts.

Token-aware chunking helps you reserve space for:

- the system prompt
- the user query
- chat history
- retrieved context
- tool output
- the model response
- a safety margin

## Token Budgeting Example

The included cost estimator uses the educational tokenizer to approximate cost:

```python
from llm_tokenization_lab import estimate_prompt_cost

estimate = estimate_prompt_cost(
    input_text="Summarize this incident log...",
    expected_output_tokens=300,
    input_cost_per_1k=0.005,
    output_cost_per_1k=0.015,
)

print(estimate.total_tokens())
print(estimate.estimated_cost())
```

This is not a billing calculator. It is a first-principles tool for understanding why token measurement should happen early.

## Project Structure

```text
llm-tokenization-lab/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── src/
│   └── llm_tokenization_lab/
│       ├── __init__.py
│       ├── simple_tokenizer.py
│       ├── token_budget.py
│       ├── prompt_cost_estimator.py
│       └── chunk_size_demo.py
├── tests/
│   ├── test_simple_tokenizer.py
│   ├── test_token_budget.py
│   └── test_prompt_cost_estimator.py
├── docs/
│   └── tokenization_notes.md
└── examples/
    └── run_demo.py
```

## How to Run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
python examples/run_demo.py
```

## How to Test

```bash
pytest
```

## Key Takeaways

- Text is not what the model sees.
- Models process token IDs, not raw words.
- Human-visible length and model-visible length are different.
- Context windows are token budgets.
- RAG chunking should be token-aware.
- JSON, SQL, logs, and tables can consume many tokens quickly.
- Token budgeting is a production LLM engineering concern.

