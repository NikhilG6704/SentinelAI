from __future__ import annotations


class RiskAssessor:
    """
    Computes infrastructure risk level.
    """

    def assess(
        self,
        *,
        failure_probability: float,
        confidence: float,
        severity: str,
    ) -> dict:

        severity_weight = {
            "Low": 0.25,
            "Medium": 0.50,
            "High": 0.75,
            "Critical": 1.00,
        }

        score = (
            0.5 * failure_probability
            + 0.3 * confidence
            + 0.2 * severity_weight.get(
                severity,
                0.50,
            )
        )

        if score >= 0.85:
            level = "Critical"
        elif score >= 0.65:
            level = "High"
        elif score >= 0.40:
            level = "Medium"
        else:
            level = "Low"

        return {
            "risk_score": round(score, 3),
            "risk_level": level,
        }