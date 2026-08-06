from __future__ import annotations

from decision_engine.action_planner import ActionPlanner
from decision_engine.decision_engine import DecisionEngine
from decision_engine.simulation import SimulationEngine


class DecisionInferenceEngine:
    """
    End-to-end decision planner.
    """

    def __init__(self) -> None:

        self.engine = DecisionEngine()

        self.planner = ActionPlanner()

        self.simulator = SimulationEngine()

    def infer(
        self,
        *,
        failure_probability: float,
        confidence: float,
        severity: str,
        recommendation: str,
    ) -> dict:

        decision = self.engine.decide(
            failure_probability=failure_probability,
            confidence=confidence,
            severity=severity,
        )

        actions = self.planner.create_plan(
            recommendation
        )

        simulation = self.simulator.simulate(
            actions
        )

        return {
            **decision,
            "actions": actions,
            "simulation": simulation,
        }