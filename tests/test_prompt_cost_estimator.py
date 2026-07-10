import pytest

from llm_tokenization_lab import PromptCostEstimate, estimate_prompt_cost


def test_estimate_prompt_cost_returns_prompt_cost_estimate() -> None:
    estimate = estimate_prompt_cost("hello world", 20, 0.01, 0.03)
    assert isinstance(estimate, PromptCostEstimate)


def test_total_tokens_equals_input_plus_output() -> None:
    estimate = PromptCostEstimate(10, 20, 0.01, 0.03)
    assert estimate.total_tokens() == 30


def test_estimated_cost_calculates_input_and_output_cost() -> None:
    estimate = PromptCostEstimate(
        input_tokens=1000,
        output_tokens=500,
        input_cost_per_1k=0.01,
        output_cost_per_1k=0.04,
    )
    assert estimate.estimated_cost() == pytest.approx(0.03)


def test_negative_output_tokens_raises_value_error() -> None:
    with pytest.raises(ValueError):
        estimate_prompt_cost("hello", -1, 0.01, 0.03)


def test_negative_cost_raises_value_error() -> None:
    with pytest.raises(ValueError):
        estimate_prompt_cost("hello", 10, -0.01, 0.03)

