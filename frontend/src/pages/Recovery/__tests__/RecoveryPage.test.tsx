import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import RecoveryPage from "../RecoveryPage";

// Mock subcomponents
vi.mock("../RecoverySummary", () => ({ default: () => <div data-testid="recovery-summary" /> }));
vi.mock("../RecoveryFilters", () => ({ default: () => <div data-testid="recovery-filters" /> }));
vi.mock("../RecoveryTable", () => ({ default: () => <div data-testid="recovery-table" /> }));
vi.mock("../RecoveryDetails", () => ({ default: () => <div data-testid="recovery-details" /> }));
vi.mock("../RecoveryCreateForm", () => ({ default: ({ onClose }: any) => <div data-testid="recovery-create-form"><button onClick={onClose}>Close Form</button></div> }));

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
      <RecoveryPage />
    </QueryClientProvider>
  );
}

describe("RecoveryPage", () => {
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

    expect(screen.getByText("Recovery")).toBeInTheDocument();

    expect(screen.getByTestId("recovery-summary")).toBeInTheDocument();
    expect(screen.getByTestId("recovery-filters")).toBeInTheDocument();
    expect(screen.getByTestId("recovery-table")).toBeInTheDocument();
    expect(screen.getByTestId("recovery-details")).toBeInTheDocument();
  });
});
