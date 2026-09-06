import { useQuery } from "@tanstack/react-query";
import { getMetricsByAgent } from "../api/metrics";
import type { SystemMetric } from "../api/metrics";
import { getAgentsByAsset } from "../api/agents";

/** Polls the latest metric snapshot for a given monitoring agent every 3s */
export function useAgentLatestMetric(agentId: number) {
  return useQuery({
    queryKey: ["metrics", "agent", "live", agentId],
    queryFn: async (): Promise<SystemMetric | null> => {
      const res = await getMetricsByAgent(agentId);
      const metrics = res.data ?? [];
      if (!metrics.length) return null;
      // Return the most recently collected metric
      return metrics.reduce((latest, m) =>
        new Date(m.collection_timestamp) > new Date(latest.collection_timestamp)
          ? m
          : latest
      );
    },
    enabled: agentId > 0,
    refetchInterval: 3_000,
  });
}

/** Fetches all agents for a given asset, then returns the first one's id */
export function useAssetAgentId(assetId: number) {
  return useQuery({
    queryKey: ["agents", "by-asset", assetId],
    queryFn: async (): Promise<number | null> => {
      const res = await getAgentsByAsset(assetId);
      const agents = res.data ?? [];
      return agents.length > 0 ? agents[0].id : null;
    },
    enabled: assetId > 0,
  });
}
