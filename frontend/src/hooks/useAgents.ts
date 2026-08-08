import { useQuery } from "@tanstack/react-query";

import { getAgents, getAgent, getAgentsByAsset } from "../api/agents";

export function useAgents() {
  return useQuery({
    queryKey: ["agents"],
    queryFn: getAgents,
    refetchInterval: 30_000,
  });
}

export function useAgent(agentId: number) {
  return useQuery({
    queryKey: ["agents", "agent", agentId],
    queryFn: () => getAgent(agentId),
    enabled: Number.isInteger(agentId) && agentId > 0,
    refetchInterval: 30_000,
  });
}

export function useAgentsByAsset(assetId: number) {
  return useQuery({
    queryKey: ["agents", "asset", assetId],
    queryFn: () => getAgentsByAsset(assetId),
    enabled: Number.isInteger(assetId) && assetId > 0,
    refetchInterval: 30_000,
  });
}
