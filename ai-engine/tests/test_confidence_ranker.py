from recommendation_engine.confidence_calculator import (
    ConfidenceCalculator,
)
from recommendation_engine.knowledge_base import (
    Recommendation,
)
from recommendation_engine.recommendation_ranker import (
    RecommendationRanker,
)


def sample_recommendation():

    return Recommendation(
        action="Restart Service",
        reason="High CPU",
        estimated_recovery_time=5,
        severity="High",
        asset_types=["Server"],
    )


def test_confidence():

    calculator = ConfidenceCalculator()

    score = calculator.calculate(
        sample_recommendation()
    )

    assert score > 80


def test_ranking():

    recommendation = sample_recommendation()

    ranker = RecommendationRanker()

    ranked = ranker.rank(
        [recommendation]
    )

    assert len(ranked) == 1

    assert ranked[0][0].action == "Restart Service"

    assert ranked[0][1] > 80