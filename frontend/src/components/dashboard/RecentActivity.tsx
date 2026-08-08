import {
  FiActivity,
  FiAlertTriangle,
  FiCheckCircle,
  FiClock,
  FiCpu,
} from "react-icons/fi";

import { useAuditLogs } from "../../hooks/useAudit";

import Card from "../ui/Card";

interface ActivityItemProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  time: string;
  iconClassName: string;
}

function ActivityItem({
  icon,
  title,
  description,
  time,
  iconClassName,
}: ActivityItemProps) {
  return (
    <div className="flex gap-3">
      <div
        className={[
          "flex h-8 w-8 shrink-0 items-center justify-center rounded-lg",
          iconClassName,
        ].join(" ")}
      >
        {icon}
      </div>

      <div className="min-w-0 flex-1">
        <div className="flex items-start justify-between gap-3">
          <p className="text-xs font-medium text-zinc-300">{title}</p>

          <span className="flex shrink-0 items-center gap-1 text-[10px] text-zinc-600">
            <FiClock className="h-3 w-3" />
            {time}
          </span>
        </div>

        <p className="mt-1 text-[11px] leading-relaxed text-zinc-600">
          {description}
        </p>
      </div>
    </div>
  );
}

function getActivityIcon(action: string) {
  const normalizedAction = action.toLowerCase();

  if (
    normalizedAction.includes("incident") ||
    normalizedAction.includes("alert")
  ) {
    return {
      icon: <FiAlertTriangle className="h-4 w-4 text-red-400" />,
      iconClassName: "bg-red-500/10",
    };
  }

  if (
    normalizedAction.includes("ai") ||
    normalizedAction.includes("prediction") ||
    normalizedAction.includes("analysis")
  ) {
    return {
      icon: <FiCpu className="h-4 w-4 text-blue-400" />,
      iconClassName: "bg-blue-500/10",
    };
  }

  if (
    normalizedAction.includes("recover") ||
    normalizedAction.includes("complete") ||
    normalizedAction.includes("success")
  ) {
    return {
      icon: <FiCheckCircle className="h-4 w-4 text-emerald-400" />,
      iconClassName: "bg-emerald-500/10",
    };
  }

  return {
    icon: <FiActivity className="h-4 w-4 text-amber-400" />,
    iconClassName: "bg-amber-500/10",
  };
}

function getTimeAgo(timestamp: string) {
  const diff = Date.now() - new Date(timestamp).getTime();

  const minutes = Math.max(0, Math.floor(diff / (1000 * 60)));

  if (minutes < 1) {
    return "Just now";
  }

  if (minutes < 60) {
    return `${minutes} min`;
  }

  const hours = Math.floor(minutes / 60);

  if (hours < 24) {
    return `${hours} hr`;
  }

  const days = Math.floor(hours / 24);

  return `${days}d`;
}

function RecentActivity() {
  const {
    data: auditResponse,
    isLoading,
    isError,
  } = useAuditLogs({
    limit: 5,
  });

  const activities = auditResponse?.data ?? [];

  const sortedActivities = [...activities]
    .sort(
      (a, b) =>
        new Date(b.performed_at).getTime() - new Date(a.performed_at).getTime(),
    )
    .slice(0, 4);

  return (
    <Card>
      <div>
        <h2 className="text-sm font-semibold text-zinc-200">Recent Activity</h2>

        <p className="mt-1 text-xs text-zinc-500">
          Latest events across the SentinelAI platform
        </p>
      </div>

      <div className="mt-5 space-y-5">
        {isLoading && (
          <div className="flex h-24 items-center justify-center text-sm text-zinc-500">
            Loading recent activity...
          </div>
        )}

        {isError && (
          <div className="flex h-24 items-center justify-center text-sm text-red-400">
            Unable to load recent activity.
          </div>
        )}

        {!isLoading && !isError && sortedActivities.length === 0 && (
          <div className="flex h-24 items-center justify-center rounded-lg border border-zinc-800/70 bg-zinc-950/40 text-sm text-zinc-500">
            No recent activity.
          </div>
        )}

        {!isLoading &&
          !isError &&
          sortedActivities.map((activity) => {
            const visual = getActivityIcon(activity.action);

            return (
              <ActivityItem
                key={activity.id}
                icon={visual.icon}
                iconClassName={visual.iconClassName}
                title={activity.action}
                description={
                  activity.details ??
                  `${activity.entity_type} #${activity.entity_id} · ${activity.source_module}`
                }
                time={getTimeAgo(activity.performed_at)}
              />
            );
          })}
      </div>
    </Card>
  );
}

export default RecentActivity;
