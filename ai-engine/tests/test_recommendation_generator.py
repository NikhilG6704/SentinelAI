from recommendation_engine.recommendation_generator import (
    RecommendationGenerator,
)


def test_generate_from_root_cause():

    generator = RecommendationGenerator()

    recommendations = generator.generate(
        root_cause="Memory Leak",
    )

    assert len(recommendations) == 1

    assert recommendations[0].action == "Restart Application"


def test_generate_from_anomaly():

    generator = RecommendationGenerator()

    recommendations = generator.generate(
        anomaly="High CPU",
    )

    assert len(recommendations) == 2


def test_duplicate_removal():

    generator = RecommendationGenerator()

    recommendations = generator.generate(
        anomaly="High CPU",
        root_cause="High CPU",
    )

    actions = [
        recommendation.action
        for recommendation in recommendations
    ]

    assert len(actions) == len(set(actions))


def test_unknown_issue():

    generator = RecommendationGenerator()

    recommendations = generator.generate(
        anomaly="Unknown",
    )

    assert recommendations == []