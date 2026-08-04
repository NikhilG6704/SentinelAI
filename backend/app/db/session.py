"""
Database session and engine configuration.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.logger import logger

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)


def check_database_connection() -> bool:
    """
    Verify database connectivity.

    Returns
    -------
    bool
        True if database connection succeeds.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        logger.info("PostgreSQL connection established successfully.")
        return True

    except SQLAlchemyError as exc:
        logger.error("Database connection failed: %s", exc)
        return False