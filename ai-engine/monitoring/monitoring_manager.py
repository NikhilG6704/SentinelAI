"""
Monitoring manager for SentinelAI.

Coordinates monitoring, alerting, reporting, and retraining decisions.
"""

from __future__ import annotations

from typing import Any

from monitoring.alert_manager import alert_manager
from monitoring.concept_drift import concept_drift_detector
from monitoring.data_drift import data_drift_detector
from monitoring.latency_monitor import latency_monitor
from monitoring.performance_monitor import performance_monitor
from monitoring.report_generator import report_generator
from monitoring.resource_monitor import resource_monitor
from retraining.trigger import retraining_trigger
from utils.logger import logger


class MonitoringManager:
    """
    Central monitoring orchestrator.
    """

    def monitor(
        self,
        *,
        model_name: str,
        reference_data,
        current_data,
        previous_predictions,
        current_predictions,
        previous_confidence,
        current_confidence,
        previous_labels,
        current_labels,
        y_true,
        y_pred,
        probabilities,
        latencies_ms,
        model_load_time_ms: float = 0.0,
    ) -> dict[str, Any]:
        """
        Execute the complete monitoring workflow.
        """

        logger.info(
            f"Monitoring '{model_name}'."
        )

        # ----------------------------------------------------------
        # Drift Detection
        # ----------------------------------------------------------

        data_drift = data_drift_detector.detect(
            reference_data,
            current_data,
        )

        concept_drift = concept_drift_detector.detect(
            previous_predictions=previous_predictions,
            current_predictions=current_predictions,
            previous_confidence=previous_confidence,
            current_confidence=current_confidence,
            previous_labels=previous_labels,
            current_labels=current_labels,
        )

        # ----------------------------------------------------------
        # Performance
        # ----------------------------------------------------------

        performance = performance_monitor.evaluate(
            y_true=y_true,
            y_pred=y_pred,
            probabilities=probabilities,
        )

        # ----------------------------------------------------------
        # Latency
        # ----------------------------------------------------------

        latency = latency_monitor.evaluate(
            latencies_ms,
        )

        # ----------------------------------------------------------
        # Resources
        # ----------------------------------------------------------

        resources = resource_monitor.evaluate(
            model_load_time_ms=model_load_time_ms,
        )

        # ----------------------------------------------------------
        # Alerts
        # ----------------------------------------------------------

        alert_manager.clear()

        if data_drift.drift_detected:
            alert_manager.data_drift(
                {
                    "psi": data_drift.psi,
                    "js": data_drift.js_distance,
                }
            )

        if concept_drift.drift_detected:
            alert_manager.concept_drift(
                {
                    "prediction_shift": concept_drift.prediction_shift,
                }
            )

        if not performance.performance_ok:
            alert_manager.performance(
                {
                    "f1": performance.f1_score,
                }
            )

        if not latency.latency_ok:
            alert_manager.latency(
                {
                    "p95": latency.p95_ms,
                }
            )

        if not resources.resources_ok:
            alert_manager.resources(
                {
                    "cpu": resources.cpu_percent,
                    "memory": resources.memory_percent,
                }
            )

        alerts = alert_manager.history()

        # ----------------------------------------------------------
        # Report
        # ----------------------------------------------------------

        report = report_generator.generate(
            model_name=model_name,
            data_drift=data_drift,
            concept_drift=concept_drift,
            performance=performance,
            latency=latency,
            resources=resources,
            alerts=alerts,
        )

        report_path = report_generator.save(
            report,
        )

        return {
            "report": report,
            "report_path": report_path,
            "alerts": alerts,
            "retraining_required": (
                data_drift.drift_detected
                or concept_drift.drift_detected
                or not performance.performance_ok
            ),
        }

    # --------------------------------------------------------------
    # Retraining Integration
    # --------------------------------------------------------------

    def trigger_retraining_if_required(
        self,
        *,
        monitoring_result: dict[str, Any],
        **pipeline_kwargs,
    ):
        """
        Trigger retraining if monitoring requires it.
        """

        if not monitoring_result[
            "retraining_required"
        ]:
            return None

        logger.warning(
            "Retraining triggered by monitoring."
        )

        return retraining_trigger.trigger_retraining(
            **pipeline_kwargs,
        )


monitoring_manager = MonitoringManager()