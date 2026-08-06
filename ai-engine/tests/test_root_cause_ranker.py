from root_cause_analysis.root_cause_ranker import (
    RootCauseRanker,
)


def sample_evidence():

    return [
        {
            "cause": "Memory Leak",
            "score": 0.91,
            "evidence": [
                "High Memory",
                "OOM Errors",
            ],
            "affected_components": [
                "Service A",
            ],
        },
        {
            "cause": "CPU Saturation",
            "score": 0.73,
            "evidence": [
                "CPU >95%",
            ],
            "affected_components": [
                "Server-1",
            ],
        },
        {
            "cause": "Database Failure",
            "score": 0.81,
            "evidence": [
                "Connection Timeout",
            ],
            "affected_components": [
                "DB-Primary",
            ],
        },
    ]


def test_ranking():

    ranker = RootCauseRanker()

    ranked = ranker.rank(
        sample_evidence()
    )

    assert ranked[0].cause == "Memory Leak"

    assert ranked[1].cause == "Database Failure"

    assert ranked[2].cause == "CPU Saturation"


def test_top():

    ranker = RootCauseRanker()

    ranker.rank(
        sample_evidence()
    )

    top = ranker.top(2)

    assert len(top) == 2

    assert top[0].confidence >= top[1].confidence


def test_clear():

    ranker = RootCauseRanker()

    ranker.rank(
        sample_evidence()
    )

    ranker.clear()

    assert len(ranker.results) == 0