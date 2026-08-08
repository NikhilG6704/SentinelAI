import apiClient from "./client";
import type { ApiResponse } from "../types/api";

export interface SystemMetric {
  monitoring_agent_id: number;
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  network_in: number;
  network_out: number;
  uptime_seconds: number;
  id: number;
  collection_timestamp: string;
  created_at: string;
  updated_at: string;
}

export interface SystemMetricCreate {
  monitoring_agent_id: number;
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  network_in: number;
  network_out: number;
  uptime_seconds: number;
}

export async function getMetrics(): Promise<ApiResponse<SystemMetric[]>> {
  const response =
    await apiClient.get<ApiResponse<SystemMetric[]>>("/system-metrics");

  return response.data;
}

export async function getMetric(
  metricId: number,
): Promise<ApiResponse<SystemMetric>> {
  const response = await apiClient.get<ApiResponse<SystemMetric>>(
    `/system-metrics/${metricId}`,
  );

  return response.data;
}

export async function getMetricsByAgent(
  agentId: number,
): Promise<ApiResponse<SystemMetric[]>> {
  const response = await apiClient.get<ApiResponse<SystemMetric[]>>(
    `/system-metrics/agent/${agentId}`,
  );

  return response.data;
}

export async function createMetric(
  payload: SystemMetricCreate,
): Promise<ApiResponse<SystemMetric>> {
  const response = await apiClient.post<ApiResponse<SystemMetric>>(
    "/system-metrics",
    payload,
  );

  return response.data;
}
