import { useState } from "react";

import { useIncidents } from "../../hooks/useIncidents";

import AIAnalysisPanel from "./AIAnalysisPanel";
import AIIncidentSelector from "./AIIncidentSelector";

function AIPage() {
  const [selectedIncidentId, setSelectedIncidentId] = useState<number | null>(
    null,
  );

  const { data: incidentResponse } = useIncidents();

  const incidents = incidentResponse?.data ?? [];

  const selectedIncident =
    incidents.find((incident) => incident.id === selectedIncidentId) ?? null;

  const infrastructureAssetId =
    selectedIncident?.infrastructure_asset_id ?? null;

  const monitoringAgentId = selectedIncident?.monitoring_agent_id ?? null;

  return (
    <div className="min-h-full">
      <div className="border-b border-zinc-800/80 px-6 py-5">
        <p className="text-xs font-medium uppercase tracking-wider text-blue-400">
          Intelligence
        </p>

        <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">
          AI Intelligence
        </h1>

        <p className="mt-1 max-w-2xl text-sm text-zinc-500">
          Analyze infrastructure anomalies, predict failures, identify probable
          root causes, and generate recommended actions.
        </p>
      </div>

      <div className="space-y-5 p-6">
        <AIIncidentSelector
          selectedIncidentId={selectedIncidentId}
          onIncidentSelect={setSelectedIncidentId}
        />

        {selectedIncident && (
          <div className="rounded-xl border border-zinc-800/80 bg-zinc-900/40 p-5">
            <p className="text-xs font-medium uppercase tracking-wider text-zinc-600">
              Selected Incident
            </p>

            <h2 className="mt-1 text-sm font-semibold text-zinc-200">
              {selectedIncident.incident_title}
            </h2>

            <p className="mt-2 text-xs leading-relaxed text-zinc-500">
              {selectedIncident.incident_description}
            </p>

            <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3">
              <div>
                <p className="text-[11px] text-zinc-600">Incident ID</p>

                <p className="mt-1 text-xs text-zinc-300">
                  #{selectedIncident.id}
                </p>
              </div>

              <div>
                <p className="text-[11px] text-zinc-600">
                  Infrastructure Asset
                </p>

                <p className="mt-1 text-xs text-zinc-300">
                  #{selectedIncident.infrastructure_asset_id}
                </p>
              </div>

              <div>
                <p className="text-[11px] text-zinc-600">Monitoring Agent</p>

                <p className="mt-1 text-xs text-zinc-300">
                  {monitoringAgentId === null
                    ? "Not assigned"
                    : `#${monitoringAgentId}`}
                </p>
              </div>
            </div>
          </div>
        )}

        <AIAnalysisPanel
          incidentId={selectedIncidentId}
          infrastructureAssetId={infrastructureAssetId}
          monitoringAgentId={monitoringAgentId}
        />
      </div>
    </div>
  );
}

export default AIPage;
