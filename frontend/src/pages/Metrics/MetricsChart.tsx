import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { SystemMetric } from "../../api/metrics";
import ChartCard from "../../components/charts/ChartCard";

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

      value:
        metric === "cpu"
          ? item.cpu_usage
          : metric === "memory"
            ? item.memory_usage
            : metric === "disk"
              ? item.disk_usage
              : undefined,

      networkIn: metric === "network" ? item.network_in : undefined,

      networkOut: metric === "network" ? item.network_out : undefined,
    }));

  const isNetwork = metric === "network";

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
        <>
          <div className="mb-3 flex items-center gap-4 text-[11px] text-zinc-500">
            {isNetwork && (
              <>
                <span>Inbound</span>
                <span>Outbound</span>
              </>
            )}
          </div>

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
                  domain={isNetwork ? ["auto", "auto"] : [0, 100]}
                  tick={{ fontSize: 10 }}
                  tickLine={false}
                  axisLine={false}
                  width={40}
                />

                <Tooltip />

                {!isNetwork && (
                  <Line
                    type="monotone"
                    dataKey="value"
                    strokeWidth={2}
                    dot={false}
                  />
                )}

                {isNetwork && (
                  <>
                    <Line
                      type="monotone"
                      dataKey="networkIn"
                      name="Inbound"
                      strokeWidth={2}
                      dot={false}
                    />

                    <Line
                      type="monotone"
                      dataKey="networkOut"
                      name="Outbound"
                      strokeWidth={2}
                      dot={false}
                    />
                  </>
                )}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </>
      )}
    </ChartCard>
  );
}

export default MetricsChart;
