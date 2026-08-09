import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import ChartCard from "../../components/charts/ChartCard";
import type { SystemMetric } from "../../api/metrics";

interface MetricsChartProps {
  metrics: SystemMetric[];
  metric: "cpu" | "memory" | "disk" | "network";
  title: string;
  description: string;
}

function MetricsChart({
  metrics,
  metric,
  title,
  description,
}: MetricsChartProps) {
  const data = [...metrics]
    .sort(
      (a, b) =>
        new Date(a.collection_timestamp).getTime() -
        new Date(b.collection_timestamp).getTime(),
    )
    .slice(-30)
    .map((item) => ({
      time: new Date(item.collection_timestamp).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
      networkIn: item.network_in,
      networkOut: item.network_out,
      value:
        metric === "cpu"
          ? item.cpu_usage
          : metric === "memory"
            ? item.memory_usage
            : metric === "disk"
              ? item.disk_usage
              : item.network_in,
    }));

  return (
    <ChartCard
      title={title}
      description={description}
      action={<span className="text-xs font-medium text-zinc-500">Recent</span>}
    >
      {data.length === 0 ? (
        <div className="flex h-56 items-center justify-center">
          <p className="text-sm text-zinc-500">No metric samples available.</p>
        </div>
      ) : (
        <div className="h-56">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <XAxis
                dataKey="time"
                tick={{ fontSize: 10 }}
                tickLine={false}
                axisLine={false}
              />

              <YAxis
                domain={metric === "network" ? ["auto", "auto"] : [0, 100]}
                tick={{ fontSize: 10 }}
                tickLine={false}
                axisLine={false}
                width={35}
              />

              <Tooltip />

              {metric === "network" ? (
                <>
                  <Line
                    type="monotone"
                    dataKey="networkIn"
                    name="Network In"
                    strokeWidth={2}
                    dot={false}
                  />

                  <Line
                    type="monotone"
                    dataKey="networkOut"
                    name="Network Out"
                    strokeWidth={2}
                    dot={false}
                  />
                </>
              ) : (
                <Line
                  type="monotone"
                  dataKey="value"
                  strokeWidth={2}
                  dot={false}
                />
              )}
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </ChartCard>
  );
}

export default MetricsChart;
