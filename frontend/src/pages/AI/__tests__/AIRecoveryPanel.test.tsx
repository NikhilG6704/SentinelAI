import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import AIRecoveryPanel from "../AIRecoveryPanel";

// ---------------------------------------------------------------------------
// Mock hooks that reach out to the network
// ---------------------------------------------------------------------------

const mockCreateMutateAsync = vi.fn();
const mockExecuteMutateAsync = vi.fn();

vi.mock("../../../hooks/useAutomation", () => ({
  useAutomationRules: () => ({
    data: {
      data: [
        { id: 1, rule_name: "High CPU Rule" },
        { id: 2, rule_name: "Memory Threshold Rule" },
      ],
    },
    isLoading: false,
  }),
}));

vi.mock("../../../hooks/useRecovery", () => ({
  useCreateRecoveryWorkflow: () => ({
    mutateAsync: mockCreateMutateAsync,
    isPending: false,
  }),
  useExecuteRecoveryWorkflow: () => ({
    mutateAsync: mockExecuteMutateAsync,
    isPending: false,
  }),
  useRecoveryWorkflow: () => ({
    data: undefined,
  }),
}));

// ---------------------------------------------------------------------------
// Test helpers
// ---------------------------------------------------------------------------

function makeClient() {
  return new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
}

function renderPanel(overrides = {}) {
  const defaultProps = {
    incidentId: 42,
    infrastructureAssetId: 7,
    recommendation: {
      recommended_action: "Restart Application Service",
      priority: "High",
      explanation: "Service is unresponsive due to high memory pressure.",
    },
    rootCause: {
      probable_cause: "Memory leak in worker process",
      confidence: 0.91,
      recommendation: "Restart the worker service to recover memory.",
    },
    ...overrides,
  };

  return render(
    <QueryClientProvider client={makeClient()}>
      <AIRecoveryPanel {...defaultProps} />
    </QueryClientProvider>,
  );
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe("AIRecoveryPanel", () => {
  beforeEach(() => {
    mockCreateMutateAsync.mockReset();
    mockExecuteMutateAsync.mockReset();
  });

  it("renders the recovery plan header", () => {
    renderPanel();

    expect(screen.getByText("Recovery Plan")).toBeInTheDocument();
    expect(screen.getByText("Simulation Mode")).toBeInTheDocument();
  });

  it("renders the AI analysis summary from props", () => {
    renderPanel();

    expect(
      screen.getByText("Restart Application Service"),
    ).toBeInTheDocument();
    expect(screen.getByText("High")).toBeInTheDocument();
    expect(screen.getByText("Memory leak in worker process")).toBeInTheDocument();
  });

  it("pre-fills workflow name from recommendation", () => {
    renderPanel();

    const input = screen.getByDisplayValue(
      "AI Recovery — Restart Application Service",
    );

    expect(input).toBeInTheDocument();
  });

  it("infers RESTART_SERVICE action type for a service recommendation", () => {
    renderPanel();

    const select = screen.getByDisplayValue("Restart Service");

    expect(select).toBeInTheDocument();
  });

  it("infers RESTART_CONTAINER for a container recommendation", () => {
    renderPanel({
      recommendation: {
        recommended_action: "Restart container pod",
        priority: "Medium",
        explanation: "Container is in CrashLoopBackOff.",
      },
    });

    expect(screen.getByDisplayValue("Restart Container")).toBeInTheDocument();
  });

  it("lists automation rules in the dropdown", () => {
    renderPanel();

    expect(screen.getByText("#1 — High CPU Rule")).toBeInTheDocument();
    expect(screen.getByText("#2 — Memory Threshold Rule")).toBeInTheDocument();
  });

  it("Create Recovery Plan button is disabled when no rule is selected", () => {
    renderPanel();

    const btn = screen.getByRole("button", { name: /create recovery plan/i });
    expect(btn).toBeDisabled();
  });

  it("Create Recovery Plan button is enabled after selecting a rule", () => {
    renderPanel();

    const ruleSelect = screen.getAllByRole("combobox")[1];

    fireEvent.change(ruleSelect, { target: { value: "1" } });

    const btn = screen.getByRole("button", { name: /create recovery plan/i });

    expect(btn).not.toBeDisabled();
  });

  it("calls createRecoveryWorkflow with correct payload on submit", async () => {
    mockCreateMutateAsync.mockResolvedValue({
      data: {
        id: 99,
        workflow_name: "AI Recovery — Restart Application Service",
        action_type: "RESTART_SERVICE",
        execution_status: "Pending",
        execution_mode: "Simulation",
        automation_rule_id: 1,
        incident_id: 42,
        infrastructure_asset_id: 7,
        executed_by: "ai-gateway",
        execution_log: null,
        started_at: null,
        completed_at: null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    });

    renderPanel();

    // Select automation rule
    const ruleSelect = screen.getAllByRole("combobox")[1];
    fireEvent.change(ruleSelect, { target: { value: "1" } });

    // Submit
    fireEvent.click(screen.getByRole("button", { name: /create recovery plan/i }));

    await waitFor(() => {
      expect(mockCreateMutateAsync).toHaveBeenCalledWith(
        expect.objectContaining({
          incident_id: 42,
          infrastructure_asset_id: 7,
          automation_rule_id: 1,
          action_type: "RESTART_SERVICE",
          executed_by: "ai-gateway",
        }),
      );
    });
  });

  it("shows an error message when workflow creation fails", async () => {
    mockCreateMutateAsync.mockRejectedValue({
      response: {
        data: { error: { message: "Automation rule not found." } },
      },
    });

    renderPanel();

    const ruleSelect = screen.getAllByRole("combobox")[1];
    fireEvent.change(ruleSelect, { target: { value: "1" } });

    fireEvent.click(screen.getByRole("button", { name: /create recovery plan/i }));

    await waitFor(() => {
      expect(
        screen.getByText("Automation rule not found."),
      ).toBeInTheDocument();
    });
  });

  it("shows fallback error message when creation fails without structured response", async () => {
    mockCreateMutateAsync.mockRejectedValue(new Error("Network error"));

    renderPanel();

    const ruleSelect = screen.getAllByRole("combobox")[1];
    fireEvent.change(ruleSelect, { target: { value: "1" } });

    fireEvent.click(screen.getByRole("button", { name: /create recovery plan/i }));

    await waitFor(() => {
      expect(
        screen.getByText("Unable to create recovery workflow."),
      ).toBeInTheDocument();
    });
  });

  it("renders without rootCause prop (optional)", () => {
    renderPanel({ rootCause: null });

    // Should still render without crashing
    expect(screen.getByText("Recovery Plan")).toBeInTheDocument();
    // Root cause section should not appear
    expect(
      screen.queryByText("Memory leak in worker process"),
    ).not.toBeInTheDocument();
  });
});
