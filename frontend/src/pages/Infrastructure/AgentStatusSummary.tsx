import { FiActivity, FiCheckCircle, FiServer, FiXCircle } from "react-icons/fi";

import { useAgents } from "../../hooks/useAgents";

import Card from "../../components/ui/Card";

function AgentStatusSummary() {
  const { data: agentsResponse, isLoading, isError } = useAgents();

  const agents = agentsResponse?.data ?? [];

  const onlineAgents = agents.filter(
    (agent) =>
      agent.status?.toLowerCase() === "online" ||
      agent.status?.toLowerCase() === "active",
  ).length;

  const offlineAgents = agents.length - onlineAgents;

  return (
    <Card>
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-sm font-semibold text-zinc-200">
            Monitoring Agents
          </h2>

          <p className="mt-1 text-xs text-zinc-500">
            Current connectivity and monitoring status
          </p>
        </div>

        <FiActivity className="h-5 w-5 text-zinc-600" />
      </div>

      <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-3">
        <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-500">Total Agents</span>

            <FiServer className="h-4 w-4 text-zinc-600" />
          </div>

          <p className="mt-2 text-xl font-semibold text-zinc-100">
            {isLoading || isError ? "—" : agents.length}
          </p>
        </div>

        <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-500">Online</span>

            <FiCheckCircle className="h-4 w-4 text-emerald-400" />
          </div>

          <p className="mt-2 text-xl font-semibold text-emerald-400">
            {isLoading || isError ? "—" : onlineAgents}
          </p>
        </div>

        <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-500">Offline</span>

            <FiXCircle className="h-4 w-4 text-red-400" />
          </div>

          <p className="mt-2 text-xl font-semibold text-zinc-300">
            {isLoading || isError ? "—" : offlineAgents}
          </p>
        </div>
      </div>

      {isError && (
        <p className="mt-4 text-xs text-red-400">
          Unable to load monitoring agent status.
        </p>
      )}
    </Card>
  );
}

export default AgentStatusSummary;
