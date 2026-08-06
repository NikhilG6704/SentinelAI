from decision_engine.action_planner import (
    ActionPlanner,
)
from decision_engine.execution_validator import (
    ExecutionValidator,
)
from decision_engine.inference import (
    DecisionInferenceEngine,
)
from decision_engine.simulation import (
    SimulationEngine,
)
from decision_engine.evaluator import (
    DecisionEvaluator,
)


def test_action_plan():

    planner = ActionPlanner()

    plan = planner.create_plan(
        "Restart Service"
    )

    assert len(plan) >= 5


def test_validator():

    validator = ExecutionValidator()

    assert validator.validate(
        asset_exists=True,
        workflow_exists=True,
        automation_enabled=True,
        permission_granted=True,
    )


def test_simulation():

    simulator = SimulationEngine()

    result = simulator.simulate(
        [
            "Restart Service",
            "Verify CPU",
        ]
    )

    assert "success_probability" in result

    assert result["estimated_recovery_time"] > 0


def test_inference():

    engine = DecisionInferenceEngine()

    result = engine.infer(
        failure_probability=0.92,
        confidence=0.95,
        severity="Critical",
        recommendation="Restart Service",
    )

    assert "actions" in result

    assert "simulation" in result

    assert "decision" in result


def test_evaluator():

    evaluator = DecisionEvaluator()

    result = evaluator.evaluate(
        planned=10,
        successful=9,
    )

    assert result["accuracy"] == 0.9