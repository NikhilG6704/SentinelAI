from __future__ import annotations

from typing import Any

from recommendation_engine.recommendation_generator import (
    RecommendationGenerator,
)
from recommendation_engine.recommendation_ranker import (
    RecommendationRanker,
)
from recommendation_engine.recommendation_validator import (
    RecommendationValidator,
)


class RecommendationInferenceEngine:
    """
    End-to-end recommendation inference engine.
    """

    def __init__(self) -> None:

        self.generator = RecommendationGenerator()
        self.validator = RecommendationValidator()
        self.ranker = RecommendationRanker()

    def infer(
        self,
        *,
        anomaly: str | None = None,
        root_cause: str | None = None,
        predicted_failure: str | None = None,
        asset_type: str,
    ) -> list[dict[str, Any]]:

        recommendations = self.generator.generate(
            anomaly=anomaly,
            root_cause=root_cause,
            predicted_failure=predicted_failure,
        )

        recommendations = self.validator.validate(
            recommendations,
            asset_type,
        )

        ranked = self.ranker.rank(
            recommendations,
        )

        results = []

        for recommendation, confidence in ranked[:5]:

            results.append(
                {
                    "action": recommendation.action,
                    "reason": recommendation.reason,
                    "confidence": confidence,
                    "severity": recommendation.severity,
                    "estimated_recovery_time": recommendation.estimated_recovery_time,
                }
            )

        return results