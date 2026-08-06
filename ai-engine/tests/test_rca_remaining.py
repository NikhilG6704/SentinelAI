from root_cause_analysis.evaluator import RCAEvaluator
from root_cause_analysis.model_selector import RCAModelSelector
from root_cause_analysis.trainer import RCATrainer


def test_evaluator():

    evaluator = RCAEvaluator()

    metrics = evaluator.evaluate(
        ["CPU", "Memory", "CPU"],
        ["CPU", "Memory", "Memory"],
    )

    assert "accuracy" in metrics
    assert "f1_score" in metrics


def test_trainer():

    trainer = RCATrainer()

    trainer.train([])

    assert trainer.is_trained


def test_model_selector():

    selector = RCAModelSelector()

    model = selector.select(
        [
            "rule_based",
            "graph_based",
        ]
    )

    assert model == "rule_based"