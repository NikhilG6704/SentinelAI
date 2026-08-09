import { useState } from "react";

import {
  type RecoveryActionType,
  type RecoveryWorkflowCreate,
} from "../../api/recovery";

import apiClient from "../../api/client";

import Card from "../../components/ui/Card";

interface RecoveryCreateFormProps {
  onCreated: () => void;
}

function RecoveryCreateForm({ onCreated }: RecoveryCreateFormProps) {
  const [workflowName, setWorkflowName] = useState("");

  const [automationRuleId, setAutomationRuleId] = useState("");

  const [incidentId, setIncidentId] = useState("");

  const [assetId, setAssetId] = useState("");

  const [actionType, setActionType] =
    useState<RecoveryActionType>("RESTART_SERVICE");

  const [executedBy, setExecutedBy] = useState("");

  const [isSubmitting, setIsSubmitting] = useState(false);

  const [error, setError] = useState<string | null>(null);

  const resetForm = () => {
    setWorkflowName("");
    setAutomationRuleId("");
    setIncidentId("");
    setAssetId("");
    setActionType("RESTART_SERVICE");
    setExecutedBy("");
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    setError(null);

    const parsedAutomationRuleId = Number(automationRuleId);

    const parsedAssetId = Number(assetId);

    const parsedIncidentId = incidentId ? Number(incidentId) : null;

    if (
      !workflowName.trim() ||
      !automationRuleId ||
      !assetId ||
      !executedBy.trim()
    ) {
      setError("Please fill in all required fields.");
      return;
    }

    if (
      !Number.isInteger(parsedAutomationRuleId) ||
      parsedAutomationRuleId <= 0
    ) {
      setError("Automation Rule ID must be a positive integer.");
      return;
    }

    if (!Number.isInteger(parsedAssetId) || parsedAssetId <= 0) {
      setError("Infrastructure Asset ID must be a positive integer.");
      return;
    }

    if (
      parsedIncidentId !== null &&
      (!Number.isInteger(parsedIncidentId) || parsedIncidentId <= 0)
    ) {
      setError("Incident ID must be a positive integer.");
      return;
    }

    const payload: RecoveryWorkflowCreate = {
      workflow_name: workflowName.trim(),
      automation_rule_id: parsedAutomationRuleId,
      incident_id: parsedIncidentId,
      infrastructure_asset_id: parsedAssetId,
      action_type: actionType,
      executed_by: executedBy.trim(),
    };

    try {
      setIsSubmitting(true);

      await apiClient.post("/recovery-workflows", payload);

      resetForm();
      onCreated();
    } catch (requestError: any) {
      const message =
        requestError?.response?.data?.error?.message ??
        requestError?.response?.data?.message ??
        "Unable to create recovery workflow.";

      setError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card>
      <div>
        <h2 className="text-sm font-semibold text-zinc-200">
          Create Recovery Workflow
        </h2>

        <p className="mt-1 text-xs text-zinc-500">
          Create a recovery workflow for simulation execution.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="mt-5 space-y-4">
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <div>
            <label className="text-xs font-medium text-zinc-400">
              Workflow Name
            </label>

            <input
              value={workflowName}
              onChange={(event) => setWorkflowName(event.target.value)}
              placeholder="Restart production API"
              className="mt-2 h-10 w-full rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 text-sm text-zinc-200 outline-none placeholder:text-zinc-700 focus:border-blue-500/40"
            />
          </div>

          <div>
            <label className="text-xs font-medium text-zinc-400">
              Executed By
            </label>

            <input
              value={executedBy}
              onChange={(event) => setExecutedBy(event.target.value)}
              placeholder="admin"
              className="mt-2 h-10 w-full rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 text-sm text-zinc-200 outline-none placeholder:text-zinc-700 focus:border-blue-500/40"
            />
          </div>

          <div>
            <label className="text-xs font-medium text-zinc-400">
              Automation Rule ID
            </label>

            <input
              type="number"
              min="1"
              value={automationRuleId}
              onChange={(event) => setAutomationRuleId(event.target.value)}
              placeholder="1"
              className="mt-2 h-10 w-full rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 text-sm text-zinc-200 outline-none placeholder:text-zinc-700 focus:border-blue-500/40"
            />
          </div>

          <div>
            <label className="text-xs font-medium text-zinc-400">
              Infrastructure Asset ID
            </label>

            <input
              type="number"
              min="1"
              value={assetId}
              onChange={(event) => setAssetId(event.target.value)}
              placeholder="1"
              className="mt-2 h-10 w-full rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 text-sm text-zinc-200 outline-none placeholder:text-zinc-700 focus:border-blue-500/40"
            />
          </div>

          <div>
            <label className="text-xs font-medium text-zinc-400">
              Incident ID
              <span className="ml-1 text-zinc-700">(optional)</span>
            </label>

            <input
              type="number"
              min="1"
              value={incidentId}
              onChange={(event) => setIncidentId(event.target.value)}
              placeholder="1"
              className="mt-2 h-10 w-full rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 text-sm text-zinc-200 outline-none placeholder:text-zinc-700 focus:border-blue-500/40"
            />
          </div>

          <div>
            <label className="text-xs font-medium text-zinc-400">
              Action Type
            </label>

            <select
              value={actionType}
              onChange={(event) =>
                setActionType(event.target.value as RecoveryActionType)
              }
              className="mt-2 h-10 w-full rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 text-sm text-zinc-300 outline-none focus:border-blue-500/40"
            >
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
          </div>
        </div>

        {error && (
          <div className="rounded-lg border border-red-500/20 bg-red-500/5 px-4 py-3">
            <p className="text-xs text-red-400">{error}</p>
          </div>
        )}

        <div className="flex items-center justify-between gap-4 border-t border-zinc-800/70 pt-4">
          <p className="text-[11px] text-zinc-600">
            Execution mode: Simulation
          </p>

          <button
            type="submit"
            disabled={isSubmitting}
            className="h-10 rounded-lg bg-blue-500 px-4 text-sm font-medium text-white transition-colors hover:bg-blue-400 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isSubmitting ? "Creating..." : "Create Workflow"}
          </button>
        </div>
      </form>
    </Card>
  );
}

export default RecoveryCreateForm;
