from __future__ import annotations

from fastapi import APIRouter

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
from app.schemas.response import SuccessResponse
from app.services.ai_gateway_service import AIGatewayService

router = APIRouter(
    prefix="/api/v1/ai",
    tags=["AI Gateway"],
)


@router.get(
    "/health",
    response_model=SuccessResponse[AIHealthResponse],
)
async def health():
    response = AIGatewayService.health()

    return SuccessResponse(
        message="AI Gateway is healthy.",
        data=response,
    )


@router.post(
    "/predict-failure",
    response_model=SuccessResponse[PredictFailureResponse],
)
async def predict_failure(
    request: PredictFailureRequest,
):
    response = AIGatewayService.predict_failure(
        request,
    )

    return SuccessResponse(
        message="Failure prediction generated successfully.",
        data=response,
    )


@router.post(
    "/detect-anomaly",
    response_model=SuccessResponse[DetectAnomalyResponse],
)
async def detect_anomaly(
    request: DetectAnomalyRequest,
):
    response = AIGatewayService.detect_anomaly(
        request,
    )

    return SuccessResponse(
        message="Anomaly detection completed successfully.",
        data=response,
    )


@router.post(
    "/root-cause",
    response_model=SuccessResponse[RootCauseResponse],
)
async def root_cause(
    request: RootCauseRequest,
):
    response = AIGatewayService.root_cause(
        request,
    )

    return SuccessResponse(
        message="Root cause analysis completed successfully.",
        data=response,
    )


@router.post(
    "/recommendation",
    response_model=SuccessResponse[RecommendationResponse],
)
async def recommendation(
    request: RecommendationRequest,
):
    response = AIGatewayService.recommendation(
        request,
    )

    return SuccessResponse(
        message="Recovery recommendation generated successfully.",
        data=response,
    )