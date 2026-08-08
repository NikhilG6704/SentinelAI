import { useMemo, useState } from "react";

import { useInfrastructureAssets } from "../../hooks/useInfrastructure";

import InfrastructureFilters from "./InfrastructureFilters";
import InfrastructureTable from "./InfrastructureTable";
import AgentStatusSummary from "./AgentStatusSummary";

function InfrastructurePage() {
  const {
    data: infrastructureResponse,
    isLoading,
    isError,
  } = useInfrastructureAssets();

  const assets = infrastructureResponse?.data ?? [];

  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("all");

  const filteredAssets = useMemo(() => {
    const normalizedSearch = search.trim().toLowerCase();

    return assets.filter((asset) => {
      const matchesSearch =
        normalizedSearch.length === 0 ||
        String(asset.id).includes(normalizedSearch) ||
        asset.hostname?.toLowerCase().includes(normalizedSearch) ||
        asset.ip_address?.toLowerCase().includes(normalizedSearch);

      const matchesStatus = status === "all" || asset.status === status;

      return matchesSearch && matchesStatus;
    });
  }, [assets, search, status]);

  const clearFilters = () => {
    setSearch("");
    setStatus("all");
  };

  return (
    <div className="min-h-full">
      <div className="border-b border-zinc-800/80 px-6 py-5">
        <p className="text-xs font-medium uppercase tracking-wider text-blue-400">
          Infrastructure
        </p>

        <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">
          Infrastructure
        </h1>

        <p className="mt-1 max-w-2xl text-sm text-zinc-500">
          Monitor infrastructure assets, system status, and connected monitoring
          agents.
        </p>
      </div>

      <div className="space-y-5 p-6">
        {isLoading && (
          <div className="flex min-h-40 items-center justify-center rounded-xl border border-zinc-800/80 bg-zinc-900/40">
            <p className="text-sm text-zinc-500">Loading infrastructure...</p>
          </div>
        )}

        {isError && (
          <div className="flex min-h-40 items-center justify-center rounded-xl border border-red-500/20 bg-red-500/5">
            <p className="text-sm text-red-400">
              Unable to load infrastructure assets.
            </p>
          </div>
        )}

        {!isLoading && !isError && (
          <>
            <AgentStatusSummary />

            <InfrastructureFilters
              search={search}
              status={status}
              onSearchChange={setSearch}
              onStatusChange={setStatus}
              onClear={clearFilters}
            />

            <InfrastructureTable assets={filteredAssets} />
          </>
        )}
      </div>
    </div>
  );
}

export default InfrastructurePage;
