import { useQuery } from "@tanstack/react-query";

import { getAuditLogs, getAuditLog, type AuditLogFilters } from "../api/audit";

export function useAuditLogs(filters?: AuditLogFilters) {
  return useQuery({
    queryKey: ["audit", "logs", filters],
    queryFn: () => getAuditLogs(filters),
  });
}

export function useAuditLog(auditLogId: number) {
  return useQuery({
    queryKey: ["audit", "log", auditLogId],
    queryFn: () => getAuditLog(auditLogId),
    enabled: Number.isInteger(auditLogId) && auditLogId > 0,
  });
}
