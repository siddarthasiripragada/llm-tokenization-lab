# LLM Tokenization Lab

A hands-on Python lab for exploring how large language model tokenizers split text, count tokens, and reconstruct strings.

The project includes a small tokenizer implementation, examples, tests, and short docs that make it easy to experiment with vocabulary design and byte-pair encoding concepts.

## Repository Structure

```text
llm-tokenization-lab/
├── docs/                  # Concept notes and lab guide
├── examples/              # Runnable examples
├── src/
│   └── llm_tokenization_lab/
│       ├── __init__.py
│       └── tokenizer.py   # Simple tokenizer and BPE-style trainer
├── tests/                 # Pytest test suite
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Quick Start

Create a virtual environment and install the project in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

Run the tests:

```bash
pytest
```

Run the example:

```bash
python examples/basic_tokenization.py
```

## What You Can Explore

- How text is split into tokens.
- Why token counts differ from word counts.
- How vocabulary size changes encoded output.
- How a small byte-pair encoding style tokenizer learns common merges.
- How decoding reconstructs text from token ids.

## Example

```python
from llm_tokenization_lab import SimpleTokenizer

tokenizer = SimpleTokenizer.train(
    ["large language models tokenize text", "tokenization changes model cost"],
    vocab_size=40,
)

ids = tokenizer.encode("language models tokenize")
print(ids)
print(tokenizer.decode(ids))
```

## Development

The package uses a `src/` layout and `pytest` for tests.

Useful commands:

```bash
pytest
python -m pip install -e .
python examples/basic_tokenization.py
```

