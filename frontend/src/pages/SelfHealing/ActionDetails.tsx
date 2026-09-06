import { useState } from "react";

import {
  FiAlertTriangle,
  FiCheckCircle,
  FiClock,
  FiPlay,
  FiX,
  FiXCircle,
} from "react-icons/fi";

import type { RecoveryWorkflow } from "../../api/recovery";

import {
  useCancelRecoveryWorkflow,
  useExecuteRecoveryWorkflow,
  useRecoveryWorkflow,
} from "../../hooks/useRecovery";

import Badge from "../../components/ui/Badge";
import Card from "../../components/ui/Card";

interface ActionDetailsProps {
  workflowId: number | null;
  onClose: () => void;
}

function getStatusVariant(status: RecoveryWorkflow["execution_status"]) {
  switch (status) {
    case "Completed":
      return "success" as const;

    case "Running":
      return "info" as const;

    case "Failed":
      return "danger" as const;

    case "Pending":
      return "warning" as const;

    case "Cancelled":
    default:
      return "default" as const;
  }
}

function formatActionType(actionType: RecoveryWorkflow["action_type"]) {
  return actionType
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function ActionDetails({ workflowId, onClose }: ActionDetailsProps) {
  const [actionError, setActionError] = useState<string | null>(null);

  const {
    data: workflowResponse,
    isLoading,
    isError,
  } = useRecoveryWorkflow(workflowId ?? 0);

  const executeMutation = useExecuteRecoveryWorkflow();

  const cancelMutation = useCancelRecoveryWorkflow();

  const workflow = workflowResponse?.data;

  if (workflowId === null) {
    return null;
  }

  const canExecute = workflow?.execution_status === "Pending";

  const canCancel =
    workflow?.execution_status === "Pending" ||
    workflow?.execution_status === "Running";

  const handleExecute = async () => {
    if (!workflow) {
      return;
    }

    setActionError(null);

    try {
      await executeMutation.mutateAsync(workflow.id);
    } catch (error) {
      console.error(error);

      setActionError("Unable to execute the recovery workflow.");
    }
  };

  const handleCancel = async () => {
    if (!workflow) {
      return;
    }

    setActionError(null);

    try {
      await cancelMutation.mutateAsync(workflow.id);
    } catch (error) {
      console.error(error);

      setActionError("Unable to cancel the recovery workflow.");
    }
  };

  const isActionLoading = executeMutation.isPending || cancelMutation.isPending;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm">
      <div className="w-full max-w-2xl">
        <Card>
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-xs font-medium uppercase tracking-wider text-blue-400">
                Recovery Workflow
              </p>

              <h2 className="mt-1 text-lg font-semibold text-zinc-100">
                {workflow?.workflow_name ?? "Workflow Details"}
              </h2>
            </div>

            <button
              type="button"
              onClick={onClose}
              className="rounded-md p-1.5 text-zinc-500 transition-colors hover:bg-zinc-800 hover:text-zinc-200"
              aria-label="Close workflow details"
            >
              <FiX className="h-4 w-4" />
            </button>
          </div>

          {isLoading && (
            <div className="flex min-h-40 items-center justify-center">
              <p className="text-sm text-zinc-500">
                Loading workflow details...
              </p>
            </div>
          )}

          {isError && (
            <div className="flex min-h-40 items-center justify-center">
              <p className="text-sm text-red-400">
                Unable to load workflow details.
              </p>
            </div>
          )}

          {!isLoading && !isError && workflow && (
            <div className="mt-6 space-y-5">
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                  <p className="text-xs text-zinc-500">Action</p>

                  <p className="mt-2 text-sm font-medium text-zinc-200">
                    {formatActionType(workflow.action_type)}
                  </p>
                </div>

                <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                  <p className="text-xs text-zinc-500">Status</p>

                  <div className="mt-2">
                    <Badge
                      variant={getStatusVariant(workflow.execution_status)}
                    >
                      {workflow.execution_status}
                    </Badge>
                  </div>
                </div>

                <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                  <p className="text-xs text-zinc-500">Infrastructure Asset</p>

                  <p className="mt-2 text-sm font-medium text-zinc-200">
                    #{workflow.infrastructure_asset_id}
                  </p>
                </div>

                <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                  <p className="text-xs text-zinc-500">Incident</p>

                  <p className="mt-2 text-sm font-medium text-zinc-200">
                    {workflow.incident_id === null
                      ? "Not associated"
                      : `#${workflow.incident_id}`}
                  </p>
                </div>

                <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                  <p className="text-xs text-zinc-500">Executed By</p>

                  <p className="mt-2 text-sm font-medium text-zinc-200">
                    {workflow.executed_by}
                  </p>
                </div>

                <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                  <p className="text-xs text-zinc-500">Execution Mode</p>

                  <p className="mt-2 text-sm font-medium text-amber-400">
                    {workflow.execution_mode}
                  </p>
                </div>
              </div>

              <div className="rounded-lg border border-amber-500/20 bg-amber-500/5 p-4">
                <div className="flex items-start gap-3">
                  <FiAlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-amber-400" />

                  <div>
                    <p className="text-xs font-medium text-amber-400">
                      Simulation Mode
                    </p>

                    <p className="mt-1 text-[11px] leading-relaxed text-zinc-500">
                      Executing this workflow currently runs in simulation mode.
                      It does not perform a real infrastructure recovery action.
                    </p>
                  </div>
                </div>
              </div>

              {workflow.execution_log && (
                <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                  <p className="text-xs text-zinc-500">Execution Log</p>

                  <pre className="mt-3 max-h-40 overflow-auto whitespace-pre-wrap rounded-md bg-zinc-950 p-3 text-[11px] leading-relaxed text-zinc-500">
                    {workflow.execution_log}
                  </pre>
                </div>
              )}

              <div className="flex flex-wrap items-center gap-4 border-t border-zinc-800/70 pt-4 text-[11px] text-zinc-600">
                {workflow.started_at && (
                  <span className="flex items-center gap-1.5">
                    <FiClock className="h-3 w-3" />
                    Started {new Date(workflow.started_at).toLocaleString()}
                  </span>
                )}

                {workflow.completed_at && (
                  <span className="flex items-center gap-1.5">
                    <FiCheckCircle className="h-3 w-3" />
                    Completed {new Date(workflow.completed_at).toLocaleString()}
                  </span>
                )}
              </div>

              {actionError && (
                <div className="flex items-start gap-2 rounded-lg border border-red-500/20 bg-red-500/5 p-3">
                  <FiXCircle className="mt-0.5 h-4 w-4 shrink-0 text-red-400" />

                  <p className="text-xs text-red-400">{actionError}</p>
                </div>
              )}

              {(canExecute || canCancel) && (
                <div className="flex flex-col-reverse gap-2 border-t border-zinc-800/70 pt-4 sm:flex-row sm:justify-end">
                  {canCancel && (
                    <button
                      type="button"
                      onClick={handleCancel}
                      disabled={isActionLoading}
                      className="flex h-10 items-center justify-center gap-2 rounded-lg border border-zinc-800 px-4 text-xs font-medium text-zinc-400 transition-colors hover:bg-zinc-800/50 hover:text-zinc-200 disabled:cursor-not-allowed disabled:opacity-40"
                    >
                      <FiX className="h-3.5 w-3.5" />
                      {cancelMutation.isPending ? "Cancelling..." : "Cancel"}
                    </button>
                  )}

                  {canExecute && (
                    <button
                      type="button"
                      onClick={handleExecute}
                      disabled={isActionLoading}
                      className="flex h-10 items-center justify-center gap-2 rounded-lg bg-blue-500 px-4 text-xs font-semibold text-white transition-colors hover:bg-blue-400 disabled:cursor-not-allowed disabled:opacity-40"
                    >
                      <FiPlay className="h-3.5 w-3.5" />
                      {executeMutation.isPending
                        ? "Executing..."
                        : "Execute Simulation"}
                    </button>
                  )}
                </div>
              )}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}

export default ActionDetails;
