import apiClient from "./client";
import type { ApiResponse } from "../types/api";

export type AssetType =
  | "Server"
  | "VM"
  | "Container"
  | "Network"
  | "Database"
  | "Other";

export type EnvironmentType =
  | "Production"
  | "Staging"
  | "Development"
  | "Testing";

export type AssetStatus = "Healthy" | "Warning" | "Critical" | "Offline";

export interface InfrastructureAsset {
  id: number;
  hostname: string;
  ip_address: string;
  operating_system: string;
  asset_type: AssetType;
  environment: EnvironmentType;
  status: AssetStatus;
  location: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface InfrastructureAssetCreate {
  hostname: string;
  ip_address: string;
  operating_system: string;
  asset_type: AssetType;
  environment: EnvironmentType;
  status?: AssetStatus;
  location: string;
  description?: string | null;
}

export interface InfrastructureAssetUpdate {
  hostname?: string | null;
  ip_address?: string | null;
  operating_system?: string | null;
  asset_type?: AssetType | null;
  environment?: EnvironmentType | null;
  status?: AssetStatus | null;
  location?: string | null;
  description?: string | null;
  is_active?: boolean | null;
}

export async function getInfrastructureAssets(): Promise<
  ApiResponse<InfrastructureAsset[]>
> {
  const response = await apiClient.get<ApiResponse<InfrastructureAsset[]>>(
    "/infrastructure-assets",
  );

  return response.data;
}

export async function getInfrastructureAsset(
  assetId: number,
): Promise<ApiResponse<InfrastructureAsset>> {
  const response = await apiClient.get<ApiResponse<InfrastructureAsset>>(
    `/infrastructure-assets/${assetId}`,
  );

  return response.data;
}

export async function createInfrastructureAsset(
  payload: InfrastructureAssetCreate,
): Promise<ApiResponse<InfrastructureAsset>> {
  const response = await apiClient.post<ApiResponse<InfrastructureAsset>>(
    "/infrastructure-assets",
    payload,
  );

  return response.data;
}

export async function updateInfrastructureAsset(
  assetId: number,
  payload: InfrastructureAssetUpdate,
): Promise<ApiResponse<InfrastructureAsset>> {
  const response = await apiClient.put<ApiResponse<InfrastructureAsset>>(
    `/infrastructure-assets/${assetId}`,
    payload,
  );

  return response.data;
}

export async function deleteInfrastructureAsset(
  assetId: number,
): Promise<ApiResponse<InfrastructureAsset>> {
  const response = await apiClient.delete<ApiResponse<InfrastructureAsset>>(
    `/infrastructure-assets/${assetId}`,
  );

  return response.data;
}
