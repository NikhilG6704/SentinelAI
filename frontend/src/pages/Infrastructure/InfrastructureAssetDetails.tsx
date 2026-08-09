import {
  FiActivity,
  FiCalendar,
  FiGlobe,
  FiMapPin,
  FiMonitor,
  FiServer,
} from "react-icons/fi";

import { useInfrastructureAsset } from "../../hooks/useInfrastructure";

import Card from "../../components/ui/Card";
import StatusDot from "../../components/ui/StatusDot";

interface InfrastructureAssetDetailsProps {
  assetId: number | null;
  onClose: () => void;
}

function InfrastructureAssetDetails({
  assetId,
  onClose,
}: InfrastructureAssetDetailsProps) {
  const {
    data: assetResponse,
    isLoading,
    isError,
  } = useInfrastructureAsset(assetId ?? 0);

  const asset = assetResponse?.data;

  if (assetId === null) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm">
      <div className="w-full max-w-2xl">
        <Card>
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-xs font-medium uppercase tracking-wider text-blue-400">
                Infrastructure Asset
              </p>

              <h2 className="mt-1 text-lg font-semibold text-zinc-100">
                {asset?.hostname ?? "Asset Details"}
              </h2>
            </div>

            <button
              type="button"
              onClick={onClose}
              className="rounded-md px-2 py-1 text-sm text-zinc-500 transition-colors hover:bg-zinc-800 hover:text-zinc-200"
            >
              Close
            </button>
          </div>

          {isLoading && (
            <div className="flex min-h-40 items-center justify-center">
              <p className="text-sm text-zinc-500">Loading asset details...</p>
            </div>
          )}

          {isError && (
            <div className="flex min-h-40 items-center justify-center">
              <p className="text-sm text-red-400">
                Unable to load asset details.
              </p>
            </div>
          )}

          {!isLoading && !isError && asset && (
            <div className="mt-6 space-y-5">
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                  <div className="flex items-center gap-2">
                    <FiMonitor className="h-4 w-4 text-blue-400" />

                    <span className="text-xs text-zinc-500">Hostname</span>
                  </div>

                  <p className="mt-2 text-sm font-medium text-zinc-200">
                    {asset.hostname}
                  </p>
                </div>

                <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                  <div className="flex items-center gap-2">
                    <FiGlobe className="h-4 w-4 text-blue-400" />

                    <span className="text-xs text-zinc-500">IP Address</span>
                  </div>

                  <p className="mt-2 text-sm font-medium text-zinc-200">
                    {asset.ip_address}
                  </p>
                </div>

                <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                  <div className="flex items-center gap-2">
                    <FiServer className="h-4 w-4 text-blue-400" />

                    <span className="text-xs text-zinc-500">
                      Operating System
                    </span>
                  </div>

                  <p className="mt-2 text-sm font-medium text-zinc-200">
                    {asset.operating_system}
                  </p>
                </div>

                <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                  <div className="flex items-center gap-2">
                    <FiActivity className="h-4 w-4 text-blue-400" />

                    <span className="text-xs text-zinc-500">Status</span>
                  </div>

                  <div className="mt-2">
                    <StatusDot
                      status={asset.status === "Healthy" ? "online" : "offline"}
                      label={asset.status}
                    />
                  </div>
                </div>

                <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                  <div className="flex items-center gap-2">
                    <FiMapPin className="h-4 w-4 text-blue-400" />

                    <span className="text-xs text-zinc-500">Location</span>
                  </div>

                  <p className="mt-2 text-sm font-medium text-zinc-200">
                    {asset.location}
                  </p>
                </div>

                <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                  <div className="flex items-center gap-2">
                    <FiCalendar className="h-4 w-4 text-blue-400" />

                    <span className="text-xs text-zinc-500">Environment</span>
                  </div>

                  <p className="mt-2 text-sm font-medium text-zinc-200">
                    {asset.environment}
                  </p>
                </div>
              </div>

              {asset.description && (
                <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
                  <p className="text-xs text-zinc-500">Description</p>

                  <p className="mt-2 text-sm leading-relaxed text-zinc-300">
                    {asset.description}
                  </p>
                </div>
              )}

              <div className="flex items-center justify-between border-t border-zinc-800/70 pt-4 text-xs text-zinc-600">
                <span>Asset ID #{asset.id}</span>

                <span>{asset.is_active ? "Active" : "Inactive"}</span>
              </div>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}

export default InfrastructureAssetDetails;
