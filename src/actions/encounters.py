"""Actions available during space encounters."""

import inspect
import logging

logger = logging.getLogger(__name__)


def attack() -> None:
    """Attack during an encounter."""
    logger.warning(f"{inspect.currentframe().f_code.co_name} is not implememented yet.")


def flee() -> None:
    """Flee from an encounter."""
    logger.warning(f"{inspect.currentframe().f_code.co_name} is not implememented yet.")


def ignore() -> None:
    """Ignore an encounter."""
    logger.warning(f"{inspect.currentframe().f_code.co_name} is not implememented yet.")
