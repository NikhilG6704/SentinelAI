import apiClient from "./client";
import type { ApiResponse } from "../types/api";

export interface AIHealthResponse {
  status: string;
}

export interface PredictFailureRequest {
  infrastructure_asset_id: number;
}

export interface PredictFailureResponse {
  prediction: string;
  confidence: number;
  explanation: string;
}

export interface DetectAnomalyRequest {
  monitoring_agent_id: number;
}

export interface DetectAnomalyResponse {
  anomaly_detected: boolean;
  anomaly_score: number;
  message: string;
}

export interface RootCauseRequest {
  incident_id: number;
}

export interface RootCauseResponse {
  probable_cause: string;
  confidence: number;
  recommendation: string;
}

export interface RecommendationRequest {
  incident_id: number;
}

export interface RecommendationResponse {
  recommended_action: string;
  priority: string;
  explanation: string;
}

export async function getAIHealth(): Promise<ApiResponse<AIHealthResponse>> {
  const response =
    await apiClient.get<ApiResponse<AIHealthResponse>>("/ai/health");

  return response.data;
}

export async function predictFailure(
  payload: PredictFailureRequest,
): Promise<ApiResponse<PredictFailureResponse>> {
  const response = await apiClient.post<ApiResponse<PredictFailureResponse>>(
    "/ai/predict-failure",
    payload,
  );

  return response.data;
}

export async function detectAnomaly(
  payload: DetectAnomalyRequest,
): Promise<ApiResponse<DetectAnomalyResponse>> {
  const response = await apiClient.post<ApiResponse<DetectAnomalyResponse>>(
    "/ai/detect-anomaly",
    payload,
  );

  return response.data;
}

export async function analyzeRootCause(
  payload: RootCauseRequest,
): Promise<ApiResponse<RootCauseResponse>> {
  const response = await apiClient.post<ApiResponse<RootCauseResponse>>(
    "/ai/root-cause",
    payload,
  );

  return response.data;
}

export async function getRecommendation(
  payload: RecommendationRequest,
): Promise<ApiResponse<RecommendationResponse>> {
  const response = await apiClient.post<ApiResponse<RecommendationResponse>>(
    "/ai/recommendation",
    payload,
  );

  return response.data;
}
