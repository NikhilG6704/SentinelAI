from __future__ import annotations


class ActionPlanner:
    """
    Generates an execution plan from the selected decision.
    """

    DEFAULT_ACTIONS = {
        "Restart Service": [
            "Verify service availability",
            "Restart service",
            "Verify CPU usage",
            "Verify memory usage",
            "Close incident if healthy",
        ],
        "Restart Application": [
            "Verify application status",
            "Restart application",
            "Check application logs",
            "Verify memory usage",
            "Close incident if healthy",
        ],
        "Restart Network Interface": [
            "Check network connectivity",
            "Restart network interface",
            "Verify latency",
            "Run connectivity tests",
            "Close incident if healthy",
        ],
        "Clean Temporary Files": [
            "Check disk utilization",
            "Clean temporary files",
            "Verify free disk space",
            "Restart affected service",
            "Close incident if healthy",
        ],
        "Scale Service": [
            "Provision additional capacity",
            "Deploy new instance",
            "Update load balancer",
            "Verify service health",
            "Close incident if healthy",
        ],
    }

    def create_plan(
        self,
        recommendation: str,
    ) -> list[str]:

        return self.DEFAULT_ACTIONS.get(
            recommendation,
            [
                "Investigate incident",
                "Collect diagnostics",
                "Notify administrator",
            ],
        )