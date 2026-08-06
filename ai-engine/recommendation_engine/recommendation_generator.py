from __future__ import annotations

from recommendation_engine.knowledge_base import (
    KnowledgeBase,
    Recommendation,
)


class RecommendationGenerator:
    """
    Generates recovery recommendations using the
    knowledge base.
    """

    def __init__(self) -> None:
        self.knowledge_base = KnowledgeBase()

    def generate(
        self,
        *,
        anomaly: str | None = None,
        root_cause: str | None = None,
        predicted_failure: str | None = None,
    ) -> list[Recommendation]:
        """
        Generate recommendations from AI outputs.
        """

        recommendations: list[Recommendation] = []

        seen: set[tuple[str, str]] = set()

        for issue in (
            anomaly,
            root_cause,
            predicted_failure,
        ):

            if issue is None:
                continue

            for recommendation in self.knowledge_base.get_recommendations(
                issue
            ):

                key = (
                    recommendation.action,
                    recommendation.reason,
                )

                if key not in seen:
                    recommendations.append(
                        recommendation
                    )
                    seen.add(key)

        return recommendations