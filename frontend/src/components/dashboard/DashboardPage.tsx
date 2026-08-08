import { useDashboardOverview } from "../../hooks/useDashboard";
import {
  FiAlertTriangle,
  FiHardDrive,
  FiServer,
  FiShield,
  FiUsers,
} from "react-icons/fi";

import ActiveIncidents from "./ActiveIncidents";
import AIInsights from "./AIInsights";
import HealthScore from "./HealthScore";
import InfrastructureOverview from "./InfrastructureOverview";
import MetricCard from "./MetricCard";
import RecentActivity from "./RecentActivity";
import ResourceOverview from "./ResourceOverview";

type DashboardOverviewData = {
  total_assets: number;
  healthy_assets: number;
  warning_assets: number;
  critical_assets: number;
  total_agents: number;
  online_agents: number;
  offline_agents: number;
  total_metrics: number;
};

function calculateHealthScore(data: DashboardOverviewData) {
  if (data.total_assets === 0) {
    return 0;
  }

  const score =
    ((data.healthy_assets + data.warning_assets * 0.5) / data.total_assets) *
    100;

  return Math.round(score);
}
function DashboardPage() {
  const {
    data: dashboardResponse,
    isLoading,
    isError,
  } = useDashboardOverview();

  const dashboard = dashboardResponse?.data as
    | DashboardOverviewData
    | undefined;
  return (
    <div className="min-h-full">
      {/* Page header */}
      <div className="border-b border-zinc-800/70 px-6 py-5">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-blue-400">
            Overview
          </p>

          <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">
            Dashboard
          </h1>

          <p className="mt-1 max-w-2xl text-sm text-zinc-500">
            Real-time infrastructure health, operational events, and AI-powered
            insights.
          </p>
        </div>
      </div>

      <div className="space-y-5 p-6">
        {/* KPI Grid */}
        <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-5">
          <MetricCard
            label="Total Assets"
            value={isLoading ? "—" : (dashboard?.total_assets ?? "—")}
            description="Registered infrastructure"
            icon={<FiServer className="h-4 w-4" />}
          />

          <MetricCard
            label="Online Agents"
            value={isLoading ? "—" : (dashboard?.online_agents ?? "—")}
            description={
              dashboard
                ? `${dashboard.total_agents} registered agents`
                : "Monitoring agents"
            }
            icon={<FiUsers className="h-4 w-4" />}
          />

          <MetricCard
            label="Healthy Assets"
            value={isLoading ? "—" : (dashboard?.healthy_assets ?? "—")}
            description={
              dashboard
                ? `${dashboard.warning_assets} warning · ${dashboard.critical_assets} critical`
                : "Current infrastructure state"
            }
            icon={<FiShield className="h-4 w-4" />}
          />

          <MetricCard
            label="Offline Agents"
            value={isLoading ? "—" : (dashboard?.offline_agents ?? "—")}
            description="Agents requiring attention"
            icon={<FiAlertTriangle className="h-4 w-4" />}
          />

          <MetricCard
            label="Collected Metrics"
            value={isLoading ? "—" : (dashboard?.total_metrics ?? "—")}
            description="Recorded system metrics"
            icon={<FiHardDrive className="h-4 w-4" />}
          />
        </section>

        {/* Health + Infrastructure */}
        <section className="grid grid-cols-1 gap-5 xl:grid-cols-[280px_minmax(0,1fr)]">
          <div className="rounded-xl border border-zinc-800/80 bg-zinc-900/40 p-5">
            <div>
              <h2 className="text-sm font-semibold text-zinc-200">
                Overall Health
              </h2>

              <p className="mt-1 text-xs text-zinc-500">
                Current infrastructure health score
              </p>
            </div>

            <div className="mt-6">
              <HealthScore
                score={dashboard ? calculateHealthScore(dashboard) : 0}
              />
            </div>
          </div>

          <InfrastructureOverview />
        </section>

        {/* Resource metrics */}
        <section>
          <div className="mb-4">
            <h2 className="text-sm font-semibold text-zinc-200">
              Resource Utilization
            </h2>

            <p className="mt-1 text-xs text-zinc-500">
              Infrastructure performance across the monitored environment
            </p>
          </div>

          <ResourceOverview />
        </section>

        {/* Incidents + Activity */}
        <section className="grid grid-cols-1 gap-5 xl:grid-cols-2">
          <ActiveIncidents />
          <RecentActivity />
        </section>

        {/* AI Intelligence */}
        <section>
          <AIInsights />
        </section>
      </div>
    </div>
  );
}

export default DashboardPage;
