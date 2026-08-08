interface StatusDotProps {
  status: "online" | "warning" | "critical" | "offline" | "neutral";
  label?: string;
}

const statusStyles = {
  online: "bg-emerald-500",
  warning: "bg-amber-500",
  critical: "bg-red-500",
  offline: "bg-zinc-500",
  neutral: "bg-blue-500",
};

function StatusDot({ status, label }: StatusDotProps) {
  return (
    <div className="inline-flex items-center gap-2">
      <span
        className={["h-2 w-2 rounded-full", statusStyles[status]].join(" ")}
      />

      {label && <span className="text-xs text-zinc-400">{label}</span>}
    </div>
  );
}

export default StatusDot;
