from root_cause_analysis.explanation_generator import (
    ExplanationGenerator,
)

from root_cause_analysis.root_cause_ranker import (
    RootCause,
)


def sample_root_cause():

    return RootCause(
        cause="Memory Leak",
        confidence=0.91,
        evidence=[
            "High Memory Usage",
            "OOM Errors",
        ],
        affected_components=[
            "Authentication Service",
        ],
    )


def test_generate():

    generator = ExplanationGenerator()

    explanation = generator.generate(
        sample_root_cause()
    )

    assert "Memory Leak" in explanation

    assert "91.00%" in explanation

    assert "Authentication Service" in explanation


def test_generate_all():

    generator = ExplanationGenerator()

    explanations = generator.generate_all(
        [
            sample_root_cause(),
            sample_root_cause(),
        ]
    )

    assert len(explanations) == 2