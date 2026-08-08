import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  getAutomationRules,
  getAutomationRule,
  createAutomationRule,
  updateAutomationRule,
  deleteAutomationRule,
  enableAutomationRule,
  disableAutomationRule,
  type AutomationRuleCreate,
  type AutomationRuleUpdate,
} from "../api/automation";

export function useAutomationRules() {
  return useQuery({
    queryKey: ["automation", "rules"],
    queryFn: getAutomationRules,
  });
}

export function useAutomationRule(ruleId: number) {
  return useQuery({
    queryKey: ["automation", "rule", ruleId],
    queryFn: () => getAutomationRule(ruleId),
    enabled: Number.isInteger(ruleId) && ruleId > 0,
  });
}

export function useCreateAutomationRule() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: AutomationRuleCreate) =>
      createAutomationRule(payload),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["automation", "rules"],
      });
    },
  });
}

export function useUpdateAutomationRule() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      ruleId,
      payload,
    }: {
      ruleId: number;
      payload: AutomationRuleUpdate;
    }) => updateAutomationRule(ruleId, payload),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["automation", "rules"],
      });

      queryClient.invalidateQueries({
        queryKey: ["automation", "rule", variables.ruleId],
      });
    },
  });
}

export function useDeleteAutomationRule() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (ruleId: number) => deleteAutomationRule(ruleId),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["automation", "rules"],
      });
    },
  });
}

export function useEnableAutomationRule() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (ruleId: number) => enableAutomationRule(ruleId),

    onSuccess: (_, ruleId) => {
      queryClient.invalidateQueries({
        queryKey: ["automation", "rules"],
      });

      queryClient.invalidateQueries({
        queryKey: ["automation", "rule", ruleId],
      });
    },
  });
}

export function useDisableAutomationRule() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (ruleId: number) => disableAutomationRule(ruleId),

    onSuccess: (_, ruleId) => {
      queryClient.invalidateQueries({
        queryKey: ["automation", "rules"],
      });

      queryClient.invalidateQueries({
        queryKey: ["automation", "rule", ruleId],
      });
    },
  });
}
