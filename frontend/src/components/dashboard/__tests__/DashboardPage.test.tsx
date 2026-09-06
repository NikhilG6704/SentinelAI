import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import DashboardPage from "../DashboardPage";

// Mock out all the sub-components to keep the test focused on the main page layout and data passing
vi.mock("../ActiveIncidents", () => ({ default: () => <div data-testid="active-incidents" /> }));
vi.mock("../AIInsights", () => ({ default: () => <div data-testid="ai-insights" /> }));
vi.mock("../HealthScore", () => ({ default: () => <div data-testid="health-score" /> }));
vi.mock("../InfrastructureOverview", () => ({ default: () => <div data-testid="infrastructure-overview" /> }));
vi.mock("../RecentActivity", () => ({ default: () => <div data-testid="recent-activity" /> }));
vi.mock("../ResourceOverview", () => ({ default: () => <div data-testid="resource-overview" /> }));

// Mock the hook
vi.mock("../../../hooks/useDashboard", () => ({
  useDashboardOverview: () => ({
    data: {
      data: {
        total_assets: 150,
        healthy_assets: 140,
        warning_assets: 8,
        critical_assets: 2,
        total_agents: 150,
        online_agents: 148,
        offline_agents: 2,
        total_metrics: 50000,
      }
    },
    isLoading: false
  })
}));

function renderDashboard() {
  const queryClient = new QueryClient();
  return render(
    <QueryClientProvider client={queryClient}>
      <DashboardPage />
    </QueryClientProvider>
  );
}

describe("DashboardPage", () => {
  it("renders the dashboard header", () => {
    renderDashboard();
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByText(/Real-time infrastructure health/i)).toBeInTheDocument();
  });

  it("renders the KPI grid with data from useDashboardOverview", () => {
    renderDashboard();
    
    // We can't rely on exact label matching without complex queries because the metric card uses small labels, but we can look for the numbers.
    expect(screen.getByText("150")).toBeInTheDocument(); // Total Assets
    expect(screen.getByText("148")).toBeInTheDocument(); // Online Agents
    expect(screen.getByText("140")).toBeInTheDocument(); // Healthy Assets
    expect(screen.getByText("2")).toBeInTheDocument();   // Offline Agents
    expect(screen.getByText("50000")).toBeInTheDocument(); // Collected Metrics
  });

  it("renders the mocked sub-components", () => {
    renderDashboard();
    
    expect(screen.getByTestId("active-incidents")).toBeInTheDocument();
    expect(screen.getByTestId("ai-insights")).toBeInTheDocument();
    expect(screen.getByTestId("health-score")).toBeInTheDocument();
    expect(screen.getByTestId("infrastructure-overview")).toBeInTheDocument();
    expect(screen.getByTestId("recent-activity")).toBeInTheDocument();
    expect(screen.getByTestId("resource-overview")).toBeInTheDocument();
  });
});
