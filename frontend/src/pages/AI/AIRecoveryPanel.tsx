import { useState } from "react";

import {
  FiAlertTriangle,
  FiCheckCircle,
  FiChevronDown,
  FiClock,
  FiLoader,
  FiPlay,
  FiShield,
  FiXCircle,
} from "react-icons/fi";

import type {
  RecommendationResponse,
  RootCauseResponse,
} from "../../api/ai";

import type { RecoveryActionType } from "../../api/recovery";

import { useAutomationRules } from "../../hooks/useAutomation";
import {
  useCreateRecoveryWorkflow,
  useExecuteRecoveryWorkflow,
  useRecoveryWorkflow,
} from "../../hooks/useRecovery";

import Badge from "../../components/ui/Badge";


// ---------------------------------------------------------------------------
// Action type mapping helpers
// ---------------------------------------------------------------------------

const ACTION_TYPE_OPTIONS: { value: RecoveryActionType; label: string }[] = [
  { value: "RESTART_SERVICE", label: "Restart Service" },
  { value: "RESTART_CONTAINER", label: "Restart Container" },
  { value: "RESTART_VM", label: "Restart VM" },
  { value: "REBOOT_SERVER", label: "Reboot Server" },
  { value: "CLEAR_CACHE", label: "Clear Cache" },
  { value: "RESTART_MONITORING_AGENT", label: "Restart Monitoring Agent" },
  { value: "SEND_NOTIFICATION", label: "Send Notification" },
];

/**
 * Best-effort mapping from an AI recommended_action string to a
 * RecoveryActionType enum value. Falls back to RESTART_SERVICE.
 */
function inferActionType(recommendedAction: string): RecoveryActionType {
  const lower = recommendedAction.toLowerCase();

  if (lower.includes("container")) return "RESTART_CONTAINER";
  if (lower.includes("vm") || lower.includes("virtual machine"))
    return "RESTART_VM";
  if (lower.includes("reboot") || lower.includes("server"))
    return "REBOOT_SERVER";
  if (lower.includes("cache")) return "CLEAR_CACHE";
  if (lower.includes("agent")) return "RESTART_MONITORING_AGENT";
  if (lower.includes("notification") || lower.includes("alert"))
    return "SEND_NOTIFICATION";

  // Default: treat any "restart *" as RESTART_SERVICE
  return "RESTART_SERVICE";
}

