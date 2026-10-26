"""Finance and account actions for the commander."""

import logging

import src.constants as c

logger = logging.getLogger(__name__)


def get_debt() -> str:
    """Return the commander's current debt."""
    return f"{c.GAME['commander'].debt} cr."


def get_max_loan() -> str:
    """Return the current placeholder maximum loan value."""
    # TODO this is a placeholder, figure out how this is calculated in soruce
    return f"{c.GAME['commander'].get_net_worth()} cr."


def get_credits() -> str:
    """Return the commander's current credits."""
    current_balance = c.GAME["commander"].credits
    logger.debug("Current balance: %s", current_balance)
    return f"Cash: {current_balance} cr."


def get_ship_value() -> str:
    """Return the value of the commander's current ship."""
    return f"{c.GAME['commander'].ship.get_value()} cr."


def get_no_claim() -> str:
    """Return the current placeholder no-claim percentage."""
    # TODO placeholder until I figure out how this is calculated in source
    return "0%"


def get_insurance_rate() -> str:
    """Return the daily insurance cost for the current ship."""
    return f"{c.INSURANCE_RATE * c.GAME['commander'].ship.get_value()} cr. daily"


def buy_insurance() -> None:
    """Buy insurance for the current ship."""
    # TODO
    logger.debug("Buying insurance!")


def get_loan() -> None:
    """Get a loan for the commander."""
    # TODO
    logger.debug("Getting a loan!")
