import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  getIncidents,
  resolveIncident,
  closeIncident,
  type IncidentFilters,
  type IncidentResolve,
} from "../api/incidents";

export function useIncidents(filters?: IncidentFilters) {
  return useQuery({
    queryKey: ["incidents", filters],
    queryFn: () => getIncidents(filters),
  });
}

export function useResolveIncident() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      incidentId,
      payload,
    }: {
      incidentId: number;
      payload: IncidentResolve;
    }) => resolveIncident(incidentId, payload),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["incidents"],
      });

      queryClient.invalidateQueries({
        queryKey: ["alerts"],
      });
    },
  });
}

export function useCloseIncident() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (incidentId: number) => closeIncident(incidentId),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["incidents"],
      });
    },
  });
}
