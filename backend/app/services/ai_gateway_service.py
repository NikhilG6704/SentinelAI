"""
AI Gateway Service.

Acts as the single interface between the backend and
future AI/ML models.

Currently returns mocked responses.
"""

from __future__ import annotations

from app.schemas.ai_gateway import (
    AIHealthResponse,
    DetectAnomalyRequest,
    DetectAnomalyResponse,
    PredictFailureRequest,
    PredictFailureResponse,
    RecommendationRequest,
    RecommendationResponse,
    RootCauseRequest,
    RootCauseResponse,
)


class AIGatewayService:
    """
    AI Gateway.

    This class will later call ML models, model servers,
    or external AI services. For now it returns mock
    responses while preserving the API contract.
    """

    @staticmethod
    def health() -> AIHealthResponse:
        return AIHealthResponse(
            status="Healthy",
            version="1.0.0",
            message="AI Gateway operational.",
        )

    @staticmethod
    def predict_failure(
        request: PredictFailureRequest,
    ) -> PredictFailureResponse:
        return PredictFailureResponse(
            prediction="Low Failure Risk",
            confidence=0.93,
            explanation=(
                f"Infrastructure Asset "
                f"{request.infrastructure_asset_id} "
                "appears healthy based on current metrics."
            ),
        )

    @staticmethod
    def detect_anomaly(
        request: DetectAnomalyRequest,
    ) -> DetectAnomalyResponse:
        return DetectAnomalyResponse(
            anomaly_detected=False,
            anomaly_score=0.08,
            message=(
                f"No anomalies detected for Monitoring Agent "
                f"{request.monitoring_agent_id}."
            ),
        )

    @staticmethod
    def root_cause(
        request: RootCauseRequest,
    ) -> RootCauseResponse:
        return RootCauseResponse(
            probable_cause="High CPU utilization",
            confidence=0.89,
            recommendation=(
                f"Investigate Incident "
                f"{request.incident_id} "
                "and review running processes."
            ),
        )

    @staticmethod
    def recommendation(
        request: RecommendationRequest,
    ) -> RecommendationResponse:
        return RecommendationResponse(
            recommended_action="Restart Monitoring Agent",
            priority="Medium",
            explanation=(
                f"Recommended recovery action for Incident "
                f"{request.incident_id}."
            ),
        )