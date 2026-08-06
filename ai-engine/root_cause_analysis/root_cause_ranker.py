from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class RootCause:
    """
    Represents a ranked root cause.
    """

    cause: str
    confidence: float
    evidence: list[str]
    affected_components: list[str]


class RootCauseRanker:
    """
    Rank potential infrastructure root causes based on
    correlated evidence.
    """

    def __init__(self) -> None:
        self.results: list[RootCause] = []

    def rank(
        self,
        evidence: list[dict[str, Any]],
    ) -> list[RootCause]:
        """
        Rank candidate root causes.
        """

        ranked: list[RootCause] = []

        for item in evidence:

            score = float(item.get("score", 0.0))

            ranked.append(
                RootCause(
                    cause=item["cause"],
                    confidence=min(max(score, 0.0), 1.0),
                    evidence=item.get("evidence", []),
                    affected_components=item.get(
                        "affected_components",
                        [],
                    ),
                )
            )

        ranked.sort(
            key=lambda x: x.confidence,
            reverse=True,
        )

        self.results = ranked

        return ranked

    def top(
        self,
        n: int = 3,
    ) -> list[RootCause]:

        return self.results[:n]

    def clear(self) -> None:

        self.results.clear()