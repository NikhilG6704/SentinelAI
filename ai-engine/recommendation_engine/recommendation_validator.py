from __future__ import annotations

from recommendation_engine.knowledge_base import Recommendation


class RecommendationValidator:
    """
    Validates generated recommendations.
    """

    def validate(
        self,
        recommendations: list[Recommendation],
        asset_type: str,
    ) -> list[Recommendation]:
        """
        Returns only valid recommendations.
        """

        valid: list[Recommendation] = []
        seen: set[str] = set()

        for recommendation in recommendations:

            if recommendation.action in seen:
                continue

            if asset_type not in recommendation.asset_types:
                continue

            seen.add(recommendation.action)
            valid.append(recommendation)

        return valid