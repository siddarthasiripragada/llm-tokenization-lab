import pytest

from llm_tokenization_lab import TokenBudget


def test_available_for_retrieval_calculates_correctly() -> None:
    budget = TokenBudget(1000, 100, 50, 200, safety_margin_tokens=100)
    assert budget.available_for_retrieval() == 550


def test_used_tokens_calculates_correctly() -> None:
    budget = TokenBudget(
        max_context_tokens=2000,
        system_prompt_tokens=100,
        user_query_tokens=50,
        expected_output_tokens=300,
        safety_margin_tokens=100,
        chat_history_tokens=200,
        tool_output_tokens=75,
    )
    assert budget.used_tokens() == 825


def test_utilization_ratio_calculates_correctly() -> None:
    budget = TokenBudget(1000, 100, 100, 200, safety_margin_tokens=100)
    assert budget.utilization_ratio() == 0.5


def test_negative_values_raise_value_error() -> None:
    with pytest.raises(ValueError):
        TokenBudget(1000, -1, 0, 0)


def test_zero_max_context_tokens_raises_value_error() -> None:
    with pytest.raises(ValueError):
        TokenBudget(0, 0, 0, 0)


def test_available_for_retrieval_never_returns_negative() -> None:
    budget = TokenBudget(100, 50, 50, 50, safety_margin_tokens=50)
    assert budget.available_for_retrieval() == 0

