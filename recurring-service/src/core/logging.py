# [Task]: T003
# [Spec]: F-010 (R-010.1)
# [Description]: Recurring service logging configuration
import logging
import sys
from typing import Optional

from .config import settings


def configure_logging() -> None:
    """Configure logging for the recurring service."""
    # Clear existing handlers
    logging.getLogger().handlers.clear()

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    # Create formatter
    if settings.log_json:
        # JSON format for production
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        )
    else:
        # Human-readable format for development
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance."""
    return logging.getLogger(name)
