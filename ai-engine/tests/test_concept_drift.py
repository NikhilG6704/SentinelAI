import numpy as np

from monitoring.concept_drift import (
    ConceptDriftDetector,
    ConceptDriftResult,
)


def test_detector_creation():
    detector = ConceptDriftDetector()

    assert detector is not None


def test_no_drift():
    detector = ConceptDriftDetector()

    predictions = np.array(
        [0, 1, 0, 1, 1]
    )

    confidence = np.array(
        [0.90, 0.91, 0.92, 0.93, 0.94]
    )

    labels = predictions.copy()

    result = detector.detect(
        previous_predictions=predictions,
        current_predictions=predictions,
        previous_confidence=confidence,
        current_confidence=confidence,
        previous_labels=labels,
        current_labels=labels,
    )

    assert isinstance(
        result,
        ConceptDriftResult,
    )

    assert not result.drift_detected


def test_prediction_drift():
    detector = ConceptDriftDetector()

    result = detector.detect(
        previous_predictions=np.zeros(100),
        current_predictions=np.ones(100),
        previous_confidence=np.full(100, 0.90),
        current_confidence=np.full(100, 0.90),
        previous_labels=np.zeros(100),
        current_labels=np.ones(100),
    )

    assert result.prediction_drift


def test_confidence_drift():
    detector = ConceptDriftDetector()

    result = detector.detect(
        previous_predictions=np.zeros(100),
        current_predictions=np.zeros(100),
        previous_confidence=np.full(100, 0.95),
        current_confidence=np.full(100, 0.20),
        previous_labels=np.zeros(100),
        current_labels=np.zeros(100),
    )

    assert result.confidence_drift


def test_error_drift():
    detector = ConceptDriftDetector()

    previous_predictions = np.zeros(100)
    previous_labels = np.zeros(100)

    current_predictions = np.zeros(100)
    current_labels = np.ones(100)

    result = detector.detect(
        previous_predictions=previous_predictions,
        current_predictions=current_predictions,
        previous_confidence=np.full(100, 0.90),
        current_confidence=np.full(100, 0.90),
        previous_labels=previous_labels,
        current_labels=current_labels,
    )

    assert result.error_drift


def test_result_fields():
    detector = ConceptDriftDetector()

    result = detector.detect(
        previous_predictions=np.zeros(10),
        current_predictions=np.ones(10),
        previous_confidence=np.full(10, 0.90),
        current_confidence=np.full(10, 0.40),
        previous_labels=np.zeros(10),
        current_labels=np.ones(10),
    )

    assert hasattr(
        result,
        "prediction_shift",
    )

    assert hasattr(
        result,
        "confidence_shift",
    )

    assert hasattr(
        result,
        "error_rate_change",
    )


def test_boolean_flags():
    detector = ConceptDriftDetector()

    result = detector.detect(
        previous_predictions=np.zeros(10),
        current_predictions=np.ones(10),
        previous_confidence=np.full(10, 0.90),
        current_confidence=np.full(10, 0.30),
        previous_labels=np.zeros(10),
        current_labels=np.ones(10),
    )

    assert isinstance(
        result.prediction_drift,
        bool,
    )

    assert isinstance(
        result.confidence_drift,
        bool,
    )

    assert isinstance(
        result.error_drift,
        bool,
    )