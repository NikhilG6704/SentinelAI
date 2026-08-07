"""
Benchmark runner for SentinelAI AI Engine.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import statistics
from pathlib import Path

from validation.configuration import validation_config
from validation.performance_validator import performance_validator
from utils.logger import logger


# ==========================================================
# Result Models
# ==========================================================


@dataclass(frozen=True)
class BenchmarkReport:
    iterations: int

    startup_average: float
    startup_min: float
    startup_max: float
    startup_std: float

    load_average: float
    load_min: float
    load_max: float
    load_std: float

    average_cpu: float
    average_memory: float


# ==========================================================
# Benchmark Runner
# ==========================================================


class BenchmarkRunner:
    """
    Executes repeatable performance benchmarks.
    """

    def run(self) -> BenchmarkReport:

        logger.info("Running AI Engine benchmark...")

        # -----------------------------
        # Warmup
        # -----------------------------

        for _ in range(validation_config.warmup_iterations):
            performance_validator.validate()

        # -----------------------------
        # Benchmark
        # -----------------------------

        startup_times = []
        load_times = []
        cpu_values = []
        memory_values = []

        for _ in range(validation_config.benchmark_iterations):

            metrics = performance_validator.validate()

            startup_times.append(metrics.startup_time)
            load_times.append(metrics.average_load_time)

            cpu_values.append(metrics.cpu_percent)
            memory_values.append(metrics.memory_percent)

        report = BenchmarkReport(
            iterations=validation_config.benchmark_iterations,

            startup_average=statistics.mean(startup_times),
            startup_min=min(startup_times),
            startup_max=max(startup_times),
            startup_std=statistics.stdev(startup_times)
            if len(startup_times) > 1 else 0.0,

            load_average=statistics.mean(load_times),
            load_min=min(load_times),
            load_max=max(load_times),
            load_std=statistics.stdev(load_times)
            if len(load_times) > 1 else 0.0,

            average_cpu=statistics.mean(cpu_values),
            average_memory=statistics.mean(memory_values),
        )

        validation_config.ensure_directories()

        report_path = (
            validation_config.reports_directory /
            "benchmark_report.json"
        )

        report_path.write_text(
            json.dumps(
                asdict(report),
                indent=4,
            )
        )

        logger.success(
            f"Benchmark report saved to {report_path}"
        )

        return report


benchmark_runner = BenchmarkRunner()