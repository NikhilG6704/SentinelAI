import { useQuery } from "@tanstack/react-query";

import { getDashboardOverview } from "../api/dashboard";

export function useDashboardOverview() {
  return useQuery({
    queryKey: ["dashboard", "overview"],
    queryFn: getDashboardOverview,
    refetchInterval: 30_000,
  });
}
