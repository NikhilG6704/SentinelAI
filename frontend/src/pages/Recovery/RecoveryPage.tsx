import { useState } from "react";

import type {
  ExecutionStatus,
  RecoveryActionType,
  RecoveryWorkflow,
} from "../../api/recovery";

import { useRecoveryWorkflows } from "../../hooks/useRecovery";

import RecoveryCreateForm from "./RecoveryCreateForm";
import RecoveryDetails from "./RecoveryDetails";
import RecoveryFilters from "./RecoveryFilters";
import RecoverySummary from "./RecoverySummary";
import RecoveryTable from "./RecoveryTable";

function RecoveryPage() {
  const [executionStatus, setExecutionStatus] = useState<
    ExecutionStatus | "all"
  >("all");

  const [actionType, setActionType] = useState<RecoveryActionType | "all">(
    "all",
  );

  const [selectedWorkflow, setSelectedWorkflow] =
    useState<RecoveryWorkflow | null>(null);

  const {
    data: recoveryResponse,
    isLoading,
    isError,
    refetch,
  } = useRecoveryWorkflows({
    execution_status: executionStatus === "all" ? undefined : executionStatus,

    action_type: actionType === "all" ? undefined : actionType,
  });

  const workflows = recoveryResponse?.data ?? [];

  const clearFilters = () => {
    setExecutionStatus("all");
    setActionType("all");
  };

  const handleWorkflowSelect = (workflowId: number) => {
    const workflow = workflows.find((item) => item.id === workflowId);

    if (workflow) {
      setSelectedWorkflow(workflow);
    }
  };

  const handleCreated = () => {
    refetch();
  };

  return (
    <div className="min-h-full">
      <div className="border-b border-zinc-800/80 px-6 py-5">
        <p className="text-xs font-medium uppercase tracking-wider text-blue-400">
          Automation
        </p>

        <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">
          Recovery
        </h1>

        <p className="mt-1 max-w-2xl text-sm text-zinc-500">
          Manage recovery workflows, simulate remediation actions, and track
          execution results.
        </p>
      </div>

      <div className="space-y-5 p-6">
        {isLoading && (
          <div className="flex min-h-40 items-center justify-center rounded-xl border border-zinc-800/80 bg-zinc-900/40">
            <p className="text-sm text-zinc-500">
              Loading recovery workflows...
            </p>
          </div>
        )}

        {isError && (
          <div className="flex min-h-40 items-center justify-center rounded-xl border border-red-500/20 bg-red-500/5">
            <p className="text-sm text-red-400">
              Unable to load recovery workflows.
            </p>
          </div>
        )}

        {!isLoading && !isError && (
          <>
            <RecoverySummary workflows={workflows} />

            <RecoveryFilters
              executionStatus={executionStatus}
              actionType={actionType}
              onExecutionStatusChange={setExecutionStatus}
              onActionTypeChange={setActionType}
              onClear={clearFilters}
            />

            <RecoveryCreateForm onCreated={handleCreated} />

            <RecoveryTable
              workflows={workflows}
              onWorkflowSelect={handleWorkflowSelect}
            />
          </>
        )}
      </div>

      <RecoveryDetails
        workflow={selectedWorkflow}
        onClose={() => setSelectedWorkflow(null)}
      />
    </div>
  );
}

export default RecoveryPage;
