import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import SelfHealingPage from "../SelfHealingPage";

// Mock subcomponents
vi.mock("../ActionSummary", () => ({ default: () => <div data-testid="action-summary" /> }));
vi.mock("../ActionTable", () => ({ default: () => <div data-testid="action-table" /> }));
vi.mock("../ActionDetails", () => ({ default: () => <div data-testid="action-details" /> }));

const mockUseRecoveryWorkflows = vi.fn();
vi.mock("../../../hooks/useRecovery", () => ({
  useRecoveryWorkflows: () => mockUseRecoveryWorkflows(),
}));

function renderPage() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <SelfHealingPage />
    </QueryClientProvider>
  );
}

describe("SelfHealingPage", () => {
  it("renders loading state", () => {
    mockUseRecoveryWorkflows.mockReturnValue({
      data: undefined,
      isLoading: true,
      isError: false,
    });

    renderPage();
    expect(screen.getByText("Loading recovery workflows...")).toBeInTheDocument();
  });

  it("renders error state", () => {
    mockUseRecoveryWorkflows.mockReturnValue({
      data: undefined,
      isLoading: false,
      isError: true,
    });

    renderPage();
    expect(screen.getByText("Unable to load recovery workflows.")).toBeInTheDocument();
  });

  it("renders successful state with workflows", () => {
    mockUseRecoveryWorkflows.mockReturnValue({
      data: {
        data: [{ id: 1, workflow_name: "Test" }],
      },
      isLoading: false,
      isError: false,
    });

    renderPage();

    expect(screen.getByText("Self-Healing")).toBeInTheDocument();
    expect(screen.getByText("Simulation Mode")).toBeInTheDocument();

    expect(screen.getByTestId("action-summary")).toBeInTheDocument();
    expect(screen.getByTestId("action-table")).toBeInTheDocument();
    expect(screen.getByTestId("action-details")).toBeInTheDocument();
  });
});
