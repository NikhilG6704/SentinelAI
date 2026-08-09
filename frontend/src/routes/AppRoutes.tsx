import { Navigate, Route, Routes } from "react-router-dom";

import AppLayout from "../layouts/AppLayout";
import MetricsPage from "../pages/Metrics/MetricsPage";
import DashboardPage from "../components/dashboard/DashboardPage";
import InfrastructurePage from "../pages/Infrastructure/InfrastructurePage";
import AlertsPage from "../pages/Alerts/AlertsPage";
import IncidentsPage from "../pages/Incidents/IncidentsPage";
import RecoveryPage from "../pages/Recovery/RecoveryPage";
export default function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/infrastructure" element={<InfrastructurePage />} />
        <Route path="/metrics" element={<MetricsPage />} />
        <Route path="/alerts" element={<AlertsPage />} />
        <Route path="/incidents" element={<IncidentsPage />} />
        <Route path="/recovery" element={<RecoveryPage />} />
      </Route>

      <Route path="/" element={<Navigate to="/dashboard" replace />} />

      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
