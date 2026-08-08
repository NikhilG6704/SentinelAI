import apiClient from "./client";
import type { ApiResponse } from "../types/api";

export type AuditStatus = "Success" | "Failed" | "Warning";

export type AuditAction = string;

export interface AuditLog {
  id: number;
  entity_type: string;
  entity_id: number;
  action: AuditAction;
  performed_by: string;
  performed_at: string;
  status: AuditStatus;
  source_module: string;
  ip_address: string | null;
  metadata_json: Record<string, unknown> | null;
  details: string | null;
  created_at: string;
  updated_at: string;
}

export interface AuditLogFilters {
  action?: AuditAction;
  entity_type?: string;
  performed_by?: string;
  keyword?: string;
  start_time?: string;
  end_time?: string;
  skip?: number;
  limit?: number;
}

export interface AuditLogCreate {
  entity_type: string;
  entity_id: number;
  action: AuditAction;
  performed_by: string;
  performed_at: string;
  status: AuditStatus;
  source_module: string;
  ip_address?: string | null;
  metadata_json?: Record<string, unknown> | null;
  details?: string | null;
}

export async function getAuditLogs(
  filters?: AuditLogFilters,
): Promise<ApiResponse<AuditLog[]>> {
  const response = await apiClient.get<ApiResponse<AuditLog[]>>("/audit-logs", {
    params: filters,
  });

  return response.data;
}

export async function getAuditLog(
  auditLogId: number,
): Promise<ApiResponse<AuditLog>> {
  const response = await apiClient.get<ApiResponse<AuditLog>>(
    `/audit-logs/${auditLogId}`,
  );

  return response.data;
}

export async function createAuditLog(
  payload: AuditLogCreate,
): Promise<ApiResponse<AuditLog>> {
  const response = await apiClient.post<ApiResponse<AuditLog>>(
    "/audit-logs",
    payload,
  );

  return response.data;
}
