import {
  FiArrowRight,
  FiGitBranch,
  FiShield,
  FiTrendingUp,
} from "react-icons/fi";

import {
  useDetectAnomaly,
  usePredictFailure,
  useRootCause,
  useRecommendation,
} from "../../hooks/useAI";
import { useIncidents } from "../../hooks/useIncidents";

import Badge from "../ui/Badge";
import Card from "../ui/Card";

function AIInsights() {
  const { data: incidentsResponse } = useIncidents({
    status: "Open",
  });

  const detectAnomalyMutation = useDetectAnomaly();
  const predictFailureMutation = usePredictFailure();
  const rootCauseMutation = useRootCause();
  const recommendationMutation = useRecommendation();

  const latestIncident = incidentsResponse?.data
    ?.slice()
    .sort(
      (a, b) =>
        new Date(b.detected_at).getTime() - new Date(a.detected_at).getTime(),
    )[0];

  const hasAgent =
    latestIncident?.monitoring_agent_id !== null &&
    latestIncident?.monitoring_agent_id !== undefined;

  const isAnalyzing =
    detectAnomalyMutation.isPending ||
    predictFailureMutation.isPending ||
    rootCauseMutation.isPending ||
    recommendationMutation.isPending;

  const handleAnalyze = () => {
    if (!latestIncident) {
      return;
    }

    if (hasAgent) {
      detectAnomalyMutation.mutate({
        monitoring_agent_id: latestIncident.monitoring_agent_id!,
      });
    }

    predictFailureMutation.mutate({
      infrastructure_asset_id: latestIncident.infrastructure_asset_id,
    });

    rootCauseMutation.mutate({
      incident_id: latestIncident.id,
    });

    recommendationMutation.mutate({
      incident_id: latestIncident.id,
    });
  };

  const anomaly = detectAnomalyMutation.data?.data;

  const prediction = predictFailureMutation.data?.data;

  const rootCause = rootCauseMutation.data?.data;

  const recommendation = recommendationMutation.data?.data;

  return (
    <Card>
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-sm font-semibold text-zinc-200">
              AI Intelligence
            </h2>

            <Badge variant="info">AI Gateway</Badge>
          </div>

          <p className="mt-1 text-xs text-zinc-500">
            AI analysis for the latest open incident
          </p>
        </div>

        <button
          type="button"
          onClick={handleAnalyze}
          disabled={!latestIncident || isAnalyzing}
          className="flex items-center gap-1.5 rounded-md border border-blue-500/20 bg-blue-500/5 px-3 py-1.5 text-xs font-medium text-blue-400 transition-colors hover:bg-blue-500/10 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isAnalyzing ? "Analyzing..." : "Analyze latest incident"}

          <FiArrowRight className="h-3.5 w-3.5" />
        </button>
      </div>

      {!latestIncident && (
        <div className="mt-5 flex min-h-32 items-center justify-center rounded-lg border border-zinc-800/70 bg-zinc-950/40">
          <p className="text-sm text-zinc-500">
            No open incident available for AI analysis.
          </p>
        </div>
      )}

      {latestIncident && (
        <>
          <div className="mt-4 rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-3">
            <p className="text-[11px] uppercase tracking-wider text-zinc-600">
              Analyzing incident
            </p>

            <p className="mt-1 truncate text-sm font-medium text-zinc-200">
              {latestIncident.incident_title}
            </p>

            <p className="mt-1 text-[11px] text-zinc-600">
              Asset #{latestIncident.infrastructure_asset_id}
            </p>
          </div>

          <div className="mt-5 grid grid-cols-1 gap-3 md:grid-cols-3">
            <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
              <div className="flex items-center justify-between">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-red-500/10">
                  <FiTrendingUp className="h-4 w-4 text-red-400" />
                </div>

                {anomaly && (
                  <Badge variant={anomaly.anomaly_detected ? "danger" : "info"}>
                    {anomaly.anomaly_detected ? "Detected" : "Normal"}
                  </Badge>
                )}
              </div>

              <p className="mt-4 text-xs font-medium text-zinc-500">
                Anomaly Detection
              </p>

              <p className="mt-1 text-lg font-semibold text-zinc-100">
                {anomaly ? `${Math.round(anomaly.anomaly_score * 100)}%` : "—"}
              </p>

              <p className="mt-1 text-[11px] text-zinc-600">
                {anomaly ? anomaly.message : "Run AI analysis to evaluate"}
              </p>
            </div>

            <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
              <div className="flex items-center justify-between">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-amber-500/10">
                  <FiTrendingUp className="h-4 w-4 text-amber-400" />
                </div>

                {prediction && <Badge variant="warning">Prediction</Badge>}
              </div>

              <p className="mt-4 text-xs font-medium text-zinc-500">
                Failure Prediction
              </p>

              <p className="mt-1 text-lg font-semibold text-zinc-100">
                {prediction
                  ? `${Math.round(prediction.confidence * 100)}%`
                  : "—"}
              </p>

              <p className="mt-1 truncate text-[11px] text-zinc-600">
                {prediction
                  ? prediction.prediction
                  : "Run AI analysis to evaluate"}
              </p>
            </div>

            <div className="rounded-lg border border-zinc-800/70 bg-zinc-950/40 p-4">
              <div className="flex items-center justify-between">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-500/10">
                  <FiGitBranch className="h-4 w-4 text-blue-400" />
                </div>

                {rootCause && (
                  <Badge variant="info">
                    {Math.round(rootCause.confidence * 100)}%
                  </Badge>
                )}
              </div>

              <p className="mt-4 text-xs font-medium text-zinc-500">
                Probable Root Cause
              </p>

              <p className="mt-1 truncate text-sm font-semibold text-zinc-100">
                {rootCause?.probable_cause ?? "—"}
              </p>

              <p className="mt-1 truncate text-[11px] text-zinc-600">
                {rootCause?.recommendation ?? "Run AI analysis to evaluate"}
              </p>
            </div>
          </div>

          <div className="mt-4 flex items-center justify-between gap-4 rounded-lg border border-blue-500/10 bg-blue-500/[0.03] p-4">
            <div className="flex min-w-0 items-center gap-3">
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-blue-500/10">
                <FiShield className="h-4 w-4 text-blue-400" />
              </div>

              <div className="min-w-0">
                <p className="text-xs font-medium text-zinc-400">
                  Recommended Action
                </p>

                <p className="mt-1 truncate text-sm font-semibold text-zinc-100">
                  {recommendation?.recommended_action ?? "—"}
                </p>
              </div>
            </div>

            {recommendation && (
              <div className="hidden max-w-xs text-right sm:block">
                <p className="text-xs text-zinc-500">Priority</p>

                <p className="mt-1 text-sm font-semibold text-emerald-400">
                  {recommendation.priority}
                </p>
              </div>
            )}
          </div>
        </>
      )}
    </Card>
  );
}

export default AIInsights;
