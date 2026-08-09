import type { IncidentSeverity, IncidentStatus } from "../../api/incidents";

interface IncidentFiltersProps {
  status: IncidentStatus | "all";
  severity: IncidentSeverity | "all";
  onStatusChange: (status: IncidentStatus | "all") => void;
  onSeverityChange: (severity: IncidentSeverity | "all") => void;
  onClear: () => void;
}

function IncidentFilters({
  status,
  severity,
  onStatusChange,
  onSeverityChange,
  onClear,
}: IncidentFiltersProps) {
  const hasFilters = status !== "all" || severity !== "all";

  return (
    <div className="rounded-xl border border-zinc-800/80 bg-zinc-900/40 p-4">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-center">
        <select
          value={status}
          onChange={(event) =>
            onStatusChange(event.target.value as IncidentStatus | "all")
          }
          className="h-10 rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 text-sm text-zinc-300 outline-none focus:border-blue-500/40"
        >
          <option value="all">All statuses</option>
          <option value="Open">Open</option>
          <option value="Investigating">Investigating</option>
          <option value="Resolved">Resolved</option>
          <option value="Closed">Closed</option>
        </select>

        <select
          value={severity}
          onChange={(event) =>
            onSeverityChange(event.target.value as IncidentSeverity | "all")
          }
          className="h-10 rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 text-sm text-zinc-300 outline-none focus:border-blue-500/40"
        >
          <option value="all">All severities</option>
          <option value="Critical">Critical</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
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

export default IncidentFilters;
