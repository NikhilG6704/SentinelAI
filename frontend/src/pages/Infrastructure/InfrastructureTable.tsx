import { FiMonitor, FiServer } from "react-icons/fi";

import Card from "../../components/ui/Card";
import StatusDot from "../../components/ui/StatusDot";
import type { InfrastructureAsset } from "../../api/infrastructure";
interface InfrastructureTableProps {
  assets: InfrastructureAsset[];
}
function getStatus(status: InfrastructureAsset["status"]) {
  switch (status) {
    case "Healthy":
      return "online" as const;

    case "Warning":
    case "Critical":
      return "offline" as const;

    case "Offline":
    default:
      return "offline" as const;
  }
}

function InfrastructureTable({ assets }: InfrastructureTableProps) {
  return (
    <Card>
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-sm font-semibold text-zinc-200">
            Infrastructure Assets
          </h2>

          <p className="mt-1 text-xs text-zinc-500">
            Registered infrastructure monitored by SentinelAI
          </p>
        </div>

        <FiServer className="h-5 w-5 text-zinc-600" />
      </div>

      <div className="mt-5 overflow-x-auto">
        <table className="w-full min-w-[760px] text-left">
          <thead>
            <tr className="border-b border-zinc-800/80">
              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Asset
              </th>

              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Type
              </th>

              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                IP Address
              </th>

              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Environment
              </th>

              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Location
              </th>

              <th className="px-3 py-3 text-[11px] font-medium uppercase tracking-wider text-zinc-600">
                Status
              </th>
            </tr>
          </thead>

          <tbody>
            {assets.map((asset) => {
              const status = getStatus(asset.status);

              return (
                <tr
                  key={asset.id}
                  className="border-b border-zinc-800/50 last:border-b-0"
                >
                  <td className="px-3 py-4">
                    <div className="flex items-center gap-3">
                      <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-500/10">
                        <FiMonitor className="h-4 w-4 text-blue-400" />
                      </div>

                      <div>
                        <p className="text-xs font-medium text-zinc-200">
                          {asset.hostname}
                        </p>

                        <p className="mt-1 text-[11px] text-zinc-600">
                          ID #{asset.id}
                        </p>
                      </div>
                    </div>
                  </td>

                  <td className="px-3 py-4 text-xs text-zinc-400">
                    {asset.asset_type}
                  </td>

                  <td className="px-3 py-4 text-xs text-zinc-400">
                    {asset.ip_address}
                  </td>

                  <td className="px-3 py-4">
                    <span className="rounded-md border border-zinc-800 bg-zinc-950/60 px-2 py-1 text-[11px] text-zinc-400">
                      {asset.environment}
                    </span>
                  </td>

                  <td className="px-3 py-4 text-xs text-zinc-400">
                    {asset.location}
                  </td>

                  <td className="px-3 py-4">
                    <StatusDot status={status} label={asset.status} />
                  </td>
                </tr>
              );
            })}

            {assets.length === 0 && (
              <tr>
                <td
                  colSpan={4}
                  className="px-3 py-12 text-center text-sm text-zinc-500"
                >
                  No infrastructure assets found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </Card>
  );
}

export default InfrastructureTable;
