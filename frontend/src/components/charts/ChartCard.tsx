import type { ReactNode } from "react";

interface ChartCardProps {
  title: string;
  description?: string;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
}

function ChartCard({
  title,
  description,
  action,
  children,
  className = "",
}: ChartCardProps) {
  return (
    <section
      className={[
        "rounded-xl border border-zinc-800/80",
        "bg-zinc-900/40 shadow-sm",
        className,
      ].join(" ")}
    >
      <div className="flex items-start justify-between gap-4 border-b border-zinc-800/70 px-5 py-4">
        <div className="min-w-0">
          <h3 className="text-sm font-semibold text-zinc-200">{title}</h3>

          {description && (
            <p className="mt-1 text-xs text-zinc-500">{description}</p>
          )}
        </div>

        {action && <div className="shrink-0">{action}</div>}
      </div>

      <div className="p-5">{children}</div>
    </section>
  );
}

export default ChartCard;
