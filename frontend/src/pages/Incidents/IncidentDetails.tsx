import { useState } from "react";

import type { Incident } from "../../api/incidents";

import { useCloseIncident, useResolveIncident } from "../../hooks/useIncidents";

import Badge from "../../components/ui/Badge";
import Card from "../../components/ui/Card";

interface IncidentDetailsProps {
  incident: Incident | null;
  onClose: () => void;
}

function getSeverityVariant(
  severity: Incident["severity"],
): "danger" | "warning" | "info" {
  switch (severity) {
    case "Critical":
    case "High":
      return "danger";

    case "Medium":
      return "warning";

    case "Low":
    default:
      return "info";
  }
}

function getStatusVariant(
  status: Incident["status"],
): "danger" | "warning" | "info" {
  switch (status) {
    case "Open":
      return "danger";

    case "Investigating":
      return "warning";

    case "Resolved":
    case "Closed":
    default:
      return "info";
  }
}

function IncidentDetails({ incident, onClose }: IncidentDetailsProps) {
  const [resolutionSummary, setResolutionSummary] = useState("");

  const resolveMutation = useResolveIncident();
  const closeMutation = useCloseIncident();

  if (!incident) {
    return null;
  }

  const canResolve =
    incident.status === "Open" || incident.status === "Investigating";

  const canClose = incident.status === "Resolved";

  const handleResolve = () => {
    if (!resolutionSummary.trim()) {
      return;
    }

    resolveMutation.mutate({
      incidentId: incident.id,
      payload: {
        resolution_summary: resolutionSummary.trim(),
      },
    });
  };

  const handleClose = () => {
    closeMutation.mutate(incident.id);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm">
      <div className="w-full max-w-2xl">
        <Card>
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0">
              <p className="text-xs font-medium uppercase tracking-wider text-blue-400">
                Incident Details
              </p>

              <h2 className="mt-1 text-lg font-semibold text-zinc-100">
                {incident.incident_title}
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
            <Badge variant={getSeverityVariant(incident.severity)}>
              {incident.severity}
            </Badge>

            <Badge variant={getStatusVariant(incident.status)}>
              {incident.status}
            </Badge>
          </div>

          <div className="mt-5 space-y-4">
            <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
              <p className="text-xs text-zinc-500">Description</p>

              <p className="mt-2 text-sm leading-relaxed text-zinc-300">
                {incident.incident_description}
              </p>
            </div>

            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
              <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                <p className="text-xs text-zinc-500">Infrastructure Asset</p>

                <p className="mt-2 text-sm font-medium text-zinc-200">
                  #{incident.infrastructure_asset_id}
                </p>
              </div>

              <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                <p className="text-xs text-zinc-500">Monitoring Agent</p>

                <p className="mt-2 text-sm font-medium text-zinc-200">
                  {incident.monitoring_agent_id
                    ? `#${incident.monitoring_agent_id}`
                    : "Not assigned"}
                </p>
              </div>

              <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                <p className="text-xs text-zinc-500">Source Alert</p>

                <p className="mt-2 text-sm font-medium text-zinc-200">
                  {incident.alert_id ? `#${incident.alert_id}` : "None"}
                </p>
              </div>

              <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                <p className="text-xs text-zinc-500">Detected</p>

                <p className="mt-2 text-sm font-medium text-zinc-200">
                  {new Date(incident.detected_at).toLocaleString()}
                </p>
              </div>
            </div>

            {incident.resolution_summary && (
              <div className="rounded-lg border border-emerald-500/10 bg-emerald-500/[0.03] p-4">
                <p className="text-xs text-zinc-500">Resolution</p>

                <p className="mt-2 text-sm text-zinc-300">
                  {incident.resolution_summary}
                </p>
              </div>
            )}
          </div>

          {canResolve && (
            <div className="mt-6 border-t border-zinc-800/70 pt-5">
              <p className="text-xs font-medium text-zinc-400">
                Resolve Incident
              </p>

              <textarea
                value={resolutionSummary}
                onChange={(event) => setResolutionSummary(event.target.value)}
                placeholder="Enter resolution summary..."
                rows={3}
                className="mt-3 w-full resize-none rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 py-2 text-sm text-zinc-200 outline-none placeholder:text-zinc-700 focus:border-blue-500/40"
              />

              <button
                type="button"
                onClick={handleResolve}
                disabled={
                  resolveMutation.isPending || !resolutionSummary.trim()
                }
                className="mt-3 h-10 rounded-lg bg-blue-500 px-4 text-sm font-medium text-white transition-colors hover:bg-blue-400 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {resolveMutation.isPending
                  ? "Resolving..."
                  : "Resolve Incident"}
              </button>
            </div>
          )}

          {canClose && (
            <div className="mt-6 border-t border-zinc-800/70 pt-5">
              <button
                type="button"
                onClick={handleClose}
                disabled={closeMutation.isPending}
                className="h-10 rounded-lg border border-zinc-800 bg-zinc-950/60 px-4 text-sm font-medium text-zinc-300 transition-colors hover:bg-zinc-800/60 hover:text-zinc-100 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {closeMutation.isPending ? "Closing..." : "Close Incident"}
              </button>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}

export default IncidentDetails;
