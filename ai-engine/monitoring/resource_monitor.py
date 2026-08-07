"""
Resource monitoring for SentinelAI.
"""

from __future__ import annotations

from dataclasses import dataclass
import time

import psutil

from monitoring.configuration import monitoring_config
from utils.logger import logger


@dataclass(frozen=True)
class ResourceResult:
    """
    System resource monitoring result.
    """

    cpu_percent: float
    memory_percent: float
    process_memory_mb: float
    model_load_time_ms: float

    resources_ok: bool


class ResourceMonitor:
    """
    Monitors system resource utilization.
    """

    def evaluate(
        self,
        *,
        model_load_time_ms: float = 0.0,
    ) -> ResourceResult:

        cpu = psutil.cpu_percent(
            interval=0.1,
        )

        memory = psutil.virtual_memory().percent

        process = psutil.Process()

        process_memory = (
            process.memory_info().rss
            / (1024 * 1024)
        )

        resources_ok = (
            cpu <= monitoring_config.max_cpu_percent
            and memory <= monitoring_config.max_memory_percent
        )

        result = ResourceResult(
            cpu_percent=cpu,
            memory_percent=memory,
            process_memory_mb=process_memory,
            model_load_time_ms=model_load_time_ms,
            resources_ok=resources_ok,
        )

        logger.info(
            f"Resources OK={result.resources_ok}"
        )

        return result

    def measure_model_load(
        self,
        loader,
        *args,
        **kwargs,
    ):
        """
        Measure model loading time.
        """

        start = time.perf_counter()

        model = loader(
            *args,
            **kwargs,
        )

        elapsed = (
            time.perf_counter()
            - start
        ) * 1000

        return model, elapsed


resource_monitor = ResourceMonitor()