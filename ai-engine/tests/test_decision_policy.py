from decision_engine.decision_engine import (
    DecisionEngine,
)
from decision_engine.policy_engine import (
    PolicyEngine,
)
from decision_engine.risk_assessor import (
    RiskAssessor,
)


def test_policy_lookup():

    engine = PolicyEngine()

    assert (
        engine.evaluate("Low")
        == "Recommendation Only"
    )

    assert (
        engine.evaluate("Critical")
        == "Automatic Recovery"
    )


def test_policy_update():

    engine = PolicyEngine()

    engine.update_policy(
        "Low",
        "Simulation",
    )

    assert (
        engine.evaluate("Low")
        == "Simulation"
    )


def test_risk_assessment():

    assessor = RiskAssessor()

    result = assessor.assess(
        failure_probability=0.9,
        confidence=0.95,
        severity="Critical",
    )

    assert result["risk_level"] == "Critical"


def test_decision_engine():

    engine = DecisionEngine()

    result = engine.decide(
        failure_probability=0.8,
        confidence=0.9,
        severity="High",
    )

    assert "decision" in result

    assert "risk_level" in result

    assert "risk_score" in result