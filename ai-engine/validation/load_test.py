"""
Load testing for SentinelAI AI Engine.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import statistics
import time

from serving.configuration import serving_config
from serving.model_loader import model_loader
from utils.logger import logger
from validation.configuration import validation_config


@dataclass(frozen=True)
class LoadTestReport:
    total_requests: int
    successful_requests: int
    failed_requests: int

    throughput: float
    average_latency: float
    max_latency: float

    error_rate: float


class LoadTester:
    """
    Executes concurrent load tests against the model loader.
    """

    def _single_request(self, model_name: str) -> tuple[bool, float]:

        start = time.perf_counter()

        try:
            model_loader.load(model_name)
            success = True

        except Exception:
            # Fresh MLflow registry may not contain models yet.
            success = False

        latency = time.perf_counter() - start

        return success, latency

    def run(self) -> LoadTestReport:

        logger.info("Running load test...")

        model_names = serving_config.supported_models

        start = time.perf_counter()

        latencies = []
        successes = 0
        failures = 0

        with ThreadPoolExecutor(
            max_workers=validation_config.concurrent_workers
        ) as executor:

            futures = []

            for _ in range(validation_config.requests_per_worker):

                for model in model_names:

                    futures.append(
                        executor.submit(
                            self._single_request,
                            model,
                        )
                    )

            for future in as_completed(futures):

                success, latency = future.result()

                latencies.append(latency)

                if success:
                    successes += 1
                else:
                    failures += 1

        duration = time.perf_counter() - start

        total = successes + failures

        report = LoadTestReport(
            total_requests=total,
            successful_requests=successes,
            failed_requests=failures,
            throughput=total / duration if duration else 0.0,
            average_latency=statistics.mean(latencies),
            max_latency=max(latencies),
            error_rate=failures / total if total else 0.0,
        )

        logger.success("Load test completed.")

        return report


load_tester = LoadTester()