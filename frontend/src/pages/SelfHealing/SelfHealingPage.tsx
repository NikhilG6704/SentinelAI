import { useState } from "react";

import { useRecoveryWorkflows } from "../../hooks/useRecovery";

import ActionSummary from "./ActionSummary";
import ActionTable from "./ActionTable";
import ActionDetails from "./ActionDetails";

function SelfHealingPage() {
  const [selectedWorkflowId, setSelectedWorkflowId] = useState<number | null>(
    null,
  );

  const {
    data: workflowsResponse,
    isLoading,
    isError,
  } = useRecoveryWorkflows();

  const workflows = workflowsResponse?.data ?? [];

  return (
    <div className="min-h-full">
      <div className="border-b border-zinc-800/80 px-6 py-5">
        <p className="text-xs font-medium uppercase tracking-wider text-blue-400">
          Automation
        </p>

        <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">
              Self-Healing
            </h1>

            <p className="mt-1 max-w-2xl text-sm text-zinc-500">
              Review, execute, and monitor automated infrastructure recovery
              workflows.
            </p>
          </div>

          <div className="rounded-lg border border-amber-500/20 bg-amber-500/5 px-3 py-2">
            <p className="text-[11px] font-medium text-amber-400">
              Simulation Mode
            </p>

            <p className="mt-0.5 text-[10px] text-zinc-600">
              Recovery actions do not affect live infrastructure.
            </p>
          </div>
        </div>
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
            <ActionSummary workflows={workflows} />

            <ActionTable
              workflows={workflows}
              onWorkflowSelect={setSelectedWorkflowId}
            />
          </>
        )}
      </div>

      <ActionDetails
        workflowId={selectedWorkflowId}
        onClose={() => setSelectedWorkflowId(null)}
      />
    </div>
  );
}

export default SelfHealingPage;
