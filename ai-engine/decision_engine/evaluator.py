from __future__ import annotations


class DecisionEvaluator:
    """
    Evaluates planning quality.
    """

    def evaluate(
        self,
        *,
        planned: int,
        successful: int,
    ) -> dict:

        if planned == 0:
            accuracy = 0.0
        else:
            accuracy = successful / planned

        return {
            "planned": planned,
            "successful": successful,
            "accuracy": round(
                accuracy,
                2,
            ),
        }