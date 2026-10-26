"""Trading actions and trade screen data."""

import inspect
import logging

import src.economy as e

logger = logging.getLogger(__name__)


def buy_news() -> None:
    """Buy news for the current system."""
    logger.debug("Buying news!")


def orbit_trade() -> None:
    """Handle a trader encounter that requests to trade with the player."""
    logger.warning(f"{inspect.currentframe().f_code.co_name} is not implememented yet.")


def get_ware_list() -> list[str]:
    """Return the available trade goods."""
    return e.Ware.lst()


def get_bays() -> str:
    """Return the current cargo bay usage placeholder."""
    # TODO placeholder value, not currently tracked
    return "Bays: 3/25"


def buy_good() -> None:
    """Buy a trade good."""
    logger.warning(f"{inspect.currentframe().f_code.co_name} is not implememented yet.")


def sell_good() -> None:
    """Sell a trade good."""
    logger.warning(f"{inspect.currentframe().f_code.co_name} is not implememented yet.")
