import numpy as np

from monitoring.data_drift import (
    DataDriftDetector,
    DriftResult,
)


def test_detector_creation():
    detector = DataDriftDetector()

    assert detector is not None


def test_psi():
    detector = DataDriftDetector()

    reference = np.random.normal(
        0,
        1,
        1000,
    )

    current = np.random.normal(
        0,
        1,
        1000,
    )

    psi = detector.population_stability_index(
        reference,
        current,
    )

    assert isinstance(
        psi,
        float,
    )


def test_js_distance():
    detector = DataDriftDetector()

    reference = np.random.normal(
        0,
        1,
        1000,
    )

    current = np.random.normal(
        0,
        1,
        1000,
    )

    js = detector.jensen_shannon_distance(
        reference,
        current,
    )

    assert isinstance(
        js,
        float,
    )


def test_no_drift():
    detector = DataDriftDetector()

    reference = np.random.normal(
        0,
        1,
        5000,
    )

    current = reference.copy()

    result = detector.detect(
        reference,
        current,
    )

    assert isinstance(
        result,
        DriftResult,
    )

    assert not result.drift_detected


def test_detect_drift():
    detector = DataDriftDetector()

    reference = np.random.normal(
        0,
        1,
        5000,
    )

    current = np.random.normal(
        4,
        1,
        5000,
    )

    result = detector.detect(
        reference,
        current,
    )

    assert result.drift_detected


def test_result_fields():
    detector = DataDriftDetector()

    reference = np.random.normal(
        0,
        1,
        1000,
    )

    current = np.random.normal(
        2,
        1,
        1000,
    )

    result = detector.detect(
        reference,
        current,
    )

    assert hasattr(
        result,
        "psi",
    )

    assert hasattr(
        result,
        "js_distance",
    )

    assert hasattr(
        result,
        "ks_statistic",
    )

    assert hasattr(
        result,
        "ks_pvalue",
    )


def test_boolean_flags():
    detector = DataDriftDetector()

    reference = np.random.normal(
        0,
        1,
        1000,
    )

    current = np.random.normal(
        3,
        1,
        1000,
    )

    result = detector.detect(
        reference,
        current,
    )

    assert isinstance(
        result.psi_drift,
        bool,
    )

    assert isinstance(
        result.js_drift,
        bool,
    )

    assert isinstance(
        result.ks_drift,
        bool,
    )