from __future__ import annotations

from recommendation_engine.confidence_calculator import (
    ConfidenceCalculator,
)
from recommendation_engine.knowledge_base import Recommendation


class RecommendationRanker:
    """
    Rank recommendations by confidence and recovery time.
    """

    def __init__(self) -> None:
        self.calculator = ConfidenceCalculator()

    def rank(
        self,
        recommendations: list[Recommendation],
    ) -> list[tuple[Recommendation, float]]:

        ranked = []

        for recommendation in recommendations:

            confidence = self.calculator.calculate(
                recommendation
            )

            ranked.append(
                (
                    recommendation,
                    confidence,
                )
            )

        ranked.sort(
            key=lambda item: (
                item[1],
                -item[0].estimated_recovery_time,
            ),
            reverse=True,
        )

        return ranked