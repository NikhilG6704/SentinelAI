import apiClient from "./client";
import type { ApiResponse } from "../types/api";

export type MetricType =
  | "CPU_USAGE"
  | "MEMORY_USAGE"
  | "DISK_USAGE"
  | "NETWORK_USAGE"
  | "LOG_ERROR_RATE"
  | "INCIDENT_COUNT";

export type RuleOperator = ">" | ">=" | "<" | "<=" | "==" | "!=";

export type RuleSeverity = "Low" | "Medium" | "High" | "Critical";

export type ActionType =
  | "CREATE_ALERT"
  | "CREATE_INCIDENT"
  | "RESTART_SERVICE"
  | "RESTART_CONTAINER"
  | "REBOOT_SERVER"
  | "SCALE_SERVICE"
  | "SEND_NOTIFICATION";

export type TargetScope = "Global" | "Asset" | "Agent";

export interface AutomationRule {
  id: number;
  rule_name: string;
  description: string;
  metric_type: MetricType;
  operator: RuleOperator;
  threshold: number;
  severity: RuleSeverity;
  action_type: ActionType;
  target_scope: TargetScope;
  is_enabled: boolean;
  priority: number;
  cooldown_minutes: number;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface AutomationRuleCreate {
  rule_name: string;
  description: string;
  metric_type: MetricType;
  operator: RuleOperator;
  threshold: number;
  severity: RuleSeverity;
  action_type: ActionType;
  target_scope?: TargetScope;
  priority?: number;
  cooldown_minutes?: number;
  created_by: string;
}

export interface AutomationRuleUpdate {
  description?: string | null;
  metric_type?: MetricType | null;
  operator?: RuleOperator | null;
  threshold?: number | null;
  severity?: RuleSeverity | null;
  action_type?: ActionType | null;
  target_scope?: TargetScope | null;
  priority?: number | null;
  cooldown_minutes?: number | null;
}

export async function getAutomationRules(): Promise<
  ApiResponse<AutomationRule[]>
> {
  const response =
    await apiClient.get<ApiResponse<AutomationRule[]>>("/automation-rules");

  return response.data;
}

export async function getAutomationRule(
  ruleId: number,
): Promise<ApiResponse<AutomationRule>> {
  const response = await apiClient.get<ApiResponse<AutomationRule>>(
    `/automation-rules/${ruleId}`,
  );

  return response.data;
}

export async function createAutomationRule(
  payload: AutomationRuleCreate,
): Promise<ApiResponse<AutomationRule>> {
  const response = await apiClient.post<ApiResponse<AutomationRule>>(
    "/automation-rules",
    payload,
  );

  return response.data;
}

export async function updateAutomationRule(
  ruleId: number,
  payload: AutomationRuleUpdate,
): Promise<ApiResponse<AutomationRule>> {
  const response = await apiClient.put<ApiResponse<AutomationRule>>(
    `/automation-rules/${ruleId}`,
    payload,
  );

  return response.data;
}

export async function deleteAutomationRule(
  ruleId: number,
): Promise<ApiResponse<AutomationRule>> {
  const response = await apiClient.delete<ApiResponse<AutomationRule>>(
    `/automation-rules/${ruleId}`,
  );

  return response.data;
}

export async function enableAutomationRule(
  ruleId: number,
): Promise<ApiResponse<AutomationRule>> {
  const response = await apiClient.patch<ApiResponse<AutomationRule>>(
    `/automation-rules/${ruleId}/enable`,
  );

  return response.data;
}

export async function disableAutomationRule(
  ruleId: number,
): Promise<ApiResponse<AutomationRule>> {
  const response = await apiClient.patch<ApiResponse<AutomationRule>>(
    `/automation-rules/${ruleId}/disable`,
  );

  return response.data;
}
