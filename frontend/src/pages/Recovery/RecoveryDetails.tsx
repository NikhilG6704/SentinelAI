import { useState } from "react";

import type { RecoveryWorkflow } from "../../api/recovery";

import {
  useCancelRecoveryWorkflow,
  useDeleteRecoveryWorkflow,
  useExecuteRecoveryWorkflow,
  useRecoveryWorkflow,
} from "../../hooks/useRecovery";

import Badge from "../../components/ui/Badge";
import Card from "../../components/ui/Card";

interface RecoveryDetailsProps {
  workflow: RecoveryWorkflow | null;
  onClose: () => void;
}

function getStatusVariant(
  status: RecoveryWorkflow["execution_status"],
): "danger" | "warning" | "info" {
  switch (status) {
    case "Failed":
      return "danger";

    case "Pending":
    case "Running":
      return "warning";

    case "Completed":
    case "Cancelled":
    default:
      return "info";
  }
}

function formatActionType(actionType: RecoveryWorkflow["action_type"]) {
  return actionType
    .split("_")
    .map((word) => word.charAt(0) + word.slice(1).toLowerCase())
    .join(" ");
}

function RecoveryDetails({ workflow, onClose }: RecoveryDetailsProps) {
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const executeMutation = useExecuteRecoveryWorkflow();

  const cancelMutation = useCancelRecoveryWorkflow();

  const deleteMutation = useDeleteRecoveryWorkflow();

  const { data: workflowResponse } = useRecoveryWorkflow(workflow?.id ?? 0);

  if (!workflow) {
    return null;
  }

  const currentWorkflow = workflowResponse?.data ?? workflow;

  const canExecute =
    currentWorkflow.execution_status === "Pending" ||
    currentWorkflow.execution_status === "Failed";

  const canCancel =
    currentWorkflow.execution_status === "Pending" ||
    currentWorkflow.execution_status === "Running";

  const canDelete =
    currentWorkflow.execution_status === "Completed" ||
    currentWorkflow.execution_status === "Failed" ||
    currentWorkflow.execution_status === "Cancelled";

  const handleExecute = () => {
    executeMutation.mutate(currentWorkflow.id);
  };

  const handleCancel = () => {
    cancelMutation.mutate(currentWorkflow.id);
  };

  const handleDelete = () => {
    deleteMutation.mutate(currentWorkflow.id, {
      onSuccess: () => {
        setShowDeleteConfirm(false);
        onClose();
      },
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm">
      <div className="w-full max-w-2xl">
        <Card>
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0">
              <p className="text-xs font-medium uppercase tracking-wider text-blue-400">
                Recovery Workflow
              </p>

              <h2 className="mt-1 text-lg font-semibold text-zinc-100">
                {currentWorkflow.workflow_name}
              </h2>
            </div>

            <button
              type="button"
              onClick={onClose}
              className="rounded-md px-2 py-1 text-sm text-zinc-500 transition-colors hover:bg-zinc-800 hover:text-zinc-200"
            >
              Close
            </button>
          </div>

          <div className="mt-5 flex flex-wrap gap-2">
            <Badge variant={getStatusVariant(currentWorkflow.execution_status)}>
              {currentWorkflow.execution_status}
            </Badge>

            <span className="rounded-md border border-zinc-800 bg-zinc-950/60 px-2 py-1 text-[10px] font-medium text-zinc-500">
              {currentWorkflow.execution_mode}
            </span>
          </div>

          <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
              <p className="text-xs text-zinc-500">Action</p>

              <p className="mt-2 text-sm font-medium text-zinc-200">
                {formatActionType(currentWorkflow.action_type)}
              </p>
            </div>

            <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
              <p className="text-xs text-zinc-500">Automation Rule</p>

              <p className="mt-2 text-sm font-medium text-zinc-200">
                #{currentWorkflow.automation_rule_id}
              </p>
            </div>

            <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
              <p className="text-xs text-zinc-500">Infrastructure Asset</p>

              <p className="mt-2 text-sm font-medium text-zinc-200">
                #{currentWorkflow.infrastructure_asset_id}
              </p>
            </div>

            <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
              <p className="text-xs text-zinc-500">Incident</p>

              <p className="mt-2 text-sm font-medium text-zinc-200">
                {currentWorkflow.incident_id
                  ? `#${currentWorkflow.incident_id}`
                  : "None"}
              </p>
            </div>

            <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
              <p className="text-xs text-zinc-500">Executed By</p>

              <p className="mt-2 text-sm font-medium text-zinc-200">
                {currentWorkflow.executed_by}
              </p>
            </div>

            <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
              <p className="text-xs text-zinc-500">Created</p>

              <p className="mt-2 text-sm font-medium text-zinc-200">
                {new Date(currentWorkflow.created_at).toLocaleString()}
              </p>
            </div>
          </div>

          {currentWorkflow.execution_log && (
            <div className="mt-5 rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
              <p className="text-xs text-zinc-500">Execution Log</p>

              <pre className="mt-2 max-h-48 overflow-auto whitespace-pre-wrap text-xs leading-relaxed text-zinc-400">
                {currentWorkflow.execution_log}
              </pre>
            </div>
          )}

          <div className="mt-6 flex flex-wrap gap-3 border-t border-zinc-800/70 pt-5">
            {canExecute && (
              <button
                type="button"
                onClick={handleExecute}
                disabled={executeMutation.isPending}
                className="h-10 rounded-lg bg-blue-500 px-4 text-sm font-medium text-white transition-colors hover:bg-blue-400 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {executeMutation.isPending
                  ? "Executing..."
                  : "Execute Simulation"}
              </button>
            )}

            {canCancel && (
              <button
                type="button"
                onClick={handleCancel}
                disabled={cancelMutation.isPending}
                className="h-10 rounded-lg border border-amber-500/20 bg-amber-500/5 px-4 text-sm font-medium text-amber-400 transition-colors hover:bg-amber-500/10 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {cancelMutation.isPending ? "Cancelling..." : "Cancel Workflow"}
              </button>
            )}

            {canDelete && (
              <button
                type="button"
                onClick={() => setShowDeleteConfirm(true)}
                className="h-10 rounded-lg border border-red-500/20 bg-red-500/5 px-4 text-sm font-medium text-red-400 transition-colors hover:bg-red-500/10"
              >
                Delete Workflow
              </button>
            )}
          </div>

          {showDeleteConfirm && (
            <div className="mt-4 rounded-lg border border-red-500/20 bg-red-500/5 p-4">
              <p className="text-sm font-medium text-zinc-200">
                Delete this workflow?
              </p>

              <p className="mt-1 text-xs text-zinc-500">
                This action cannot be undone.
              </p>

              <div className="mt-4 flex gap-2">
                <button
                  type="button"
                  onClick={handleDelete}
                  disabled={deleteMutation.isPending}
                  className="h-9 rounded-lg bg-red-500 px-3 text-xs font-medium text-white hover:bg-red-400 disabled:opacity-50"
                >
                  {deleteMutation.isPending ? "Deleting..." : "Confirm Delete"}
                </button>

                <button
                  type="button"
                  onClick={() => setShowDeleteConfirm(false)}
                  className="h-9 rounded-lg border border-zinc-800 px-3 text-xs font-medium text-zinc-400 hover:bg-zinc-800/60 hover:text-zinc-200"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}

export default RecoveryDetails;
