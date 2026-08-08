import apiClient from "./client";
import type { ApiResponse } from "../types/api";

export type AlertSeverity = "Low" | "Medium" | "High" | "Critical";

export type AlertStatus = "Active" | "Acknowledged" | "Resolved";

export interface Alert {
  id: number;
  infrastructure_asset_id: number;
  monitoring_agent_id: number;
  system_metric_id: number | null;
  incident_id: number | null;
  alert_title: string;
  alert_description: string;
  severity: AlertSeverity;
  status: AlertStatus;
  metric_name: string;
  metric_value: number;
  threshold_value: number;
  triggered_at: string;
  acknowledged_at: string | null;
  resolved_at: string | null;
  resolution_summary: string | null;
  created_at: string;
  updated_at: string;
}

export interface AlertFilters {
  status?: AlertStatus;
  severity?: AlertSeverity;
  infrastructure_asset_id?: number;
  monitoring_agent_id?: number;
  skip?: number;
  limit?: number;
}

export interface AlertUpdate {
  alert_title?: string | null;
  alert_description?: string | null;
  severity?: AlertSeverity | null;
}

export interface AlertResolve {
  resolution_summary: string;
}

export async function getAlerts(
  filters?: AlertFilters,
): Promise<ApiResponse<Alert[]>> {
  const response = await apiClient.get<ApiResponse<Alert[]>>("/alerts", {
    params: filters,
  });

  return response.data;
}

export async function getAlert(alertId: number): Promise<ApiResponse<Alert>> {
  const response = await apiClient.get<ApiResponse<Alert>>(
    `/alerts/${alertId}`,
  );

  return response.data;
}

export async function updateAlert(
  alertId: number,
  payload: AlertUpdate,
): Promise<ApiResponse<Alert>> {
  const response = await apiClient.put<ApiResponse<Alert>>(
    `/alerts/${alertId}`,
    payload,
  );

  return response.data;
}

export async function acknowledgeAlert(
  alertId: number,
): Promise<ApiResponse<Alert>> {
  const response = await apiClient.patch<ApiResponse<Alert>>(
    `/alerts/${alertId}/acknowledge`,
  );

  return response.data;
}

export async function resolveAlert(
  alertId: number,
  payload: AlertResolve,
): Promise<ApiResponse<Alert>> {
  const response = await apiClient.patch<ApiResponse<Alert>>(
    `/alerts/${alertId}/resolve`,
    payload,
  );

  return response.data;
}
