from recommendation_engine.knowledge_base import (
    KnowledgeBase,
    Recommendation,
)


def test_supported_issues():

    kb = KnowledgeBase()

    issues = kb.supported_issues()

    assert "High CPU" in issues

    assert "Memory Leak" in issues


def test_get_recommendations():

    kb = KnowledgeBase()

    recs = kb.get_recommendations(
        "High CPU"
    )

    assert len(recs) >= 1

    assert recs[0].action == "Restart Service"


def test_unknown_issue():

    kb = KnowledgeBase()

    recs = kb.get_recommendations(
        "Unknown"
    )

    assert recs == []


def test_add_recommendation():

    kb = KnowledgeBase()

    kb.add_recommendation(
        "Power Failure",
        Recommendation(
            action="Start Backup Generator",
            reason="Primary power unavailable.",
            estimated_recovery_time=2,
            severity="Critical",
            asset_types=["Data Center"],
        ),
    )

    recs = kb.get_recommendations(
        "Power Failure"
    )

    assert len(recs) == 1

    assert recs[0].action == "Start Backup Generator"


def test_size():

    kb = KnowledgeBase()

    assert kb.size() >= 4