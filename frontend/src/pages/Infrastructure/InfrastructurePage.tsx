import { useMemo, useState } from "react";
import toast from "react-hot-toast";

import { useInfrastructureAssets } from "../../hooks/useInfrastructure";
import type { InfrastructureAsset } from "../../api/infrastructure";

import AgentStatusSummary from "./AgentStatusSummary";
import InfrastructureAssetDetails from "./InfrastructureAssetDetails";
import InfrastructureFilters from "./InfrastructureFilters";
import ServerMonitorCard from "./ServerMonitorCard";

function InfrastructurePage() {
  const {
    data: infrastructureResponse,
    isLoading,
    isError,
  } = useInfrastructureAssets();

  const assets = infrastructureResponse?.data ?? [];

  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("all");
  const [selectedAsset, setSelectedAsset] = useState<InfrastructureAsset | null>(null);

  const filteredAssets = useMemo(() => {
    const normalizedSearch = search.trim().toLowerCase();

    return assets.filter((asset) => {
      const matchesSearch =
        normalizedSearch.length === 0 ||
        String(asset.id).includes(normalizedSearch) ||
        asset.hostname.toLowerCase().includes(normalizedSearch) ||
        asset.ip_address.toLowerCase().includes(normalizedSearch);

      const matchesStatus = status === "all" || asset.status === status;

      return matchesSearch && matchesStatus;
    });
  }, [assets, search, status]);

  const clearFilters = () => {
    setSearch("");
    setStatus("all");
  };

  const handleAlert = (hostname: string, message: string) => {
    toast.error(message, {
      id: `alert-${hostname}`, // Prevent duplicate toasts
      duration: 10000,
      icon: '🚨',
    });
  };

  return (
    <div className="min-h-full">
      <div className="border-b border-zinc-800/80 px-6 py-5">
        <p className="text-xs font-medium uppercase tracking-wider text-blue-400">
          Infrastructure
        </p>

        <h1 className="mt-1 text-2xl font-semibold tracking-tight text-zinc-100">
          Infrastructure Live Grid
        </h1>

        <p className="mt-1 max-w-2xl text-sm text-zinc-500">
          Real-time monitoring of all server assets.
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

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {filteredAssets.map((asset) => (
                <ServerMonitorCard
                  key={asset.id}
                  asset={asset}
                  onSelect={setSelectedAsset}
                  onAlert={handleAlert}
                />
              ))}
            </div>

            {filteredAssets.length === 0 && (
              <div className="py-12 text-center text-sm text-zinc-500">
                No assets found matching the current filters.
              </div>
            )}
          </>
        )}
      </div>

      <InfrastructureAssetDetails
        assetId={selectedAsset?.id ?? null}
        onClose={() => setSelectedAsset(null)}
      />
    </div>
  );
}

export default InfrastructurePage;
