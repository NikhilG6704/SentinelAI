from __future__ import annotations


class RCAModelSelector:
    """
    Selects the best available RCA strategy.

    Designed for future integration of:
    - Rule-based RCA
    - Graph-based RCA
    - Graph Neural Networks
    - LLM reasoning
    """

    def __init__(self) -> None:
        self.selected_model = "rule_based"

    def select(
        self,
        available_models: list[str],
    ) -> str:

        if not available_models:
            raise ValueError(
                "No RCA models available."
            )

        if self.selected_model in available_models:
            return self.selected_model

        return available_models[0]