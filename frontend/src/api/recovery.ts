import apiClient from "./client";
import type { ApiResponse } from "../types/api";

export type RecoveryActionType =
  | "RESTART_SERVICE"
  | "RESTART_CONTAINER"
  | "RESTART_VM"
  | "REBOOT_SERVER"
  | "CLEAR_CACHE"
  | "RESTART_MONITORING_AGENT"
  | "SEND_NOTIFICATION";

export type ExecutionMode = "Simulation";

export type ExecutionStatus =
  | "Pending"
  | "Running"
  | "Completed"
  | "Failed"
  | "Cancelled";

export interface RecoveryWorkflow {
  id: number;
  workflow_name: string;
  automation_rule_id: number;
  incident_id: number | null;
  infrastructure_asset_id: number;
  action_type: RecoveryActionType;
  execution_mode: ExecutionMode;
  execution_status: ExecutionStatus;
  execution_log: string | null;
  started_at: string | null;
  completed_at: string | null;
  executed_by: string;
  created_at: string;
  updated_at: string;
}

export interface RecoveryWorkflowCreate {
  workflow_name: string;
  automation_rule_id: number;
  incident_id?: number | null;
  infrastructure_asset_id: number;
  action_type: RecoveryActionType;
  executed_by: string;
}

export interface RecoveryWorkflowFilters {
  execution_status?: ExecutionStatus;
  action_type?: RecoveryActionType;
  skip?: number;
  limit?: number;
}

export async function getRecoveryWorkflows(
  filters?: RecoveryWorkflowFilters,
): Promise<ApiResponse<RecoveryWorkflow[]>> {
  const response = await apiClient.get<ApiResponse<RecoveryWorkflow[]>>(
    "/recovery-workflows",
    {
      params: filters,
    },
  );

  return response.data;
}

export async function getRecoveryWorkflow(
  workflowId: number,
): Promise<ApiResponse<RecoveryWorkflow>> {
  const response = await apiClient.get<ApiResponse<RecoveryWorkflow>>(
    `/recovery-workflows/${workflowId}`,
  );

  return response.data;
}

export async function createRecoveryWorkflow(
  payload: RecoveryWorkflowCreate,
): Promise<ApiResponse<RecoveryWorkflow>> {
  const response = await apiClient.post<ApiResponse<RecoveryWorkflow>>(
    "/recovery-workflows",
    payload,
  );

  return response.data;
}

export async function executeRecoveryWorkflow(
  workflowId: number,
): Promise<ApiResponse<RecoveryWorkflow>> {
  const response = await apiClient.post<ApiResponse<RecoveryWorkflow>>(
    `/recovery-workflows/${workflowId}/execute`,
  );

  return response.data;
}

export async function cancelRecoveryWorkflow(
  workflowId: number,
): Promise<ApiResponse<RecoveryWorkflow>> {
  const response = await apiClient.patch<ApiResponse<RecoveryWorkflow>>(
    `/recovery-workflows/${workflowId}/cancel`,
  );

  return response.data;
}

export async function deleteRecoveryWorkflow(
  workflowId: number,
): Promise<ApiResponse<RecoveryWorkflow>> {
  const response = await apiClient.delete<ApiResponse<RecoveryWorkflow>>(
    `/recovery-workflows/${workflowId}`,
  );

  return response.data;
}
