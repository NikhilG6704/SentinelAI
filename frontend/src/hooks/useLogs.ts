import { useQuery } from "@tanstack/react-query";

import { getLogs, getLog, type LogFilters } from "../api/logs";

export function useLogs(filters?: LogFilters) {
  return useQuery({
    queryKey: ["logs", filters],
    queryFn: () => getLogs(filters),
  });
}

export function useLog(logId: number) {
  return useQuery({
    queryKey: ["logs", "log", logId],
    queryFn: () => getLog(logId),
    enabled: Number.isInteger(logId) && logId > 0,
  });
}
