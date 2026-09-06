import type { ReactNode } from "react";

import Card from "../../components/ui/Card";

interface AIInsightCardProps {
  title: string;
  value: string;
  description: string;
  icon: ReactNode;
  status?: string;
  statusClassName?: string;
}

function AIInsightCard({
  title,
  value,
  description,
  icon,
  status,
  statusClassName = "bg-blue-500/10 text-blue-400",
}: AIInsightCardProps) {
  return (
    <Card>
      <div className="flex items-start justify-between gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-500/10">
          {icon}
        </div>

        {status && (
          <span
            className={[
              "rounded-full px-2 py-1 text-[10px] font-medium",
              statusClassName,
            ].join(" ")}
          >
            {status}
          </span>
        )}
      </div>

      <p className="mt-4 text-xs font-medium text-zinc-500">{title}</p>

      <p className="mt-1 text-xl font-semibold text-zinc-100">{value}</p>

      <p className="mt-1 text-[11px] leading-relaxed text-zinc-600">
        {description}
      </p>
    </Card>
  );
}

export default AIInsightCard;
