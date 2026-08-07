from unittest.mock import MagicMock, patch

from retraining.trigger import RetrainingTrigger


def test_trigger_creation():
    trigger = RetrainingTrigger()

    assert trigger is not None


@patch("retraining.trigger.retraining_pipeline")
def test_trigger_retraining(
    mock_pipeline,
):
    mock_pipeline.run.return_value = {
        "status": "success"
    }

    trigger = RetrainingTrigger()

    result = trigger.trigger_retraining(
        model_name="failure_prediction"
    )

    assert result["status"] == "success"

    mock_pipeline.run.assert_called_once()


@patch("retraining.trigger.retraining_pipeline")
def test_trigger_full_pipeline(
    mock_pipeline,
):
    mock_pipeline.run.return_value = {
        "status": "success"
    }

    trigger = RetrainingTrigger()

    result = trigger.trigger_full_pipeline(
        [
            {
                "model_name": "failure_prediction",
            },
            {
                "model_name": "anomaly_detection",
            },
        ]
    )

    assert len(result) == 2

    assert mock_pipeline.run.call_count == 2