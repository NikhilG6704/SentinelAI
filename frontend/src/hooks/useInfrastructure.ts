import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  getInfrastructureAssets,
  getInfrastructureAsset,
  createInfrastructureAsset,
  updateInfrastructureAsset,
  deleteInfrastructureAsset,
  type InfrastructureAssetCreate,
  type InfrastructureAssetUpdate,
} from "../api/infrastructure";

export function useInfrastructureAssets() {
  return useQuery({
    queryKey: ["infrastructure", "assets"],
    queryFn: getInfrastructureAssets,
  });
}

export function useInfrastructureAsset(assetId: number) {
  return useQuery({
    queryKey: ["infrastructure", "asset", assetId],
    queryFn: () => getInfrastructureAsset(assetId),
    enabled: Number.isInteger(assetId) && assetId > 0,
  });
}

export function useCreateInfrastructureAsset() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: InfrastructureAssetCreate) =>
      createInfrastructureAsset(payload),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["infrastructure", "assets"],
      });
    },
  });
}

export function useUpdateInfrastructureAsset() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      assetId,
      payload,
    }: {
      assetId: number;
      payload: InfrastructureAssetUpdate;
    }) => updateInfrastructureAsset(assetId, payload),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["infrastructure", "assets"],
      });

      queryClient.invalidateQueries({
        queryKey: ["infrastructure", "asset", variables.assetId],
      });
    },
  });
}

export function useDeleteInfrastructureAsset() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (assetId: number) => deleteInfrastructureAsset(assetId),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["infrastructure", "assets"],
      });
    },
  });
}
