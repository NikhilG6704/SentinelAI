import { FiAlertTriangle, FiClock, FiServer } from "react-icons/fi";

import type { Incident } from "../../api/incidents";

import Badge from "../../components/ui/Badge";
import Card from "../../components/ui/Card";

interface IncidentTableProps {
  incidents: Incident[];
  onIncidentSelect: (incidentId: number) => void;
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

function IncidentTable({ incidents, onIncidentSelect }: IncidentTableProps) {
  return (
    <Card>
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-sm font-semibold text-zinc-200">
            Infrastructure Incidents
          </h2>

          <p className="mt-1 text-xs text-zinc-500">
            Operational incidents requiring investigation or resolution
          </p>
        </div>

        <FiServer className="h-5 w-5 text-zinc-600" />
      </div>

      <div className="mt-5 overflow-x-auto">
        <table className="w-full min-w-[900px] text-left">
          <thead>
            <tr className="border-b border-zinc-800/80">
              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Incident
              </th>

              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Asset
              </th>

              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Severity
              </th>

              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Status
              </th>

              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Detected
              </th>
            </tr>
          </thead>

          <tbody>
            {incidents.map((incident) => (
              <tr
                key={incident.id}
                className="border-b border-zinc-800/50 last:border-b-0"
              >
                <td className="px-3 py-4">
                  <button
                    type="button"
                    onClick={() => onIncidentSelect(incident.id)}
                    className="text-left"
                  >
                    <div className="flex items-start gap-3">
                      <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-red-500/10">
                        <FiAlertTriangle className="h-4 w-4 text-red-400" />
                      </div>

                      <div className="min-w-0">
                        <p className="text-xs font-medium text-zinc-200 transition-colors hover:text-blue-400">
                          {incident.incident_title}
                        </p>

                        <p className="mt-1 max-w-xs truncate text-[11px] text-zinc-600">
                          {incident.incident_description}
                        </p>
                      </div>
                    </div>
                  </button>
                </td>

                <td className="px-3 py-4">
                  <span className="text-xs text-zinc-400">
                    #{incident.infrastructure_asset_id}
                  </span>
                </td>

                <td className="px-3 py-4">
                  <Badge variant={getSeverityVariant(incident.severity)}>
                    {incident.severity}
                  </Badge>
                </td>

                <td className="px-3 py-4">
                  <Badge variant={getStatusVariant(incident.status)}>
                    {incident.status}
                  </Badge>
                </td>

                <td className="px-3 py-4">
                  <span className="flex items-center gap-1 text-[11px] text-zinc-600">
                    <FiClock className="h-3 w-3" />
                    {getTimeAgo(incident.detected_at)}
                  </span>
                </td>
              </tr>
            ))}

            {incidents.length === 0 && (
              <tr>
                <td
                  colSpan={5}
                  className="px-3 py-12 text-center text-sm text-zinc-500"
                >
                  No incidents found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </Card>
  );
}

export default IncidentTable;
