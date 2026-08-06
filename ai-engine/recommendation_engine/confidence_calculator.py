from __future__ import annotations

from recommendation_engine.knowledge_base import Recommendation


class ConfidenceCalculator:
    """
    Calculates confidence scores for recommendations.
    """

    SEVERITY_WEIGHT = {
        "Critical": 1.00,
        "High": 0.90,
        "Medium": 0.75,
        "Low": 0.60,
    }

    def calculate(
        self,
        recommendation: Recommendation,
        historical_success_rate: float = 0.90,
    ) -> float:
        """
        Returns a confidence score between 0 and 100.
        """

        severity_score = self.SEVERITY_WEIGHT.get(
            recommendation.severity,
            0.70,
        )

        confidence = (
            severity_score * 0.6
            + historical_success_rate * 0.4
        )

        return round(confidence * 100, 2)