from recommendation_engine.evaluator import (
    RecommendationEvaluator,
)
from recommendation_engine.inference import (
    RecommendationInferenceEngine,
)
from recommendation_engine.recommendation_generator import (
    RecommendationGenerator,
)
from recommendation_engine.recommendation_validator import (
    RecommendationValidator,
)


def test_validator():

    generator = RecommendationGenerator()

    validator = RecommendationValidator()

    recommendations = generator.generate(
        anomaly="High CPU",
    )

    valid = validator.validate(
        recommendations,
        "Service",
    )

    assert len(valid) > 0


def test_inference():

    engine = RecommendationInferenceEngine()

    result = engine.infer(
        anomaly="High CPU",
        asset_type="Service",
    )

    assert len(result) > 0

    assert "action" in result[0]

    assert "confidence" in result[0]


def test_evaluator():

    evaluator = RecommendationEvaluator()

    metrics = evaluator.evaluate(
        generated=10,
        accepted=8,
    )

    assert metrics["precision"] == 0.8