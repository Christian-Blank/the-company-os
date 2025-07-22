"""
Logging configuration for Repo Guardian service.

This module provides structured logging setup with context propagation.
"""

import sys
import structlog
from typing import Any, Dict, Optional
from ..config import settings


def setup_logging() -> None:
    """Configure structured logging for the service."""

    # Choose processors based on format
    if settings.log_format == "json":
        processors = [
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ]
    else:
        # Console format for development
        processors = [
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.dev.ConsoleRenderer(colors=True)
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure stdlib logging level
    import logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper())
    )


def get_logger(name: Optional[str] = None, **context: Any) -> structlog.BoundLogger:
    """Get a structured logger with optional context."""
    logger = structlog.get_logger(name)
    if context:
        logger = logger.bind(**context)
    return logger


def add_context(logger: structlog.BoundLogger, **context: Any) -> structlog.BoundLogger:
    """Add context to an existing logger."""
    return logger.bind(**context)


# Initialize logging on import if not already configured
try:
    # Test if structlog is already configured
    structlog.get_logger().info("test")
except structlog.exceptions.NotConfiguredError:
    setup_logging()
