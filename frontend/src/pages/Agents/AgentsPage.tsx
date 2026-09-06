import { useAgents } from "../../hooks/useAgents";

export default function AgentsPage() {
  const { data: response, isLoading, isError } = useAgents();
  const agents = response?.data ?? [];

  return (
    <div className="min-h-full">
      <div className="border-b border-zinc-800/80 px-6 py-5">
        <p className="text-xs font-medium uppercase tracking-wider text-blue-400">
          Infrastructure
        </p>
        <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">
          Monitoring Agents
        </h1>
        <p className="mt-1 max-w-2xl text-sm text-zinc-500">
          Manage and monitor all installed agents across your infrastructure.
        </p>
      </div>

      <div className="p-6">
        {isLoading ? (
          <div className="flex h-32 items-center justify-center text-zinc-500">
            Loading agents...
          </div>
        ) : isError ? (
          <div className="flex h-32 items-center justify-center text-red-500">
            Error loading agents.
          </div>
        ) : (
          <div className="overflow-hidden rounded-xl border border-zinc-800/80 bg-zinc-900/40">
            <table className="min-w-full divide-y divide-zinc-800/80 text-left text-sm">
              <thead className="bg-zinc-950/50">
                <tr>
                  <th className="px-4 py-3 font-semibold text-zinc-300">Name</th>
                  <th className="px-4 py-3 font-semibold text-zinc-300">Version</th>
                  <th className="px-4 py-3 font-semibold text-zinc-300">Status</th>
                  <th className="px-4 py-3 font-semibold text-zinc-300">Asset ID</th>
                  <th className="px-4 py-3 font-semibold text-zinc-300">Last Heartbeat</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800/80">
                {agents.map((agent) => (
                  <tr key={agent.id} className="hover:bg-zinc-800/50">
                    <td className="px-4 py-3 text-zinc-100">{agent.agent_name}</td>
                    <td className="px-4 py-3 text-zinc-400">{agent.agent_version}</td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-[10px] font-medium uppercase tracking-wider ${
                        agent.status === "Online"
                          ? "bg-emerald-500/10 text-emerald-400"
                          : "bg-red-500/10 text-red-400"
                      }`}>
                        {agent.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-zinc-400">{agent.infrastructure_asset_id}</td>
                    <td className="px-4 py-3 text-zinc-500 text-xs">
                      {new Date(agent.last_heartbeat).toLocaleString()}
                    </td>
                  </tr>
                ))}
                {agents.length === 0 && (
                  <tr>
                    <td colSpan={5} className="py-8 text-center text-zinc-500">
                      No agents found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
