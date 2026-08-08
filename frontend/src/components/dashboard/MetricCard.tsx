import type { ReactNode } from "react";

interface MetricCardProps {
  label: string;
  value: string | number;
  description?: string;
  icon: ReactNode;
  trend?: {
    value: string;
    direction: "up" | "down" | "neutral";
  };
}

function MetricCard({
  label,
  value,
  description,
  icon,
  trend,
}: MetricCardProps) {
  const trendStyles = {
    up: "text-emerald-400",
    down: "text-red-400",
    neutral: "text-zinc-500",
  };

  return (
    <div className="rounded-xl border border-zinc-800/80 bg-zinc-900/40 p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-xs font-medium text-zinc-500">{label}</p>

          <p className="mt-2 text-2xl font-semibold tracking-tight text-zinc-100">
            {value}
          </p>

          {description && (
            <p className="mt-1 text-xs text-zinc-600">{description}</p>
          )}
        </div>

        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-zinc-800/70 text-zinc-400">
          {icon}
        </div>
      </div>

      {trend && (
        <div className="mt-4 flex items-center gap-1.5">
          <span
            className={[
              "text-xs font-medium",
              trendStyles[trend.direction],
            ].join(" ")}
          >
            {trend.value}
          </span>

          <span className="text-[11px] text-zinc-600">vs previous period</span>
        </div>
      )}
    </div>
  );
}

export default MetricCard;
