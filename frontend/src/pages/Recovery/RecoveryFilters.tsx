import type { ExecutionStatus, RecoveryActionType } from "../../api/recovery";

interface RecoveryFiltersProps {
  executionStatus: ExecutionStatus | "all";
  actionType: RecoveryActionType | "all";
  onExecutionStatusChange: (status: ExecutionStatus | "all") => void;
  onActionTypeChange: (actionType: RecoveryActionType | "all") => void;
  onClear: () => void;
}

function RecoveryFilters({
  executionStatus,
  actionType,
  onExecutionStatusChange,
  onActionTypeChange,
  onClear,
}: RecoveryFiltersProps) {
  const hasFilters = executionStatus !== "all" || actionType !== "all";

  return (
    <div className="rounded-xl border border-zinc-800/80 bg-zinc-900/40 p-4">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-center">
        <select
          value={executionStatus}
          onChange={(event) =>
            onExecutionStatusChange(
              event.target.value as ExecutionStatus | "all",
            )
          }
          className="h-10 rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 text-sm text-zinc-300 outline-none focus:border-blue-500/40"
        >
          <option value="all">All execution statuses</option>
          <option value="Pending">Pending</option>
          <option value="Running">Running</option>
          <option value="Completed">Completed</option>
          <option value="Failed">Failed</option>
          <option value="Cancelled">Cancelled</option>
        </select>

        <select
          value={actionType}
          onChange={(event) =>
            onActionTypeChange(event.target.value as RecoveryActionType | "all")
          }
          className="h-10 rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 text-sm text-zinc-300 outline-none focus:border-blue-500/40"
        >
          <option value="all">All action types</option>

          <option value="RESTART_SERVICE">Restart Service</option>

          <option value="RESTART_CONTAINER">Restart Container</option>

          <option value="RESTART_VM">Restart VM</option>

          <option value="REBOOT_SERVER">Reboot Server</option>

          <option value="CLEAR_CACHE">Clear Cache</option>

          <option value="RESTART_MONITORING_AGENT">
            Restart Monitoring Agent
          </option>

          <option value="SEND_NOTIFICATION">Send Notification</option>
        </select>

        {hasFilters && (
          <button
            type="button"
            onClick={onClear}
            className="h-10 rounded-lg border border-zinc-800 px-4 text-xs font-medium text-zinc-400 transition-colors hover:bg-zinc-800/50 hover:text-zinc-200"
          >
            Clear filters
          </button>
        )}
      </div>
    </div>
  );
}

export default RecoveryFilters;
