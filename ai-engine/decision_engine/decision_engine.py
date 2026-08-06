from __future__ import annotations

from decision_engine.policy_engine import (
    PolicyEngine,
)
from decision_engine.risk_assessor import (
    RiskAssessor,
)


class DecisionEngine:
    """
    Aggregates AI outputs into one decision.
    """

    def __init__(self) -> None:

        self.risk_assessor = RiskAssessor()

        self.policy_engine = PolicyEngine()

    def decide(
        self,
        *,
        failure_probability: float,
        confidence: float,
        severity: str,
    ) -> dict:

        risk = self.risk_assessor.assess(
            failure_probability=failure_probability,
            confidence=confidence,
            severity=severity,
        )

        decision = self.policy_engine.evaluate(
            risk["risk_level"]
        )

        return {
            "risk_level": risk["risk_level"],
            "risk_score": risk["risk_score"],
            "decision": decision,
        }