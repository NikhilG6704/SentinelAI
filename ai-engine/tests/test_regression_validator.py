from validation.regression_validator import regression_validator


def test_regression_validator():

    report = regression_validator.validate(
        "IsolationForest",
    )

    assert isinstance(
        report.passed,
        bool,
    )