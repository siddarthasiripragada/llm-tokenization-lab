"""Token budget helpers for context window planning."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TokenBudget:
    """Represent reserved token categories inside a model context window."""

    max_context_tokens: int
    system_prompt_tokens: int
    user_query_tokens: int
    expected_output_tokens: int
    safety_margin_tokens: int = 500
    chat_history_tokens: int = 0
    tool_output_tokens: int = 0

    def __post_init__(self) -> None:
        if self.max_context_tokens <= 0:
            raise ValueError("max_context_tokens must be greater than 0")

        fields = {
            "system_prompt_tokens": self.system_prompt_tokens,
            "user_query_tokens": self.user_query_tokens,
            "expected_output_tokens": self.expected_output_tokens,
            "safety_margin_tokens": self.safety_margin_tokens,
            "chat_history_tokens": self.chat_history_tokens,
            "tool_output_tokens": self.tool_output_tokens,
        }
        for name, value in fields.items():
            if value < 0:
                raise ValueError(f"{name} must be greater than or equal to 0")

    def used_tokens(self) -> int:
        """Return all reserved tokens except retrieval context."""

        return (
            self.system_prompt_tokens
            + self.user_query_tokens
            + self.expected_output_tokens
            + self.safety_margin_tokens
            + self.chat_history_tokens
            + self.tool_output_tokens
        )

    def available_for_retrieval(self) -> int:
        """Return remaining tokens available for retrieved context."""

        return max(self.max_context_tokens - self.used_tokens(), 0)

    def utilization_ratio(self) -> float:
        """Return used tokens divided by the maximum context size."""

        return self.used_tokens() / self.max_context_tokens

