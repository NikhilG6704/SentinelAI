import { useMetrics } from "../../hooks/useMetrics";

import MetricsSummary from "./MetricsSummary";
import MetricsChart from "./MetricsChart";
function MetricsPage() {
  const { data: metricsResponse, isLoading, isError } = useMetrics();

  const metrics = metricsResponse?.data ?? [];

  return (
    <div className="min-h-full">
      <div className="border-b border-zinc-800/80 px-6 py-5">
        <p className="text-xs font-medium uppercase tracking-wider text-blue-400">
          Observability
        </p>

        <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">
          Metrics
        </h1>

        <p className="mt-1 max-w-2xl text-sm text-zinc-500">
          Monitor CPU, memory, disk, and network performance across
          infrastructure.
        </p>
      </div>

      <div className="space-y-5 p-6">
        {isLoading && (
          <div className="flex min-h-40 items-center justify-center rounded-xl border border-zinc-800/80 bg-zinc-900/40">
            <p className="text-sm text-zinc-500">Loading metrics...</p>
          </div>
        )}

        {isError && (
          <div className="flex min-h-40 items-center justify-center rounded-xl border border-red-500/20 bg-red-500/5">
            <p className="text-sm text-red-400">
              Unable to load system metrics.
            </p>
          </div>
        )}

        {!isLoading && !isError && (
          <>
            <MetricsSummary metrics={metrics} />

            <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
              <MetricsChart
                metrics={metrics}
                metric="cpu"
                title="CPU Utilization"
                description="CPU utilization across recent metric samples"
              />

              <MetricsChart
                metrics={metrics}
                metric="memory"
                title="Memory Utilization"
                description="Memory utilization across recent metric samples"
              />

              <MetricsChart
                metrics={metrics}
                metric="disk"
                title="Disk Utilization"
                description="Disk utilization across recent metric samples"
              />
              <MetricsChart
                metrics={metrics}
                metric="network"
                title="Network Utilization"
                description="Inbound and outbound network traffic across recent metric samples"
              />
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default MetricsPage;
