import { FiActivity, FiAlertCircle, FiServer } from "react-icons/fi";

import { useDashboardOverview } from "../../hooks/useDashboard";

import Card from "../ui/Card";
import StatusDot from "../ui/StatusDot";

function InfrastructureOverview() {
  const {
    data: dashboardResponse,
    isLoading,
    isError,
  } = useDashboardOverview();

  const dashboard = dashboardResponse?.data;

  const totalAssets = dashboard?.total_assets ?? 0;
  const onlineAgents = dashboard?.online_agents ?? 0;
  const offlineAgents = dashboard?.offline_agents ?? 0;
  const attentionAssets =
    (dashboard?.warning_assets ?? 0) + (dashboard?.critical_assets ?? 0);

  return (
    <Card>
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-sm font-semibold text-zinc-200">
            Infrastructure Overview
          </h2>

          <p className="mt-1 text-xs text-zinc-500">
            Current status of monitored infrastructure
          </p>
        </div>

        <FiServer className="h-5 w-5 text-zinc-600" />
      </div>

      <div className="mt-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/50 p-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-500">Total Assets</span>

            <FiServer className="h-4 w-4 text-zinc-600" />
          </div>

          <p className="mt-2 text-xl font-semibold text-zinc-100">
            {isLoading ? "—" : isError ? "—" : totalAssets}
          </p>
        </div>

        <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/50 p-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-500">Online</span>

            <StatusDot status="online" />
          </div>

          <p className="mt-2 text-xl font-semibold text-emerald-400">
            {isLoading ? "—" : isError ? "—" : onlineAgents}
          </p>
        </div>

        <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/50 p-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-500">Offline</span>

            <StatusDot status="offline" />
          </div>

          <p className="mt-2 text-xl font-semibold text-zinc-300">
            {isLoading ? "—" : isError ? "—" : offlineAgents}
          </p>
        </div>

        <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/50 p-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-500">Attention</span>

            <FiAlertCircle className="h-4 w-4 text-amber-400" />
          </div>

          <p className="mt-2 text-xl font-semibold text-amber-400">
            {isLoading ? "—" : isError ? "—" : attentionAssets}
          </p>
        </div>
      </div>

      <div className="mt-5 flex items-center justify-between border-t border-zinc-800/70 pt-4">
        <div className="flex items-center gap-2">
          <StatusDot status="online" label="Monitoring operational" />
        </div>

        <div className="flex items-center gap-2 text-xs text-zinc-600">
          <FiActivity className="h-3.5 w-3.5" />

          <span>
            {isLoading
              ? "Updating..."
              : isError
                ? "Unable to update"
                : "Live monitoring data"}
          </span>
        </div>
      </div>
    </Card>
  );
}

export default InfrastructureOverview;
