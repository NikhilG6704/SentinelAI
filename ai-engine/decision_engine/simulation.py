from __future__ import annotations

import random


class SimulationEngine:
    """
    Simulates a recovery plan.
    """

    def simulate(
        self,
        actions: list[str],
    ) -> dict:

        return {
            "planned_actions": actions,
            "estimated_recovery_time": len(actions) * 2,
            "success_probability": round(
                random.uniform(0.80, 0.99),
                2,
            ),
            "expected_system_impact": "Low",
        }