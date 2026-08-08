import { FiCpu, FiDatabase, FiHardDrive, FiWifi } from "react-icons/fi";
import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { useMetrics } from "../../hooks/useMetrics";

import ChartCard from "../charts/ChartCard";

function ResourceOverview() {
  const { data: metricsResponse, isLoading, isError } = useMetrics();

  const metrics = metricsResponse?.data ?? [];

  const chartData = [...metrics]
    .sort(
      (a, b) =>
        new Date(a.collection_timestamp).getTime() -
        new Date(b.collection_timestamp).getTime(),
    )
    .slice(-24)
    .map((metric) => ({
      time: new Date(metric.collection_timestamp).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
      cpu: metric.cpu_usage,
      memory: metric.memory_usage,
      disk: metric.disk_usage,
      networkIn: metric.network_in,
      networkOut: metric.network_out,
    }));

  const renderEmptyState = (icon: React.ReactNode, message: string) => (
    <div className="flex h-48 flex-col items-center justify-center">
      {icon}

      <p className="mt-3 text-sm text-zinc-500">
        {isLoading
          ? "Loading metrics..."
          : isError
            ? "Unable to load metrics"
            : message}
      </p>
    </div>
  );

  return (
    <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
      <ChartCard
        title="CPU Utilization"
        description="CPU usage across monitored infrastructure"
        action={
          <span className="text-xs font-medium text-zinc-500">Recent</span>
        }
      >
        {chartData.length > 0 ? (
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <XAxis
                  dataKey="time"
                  tick={{ fontSize: 10 }}
                  tickLine={false}
                  axisLine={false}
                />

                <YAxis
                  domain={[0, 100]}
                  tick={{ fontSize: 10 }}
                  tickLine={false}
                  axisLine={false}
                  width={30}
                />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="cpu"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ) : (
          renderEmptyState(
            <FiCpu className="h-8 w-8 text-zinc-700" />,
            "CPU metrics will appear here",
          )
        )}
      </ChartCard>

      <ChartCard
        title="Memory Utilization"
        description="Memory usage across monitored infrastructure"
        action={
          <span className="text-xs font-medium text-zinc-500">Recent</span>
        }
      >
        {chartData.length > 0 ? (
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <XAxis
                  dataKey="time"
                  tick={{ fontSize: 10 }}
                  tickLine={false}
                  axisLine={false}
                />

                <YAxis
                  domain={[0, 100]}
                  tick={{ fontSize: 10 }}
                  tickLine={false}
                  axisLine={false}
                  width={30}
                />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="memory"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ) : (
          renderEmptyState(
            <FiDatabase className="h-8 w-8 text-zinc-700" />,
            "Memory metrics will appear here",
          )
        )}
      </ChartCard>

      <ChartCard
        title="Disk Utilization"
        description="Storage utilization across monitored infrastructure"
        action={
          <span className="text-xs font-medium text-zinc-500">Recent</span>
        }
      >
        {chartData.length > 0 ? (
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <XAxis
                  dataKey="time"
                  tick={{ fontSize: 10 }}
                  tickLine={false}
                  axisLine={false}
                />

                <YAxis
                  domain={[0, 100]}
                  tick={{ fontSize: 10 }}
                  tickLine={false}
                  axisLine={false}
                  width={30}
                />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="disk"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ) : (
          renderEmptyState(
            <FiHardDrive className="h-8 w-8 text-zinc-700" />,
            "Disk metrics will appear here",
          )
        )}
      </ChartCard>

      <ChartCard
        title="Network Utilization"
        description="Network traffic across monitored infrastructure"
        action={
          <span className="text-xs font-medium text-zinc-500">Recent</span>
        }
      >
        {chartData.length > 0 ? (
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <XAxis
                  dataKey="time"
                  tick={{ fontSize: 10 }}
                  tickLine={false}
                  axisLine={false}
                />

                <YAxis
                  tick={{ fontSize: 10 }}
                  tickLine={false}
                  axisLine={false}
                  width={40}
                />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="networkIn"
                  strokeWidth={2}
                  dot={false}
                />

                <Line
                  type="monotone"
                  dataKey="networkOut"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ) : (
          renderEmptyState(
            <FiWifi className="h-8 w-8 text-zinc-700" />,
            "Network metrics will appear here",
          )
        )}
      </ChartCard>
    </div>
  );
}

export default ResourceOverview;
