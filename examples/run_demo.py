from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from llm_tokenization_lab import (
    TokenBudget,
    chunk_by_token_budget,
    estimate_prompt_cost,
    simple_tokenize,
    token_count,
)


def show_tokens(label: str, text: str) -> None:
    tokens = simple_tokenize(text)
    print(f"\n{label}")
    print(f"Text: {text}")
    print(f"Tokens ({len(tokens)}): {tokens}")


def main() -> None:
    show_tokens("Normal English", "Tokenization happens before reasoning.")
    show_tokens("SQL", "SELECT user_id, COUNT(*) FROM events WHERE status = 'failed';")
    show_tokens("JSON", '{"user_id":"acct_123","plan":"enterprise","active":true}')
    show_tokens("Identifier", "customerBillingExportJob_v2_failed_count")

    budget = TokenBudget(
        max_context_tokens=8192,
        system_prompt_tokens=600,
        user_query_tokens=token_count("Summarize the latest incident."),
        expected_output_tokens=800,
        safety_margin_tokens=500,
        chat_history_tokens=900,
        tool_output_tokens=250,
    )

    print("\nToken Budget")
    print(f"Used tokens: {budget.used_tokens()}")
    print(f"Available for retrieval: {budget.available_for_retrieval()}")
    print(f"Utilization ratio: {budget.utilization_ratio():.2%}")

    estimate = estimate_prompt_cost(
        input_text="Summarize this incident log and identify likely root cause.",
        expected_output_tokens=300,
        input_cost_per_1k=0.005,
        output_cost_per_1k=0.015,
    )

    print("\nPrompt Cost Estimate")
    print(f"Input tokens: {estimate.input_tokens}")
    print(f"Expected output tokens: {estimate.output_tokens}")
    print(f"Estimated cost: ${estimate.estimated_cost():.6f}")

    text = (
        "Tokenization affects cost latency context windows retrieval quality "
        "and prompt design in production LLM systems."
    )
    chunks = chunk_by_token_budget(text, max_tokens_per_chunk=6, overlap_tokens=2)

    print("\nToken-Aware Chunks")
    for index, chunk in enumerate(chunks, start=1):
        print(f"{index}. {chunk}")


if __name__ == "__main__":
    main()
