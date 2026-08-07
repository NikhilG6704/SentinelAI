from validation.integration_validator import integration_validator


def test_integration_validator():

    result = integration_validator.validate()

    assert result is not None
    assert isinstance(result.success, bool)
    assert len(result.checks) == 6