from __future__ import annotations

from typing import Any

import pandas as pd

from root_cause_analysis.correlation_engine import (
    CorrelationEngine,
)
from root_cause_analysis.explanation_generator import (
    ExplanationGenerator,
)
from root_cause_analysis.root_cause_ranker import (
    RootCause,
    RootCauseRanker,
)


class RootCauseInferenceEngine:
    """
    End-to-end Root Cause Analysis inference engine.
    """

    def __init__(self) -> None:

        self.correlation_engine = CorrelationEngine()
        self.ranker = RootCauseRanker()
        self.explainer = ExplanationGenerator()

    def infer(
        self,
        metrics: pd.DataFrame,
        candidate_causes: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Perform root cause inference.
        """

        correlations = self.correlation_engine.correlate_metrics(
            metrics
        )

        ranked = self.ranker.rank(
            candidate_causes
        )

        explanations = self.explainer.generate_all(
            ranked
        )

        return {
            "correlations": correlations,
            "root_causes": ranked,
            "explanations": explanations,
        }

    def top_root_cause(
        self,
        metrics: pd.DataFrame,
        candidate_causes: list[dict[str, Any]],
    ) -> RootCause:

        result = self.infer(
            metrics,
            candidate_causes,
        )

        return result["root_causes"][0]