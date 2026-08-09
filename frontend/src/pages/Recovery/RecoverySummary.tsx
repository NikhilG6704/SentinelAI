import { FiCheckCircle, FiClock, FiLoader, FiXCircle } from "react-icons/fi";

import type { RecoveryWorkflow } from "../../api/recovery";

import Card from "../../components/ui/Card";

interface RecoverySummaryProps {
  workflows: RecoveryWorkflow[];
}

function RecoverySummary({ workflows }: RecoverySummaryProps) {
  const pending = workflows.filter(
    (workflow) => workflow.execution_status === "Pending",
  ).length;

  const running = workflows.filter(
    (workflow) => workflow.execution_status === "Running",
  ).length;

  const completed = workflows.filter(
    (workflow) => workflow.execution_status === "Completed",
  ).length;

  const failed = workflows.filter(
    (workflow) => workflow.execution_status === "Failed",
  ).length;

  const cards = [
    {
      label: "Pending",
      value: pending,
      icon: <FiClock className="h-4 w-4 text-amber-400" />,
      valueClass: "text-amber-400",
    },
    {
      label: "Running",
      value: running,
      icon: <FiLoader className="h-4 w-4 text-blue-400" />,
      valueClass: "text-blue-400",
    },
    {
      label: "Completed",
      value: completed,
      icon: <FiCheckCircle className="h-4 w-4 text-emerald-400" />,
      valueClass: "text-emerald-400",
    },
    {
      label: "Failed",
      value: failed,
      icon: <FiXCircle className="h-4 w-4 text-red-400" />,
      valueClass: "text-red-400",
    },
  ];

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {cards.map((card) => (
        <Card key={card.label}>
          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-500">{card.label}</span>

            {card.icon}
          </div>

          <p className={`mt-3 text-2xl font-semibold ${card.valueClass}`}>
            {card.value}
          </p>

          <p className="mt-1 text-[11px] text-zinc-600">
            From current workflow results
          </p>
        </Card>
      ))}
    </div>
  );
}

export default RecoverySummary;
