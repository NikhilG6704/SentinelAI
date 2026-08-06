from __future__ import annotations


class PolicyEngine:
    """
    Rule-based automation policy evaluator.
    """

    DEFAULT_POLICIES = {
        "Low": "Recommendation Only",
        "Medium": "Manual Approval",
        "High": "Simulation",
        "Critical": "Automatic Recovery",
    }

    def __init__(self) -> None:
        self.policies = self.DEFAULT_POLICIES.copy()

    def evaluate(
        self,
        risk_level: str,
    ) -> str:
        """
        Return the automation policy for a risk level.
        """

        return self.policies.get(
            risk_level,
            "Recommendation Only",
        )

    def update_policy(
        self,
        risk_level: str,
        decision: str,
    ) -> None:

        self.policies[risk_level] = decision