from __future__ import annotations

from pydantic import BaseModel, Field


class AIHealthResponse(BaseModel):
    status: str
    version: str
    message: str


class PredictFailureRequest(BaseModel):
    infrastructure_asset_id: int


class PredictFailureResponse(BaseModel):
    prediction: str
    confidence: float
    explanation: str


class DetectAnomalyRequest(BaseModel):
    monitoring_agent_id: int


class DetectAnomalyResponse(BaseModel):
    anomaly_detected: bool
    anomaly_score: float
    message: str


class RootCauseRequest(BaseModel):
    incident_id: int


class RootCauseResponse(BaseModel):
    probable_cause: str
    confidence: float
    recommendation: str


class RecommendationRequest(BaseModel):
    incident_id: int


class RecommendationResponse(BaseModel):
    recommended_action: str
    priority: str
    explanation: str