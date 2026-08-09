import {
  FiAlertTriangle,
  FiCheckCircle,
  FiClock,
  FiShield,
} from "react-icons/fi";

import type { Incident } from "../../api/incidents";

import Card from "../../components/ui/Card";

interface IncidentSummaryProps {
  incidents: Incident[];
}

function IncidentSummary({ incidents }: IncidentSummaryProps) {
  const open = incidents.filter(
    (incident) => incident.status === "Open",
  ).length;

  const investigating = incidents.filter(
    (incident) => incident.status === "Investigating",
  ).length;

  const critical = incidents.filter(
    (incident) => incident.severity === "Critical",
  ).length;

  const resolved = incidents.filter(
    (incident) =>
      incident.status === "Resolved" || incident.status === "Closed",
  ).length;

  const cards = [
    {
      label: "Open",
      value: open,
      icon: <FiAlertTriangle className="h-4 w-4 text-red-400" />,
      valueClass: "text-red-400",
    },
    {
      label: "Investigating",
      value: investigating,
      icon: <FiClock className="h-4 w-4 text-amber-400" />,
      valueClass: "text-amber-400",
    },
    {
      label: "Critical",
      value: critical,
      icon: <FiShield className="h-4 w-4 text-red-400" />,
      valueClass: "text-red-400",
    },
    {
      label: "Resolved",
      value: resolved,
      icon: <FiCheckCircle className="h-4 w-4 text-emerald-400" />,
      valueClass: "text-emerald-400",
    },
  ];

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {cards.map((card) => (
        <Card key={card.label}>
          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-500">{card.label}</span>

            {card.icon}
          </div>

          <p className={`mt-3 text-2xl font-semibold ${card.valueClass}`}>
            {card.value}
          </p>

          <p className="mt-1 text-[11px] text-zinc-600">
            From current incident results
          </p>
        </Card>
      ))}
    </div>
  );
}

export default IncidentSummary;
