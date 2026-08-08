import apiClient from "./client";
import type { ApiResponse } from "../types/api";

export type ReportType =
  | "Infrastructure"
  | "Incident"
  | "Alert"
  | "Metrics"
  | "AI";

export interface Report {
  id: number;
  report_type: ReportType;
  title: string;
  description: string | null;
  generated_at: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface ReportFilters {
  report_type?: ReportType;
  status?: string;
  skip?: number;
  limit?: number;
}

export async function getReports(
  filters?: ReportFilters,
): Promise<ApiResponse<Report[]>> {
  const response = await apiClient.get<ApiResponse<Report[]>>("/reports", {
    params: filters,
  });

  return response.data;
}

export async function getReport(
  reportId: number,
): Promise<ApiResponse<Report>> {
  const response = await apiClient.get<ApiResponse<Report>>(
    `/reports/${reportId}`,
  );

  return response.data;
}
