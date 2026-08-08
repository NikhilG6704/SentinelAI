import { useQuery } from "@tanstack/react-query";

import { getReports, getReport, type ReportFilters } from "../api/reports";

export function useReports(filters?: ReportFilters) {
  return useQuery({
    queryKey: ["reports", filters],
    queryFn: () => getReports(filters),
  });
}

export function useReport(reportId: number) {
  return useQuery({
    queryKey: ["reports", "report", reportId],
    queryFn: () => getReport(reportId),
    enabled: Number.isInteger(reportId) && reportId > 0,
  });
}
