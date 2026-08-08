interface HealthScoreProps {
  score: number;
}

function HealthScore({ score }: HealthScoreProps) {
  const normalizedScore = Math.max(0, Math.min(100, score));

  const getStatus = () => {
    if (normalizedScore >= 90) {
      return {
        label: "Excellent",
        text: "text-emerald-400",
        ring: "border-emerald-500/30",
      };
    }

    if (normalizedScore >= 75) {
      return {
        label: "Healthy",
        text: "text-blue-400",
        ring: "border-blue-500/30",
      };
    }

    if (normalizedScore >= 50) {
      return {
        label: "Warning",
        text: "text-amber-400",
        ring: "border-amber-500/30",
      };
    }

    return {
      label: "Critical",
      text: "text-red-400",
      ring: "border-red-500/30",
    };
  };

  const status = getStatus();

  return (
    <div className="flex flex-col items-center justify-center">
      <div
        className={[
          "flex h-32 w-32 items-center justify-center rounded-full",
          "border-8 bg-zinc-950",
          status.ring,
        ].join(" ")}
      >
        <div className="text-center">
          <p className="text-3xl font-semibold tracking-tight text-zinc-100">
            {normalizedScore}
          </p>

          <p className="text-[10px] font-medium uppercase tracking-wider text-zinc-600">
            / 100
          </p>
        </div>
      </div>

      <div className="mt-4 text-center">
        <p className={["text-sm font-semibold", status.text].join(" ")}>
          {status.label}
        </p>

        <p className="mt-1 text-xs text-zinc-600">
          Overall infrastructure health
        </p>
      </div>
    </div>
  );
}

export default HealthScore;
