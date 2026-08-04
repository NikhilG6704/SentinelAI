"""
Application logging configuration.

This module provides a centralized logger instance for the SentinelAI
backend application.
"""

import logging
from typing import Final

LOGGER_NAME: Final[str] = "sentinelai"


def configure_logger() -> logging.Logger:
    """
    Configure and return the application logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(LOGGER_NAME)

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.propagate = False

    return logger


logger = configure_logger()