import { FiAlertTriangle, FiArrowRight, FiClock } from "react-icons/fi";

import { useIncidents } from "../../hooks/useIncidents";

import Badge from "../ui/Badge";
import Card from "../ui/Card";

function getBadgeVariant(severity: string): "danger" | "warning" | "info" {
  switch (severity) {
    case "Critical":
    case "High":
      return "danger";

    case "Medium":
      return "warning";

    default:
      return "info";
  }
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

function ActiveIncidents() {
  const {
    data: incidentsResponse,
    isLoading,
    isError,
  } = useIncidents({
    status: "Open",
  });

  const incidents = incidentsResponse?.data ?? [];

  const visibleIncidents = [...incidents]
    .sort(
      (a, b) =>
        new Date(b.detected_at).getTime() - new Date(a.detected_at).getTime(),
    )
    .slice(0, 3);

  return (
    <Card>
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-sm font-semibold text-zinc-200">
            Active Incidents
          </h2>

          <p className="mt-1 text-xs text-zinc-500">
            Incidents requiring operational attention
          </p>
        </div>

        <button
          type="button"
          className="flex items-center gap-1.5 text-xs font-medium text-blue-400 transition-colors hover:text-blue-300"
        >
          View all
          <FiArrowRight className="h-3.5 w-3.5" />
        </button>
      </div>

      <div className="mt-5 space-y-2">
        {isLoading && (
          <div className="flex h-24 items-center justify-center text-sm text-zinc-500">
            Loading incidents...
          </div>
        )}

        {isError && (
          <div className="flex h-24 items-center justify-center text-sm text-red-400">
            Unable to load incidents.
          </div>
        )}

        {!isLoading && !isError && visibleIncidents.length === 0 && (
          <div className="flex h-24 items-center justify-center rounded-lg border border-zinc-800/70 bg-zinc-950/40 text-sm text-zinc-500">
            No active incidents.
          </div>
        )}

        {!isLoading &&
          !isError &&
          visibleIncidents.map((incident) => (
            <div
              key={incident.id}
              className="flex items-center justify-between gap-4 rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-3"
            >
              <div className="flex min-w-0 items-center gap-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-red-500/10">
                  <FiAlertTriangle className="h-4 w-4 text-red-400" />
                </div>

                <div className="min-w-0">
                  <p className="truncate text-xs font-medium text-zinc-200">
                    {incident.incident_title}
                  </p>

                  <div className="mt-1 flex items-center gap-2">
                    <span className="truncate text-[11px] text-zinc-600">
                      Asset #{incident.infrastructure_asset_id}
                    </span>

                    <span className="text-zinc-700">•</span>

                    <span className="flex items-center gap-1 text-[11px] text-zinc-600">
                      <FiClock className="h-3 w-3" />
                      {getTimeAgo(incident.detected_at)}
                    </span>
                  </div>
                </div>
              </div>

              <Badge variant={getBadgeVariant(incident.severity)}>
                {incident.severity}
              </Badge>
            </div>
          ))}
      </div>
    </Card>
  );
}

export default ActiveIncidents;