function formatActionType(actionType: RecoveryActionType): string {
  return actionType
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function getStatusVariant(status: string) {
  switch (status) {
    case "Completed":
      return "success" as const;
    case "Running":
      return "info" as const;
    case "Failed":
      return "danger" as const;
    case "Pending":
      return "warning" as const;
    default:
      return "default" as const;
  }
}

// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

interface AIRecoveryPanelProps {
  incidentId: number;
  infrastructureAssetId: number;
  recommendation: RecommendationResponse;
  rootCause: RootCauseResponse | null;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

function AIRecoveryPanel({
  incidentId,
  infrastructureAssetId,
  recommendation,
  rootCause,
}: AIRecoveryPanelProps) {
  // Pre-fill form from AI analysis
  const [workflowName, setWorkflowName] = useState(
    `AI Recovery — ${recommendation.recommended_action}`,
  );
  const [actionType, setActionType] = useState<RecoveryActionType>(
    inferActionType(recommendation.recommended_action),
  );
  const [selectedRuleId, setSelectedRuleId] = useState<string>("");
  const [executedBy, setExecutedBy] = useState("ai-gateway");

  // Workflow created from this session (tracks the created workflow ID)
  const [createdWorkflowId, setCreatedWorkflowId] = useState<number | null>(
    null,
  );

  const [createError, setCreateError] = useState<string | null>(null);
  const [executeError, setExecuteError] = useState<string | null>(null);

  // Hooks
  const { data: rulesResponse, isLoading: isLoadingRules } =
    useAutomationRules();
  const automationRules = rulesResponse?.data ?? [];

  const createMutation = useCreateRecoveryWorkflow();
  const executeMutation = useExecuteRecoveryWorkflow();

  // Poll the workflow once created
  const { data: workflowResponse } = useRecoveryWorkflow(
    createdWorkflowId ?? 0,
  );
  const workflow = workflowResponse?.data;

  // ---------------------------------------------------------------------------
  // Derived state
  // ---------------------------------------------------------------------------

  const canCreate =
    selectedRuleId !== "" &&
    workflowName.trim() !== "" &&
    executedBy.trim() !== "" &&
    createdWorkflowId === null;

  const canExecute =
    workflow?.execution_status === "Pending" ||
    workflow?.execution_status === "Failed";

  // ---------------------------------------------------------------------------
  // Handlers
  // ---------------------------------------------------------------------------

  const handleCreate = async () => {
    if (!canCreate) return;

    setCreateError(null);

    try {
      const result = await createMutation.mutateAsync({
        workflow_name: workflowName.trim(),
        automation_rule_id: Number(selectedRuleId),
        incident_id: incidentId,
        infrastructure_asset_id: infrastructureAssetId,
        action_type: actionType,
        executed_by: executedBy.trim(),
      });

      setCreatedWorkflowId(result.data.id);
    } catch (err: unknown) {
      const axiosErr = err as {
        response?: { data?: { error?: { message?: string }; message?: string } };
      };
      const message =
        axiosErr?.response?.data?.error?.message ??
        axiosErr?.response?.data?.message ??
        "Unable to create recovery workflow.";

      setCreateError(message);
    }
  };

  const handleExecute = async () => {
    if (!workflow) return;

    setExecuteError(null);

    try {
      await executeMutation.mutateAsync(workflow.id);
    } catch (err) {
      console.error(err);
      setExecuteError("Unable to execute the recovery workflow.");
    }
  };

  // ---------------------------------------------------------------------------
  // Render
  // ---------------------------------------------------------------------------

  return (
    <div className="space-y-4">
      {/* ------------------------------------------------------------------ */}
      {/* Header */}
      {/* ------------------------------------------------------------------ */}
      <div className="flex items-center gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-500/10">
          <FiShield className="h-4 w-4 text-emerald-400" />
        </div>

        <div>
          <h2 className="text-sm font-semibold text-zinc-200">Recovery Plan</h2>

          <p className="mt-0.5 text-xs text-zinc-500">
            Convert the AI recommendation into a recovery workflow.
          </p>
        </div>

        <div className="ml-auto rounded-lg border border-amber-500/20 bg-amber-500/5 px-3 py-1.5">
          <p className="text-[11px] font-medium text-amber-400">
            Simulation Mode
          </p>
        </div>
      </div>

      {/* ------------------------------------------------------------------ */}
      {/* AI Context Summary */}
      {/* ------------------------------------------------------------------ */}
      <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
        <p className="text-[11px] font-medium uppercase tracking-wider text-zinc-600">
          AI Analysis Summary
        </p>

        <div className="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2">
          <div>
            <p className="text-[11px] text-zinc-600">Recommended Action</p>

            <p className="mt-1 text-sm font-medium text-emerald-400">
              {recommendation.recommended_action}
            </p>
          </div>

          <div>
            <p className="text-[11px] text-zinc-600">Priority</p>

            <p className="mt-1 text-sm font-medium text-zinc-200">
              {recommendation.priority}
            </p>
          </div>

          {rootCause && (
            <div className="sm:col-span-2">
              <p className="text-[11px] text-zinc-600">Probable Root Cause</p>

              <p className="mt-1 text-xs leading-relaxed text-zinc-400">
                {rootCause.probable_cause}
              </p>
            </div>
          )}

          <div className="sm:col-span-2">
            <p className="text-[11px] text-zinc-600">Explanation</p>

            <p className="mt-1 text-xs leading-relaxed text-zinc-500">
              {recommendation.explanation}
            </p>
          </div>
        </div>
      </div>

      {/* ------------------------------------------------------------------ */}
      {/* Workflow Configuration Form — only shown before workflow is created */}
      {/* ------------------------------------------------------------------ */}
      {createdWorkflowId === null && (
        <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
          <p className="text-[11px] font-medium uppercase tracking-wider text-zinc-600">
            Workflow Configuration
          </p>

          <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
            {/* Workflow name */}
            <div className="sm:col-span-2">
              <label className="text-xs font-medium text-zinc-400">
                Workflow Name
              </label>

              <input
                id="ai-recovery-workflow-name"
                value={workflowName}
                onChange={(e) => setWorkflowName(e.target.value)}
                className="mt-2 h-10 w-full rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 text-sm text-zinc-200 outline-none placeholder:text-zinc-700 focus:border-blue-500/40"
              />
            </div>

            {/* Action type */}
            <div>
              <label className="text-xs font-medium text-zinc-400">
                Action Type
              </label>

              <div className="relative mt-2">
                <select
                  id="ai-recovery-action-type"
                  value={actionType}
                  onChange={(e) =>
                    setActionType(e.target.value as RecoveryActionType)
                  }
                  className="h-10 w-full appearance-none rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 pr-10 text-sm text-zinc-300 outline-none focus:border-blue-500/40"
                >
                  {ACTION_TYPE_OPTIONS.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>

                <FiChevronDown className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-600" />
              </div>
            </div>

            {/* Automation rule */}
            <div>
              <label className="text-xs font-medium text-zinc-400">
                Automation Rule
              </label>

              <div className="relative mt-2">
                <select
                  id="ai-recovery-automation-rule"
                  value={selectedRuleId}
                  onChange={(e) => setSelectedRuleId(e.target.value)}
                  disabled={isLoadingRules}
                  className="h-10 w-full appearance-none rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 pr-10 text-sm text-zinc-300 outline-none focus:border-blue-500/40 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <option value="">
                    {isLoadingRules
                      ? "Loading rules..."
                      : automationRules.length === 0
                        ? "No rules available"
                        : "Select a rule"}
                  </option>

                  {automationRules.map((rule) => (
                    <option key={rule.id} value={rule.id}>
                      #{rule.id} — {rule.rule_name}
                    </option>
                  ))}
                </select>

                <FiChevronDown className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-600" />
              </div>
            </div>

            {/* Executed by */}
            <div>
              <label className="text-xs font-medium text-zinc-400">
                Executed By
              </label>

              <input
                id="ai-recovery-executed-by"
                value={executedBy}
                onChange={(e) => setExecutedBy(e.target.value)}
                className="mt-2 h-10 w-full rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 text-sm text-zinc-200 outline-none placeholder:text-zinc-700 focus:border-blue-500/40"
              />
            </div>
          </div>

          {/* Error */}
          {createError && (
            <div className="mt-4 flex items-start gap-2 rounded-lg border border-red-500/20 bg-red-500/5 p-3">
              <FiXCircle className="mt-0.5 h-4 w-4 shrink-0 text-red-400" />

              <p className="text-xs text-red-400">{createError}</p>
            </div>
          )}

          {/* Create button */}
          <div className="mt-5 flex items-center justify-between border-t border-zinc-800/70 pt-4">
            <p className="text-[11px] text-zinc-600">
              Execution mode: Simulation &nbsp;·&nbsp; Incident #{incidentId}
            </p>

            <button
              type="button"
              id="ai-recovery-create-btn"
              onClick={handleCreate}
              disabled={!canCreate || createMutation.isPending}
              className="flex h-10 items-center gap-2 rounded-lg bg-emerald-500 px-4 text-xs font-semibold text-white transition-colors hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {createMutation.isPending && (
                <FiLoader className="h-3.5 w-3.5 animate-spin" />
              )}

              {createMutation.isPending ? "Creating..." : "Create Recovery Plan"}
            </button>
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------------ */}
      {/* Workflow Execution Panel — shown after workflow created */}
      {/* ------------------------------------------------------------------ */}
      {createdWorkflowId !== null && (
        <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
          <div className="flex items-center justify-between">
            <p className="text-[11px] font-medium uppercase tracking-wider text-zinc-600">
              Recovery Workflow Created
            </p>

            {workflow && (
              <Badge variant={getStatusVariant(workflow.execution_status)}>
                {workflow.execution_status}
              </Badge>
            )}
          </div>

          {/* Workflow details */}
          {workflow && (
            <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
              <div>
                <p className="text-[11px] text-zinc-600">Workflow</p>

                <p className="mt-1 text-xs font-medium text-zinc-200">
                  {workflow.workflow_name}
                </p>
              </div>

              <div>
                <p className="text-[11px] text-zinc-600">Action</p>

                <p className="mt-1 text-xs font-medium text-zinc-200">
                  {formatActionType(workflow.action_type)}
                </p>
              </div>

              <div>
                <p className="text-[11px] text-zinc-600">Execution Mode</p>

                <p className="mt-1 text-xs font-medium text-amber-400">
                  {workflow.execution_mode}
                </p>
              </div>

              <div>
                <p className="text-[11px] text-zinc-600">Workflow ID</p>

                <p className="mt-1 text-xs font-medium text-zinc-400">
                  #{workflow.id}
                </p>
              </div>

              {workflow.started_at && (
                <div>
                  <p className="text-[11px] text-zinc-600">Started</p>

                  <p className="mt-1 text-xs text-zinc-400 flex items-center gap-1">
                    <FiClock className="h-3 w-3" />
                    {new Date(workflow.started_at).toLocaleString()}
                  </p>
                </div>
              )}

              {workflow.completed_at && (
                <div>
                  <p className="text-[11px] text-zinc-600">Completed</p>

                  <p className="mt-1 text-xs text-zinc-400 flex items-center gap-1">
                    <FiCheckCircle className="h-3 w-3" />
                    {new Date(workflow.completed_at).toLocaleString()}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Simulation disclaimer */}
          <div className="mt-4 flex items-start gap-2 rounded-lg border border-amber-500/20 bg-amber-500/5 p-3">
            <FiAlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-amber-400" />

            <p className="text-[11px] leading-relaxed text-zinc-500">
              Executing this workflow runs in{" "}
              <span className="font-medium text-amber-400">Simulation Mode</span>
              . No real infrastructure changes will be made.
            </p>
          </div>

          {/* Execution log */}
          {workflow?.execution_log && (
            <div className="mt-4">
              <p className="text-[11px] text-zinc-600">Execution Log</p>

              <pre className="mt-2 max-h-36 overflow-auto rounded-md bg-zinc-950 p-3 text-[11px] leading-relaxed text-zinc-500 whitespace-pre-wrap">
                {workflow.execution_log}
              </pre>
            </div>
          )}

          {/* Execute error */}
          {executeError && (
            <div className="mt-4 flex items-start gap-2 rounded-lg border border-red-500/20 bg-red-500/5 p-3">
              <FiXCircle className="mt-0.5 h-4 w-4 shrink-0 text-red-400" />

              <p className="text-xs text-red-400">{executeError}</p>
            </div>
          )}

          {/* Action buttons */}
          {canExecute && (
            <div className="mt-5 flex justify-end border-t border-zinc-800/70 pt-4">
              <button
                type="button"
                id="ai-recovery-execute-btn"
                onClick={handleExecute}
                disabled={executeMutation.isPending}
                className="flex h-10 items-center gap-2 rounded-lg bg-blue-500 px-4 text-xs font-semibold text-white transition-colors hover:bg-blue-400 disabled:cursor-not-allowed disabled:opacity-40"
              >
                {executeMutation.isPending ? (
                  <FiLoader className="h-3.5 w-3.5 animate-spin" />
                ) : (
                  <FiPlay className="h-3.5 w-3.5" />
                )}

                {executeMutation.isPending ? "Executing..." : "Execute Simulation"}
              </button>
            </div>
          )}

          {/* Completed state */}
          {workflow?.execution_status === "Completed" && (
            <div className="mt-4 flex items-center gap-2 rounded-lg border border-emerald-500/20 bg-emerald-500/5 p-3">
              <FiCheckCircle className="h-4 w-4 shrink-0 text-emerald-400" />

              <p className="text-xs font-medium text-emerald-400">
                Simulation completed successfully. Review the execution log
                above for details.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default AIRecoveryPanel;
