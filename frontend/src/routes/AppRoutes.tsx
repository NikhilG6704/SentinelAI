import { Navigate, Route, Routes } from "react-router-dom";

import AppLayout from "../layouts/AppLayout";
import MetricsPage from "../pages/Metrics/MetricsPage";
import DashboardPage from "../components/dashboard/DashboardPage";
import InfrastructurePage from "../pages/Infrastructure/InfrastructurePage";
import AlertsPage from "../pages/Alerts/AlertsPage";
import IncidentsPage from "../pages/Incidents/IncidentsPage";
import RecoveryPage from "../pages/Recovery/RecoveryPage";
import AIPage from "../pages/AI/AIPage";
import SelfHealingPage from "../pages/SelfHealing/SelfHealingPage";
import AgentsPage from "../pages/Agents/AgentsPage";
import LogsPage from "../pages/Logs/LogsPage";

export default function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/infrastructure" element={<InfrastructurePage />} />
        <Route path="/infrastructure/agents" element={<AgentsPage />} />
        <Route path="/metrics" element={<MetricsPage />} />
        <Route path="/logs" element={<LogsPage />} />
        <Route path="/alerts" element={<AlertsPage />} />
        <Route path="/incidents" element={<IncidentsPage />} />
        <Route path="/recovery" element={<RecoveryPage />} />
        <Route path="/ai" element={<AIPage />} />
        <Route path="/ai/anomalies" element={<AIPage />} />
        <Route path="/ai/predictions" element={<AIPage />} />
        <Route path="/ai/root-cause" element={<AIPage />} />
        <Route path="/ai/recommendations" element={<AIPage />} />
        <Route path="/self-healing" element={<SelfHealingPage />} />
      </Route>

      <Route path="/" element={<Navigate to="/dashboard" replace />} />

      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
