import apiClient from "./client";
import type { ApiResponse } from "../types/api";

export type AgentStatus = "Online" | "Offline" | "Warning";

export interface MonitoringAgent {
  id: number;
  infrastructure_asset_id: number;
  agent_name: string;
  agent_version: string;
  registration_token: string;
  last_heartbeat: string;
  status: AgentStatus;
  created_at: string;
  updated_at: string;
}

export interface AgentCreate {
  infrastructure_asset_id: number;
  agent_name: string;
  agent_version: string;
}

export interface AgentUpdate {
  agent_version?: string | null;
  status?: AgentStatus | null;
  last_heartbeat?: string | null;
}

export async function getAgents(): Promise<ApiResponse<MonitoringAgent[]>> {
  const response =
    await apiClient.get<ApiResponse<MonitoringAgent[]>>("/monitoring-agents");

  return response.data;
}

export async function getAgent(
  agentId: number,
): Promise<ApiResponse<MonitoringAgent>> {
  const response = await apiClient.get<ApiResponse<MonitoringAgent>>(
    `/monitoring-agents/${agentId}`,
  );

  return response.data;
}

export async function getAgentsByAsset(
  assetId: number,
): Promise<ApiResponse<MonitoringAgent[]>> {
  const response = await apiClient.get<ApiResponse<MonitoringAgent[]>>(
    `/monitoring-agents/asset/${assetId}`,
  );

  return response.data;
}

export async function createAgent(
  payload: AgentCreate,
): Promise<ApiResponse<MonitoringAgent>> {
  const response = await apiClient.post<ApiResponse<MonitoringAgent>>(
    "/monitoring-agents",
    payload,
  );

  return response.data;
}

export async function updateAgent(
  agentId: number,
  payload: AgentUpdate,
): Promise<ApiResponse<MonitoringAgent>> {
  const response = await apiClient.put<ApiResponse<MonitoringAgent>>(
    `/monitoring-agents/${agentId}`,
    payload,
  );

  return response.data;
}

export async function deleteAgent(
  agentId: number,
): Promise<ApiResponse<unknown>> {
  const response = await apiClient.delete<ApiResponse<unknown>>(
    `/monitoring-agents/${agentId}`,
  );

  return response.data;
}
