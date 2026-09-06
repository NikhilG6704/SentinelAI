import { FiAlertTriangle, FiChevronDown } from "react-icons/fi";

import { useIncidents } from "../../hooks/useIncidents";

interface AIIncidentSelectorProps {
  selectedIncidentId: number | null;
  onIncidentSelect: (incidentId: number | null) => void;
}

function AIIncidentSelector({
  selectedIncidentId,
  onIncidentSelect,
}: AIIncidentSelectorProps) {
  const {
    data: incidentsResponse,
    isLoading,
    isError,
  } = useIncidents({
    status: "Open",
  });

  const incidents = incidentsResponse?.data ?? [];

  return (
    <div className="rounded-xl border border-zinc-800/80 bg-zinc-900/40 p-5">
      <div className="flex items-start gap-3">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-red-500/10">
          <FiAlertTriangle className="h-4 w-4 text-red-400" />
        </div>

        <div className="min-w-0 flex-1">
          <h2 className="text-sm font-semibold text-zinc-200">
            Select Incident
          </h2>

          <p className="mt-1 text-xs text-zinc-500">
            Choose an open incident to run AI analysis against.
          </p>

          <div className="relative mt-4">
            <select
              value={selectedIncidentId ?? ""}
              onChange={(event) => {
                const value = event.target.value;

                onIncidentSelect(value === "" ? null : Number(value));
              }}
              disabled={isLoading || isError}
              className="h-11 w-full appearance-none rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 pr-10 text-sm text-zinc-300 outline-none transition-colors focus:border-blue-500/40 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <option value="">
                {isLoading
                  ? "Loading incidents..."
                  : isError
                    ? "Unable to load incidents"
                    : incidents.length === 0
                      ? "No open incidents"
                      : "Select an incident"}
              </option>

              {incidents.map((incident) => (
                <option key={incident.id} value={incident.id}>
                  {incident.incident_title} — Asset #
                  {incident.infrastructure_asset_id}
                </option>
              ))}
            </select>

            <FiChevronDown className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-600" />
          </div>

          {selectedIncidentId !== null && (
            <p className="mt-2 text-[11px] text-zinc-600">
              Incident #{selectedIncidentId} selected.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default AIIncidentSelector;
