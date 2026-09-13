"""Structured logging configuration."""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(level: str = "INFO", log_file: Optional[str] = None, log_format: Optional[str] = None) -> None:
    """Initialize root and application loggers."""
    if not log_format:
        log_format = "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"

    numeric_level = getattr(logging, level.upper(), logging.INFO)

    handlers = [
        logging.StreamHandler(sys.stdout)
    ]

    if log_file:
        log_path = Path(log_file)
        if not log_path.is_absolute():
            if getattr(sys, "frozen", False):
                base_dir = Path(sys.executable).resolve().parent
            else:
                base_dir = Path(__file__).resolve().parent.parent
            log_path = base_dir / log_file
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(str(log_path), encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(file_handler)

    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        handlers=handlers,
        force=True
    )

    # Silence overly verbose third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("watchfiles").setLevel(logging.WARNING)
