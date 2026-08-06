from __future__ import annotations


class RecommendationEvaluator:
    """
    Simple evaluator for recommendation quality.
    """

    def evaluate(
        self,
        generated: int,
        accepted: int,
    ) -> dict[str, float]:

        if generated == 0:
            precision = 0.0
        else:
            precision = accepted / generated

        return {
            "generated": generated,
            "accepted": accepted,
            "precision": round(precision, 2),
        }