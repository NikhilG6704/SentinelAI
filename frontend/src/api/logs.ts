import apiClient from "./client";
import type { ApiResponse } from "../types/api";

export type LogLevel = "DEBUG" | "INFO" | "WARNING" | "ERROR" | "CRITICAL";

export interface SystemLog {
  id: number;
  infrastructure_asset_id: number;
  monitoring_agent_id: number;
  log_level: LogLevel;
  source: string;
  service_name: string;
  message: string;
  log_metadata: Record<string, unknown> | null;
  event_timestamp: string;
  created_at: string;
  updated_at: string;
}

export interface LogFilters {
  infrastructure_asset_id?: number;
  monitoring_agent_id?: number;
  log_level?: LogLevel;
  source?: string;
  service_name?: string;
  skip?: number;
  limit?: number;
}

export interface SystemLogCreate {
  infrastructure_asset_id: number;
  monitoring_agent_id: number;
  log_level: LogLevel;
  source: string;
  service_name: string;
  message: string;
  log_metadata?: Record<string, unknown> | null;
  event_timestamp: string;
}

export async function getLogs(
  filters?: LogFilters,
): Promise<ApiResponse<SystemLog[]>> {
  const response = await apiClient.get<ApiResponse<SystemLog[]>>(
    "/system-logs",
    {
      params: filters,
    },
  );

  return response.data;
}

export async function getLog(logId: number): Promise<ApiResponse<SystemLog>> {
  const response = await apiClient.get<ApiResponse<SystemLog>>(
    `/system-logs/${logId}`,
  );

  return response.data;
}

export async function createLog(
  payload: SystemLogCreate,
): Promise<ApiResponse<SystemLog>> {
  const response = await apiClient.post<ApiResponse<SystemLog>>(
    "/system-logs",
    payload,
  );

  return response.data;
}
