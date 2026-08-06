from __future__ import annotations

import numpy as np
import pandas as pd

from root_cause_analysis.inference import (
    RootCauseInferenceEngine,
)


def sample_metrics():

    np.random.seed(42)

    cpu = np.random.normal(
        70,
        5,
        100,
    )

    memory = cpu * 0.9 + np.random.normal(
        0,
        1,
        100,
    )

    return pd.DataFrame(
        {
            "cpu": cpu,
            "memory": memory,
        }
    )


def sample_causes():

    return [
        {
            "cause": "Memory Leak",
            "score": 0.91,
            "evidence": [
                "High Memory",
                "OOM Errors",
            ],
            "affected_components": [
                "Service-A",
            ],
        },
        {
            "cause": "CPU Saturation",
            "score": 0.74,
            "evidence": [
                "CPU >95%",
            ],
            "affected_components": [
                "Server-1",
            ],
        },
    ]


def test_inference():

    engine = RootCauseInferenceEngine()

    result = engine.infer(
        sample_metrics(),
        sample_causes(),
    )

    assert "correlations" in result

    assert "root_causes" in result

    assert "explanations" in result

    assert len(result["root_causes"]) == 2


def test_top_root_cause():

    engine = RootCauseInferenceEngine()

    cause = engine.top_root_cause(
        sample_metrics(),
        sample_causes(),
    )

    assert cause.cause == "Memory Leak"

    assert cause.confidence == 0.91