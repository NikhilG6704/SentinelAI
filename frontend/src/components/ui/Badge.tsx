interface BadgeProps {
  children: React.ReactNode;
  variant?: "default" | "success" | "warning" | "danger" | "info";
}

const variantStyles = {
  default: "bg-zinc-800 text-zinc-300",
  success: "bg-emerald-500/10 text-emerald-400 ring-1 ring-emerald-500/20",
  warning: "bg-amber-500/10 text-amber-400 ring-1 ring-amber-500/20",
  danger: "bg-red-500/10 text-red-400 ring-1 ring-red-500/20",
  info: "bg-blue-500/10 text-blue-400 ring-1 ring-blue-500/20",
};

function Badge({ children, variant = "default" }: BadgeProps) {
  return (
    <span
      className={[
        "inline-flex items-center rounded-md px-2 py-1",
        "text-[11px] font-medium",
        variantStyles[variant],
      ].join(" ")}
    >
      {children}
    </span>
  );
}

export default Badge;
