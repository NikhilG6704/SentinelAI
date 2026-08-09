import { FiClock, FiGitBranch, FiServer } from "react-icons/fi";

import type { RecoveryWorkflow } from "../../api/recovery";

import Badge from "../../components/ui/Badge";
import Card from "../../components/ui/Card";

interface RecoveryTableProps {
  workflows: RecoveryWorkflow[];
  onWorkflowSelect: (workflowId: number) => void;
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

function getTimeAgo(timestamp: string) {
  const diff = Date.now() - new Date(timestamp).getTime();

  const minutes = Math.max(0, Math.floor(diff / (1000 * 60)));

  if (minutes < 1) {
    return "Just now";
  }

  if (minutes < 60) {
    return `${minutes} min ago`;
  }

  const hours = Math.floor(minutes / 60);

  if (hours < 24) {
    return `${hours} hr ago`;
  }

  const days = Math.floor(hours / 24);

  return `${days}d ago`;
}

function RecoveryTable({ workflows, onWorkflowSelect }: RecoveryTableProps) {
  return (
    <Card>
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-sm font-semibold text-zinc-200">
            Recovery Workflows
          </h2>

          <p className="mt-1 text-xs text-zinc-500">
            Automated recovery workflows and simulation executions
          </p>
        </div>

        <FiGitBranch className="h-5 w-5 text-zinc-600" />
      </div>

      <div className="mt-5 overflow-x-auto">
        <table className="w-full min-w-[950px] text-left">
          <thead>
            <tr className="border-b border-zinc-800/80">
              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Workflow
              </th>

              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Asset
              </th>

              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Action
              </th>

              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Mode
              </th>

              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Status
              </th>

              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Created
              </th>
            </tr>
          </thead>

          <tbody>
            {workflows.map((workflow) => (
              <tr
                key={workflow.id}
                className="border-b border-zinc-800/50 last:border-b-0"
              >
                <td className="px-3 py-4">
                  <button
                    type="button"
                    onClick={() => onWorkflowSelect(workflow.id)}
                    className="text-left"
                  >
                    <div className="flex items-start gap-3">
                      <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-blue-500/10">
                        <FiGitBranch className="h-4 w-4 text-blue-400" />
                      </div>

                      <div className="min-w-0">
                        <p className="text-xs font-medium text-zinc-200 transition-colors hover:text-blue-400">
                          {workflow.workflow_name}
                        </p>

                        <p className="mt-1 text-[11px] text-zinc-600">
                          Rule #{workflow.automation_rule_id}
                        </p>
                      </div>
                    </div>
                  </button>
                </td>

                <td className="px-3 py-4">
                  <span className="flex items-center gap-1.5 text-xs text-zinc-400">
                    <FiServer className="h-3.5 w-3.5 text-zinc-600" />#
                    {workflow.infrastructure_asset_id}
                  </span>
                </td>

                <td className="px-3 py-4">
                  <span className="text-xs text-zinc-400">
                    {formatActionType(workflow.action_type)}
                  </span>
                </td>

                <td className="px-3 py-4">
                  <span className="rounded-md border border-zinc-800 bg-zinc-950/60 px-2 py-1 text-[10px] font-medium text-zinc-500">
                    {workflow.execution_mode}
                  </span>
                </td>

                <td className="px-3 py-4">
                  <Badge variant={getStatusVariant(workflow.execution_status)}>
                    {workflow.execution_status}
                  </Badge>
                </td>

                <td className="px-3 py-4">
                  <span className="flex items-center gap-1 text-[11px] text-zinc-600">
                    <FiClock className="h-3 w-3" />
                    {getTimeAgo(workflow.created_at)}
                  </span>
                </td>
              </tr>
            ))}

            {workflows.length === 0 && (
              <tr>
                <td
                  colSpan={6}
                  className="px-3 py-12 text-center text-sm text-zinc-500"
                >
                  No recovery workflows found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </Card>
  );
}

export default RecoveryTable;
