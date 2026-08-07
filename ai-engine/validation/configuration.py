"""
Configuration for the SentinelAI validation framework.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ValidationConfig:
    """
    Configuration for validation and benchmarking.
    """

    # ------------------------------------------------------------------
    # Benchmark
    # ------------------------------------------------------------------

    benchmark_iterations: int = 100
    warmup_iterations: int = 10

    # ------------------------------------------------------------------
    # Load Testing
    # ------------------------------------------------------------------

    concurrent_workers: int = 10
    requests_per_worker: int = 50

    # ------------------------------------------------------------------
    # Performance Thresholds
    # ------------------------------------------------------------------

    max_startup_time: float = 10.0          # seconds
    max_model_load_time: float = 5.0        # seconds

    max_average_latency: float = 0.50       # seconds
    max_p95_latency: float = 1.00
    max_p99_latency: float = 2.00

    max_cpu_percent: float = 80.0
    max_memory_percent: float = 80.0

    # ------------------------------------------------------------------
    # Reports
    # ------------------------------------------------------------------

    reports_directory: Path = Path("reports")
    certification_directory: Path = Path("reports")

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    fail_on_missing_models: bool = False
    generate_markdown_reports: bool = True
    generate_json_reports: bool = True

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def ensure_directories(self) -> None:
        """Create report directories if they do not exist."""
        self.reports_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.certification_directory.mkdir(
            parents=True,
            exist_ok=True,
        )


validation_config = ValidationConfig()