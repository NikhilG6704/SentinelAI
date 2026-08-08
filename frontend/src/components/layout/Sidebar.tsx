import {
  FiActivity,
  FiAlertTriangle,
  FiBarChart2,
  FiBell,
  FiBookOpen,
  FiCpu,
  FiFileText,
  FiGitBranch,
  FiList,
  FiMonitor,
  FiRefreshCw,
  FiServer,
  FiSettings,
  FiShield,
  FiTerminal,
  FiZap,
} from "react-icons/fi";

import NavigationItem from "./NavigationItem";

function NavigationGroup({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="space-y-1">
      <p className="px-3 pb-2 pt-4 text-[10px] font-semibold uppercase tracking-[0.12em] text-zinc-600">
        {title}
      </p>

      <div className="space-y-0.5">{children}</div>
    </div>
  );
}

function Sidebar() {
  return (
    <aside className="flex h-screen w-64 shrink-0 flex-col border-r border-zinc-800/80 bg-zinc-950">
      {/* Brand */}
      <div className="flex h-16 shrink-0 items-center border-b border-zinc-800/80 px-5">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-500/10 ring-1 ring-blue-500/20">
            <FiShield className="h-4 w-4 text-blue-400" />
          </div>

          <div>
            <h1 className="text-sm font-semibold tracking-wide text-zinc-100">
              SENTINELAI
            </h1>

            <p className="text-[10px] text-zinc-500">Enterprise Operations</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-3 pb-6">
        <NavigationGroup title="Overview">
          <NavigationItem
            label="Dashboard"
            path="/dashboard"
            icon={FiActivity}
          />
        </NavigationGroup>

        <NavigationGroup title="Infrastructure">
          <NavigationItem
            label="Assets"
            path="/infrastructure"
            icon={FiServer}
          />

          <NavigationItem
            label="Agents"
            path="/infrastructure/agents"
            icon={FiMonitor}
          />

          <NavigationItem label="Metrics" path="/metrics" icon={FiBarChart2} />

          <NavigationItem label="Logs" path="/logs" icon={FiTerminal} />
        </NavigationGroup>

        <NavigationGroup title="Operations">
          <NavigationItem label="Alerts" path="/alerts" icon={FiBell} />

          <NavigationItem
            label="Incidents"
            path="/incidents"
            icon={FiAlertTriangle}
          />

          <NavigationItem
            label="Recovery"
            path="/recovery"
            icon={FiRefreshCw}
          />
        </NavigationGroup>

        <NavigationGroup title="AI Intelligence">
          <NavigationItem label="AI Overview" path="/ai" icon={FiCpu} />

          <NavigationItem
            label="Anomalies"
            path="/ai/anomalies"
            icon={FiActivity}
          />

          <NavigationItem
            label="Predictions"
            path="/ai/predictions"
            icon={FiZap}
          />

          <NavigationItem
            label="Root Cause"
            path="/ai/root-cause"
            icon={FiGitBranch}
          />

          <NavigationItem
            label="Recommendations"
            path="/ai/recommendations"
            icon={FiBookOpen}
          />

          <NavigationItem
            label="Self-Healing"
            path="/self-healing"
            icon={FiShield}
          />
        </NavigationGroup>

        <NavigationGroup title="Administration">
          <NavigationItem
            label="Automation Rules"
            path="/automation"
            icon={FiSettings}
          />

          <NavigationItem label="Reports" path="/reports" icon={FiFileText} />

          <NavigationItem label="Audit Logs" path="/audit" icon={FiList} />
        </NavigationGroup>
      </nav>

      {/* System status */}
      <div className="shrink-0 border-t border-zinc-800/80 p-3">
        <div className="flex items-center gap-3 rounded-lg bg-zinc-900/60 px-3 py-2.5">
          <span className="relative flex h-2.5 w-2.5">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-40" />
            <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-emerald-500" />
          </span>

          <div className="min-w-0">
            <p className="text-xs font-medium text-zinc-300">
              System Operational
            </p>

            <p className="text-[10px] text-zinc-600">All services healthy</p>
          </div>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
