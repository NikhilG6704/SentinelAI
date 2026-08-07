"""
Latency monitoring for SentinelAI.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from monitoring.configuration import monitoring_config
from utils.logger import logger


@dataclass(frozen=True)
class LatencyResult:
    """
    Latency statistics.
    """

    average_ms: float
    median_ms: float
    p95_ms: float
    p99_ms: float
    maximum_ms: float

    latency_ok: bool


class LatencyMonitor:
    """
    Monitors inference latency.
    """

    def evaluate(
        self,
        latencies_ms: np.ndarray | list[float],
    ) -> LatencyResult:

        latencies = np.asarray(
            latencies_ms,
            dtype=float,
        )

        average = float(
            np.mean(latencies)
        )

        median = float(
            np.median(latencies)
        )

        p95 = float(
            np.percentile(
                latencies,
                95,
            )
        )

        p99 = float(
            np.percentile(
                latencies,
                99,
            )
        )

        maximum = float(
            np.max(latencies)
        )

        latency_ok = (
            average <= monitoring_config.max_average_latency_ms
            and p95 <= monitoring_config.max_p95_latency_ms
            and p99 <= monitoring_config.max_p99_latency_ms
        )

        result = LatencyResult(
            average_ms=average,
            median_ms=median,
            p95_ms=p95,
            p99_ms=p99,
            maximum_ms=maximum,
            latency_ok=latency_ok,
        )

        logger.info(
            f"Latency OK={result.latency_ok}"
        )

        return result


latency_monitor = LatencyMonitor()