import { useEffect, useRef } from "react";
import { useAgentLatestMetric, useAssetAgentId } from "../../hooks/useLiveMetrics";
import type { InfrastructureAsset } from "../../api/infrastructure";

interface ServerMonitorCardProps {
  asset: InfrastructureAsset;
  onSelect: (asset: InfrastructureAsset) => void;
  onAlert: (hostname: string, message: string) => void;
}

function MetricBar({
  label,
  value,
  unit = "%",
  danger = 80,
  warn = 60,
}: {
  label: string;
  value: number | null;
  unit?: string;
  danger?: number;
  warn?: number;
}) {
  const pct = value ?? 0;
  const color =
    pct >= danger
      ? "bg-red-500"
      : pct >= warn
        ? "bg-amber-400"
        : "bg-emerald-500";

  return (
    <div>
      <div className="mb-1 flex items-center justify-between">
        <span className="text-[10px] uppercase tracking-widest text-zinc-500">
          {label}
        </span>
        <span
          className={`text-xs font-semibold tabular-nums ${
            pct >= danger
              ? "text-red-400"
              : pct >= warn
                ? "text-amber-400"
                : "text-zinc-300"
          }`}
        >
          {value !== null ? `${pct.toFixed(1)}${unit}` : "—"}
        </span>
      </div>
      <div className="h-1.5 w-full overflow-hidden rounded-full bg-zinc-800">
        <div
          className={`h-full rounded-full transition-all duration-700 ${color}`}
          style={{ width: `${Math.min(pct, 100)}%` }}
        />
      </div>
    </div>
  );
}

export default function ServerMonitorCard({
  asset,
  onSelect,
  onAlert,
}: ServerMonitorCardProps) {
  const { data: agentId } = useAssetAgentId(asset.id);
  const { data: metric } = useAgentLatestMetric(agentId ?? 0);
  const prevAlerted = useRef(false);

  const cpu = metric?.cpu_usage ?? null;
  const mem = metric?.memory_usage ?? null;
  const disk = metric?.disk_usage ?? null;
  const netIn = metric?.network_in ?? null;
  const uptime = metric?.uptime_seconds ?? null;

  const isCritical = cpu !== null && cpu >= 90;
  const isWarning = cpu !== null && cpu >= 70 && cpu < 90;

  // Toast notification when CPU first crosses 90%
  useEffect(() => {
    if (isCritical && !prevAlerted.current) {
      prevAlerted.current = true;
      onAlert(
        asset.hostname,
        `CPU at ${cpu?.toFixed(1)}% — anomaly detected!`,
      );
    }
    if (!isCritical) {
      prevAlerted.current = false;
    }
  }, [isCritical, cpu, asset.hostname, onAlert]);

  const statusRing = isCritical
    ? "border-red-500/70 shadow-red-500/20"
    : isWarning
      ? "border-amber-500/50 shadow-amber-500/10"
      : "border-zinc-700/50";

  const pulseClass = isCritical ? "animate-pulse" : "";

  const uptimeStr =
    uptime !== null
      ? uptime < 3600
        ? `${Math.floor(uptime / 60)}m`
        : `${Math.floor(uptime / 3600)}h`
      : "—";

  return (
    <button
      type="button"
      onClick={() => onSelect(asset)}
      className={`group relative w-full cursor-pointer rounded-xl border bg-zinc-900/60 p-4 text-left shadow-lg backdrop-blur-sm transition-all duration-300 hover:bg-zinc-900 hover:shadow-xl ${statusRing} ${isCritical ? "shadow-lg" : ""}`}
    >
      {/* Critical pulse ring */}
      {isCritical && (
        <span className="absolute -inset-px animate-ping rounded-xl border border-red-500/40" />
      )}

      {/* Header */}
      <div className="mb-3 flex items-start justify-between gap-2">
        <div className="min-w-0">
          <p className="truncate text-sm font-semibold text-zinc-100">
            {asset.hostname}
          </p>
          <p className="mt-0.5 truncate text-[10px] text-zinc-500">
            {asset.ip_address} · {asset.location}
          </p>
        </div>

        {/* Status badge */}
        <span
          className={`flex-shrink-0 rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider ${pulseClass} ${
            isCritical
              ? "bg-red-500/15 text-red-400"
              : isWarning
                ? "bg-amber-500/15 text-amber-400"
                : "bg-emerald-500/10 text-emerald-400"
          }`}
        >
          {isCritical ? "Critical" : isWarning ? "Warning" : "Healthy"}
        </span>
      </div>

      {/* Live metric bars */}
      <div className="space-y-2.5">
        <MetricBar label="CPU" value={cpu} danger={90} warn={70} />
        <MetricBar label="Memory" value={mem} danger={85} warn={65} />
        <MetricBar label="Disk" value={disk} danger={90} warn={75} />
      </div>

      {/* Footer row */}
      <div className="mt-3 flex items-center justify-between border-t border-zinc-800/60 pt-2.5 text-[10px] text-zinc-600">
        <span>
          Net In:{" "}
          <span className="text-zinc-400">
            {netIn !== null ? `${netIn.toFixed(0)} KB/s` : "—"}
          </span>
        </span>
        <span>
          Uptime: <span className="text-zinc-400">{uptimeStr}</span>
        </span>
      </div>

      {/* Hover indicator */}
      <div className="absolute bottom-3 right-3 opacity-0 transition-opacity group-hover:opacity-100">
        <span className="text-[9px] text-zinc-500">Click for details →</span>
      </div>
    </button>
  );
}
