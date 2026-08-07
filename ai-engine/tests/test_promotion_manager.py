from retraining.comparison import ComparisonResult
from retraining.promotion_manager import (
    PromotionDecision,
    PromotionManager,
)


def comparison(
    current_f1=0.90,
    candidate_f1=0.93,
    current_precision=0.92,
    candidate_precision=0.93,
):
    return ComparisonResult(
        improved=candidate_f1 > current_f1,
        metric_changes={
            "f1_score": candidate_f1 - current_f1,
            "precision": candidate_precision - current_precision,
        },
        current_metrics={
            "f1_score": current_f1,
            "precision": current_precision,
        },
        candidate_metrics={
            "f1_score": candidate_f1,
            "precision": candidate_precision,
        },
    )


def test_promote():
    manager = PromotionManager()

    decision = manager.should_promote(
        comparison()
    )

    assert isinstance(
        decision,
        PromotionDecision,
    )

    assert decision.promote


def test_small_improvement():
    manager = PromotionManager()

    decision = manager.should_promote(
        comparison(
            current_f1=0.90,
            candidate_f1=0.91,
        )
    )

    assert not decision.promote


def test_precision_drop():
    manager = PromotionManager()

    decision = manager.should_promote(
        comparison(
            candidate_precision=0.85,
        )
    )

    assert not decision.promote


def test_rollback():
    manager = PromotionManager()

    decision = manager.rollback_decision()

    assert not decision.promote
    assert decision.rollback_available


def test_reason():
    manager = PromotionManager()

    decision = manager.should_promote(
        comparison()
    )

    assert isinstance(
        decision.reason,
        str,
    )

    assert len(
        decision.reason
    ) > 0