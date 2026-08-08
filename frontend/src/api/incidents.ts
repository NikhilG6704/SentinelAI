import apiClient from "./client";
import type { ApiResponse } from "../types/api";

export type IncidentSeverity = "Low" | "Medium" | "High" | "Critical";

export type IncidentStatus = "Open" | "Investigating" | "Resolved" | "Closed";

export interface Incident {
  id: number;
  infrastructure_asset_id: number;
  monitoring_agent_id: number | null;
  alert_id: number | null;
  incident_title: string;
  incident_description: string;
  severity: IncidentSeverity;
  status: IncidentStatus;
  detected_at: string;
  resolved_at: string | null;
  resolution_summary: string | null;
  created_at: string;
  updated_at: string;
}

export interface IncidentFilters {
  status?: IncidentStatus;
  severity?: IncidentSeverity;
  skip?: number;
  limit?: number;
}

export interface IncidentCreate {
  infrastructure_asset_id: number;
  monitoring_agent_id?: number | null;
  alert_id?: number | null;
  incident_title: string;
  incident_description: string;
  severity: IncidentSeverity;
}

export interface IncidentUpdate {
  incident_title?: string | null;
  incident_description?: string | null;
  severity?: IncidentSeverity | null;
  status?: IncidentStatus | null;
}

export interface IncidentResolve {
  resolution_summary: string;
}

export async function getIncidents(
  filters?: IncidentFilters,
): Promise<ApiResponse<Incident[]>> {
  const response = await apiClient.get<ApiResponse<Incident[]>>("/incidents", {
    params: filters,
  });

  return response.data;
}

export async function getIncident(
  incidentId: number,
): Promise<ApiResponse<Incident>> {
  const response = await apiClient.get<ApiResponse<Incident>>(
    `/incidents/${incidentId}`,
  );

  return response.data;
}

export async function createIncident(
  payload: IncidentCreate,
): Promise<ApiResponse<Incident>> {
  const response = await apiClient.post<ApiResponse<Incident>>(
    "/incidents",
    payload,
  );

  return response.data;
}

export async function updateIncident(
  incidentId: number,
  payload: IncidentUpdate,
): Promise<ApiResponse<Incident>> {
  const response = await apiClient.put<ApiResponse<Incident>>(
    `/incidents/${incidentId}`,
    payload,
  );

  return response.data;
}

export async function resolveIncident(
  incidentId: number,
  payload: IncidentResolve,
): Promise<ApiResponse<Incident>> {
  const response = await apiClient.patch<ApiResponse<Incident>>(
    `/incidents/${incidentId}/resolve`,
    payload,
  );

  return response.data;
}

export async function closeIncident(
  incidentId: number,
): Promise<ApiResponse<Incident>> {
  const response = await apiClient.patch<ApiResponse<Incident>>(
    `/incidents/${incidentId}/close`,
  );

  return response.data;
}
