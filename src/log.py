"""
    Logging Module

    Centralised logging configuration for the entire application.
"""

import logging
import logging.handlers
from pathlib import Path

_LOG_DIR = Path("logs")
_LOG_FILE = _LOG_DIR / "spacetrader.log"

# "%(levelname)-8s"  pads to 8 chars — the length of "CRITICAL" (longest level name)
_FMT = "%(asctime)s | %(levelname)-8s | %(name)s %(lineno)d | %(message)s"
_DATE_FMT = "%Y-%m-%d %H:%M:%S"


def setup_logging(console_level: int = logging.DEBUG) -> None:
    """
    Configure the root logger with a console handler and a rotating file handler.

    Should be called exactly once at application startup, before any other module produces log output.

    Args:
        console_level: Minimum level emitted to the console.
            The file handler always captures DEBUG and above. Defaults to logging.DEBUG.
    """
    _LOG_DIR.mkdir(exist_ok=True)

    formatter = logging.Formatter(_FMT, datefmt=_DATE_FMT)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)

    # Rotate at 10 MB, keep 5 backups so logs don't consume excessive disk space.
    file_handler = logging.handlers.RotatingFileHandler(
        _LOG_FILE,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(console_handler)
    root.addHandler(file_handler)
