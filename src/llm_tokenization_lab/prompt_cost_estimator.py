"""Educational prompt cost estimation utilities."""

from __future__ import annotations

from dataclasses import dataclass

from .simple_tokenizer import token_count


@dataclass(frozen=True)
class PromptCostEstimate:
    """Approximate token and cost estimate for one prompt."""

    input_tokens: int
    output_tokens: int
    input_cost_per_1k: float
    output_cost_per_1k: float

    def __post_init__(self) -> None:
        if self.input_tokens < 0:
            raise ValueError("input_tokens must be greater than or equal to 0")
        if self.output_tokens < 0:
            raise ValueError("output_tokens must be greater than or equal to 0")
        if self.input_cost_per_1k < 0:
            raise ValueError("input_cost_per_1k must be greater than or equal to 0")
        if self.output_cost_per_1k < 0:
            raise ValueError("output_cost_per_1k must be greater than or equal to 0")

    def total_tokens(self) -> int:
        """Return input plus expected output tokens."""

        return self.input_tokens + self.output_tokens

    def estimated_cost(self) -> float:
        """Return approximate total cost for input and output tokens."""

        input_cost = (self.input_tokens / 1_000) * self.input_cost_per_1k
        output_cost = (self.output_tokens / 1_000) * self.output_cost_per_1k
        return input_cost + output_cost


def estimate_prompt_cost(
    input_text: str,
    expected_output_tokens: int,
    input_cost_per_1k: float,
    output_cost_per_1k: float,
) -> PromptCostEstimate:
    """Estimate prompt cost using the educational tokenizer.

    This is useful for learning and planning. It is not a provider billing
    calculator because production tokenizers differ by model.
    """

    if expected_output_tokens < 0:
        raise ValueError("expected_output_tokens must be greater than or equal to 0")
    if input_cost_per_1k < 0:
        raise ValueError("input_cost_per_1k must be greater than or equal to 0")
    if output_cost_per_1k < 0:
        raise ValueError("output_cost_per_1k must be greater than or equal to 0")

    return PromptCostEstimate(
        input_tokens=token_count(input_text),
        output_tokens=expected_output_tokens,
        input_cost_per_1k=input_cost_per_1k,
        output_cost_per_1k=output_cost_per_1k,
    )

