"""
Performance validator for SentinelAI AI Engine.
"""

from __future__ import annotations

from dataclasses import dataclass
import statistics
import time

import psutil

from deployment.startup import startup_service
from serving.configuration import serving_config
from serving.model_loader import model_loader
from utils.logger import logger


# ==========================================================
# Result Models
# ==========================================================


@dataclass(frozen=True)
class PerformanceMetrics:
    startup_time: float
    average_load_time: float
    p95_load_time: float
    p99_load_time: float
    cpu_percent: float
    memory_percent: float


# ==========================================================
# Validator
# ==========================================================


class PerformanceValidator:
    """
    Measures startup and model loading performance.
    """

    def measure_startup(self) -> float:
        """
        Measure startup initialization time.
        """

        start = time.perf_counter()

        startup_service.initialize(
            warm_models=False,
        )

        return time.perf_counter() - start

    def measure_model_loading(self) -> list[float]:
        """
        Measure loading time for each supported model.
        """

        timings: list[float] = []

        for model_name in serving_config.supported_models:

            start = time.perf_counter()

            try:
                model_loader.load(model_name)
            except Exception:
                # Ignore missing registry models.
                pass

            timings.append(
                time.perf_counter() - start
            )

        return timings

    def validate(self) -> PerformanceMetrics:
        """
        Execute all performance measurements.
        """

        logger.info(
            "Running performance validation..."
        )

        startup_time = self.measure_startup()

        load_times = self.measure_model_loading()

        cpu = psutil.cpu_percent(interval=1)

        memory = psutil.virtual_memory().percent

        average = statistics.mean(load_times)

        load_times = sorted(load_times)

        p95 = load_times[
            int(len(load_times) * 0.95)
        ]

        p99 = load_times[
            int(len(load_times) * 0.99)
        ]

        logger.success(
            "Performance validation completed."
        )

        return PerformanceMetrics(
            startup_time=startup_time,
            average_load_time=average,
            p95_load_time=p95,
            p99_load_time=p99,
            cpu_percent=cpu,
            memory_percent=memory,
        )


performance_validator = PerformanceValidator()