import { useState } from "react";

import type {
  Incident,
  IncidentSeverity,
  IncidentStatus,
} from "../../api/incidents";

import { useIncidents } from "../../hooks/useIncidents";

import IncidentDetails from "./IncidentDetails";
import IncidentFilters from "./IncidentFilters";
import IncidentSummary from "./IncidentSummary";
import IncidentTable from "./IncidentTable";

function IncidentsPage() {
  const [status, setStatus] = useState<IncidentStatus | "all">("all");

  const [severity, setSeverity] = useState<IncidentSeverity | "all">("all");

  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(
    null,
  );

  const {
    data: incidentsResponse,
    isLoading,
    isError,
  } = useIncidents({
    status: status === "all" ? undefined : status,

    severity: severity === "all" ? undefined : severity,
  });

  const incidents = incidentsResponse?.data ?? [];

  const clearFilters = () => {
    setStatus("all");
    setSeverity("all");
  };

  const handleIncidentSelect = (incidentId: number) => {
    const incident = incidents.find((item) => item.id === incidentId);

    if (incident) {
      setSelectedIncident(incident);
    }
  };

  return (
    <div className="min-h-full">
      {/* Page Header */}
      <div className="border-b border-zinc-800/80 px-6 py-5">
        <p className="text-xs font-medium uppercase tracking-wider text-blue-400">
          Operations
        </p>

        <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">
          Incidents
        </h1>

        <p className="mt-1 max-w-2xl text-sm text-zinc-500">
          Investigate infrastructure incidents, track operational impact, and
          manage resolution.
        </p>
      </div>

      <div className="space-y-5 p-6">
        {isLoading && (
          <div className="flex min-h-40 items-center justify-center rounded-xl border border-zinc-800/80 bg-zinc-900/40">
            <p className="text-sm text-zinc-500">Loading incidents...</p>
          </div>
        )}

        {isError && (
          <div className="flex min-h-40 items-center justify-center rounded-xl border border-red-500/20 bg-red-500/5">
            <p className="text-sm text-red-400">Unable to load incidents.</p>
          </div>
        )}

        {!isLoading && !isError && (
          <>
            <IncidentSummary incidents={incidents} />

            <IncidentFilters
              status={status}
              severity={severity}
              onStatusChange={setStatus}
              onSeverityChange={setSeverity}
              onClear={clearFilters}
            />

            <IncidentTable
              incidents={incidents}
              onIncidentSelect={handleIncidentSelect}
            />
          </>
        )}
      </div>

      <IncidentDetails
        incident={selectedIncident}
        onClose={() => setSelectedIncident(null)}
      />
    </div>
  );
}

export default IncidentsPage;
