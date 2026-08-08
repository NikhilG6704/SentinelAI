import apiClient from "./client";
import type { ApiResponse } from "../types/api";

export async function getDashboardOverview(): Promise<ApiResponse<unknown>> {
  const response = await apiClient.get<ApiResponse<unknown>>(
    "/dashboard/overview",
  );

  return response.data;
}

export async function getDashboardHealth(): Promise<ApiResponse<unknown>> {
  const response =
    await apiClient.get<ApiResponse<unknown>>("/dashboard/health");

  return response.data;
}

export async function getDashboardAgents(): Promise<ApiResponse<unknown>> {
  const response =
    await apiClient.get<ApiResponse<unknown>>("/dashboard/agents");

  return response.data;
}

export async function getDashboardTrends(): Promise<ApiResponse<unknown>> {
  const response =
    await apiClient.get<ApiResponse<unknown>>("/dashboard/trends");

  return response.data;
}
