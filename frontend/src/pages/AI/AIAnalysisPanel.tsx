import { useState } from "react";

import {
  FiAlertTriangle,
  FiGitBranch,
  FiLoader,
  FiShield,
  FiTrendingUp,
} from "react-icons/fi";

import {
  analyzeRootCause,
  detectAnomaly,
  getRecommendation,
  predictFailure,
} from "../../api/ai";

import type {
  DetectAnomalyResponse,
  PredictFailureResponse,
  RecommendationResponse,
  RootCauseResponse,
} from "../../api/ai";

import AIInsightCard from "./AIInsightCard";

interface AIAnalysisPanelProps {
  incidentId: number | null;
  infrastructureAssetId: number | null;
  monitoringAgentId: number | null;
}

function AIAnalysisPanel({
  incidentId,
  infrastructureAssetId,
  monitoringAgentId,
}: AIAnalysisPanelProps) {
  const [isLoading, setIsLoading] = useState(false);

  const [failurePrediction, setFailurePrediction] =
    useState<PredictFailureResponse | null>(null);

  const [anomaly, setAnomaly] = useState<DetectAnomalyResponse | null>(null);

  const [rootCause, setRootCause] = useState<RootCauseResponse | null>(null);

  const [recommendation, setRecommendation] =
    useState<RecommendationResponse | null>(null);

  const [error, setError] = useState<string | null>(null);

  const canAnalyze = incidentId !== null && infrastructureAssetId !== null;

  const runAnalysis = async () => {
    if (!canAnalyze || incidentId === null) {
      return;
    }

    setIsLoading(true);
    setError(null);

    setFailurePrediction(null);
    setAnomaly(null);
    setRootCause(null);
    setRecommendation(null);

    try {
      const analysisRequests: Promise<unknown>[] = [
        predictFailure({
          infrastructure_asset_id: infrastructureAssetId,
        }),

        analyzeRootCause({
          incident_id: incidentId,
        }),

        getRecommendation({
          incident_id: incidentId,
        }),
      ];

      if (monitoringAgentId !== null) {
        analysisRequests.push(
          detectAnomaly({
            monitoring_agent_id: monitoringAgentId,
          }),
        );
      }

      const results = await Promise.allSettled(analysisRequests);

      const [
        failureResult,
        rootCauseResult,
        recommendationResult,
        anomalyResult,
      ] = results;

      if (failureResult?.status === "fulfilled") {
        setFailurePrediction(
          (failureResult.value as { data: PredictFailureResponse }).data,
        );
      }

      if (rootCauseResult?.status === "fulfilled") {
        setRootCause(
          (rootCauseResult.value as { data: RootCauseResponse }).data,
        );
      }

      if (recommendationResult?.status === "fulfilled") {
        setRecommendation(
          (
            recommendationResult.value as {
              data: RecommendationResponse;
            }
          ).data,
        );
      }

      if (anomalyResult && anomalyResult.status === "fulfilled") {
        setAnomaly(
          (anomalyResult.value as { data: DetectAnomalyResponse }).data,
        );
      }

      const hasSuccessfulResult = results.some(
        (result) => result.status === "fulfilled",
      );

      if (!hasSuccessfulResult) {
        setError("Unable to complete AI analysis. Please try again.");
      }
    } catch (err) {
      console.error(err);

      setError("Unable to complete AI analysis. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-5">
      <div className="rounded-xl border border-zinc-800/80 bg-zinc-900/40 p-5">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-sm font-semibold text-zinc-200">AI Analysis</h2>

            <p className="mt-1 text-xs text-zinc-500">
              Run anomaly detection, failure prediction, root cause analysis,
              and remediation recommendation.
            </p>
          </div>

          <button
            type="button"
            onClick={runAnalysis}
            disabled={!canAnalyze || isLoading}
            className="flex h-10 items-center justify-center gap-2 rounded-lg bg-blue-500 px-4 text-xs font-semibold text-white transition-colors hover:bg-blue-400 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {isLoading && <FiLoader className="h-3.5 w-3.5 animate-spin" />}

            {isLoading ? "Analyzing..." : "Run AI Analysis"}
          </button>
        </div>

        {!canAnalyze && (
          <p className="mt-4 text-xs text-zinc-600">
            Select an incident with an associated infrastructure asset before
            running analysis.
          </p>
        )}

        {incidentId !== null &&
          infrastructureAssetId !== null &&
          monitoringAgentId === null && (
            <p className="mt-3 text-xs text-amber-400">
              No monitoring agent is assigned to this incident. Anomaly
              detection will be skipped.
            </p>
          )}

        {error && (
          <div className="mt-4 rounded-lg border border-red-500/20 bg-red-500/5 p-3">
            <p className="text-xs text-red-400">{error}</p>
          </div>
        )}
      </div>

      {(failurePrediction || anomaly || rootCause || recommendation) && (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          {anomaly && (
            <AIInsightCard
              title="Anomaly Detection"
              value={`${anomaly.anomaly_score.toFixed(1)}%`}
              description={anomaly.message}
              icon={<FiAlertTriangle className="h-4 w-4 text-red-400" />}
            />
          )}

          {failurePrediction && (
            <AIInsightCard
              title="Failure Prediction"
              value={`${failurePrediction.confidence.toFixed(1)}%`}
              description={failurePrediction.explanation}
              icon={<FiTrendingUp className="h-4 w-4 text-amber-400" />}
            />
          )}

          {rootCause && (
            <AIInsightCard
              title="Probable Root Cause"
              value={rootCause.probable_cause}
              description={rootCause.recommendation}
              icon={<FiGitBranch className="h-4 w-4 text-blue-400" />}
            />
          )}

          {recommendation && (
            <AIInsightCard
              title="Recommended Action"
              value={recommendation.recommended_action}
              description={recommendation.explanation}
              icon={<FiShield className="h-4 w-4 text-emerald-400" />}
            />
          )}
        </div>
      )}
    </div>
  );
}

export default AIAnalysisPanel;
