import { FiCpu, FiDatabase, FiHardDrive, FiWifi } from "react-icons/fi";

import Card from "../../components/ui/Card";

interface MetricsSummaryProps {
  metrics: Array<{
    cpu_usage: number;
    memory_usage: number;
    disk_usage: number;
    network_in: number;
    network_out: number;
  }>;
}

function average(values: number[]) {
  if (values.length === 0) {
    return 0;
  }

  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function MetricsSummary({ metrics }: MetricsSummaryProps) {
  const cpu = average(metrics.map((metric) => metric.cpu_usage));

  const memory = average(metrics.map((metric) => metric.memory_usage));

  const disk = average(metrics.map((metric) => metric.disk_usage));

  const networkIn = average(metrics.map((metric) => metric.network_in));

  const networkOut = average(metrics.map((metric) => metric.network_out));

  const cards = [
    {
      label: "Average CPU",
      value: `${cpu.toFixed(1)}%`,
      icon: <FiCpu className="h-4 w-4" />,
    },
    {
      label: "Average Memory",
      value: `${memory.toFixed(1)}%`,
      icon: <FiDatabase className="h-4 w-4" />,
    },
    {
      label: "Average Disk",
      value: `${disk.toFixed(1)}%`,
      icon: <FiHardDrive className="h-4 w-4" />,
    },
    {
      label: "Network In",
      value: networkIn.toFixed(1),
      icon: <FiWifi className="h-4 w-4" />,
    },
    {
      label: "Network Out",
      value: networkOut.toFixed(1),
      icon: <FiWifi className="h-4 w-4" />,
    },
  ];

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-5">
      {cards.map((card) => (
        <Card key={card.label}>
          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-500">{card.label}</span>

            <div className="text-zinc-600">{card.icon}</div>
          </div>

          <p className="mt-3 text-2xl font-semibold text-zinc-100">
            {card.value}
          </p>

          <p className="mt-1 text-[11px] text-zinc-600">
            Based on returned system metrics
          </p>
        </Card>
      ))}
    </div>
  );
}

export default MetricsSummary;
