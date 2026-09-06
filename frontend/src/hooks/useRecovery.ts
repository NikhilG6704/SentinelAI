import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  getRecoveryWorkflows,
  getRecoveryWorkflow,
  createRecoveryWorkflow,
  executeRecoveryWorkflow,
  cancelRecoveryWorkflow,
  deleteRecoveryWorkflow,
  type RecoveryWorkflowCreate,
  type RecoveryWorkflowFilters,
} from "../api/recovery";

export function useRecoveryWorkflows(filters?: RecoveryWorkflowFilters) {
  return useQuery({
    queryKey: ["recovery", "workflows", filters],
    queryFn: () => getRecoveryWorkflows(filters),
    refetchInterval: 15_000,
  });
}

export function useRecoveryWorkflow(workflowId: number) {
  return useQuery({
    queryKey: ["recovery", "workflow", workflowId],
    queryFn: () => getRecoveryWorkflow(workflowId),
    enabled: Number.isInteger(workflowId) && workflowId > 0,
    refetchInterval: 15_000,
  });
}

export function useExecuteRecoveryWorkflow() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (workflowId: number) => executeRecoveryWorkflow(workflowId),

    onSuccess: (_, workflowId) => {
      queryClient.invalidateQueries({
        queryKey: ["recovery", "workflows"],
      });

      queryClient.invalidateQueries({
        queryKey: ["recovery", "workflow", workflowId],
      });
    },
  });
}

export function useCancelRecoveryWorkflow() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (workflowId: number) => cancelRecoveryWorkflow(workflowId),

    onSuccess: (_, workflowId) => {
      queryClient.invalidateQueries({
        queryKey: ["recovery", "workflows"],
      });

      queryClient.invalidateQueries({
        queryKey: ["recovery", "workflow", workflowId],
      });
    },
  });
}

export function useDeleteRecoveryWorkflow() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (workflowId: number) => deleteRecoveryWorkflow(workflowId),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["recovery", "workflows"],
      });
    },
  });
}

export function useCreateRecoveryWorkflow() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: RecoveryWorkflowCreate) =>
      createRecoveryWorkflow(payload),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["recovery", "workflows"],
      });
    },
  });
}
