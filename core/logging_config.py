"""
Centralized logging configuration for the application.
This module sets up the logging format, level, and handlers to ensure consistent logging across different parts of the application.
"""

import logging
import sys

from config import LOG_LEVEL, LOG_FORMAT


def setup_logging() -> None:
    """Configures the global logging settings for the application."""
    logging.basicConfig(
        level=LOG_LEVEL, format=LOG_FORMAT, handlers=[logging.StreamHandler(sys.stdout)]
    )


def get_logger(name: str) -> logging.Logger:
    """Returns a logger instance with the specified name.
    Args:
        name (str): The name of the logger.
    Returns:
        logging.Logger: Configured logger instance.
    """
    return logging.getLogger(name)
