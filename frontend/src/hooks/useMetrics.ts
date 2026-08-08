import { useQuery } from "@tanstack/react-query";

import { getMetrics, getMetric, getMetricsByAgent } from "../api/metrics";

export function useMetrics() {
  return useQuery({
    queryKey: ["metrics"],
    queryFn: getMetrics,
    refetchInterval: 30_000,
  });
}

export function useMetric(metricId: number) {
  return useQuery({
    queryKey: ["metrics", "metric", metricId],
    queryFn: () => getMetric(metricId),
    enabled: Number.isInteger(metricId) && metricId > 0,
  });
}

export function useMetricsByAgent(agentId: number) {
  return useQuery({
    queryKey: ["metrics", "agent", agentId],
    queryFn: () => getMetricsByAgent(agentId),
    enabled: Number.isInteger(agentId) && agentId > 0,
    refetchInterval: 30_000,
  });
}
