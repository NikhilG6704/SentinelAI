from app.db.session import SessionLocal


def test_session_creation():
    """
    Verify that a SQLAlchemy session can be created.
    """
    session = SessionLocal()

    assert session is not None

    session.close()