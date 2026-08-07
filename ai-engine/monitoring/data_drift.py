"""
Data drift detection for SentinelAI.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.spatial.distance import jensenshannon
from scipy.stats import ks_2samp

from monitoring.configuration import monitoring_config
from utils.logger import logger


@dataclass(frozen=True)
class DriftResult:
    """
    Result of a drift analysis.
    """

    psi: float
    js_distance: float
    ks_statistic: float
    ks_pvalue: float

    psi_drift: bool
    js_drift: bool
    ks_drift: bool

    @property
    def drift_detected(self) -> bool:
        return (
            self.psi_drift
            or self.js_drift
            or self.ks_drift
        )


class DataDriftDetector:
    """
    Detects feature distribution drift.
    """

    # --------------------------------------------------------------
    # Public API
    # --------------------------------------------------------------

    def detect(
        self,
        reference: np.ndarray,
        current: np.ndarray,
        *,
        bins: int = 10,
    ) -> DriftResult:

        reference = np.asarray(reference)
        current = np.asarray(current)

        psi = self.population_stability_index(
            reference,
            current,
            bins=bins,
        )

        js = self.jensen_shannon_distance(
            reference,
            current,
            bins=bins,
        )

        ks = ks_2samp(
            reference,
            current,
        )

        result = DriftResult(
            psi=psi,
            js_distance=js,
            ks_statistic=ks.statistic,
            ks_pvalue=ks.pvalue,
            psi_drift=bool(
                psi >= monitoring_config.psi_threshold
            ),
            js_drift=bool(
                js >= monitoring_config.js_threshold
            ),
            ks_drift=bool(
                ks.pvalue < monitoring_config.ks_threshold
            ),
        )

        logger.info(
            f"Drift detected={result.drift_detected}"
        )

        return result

    # --------------------------------------------------------------
    # PSI
    # --------------------------------------------------------------

    @staticmethod
    def population_stability_index(
        expected: np.ndarray,
        actual: np.ndarray,
        *,
        bins: int = 10,
    ) -> float:

        breakpoints = np.histogram_bin_edges(
            expected,
            bins=bins,
        )

        expected_counts, _ = np.histogram(
            expected,
            bins=breakpoints,
        )

        actual_counts, _ = np.histogram(
            actual,
            bins=breakpoints,
        )

        expected_pct = expected_counts / max(
            expected_counts.sum(),
            1,
        )

        actual_pct = actual_counts / max(
            actual_counts.sum(),
            1,
        )

        epsilon = 1e-10

        expected_pct = np.clip(
            expected_pct,
            epsilon,
            None,
        )

        actual_pct = np.clip(
            actual_pct,
            epsilon,
            None,
        )

        psi = np.sum(
            (
                actual_pct - expected_pct
            )
            * np.log(
                actual_pct / expected_pct
            )
        )

        return float(psi)

    # --------------------------------------------------------------
    # Jensen-Shannon
    # --------------------------------------------------------------

    @staticmethod
    def jensen_shannon_distance(
        reference: np.ndarray,
        current: np.ndarray,
        *,
        bins: int = 10,
    ) -> float:

        edges = np.histogram_bin_edges(
            reference,
            bins=bins,
        )

        p, _ = np.histogram(
            reference,
            bins=edges,
            density=True,
        )

        q, _ = np.histogram(
            current,
            bins=edges,
            density=True,
        )

        p = p / np.sum(p)
        q = q / np.sum(q)

        return float(
            jensenshannon(
                p,
                q,
            )
        )


data_drift_detector = DataDriftDetector()