"""
Model promotion manager for SentinelAI.

Decides whether a newly trained model should replace the current
production model.
"""

from __future__ import annotations

from dataclasses import dataclass

from retraining.comparison import ComparisonResult
from retraining.configuration import retraining_config
from utils.logger import logger


@dataclass(frozen=True)
class PromotionDecision:
    """
    Result of a promotion decision.
    """

    promote: bool
    reason: str
    rollback_available: bool = True


class PromotionManager:
    """
    Applies promotion rules to candidate models.
    """

    def should_promote(
        self,
        comparison: ComparisonResult,
    ) -> PromotionDecision:
        """
        Decide whether the candidate model should be promoted.
        """

        current = comparison.current_metrics
        candidate = comparison.candidate_metrics

        current_f1 = current.get("f1_score", 0.0)
        candidate_f1 = candidate.get("f1_score", 0.0)

        current_precision = current.get("precision", 0.0)
        candidate_precision = candidate.get("precision", 0.0)

        f1_improvement = candidate_f1 - current_f1

        # ----------------------------------------------------------
        # Rule 1
        # ----------------------------------------------------------

        if (
            f1_improvement
            < retraining_config.minimum_f1_improvement
        ):
            return PromotionDecision(
                promote=False,
                reason=(
                    "F1-score improvement below "
                    f"{retraining_config.minimum_f1_improvement:.2%}"
                ),
            )

        # ----------------------------------------------------------
        # Rule 2
        # ----------------------------------------------------------

        if (
            not retraining_config.allow_precision_drop
            and candidate_precision < current_precision
        ):
            return PromotionDecision(
                promote=False,
                reason="Precision decreased.",
            )

        logger.success(
            "Candidate approved for promotion."
        )

        return PromotionDecision(
            promote=True,
            reason="Promotion criteria satisfied.",
        )

    def rollback_decision(
        self,
    ) -> PromotionDecision:
        """
        Rollback to the previous production model.
        """

        logger.warning(
            "Rollback to previous production model."
        )

        return PromotionDecision(
            promote=False,
            reason="Rollback to previous production model.",
            rollback_available=True,
        )


promotion_manager = PromotionManager()