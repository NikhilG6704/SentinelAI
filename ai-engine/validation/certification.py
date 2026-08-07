"""
Production certification for SentinelAI AI Engine.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
import json
from pathlib import Path

from utils.logger import logger

from validation.configuration import validation_config
from validation.integration_validator import (
    integration_validator,
    IntegrationValidationResult,
)
from validation.performance_validator import (
    performance_validator,
    PerformanceMetrics,
)
from validation.benchmark import (
    benchmark_runner,
    BenchmarkReport,
)
from validation.load_test import (
    load_tester,
    LoadTestReport,
)
from validation.regression_validator import (
    regression_validator,
    RegressionReport,
)


# ==========================================================
# Result Model
# ==========================================================


@dataclass(frozen=True)
class CertificationReport:

    certified: bool

    generated_at: str

    integration: IntegrationValidationResult

    performance: PerformanceMetrics

    benchmark: BenchmarkReport

    load_test: LoadTestReport

    regression: RegressionReport


# ==========================================================
# Certification
# ==========================================================


class ProductionCertification:

    def generate(
        self,
    ) -> CertificationReport:

        logger.info(
            "Generating production certification..."
        )

        integration = integration_validator.validate()

        performance = performance_validator.validate()

        benchmark = benchmark_runner.run()

        load = load_tester.run()

        regression = regression_validator.validate(
            "isolation_forest",
        )

        certified = all(
            [
                integration.success,
                regression.passed,
            ]
        )

        report = CertificationReport(
            certified=certified,
            generated_at=datetime.now(
                UTC
            ).isoformat(),

            integration=integration,
            performance=performance,
            benchmark=benchmark,
            load_test=load,
            regression=regression,
        )

        self._save(report)

        logger.success(
            f"Production certification completed "
            f"(certified={certified})"
        )

        return report

    # ------------------------------------------------------

    def _save(
        self,
        report: CertificationReport,
    ) -> None:

        validation_config.ensure_directories()

        json_file = (
            validation_config.reports_directory
            / "production_certification.json"
        )

        md_file = (
            validation_config.reports_directory
            / "production_certification.md"
        )

        json_file.write_text(
            json.dumps(
                asdict(report),
                indent=4,
                default=str,
            )
        )

        markdown = f"""# SentinelAI Production Certification

Generated:
{report.generated_at}

## Overall Status

Certified: {report.certified}

## Integration

Passed:
{report.integration.passed}/{len(report.integration.checks)}

## Performance

Startup Time:
{report.performance.startup_time:.3f}s

Average Load Time:
{report.performance.average_load_time:.3f}s

CPU:
{report.performance.cpu_percent:.2f}%

Memory:
{report.performance.memory_percent:.2f}%

## Benchmark

Iterations:
{report.benchmark.iterations}

Average Startup:
{report.benchmark.startup_average:.3f}s

Average Load:
{report.benchmark.load_average:.3f}s

## Load Test

Requests:
{report.load_test.total_requests}

Throughput:
{report.load_test.throughput:.2f} req/s

Average Latency:
{report.load_test.average_latency:.3f}s

Error Rate:
{report.load_test.error_rate:.2%}

## Regression

Registry Consistent:
{report.regression.registry_consistent}

Comparison Successful:
{report.regression.comparison_successful}

Overall:
{report.regression.passed}
"""

        md_file.write_text(markdown)


production_certification = ProductionCertification()