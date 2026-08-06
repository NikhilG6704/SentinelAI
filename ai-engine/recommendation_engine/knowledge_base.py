from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Recommendation:
    """
    Represents a recovery recommendation.
    """

    action: str
    reason: str
    estimated_recovery_time: int  # minutes
    severity: str
    asset_types: List[str]


class KnowledgeBase:
    """
    Stores mappings from infrastructure issues
    to recommended recovery actions.
    """

    def __init__(self) -> None:

        self._knowledge: Dict[str, List[Recommendation]] = {
            "High CPU": [
                Recommendation(
                    action="Restart Service",
                    reason="CPU utilization is critically high.",
                    estimated_recovery_time=5,
                    severity="High",
                    asset_types=["Server", "Service"],
                ),
                Recommendation(
                    action="Scale Service",
                    reason="Increase compute capacity.",
                    estimated_recovery_time=15,
                    severity="Critical",
                    asset_types=["Service"],
                ),
            ],
            "Memory Leak": [
                Recommendation(
                    action="Restart Application",
                    reason="Memory usage continuously increasing.",
                    estimated_recovery_time=3,
                    severity="Critical",
                    asset_types=["Application"],
                ),
            ],
            "Disk Full": [
                Recommendation(
                    action="Clean Temporary Files",
                    reason="Disk utilization exceeded threshold.",
                    estimated_recovery_time=10,
                    severity="High",
                    asset_types=["Server"],
                ),
                Recommendation(
                    action="Expand Storage",
                    reason="Persistent storage shortage.",
                    estimated_recovery_time=30,
                    severity="Critical",
                    asset_types=["Storage"],
                ),
            ],
            "Network Latency": [
                Recommendation(
                    action="Restart Network Interface",
                    reason="Network latency detected.",
                    estimated_recovery_time=5,
                    severity="Medium",
                    asset_types=["Switch", "Router", "Server"],
                ),
            ],
        }

    def get_recommendations(
        self,
        issue: str,
    ) -> List[Recommendation]:
        """
        Return recommendations for a given issue.
        """

        return list(
            self._knowledge.get(issue, [])
        )

    def add_recommendation(
        self,
        issue: str,
        recommendation: Recommendation,
    ) -> None:
        """
        Add a new recommendation.
        """

        self._knowledge.setdefault(
            issue,
            [],
        ).append(recommendation)

    def supported_issues(self) -> List[str]:
        """
        Return all supported issue names.
        """

        return sorted(
            self._knowledge.keys()
        )

    def size(self) -> int:
        """
        Number of supported issue categories.
        """

        return len(self._knowledge)