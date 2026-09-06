import { FiCheckCircle, FiClock, FiLoader, FiXCircle } from "react-icons/fi";

import type { RecoveryWorkflow } from "../../api/recovery";

import Card from "../../components/ui/Card";

interface ActionSummaryProps {
  workflows: RecoveryWorkflow[];
}

function ActionSummary({ workflows }: ActionSummaryProps) {
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
      label: "Total Workflows",
      value: workflows.length,
      icon: <FiClock className="h-4 w-4" />,
      valueClass: "text-zinc-100",
    },
    {
      label: "Pending",
      value: pending,
      icon: <FiClock className="h-4 w-4" />,
      valueClass: "text-amber-400",
    },
    {
      label: "Running",
      value: running,
      icon: <FiLoader className="h-4 w-4" />,
      valueClass: "text-blue-400",
    },
    {
      label: "Completed",
      value: completed,
      icon: <FiCheckCircle className="h-4 w-4" />,
      valueClass: "text-emerald-400",
    },
    {
      label: "Failed",
      value: failed,
      icon: <FiXCircle className="h-4 w-4" />,
      valueClass: "text-red-400",
    },
  ];

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-5">
      {cards.map((card) => (
        <Card key={card.label}>
          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-500">{card.label}</span>

            <div className="text-zinc-600">{card.icon}</div>
          </div>

          <p className={`mt-3 text-2xl font-semibold ${card.valueClass}`}>
            {card.value}
          </p>

          <p className="mt-1 text-[11px] text-zinc-600">
            Current recovery workflow state
          </p>
        </Card>
      ))}
    </div>
  );
}

export default ActionSummary;
