import type { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
}

function Card({ children, className = "" }: CardProps) {
  return (
    <div
      className={[
        "rounded-xl border border-zinc-800/80",
        "bg-zinc-900/40",
        "shadow-sm",
        className,
      ].join(" ")}
    >
      {children}
    </div>
  );
}

export default Card;
