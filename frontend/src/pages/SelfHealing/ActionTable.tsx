import {
  FiAlertTriangle,
  FiChevronRight,
  FiClock,
  FiPlay,
} from "react-icons/fi";

import type { RecoveryWorkflow } from "../../api/recovery";

import Badge from "../../components/ui/Badge";
import Card from "../../components/ui/Card";

interface ActionTableProps {
  workflows: RecoveryWorkflow[];
  onWorkflowSelect: (workflowId: number) => void;
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

function ActionTable({ workflows, onWorkflowSelect }: ActionTableProps) {
  return (
    <Card>
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-sm font-semibold text-zinc-200">
            Recovery Workflows
          </h2>

          <p className="mt-1 text-xs text-zinc-500">
            Automated infrastructure recovery actions
          </p>
        </div>

        <FiPlay className="h-5 w-5 text-zinc-600" />
      </div>

      {workflows.length === 0 ? (
        <div className="flex min-h-40 items-center justify-center">
          <div className="text-center">
            <FiAlertTriangle className="mx-auto h-6 w-6 text-zinc-700" />

            <p className="mt-3 text-sm text-zinc-500">
              No recovery workflows found.
            </p>
          </div>
        </div>
      ) : (
        <div className="mt-5 overflow-x-auto">
          <table className="w-full min-w-[850px]">
            <thead>
              <tr className="border-b border-zinc-800/80">
                <th className="px-3 py-3 text-left text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                  Workflow
                </th>

                <th className="px-3 py-3 text-left text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                  Action
                </th>

                <th className="px-3 py-3 text-left text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                  Asset
                </th>

                <th className="px-3 py-3 text-left text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                  Status
                </th>

                <th className="px-3 py-3 text-left text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                  Executed By
                </th>

                <th className="px-3 py-3 text-left text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                  Created
                </th>

                <th className="px-3 py-3" />
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
                      <p className="text-xs font-medium text-zinc-200 transition-colors hover:text-blue-400">
                        {workflow.workflow_name}
                      </p>

                      <p className="mt-1 text-[11px] text-zinc-600">
                        Workflow #{workflow.id}
                      </p>
                    </button>
                  </td>

                  <td className="px-3 py-4">
                    <span className="text-xs text-zinc-400">
                      {formatActionType(workflow.action_type)}
                    </span>
                  </td>

                  <td className="px-3 py-4">
                    <span className="text-xs text-zinc-400">
                      #{workflow.infrastructure_asset_id}
                    </span>
                  </td>

                  <td className="px-3 py-4">
                    <Badge
                      variant={getStatusVariant(workflow.execution_status)}
                    >
                      {workflow.execution_status}
                    </Badge>
                  </td>

                  <td className="px-3 py-4 text-xs text-zinc-500">
                    {workflow.executed_by}
                  </td>

                  <td className="px-3 py-4">
                    <div className="flex items-center gap-1.5 text-[11px] text-zinc-600">
                      <FiClock className="h-3 w-3" />

                      {new Date(workflow.created_at).toLocaleString()}
                    </div>
                  </td>

                  <td className="px-3 py-4 text-right">
                    <button
                      type="button"
                      onClick={() => onWorkflowSelect(workflow.id)}
                      className="rounded-md p-1.5 text-zinc-600 transition-colors hover:bg-zinc-800 hover:text-zinc-200"
                      aria-label={`View workflow ${workflow.id}`}
                    >
                      <FiChevronRight className="h-4 w-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Card>
  );
}

export default ActionTable;
