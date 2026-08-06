from __future__ import annotations

from root_cause_analysis.root_cause_ranker import RootCause


class ExplanationGenerator:
    """
    Generates human-readable explanations for the ranked
    root causes.
    """

    def generate(
        self,
        root_cause: RootCause,
    ) -> str:
        """
        Generate a human-readable explanation.
        """

        evidence = ", ".join(root_cause.evidence)

        components = ", ".join(
            root_cause.affected_components
        )

        return (
            f"The most probable root cause is "
            f"'{root_cause.cause}' "
            f"(confidence: {root_cause.confidence:.2%}). "
            f"This conclusion is supported by the following "
            f"evidence: {evidence}. "
            f"The affected components are: {components}."
        )

    def generate_all(
        self,
        root_causes: list[RootCause],
    ) -> list[str]:

        return [
            self.generate(cause)
            for cause in root_causes
        ]