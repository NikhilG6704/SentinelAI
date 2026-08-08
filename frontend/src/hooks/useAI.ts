import { useMutation, useQuery } from "@tanstack/react-query";

import {
  getAIHealth,
  predictFailure,
  detectAnomaly,
  analyzeRootCause,
  getRecommendation,
  type PredictFailureRequest,
  type DetectAnomalyRequest,
  type RootCauseRequest,
  type RecommendationRequest,
} from "../api/ai";

export function useAIHealth() {
  return useQuery({
    queryKey: ["ai-health"],
    queryFn: getAIHealth,
    refetchInterval: 30_000,
  });
}

export function usePredictFailure() {
  return useMutation({
    mutationFn: (payload: PredictFailureRequest) => predictFailure(payload),
  });
}

export function useDetectAnomaly() {
  return useMutation({
    mutationFn: (payload: DetectAnomalyRequest) => detectAnomaly(payload),
  });
}

export function useRootCause() {
  return useMutation({
    mutationFn: (payload: RootCauseRequest) => analyzeRootCause(payload),
  });
}

export function useRecommendation() {
  return useMutation({
    mutationFn: (payload: RecommendationRequest) => getRecommendation(payload),
  });
}
