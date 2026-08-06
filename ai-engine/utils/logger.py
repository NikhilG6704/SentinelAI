from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger

from config.settings import settings

# Remove Loguru's default logger
logger.remove()

# Console logger
logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL,
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)

# Logs directory
logs_dir = settings.BASE_DIR / "logs"
logs_dir.mkdir(exist_ok=True)

# File logger
logger.add(
    logs_dir / "ai_engine.log",
    level=settings.LOG_LEVEL,
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    enqueue=False,
    backtrace=True,
    diagnose=settings.DEBUG,
)

__all__ = ["logger"]