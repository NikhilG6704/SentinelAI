import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  getAlerts,
  acknowledgeAlert,
  resolveAlert,
  type AlertFilters,
  type AlertResolve,
} from "../api/alerts";

export function useAlerts(filters?: AlertFilters) {
  return useQuery({
    queryKey: ["alerts", filters],
    queryFn: () => getAlerts(filters),
    refetchInterval: 15_000,
  });
}

export function useAcknowledgeAlert() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (alertId: number) => acknowledgeAlert(alertId),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["alerts"],
      });
    },
  });
}

export function useResolveAlert() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      alertId,
      payload,
    }: {
      alertId: number;
      payload: AlertResolve;
    }) => resolveAlert(alertId, payload),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["alerts"],
      });
    },
  });
}
