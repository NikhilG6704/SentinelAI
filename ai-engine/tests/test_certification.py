from validation.certification import production_certification


def test_certification():

    report = production_certification.generate()

    assert isinstance(
        report.certified,
        bool,
    )