"""Trading actions and trade screen data."""

import inspect
import logging

import src.constants as c
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
    """Return the current cargo bay usage and capacity."""
    commander = c.GAME["commander"]
    used_bays = sum(commander.cargo)
    return f"Bays: {used_bays}/{commander.ship.cargo}"


def buy_good(ware_id: int, amount: int | None = None) -> None:
    """Buy as much of a ware as the requested amount and available resources allow."""
    commander = c.GAME["commander"]
    planet = c.GAME["universe"].planets[commander.currentSystem]
    if ware_id not in e.Ware.enum():
        raise ValueError(f"Invalid ware ID: {ware_id}")

    unit_price = planet.trade_prices[ware_id]
    available = int(planet.trade_items[ware_id])
    free_bays = max(0, commander.ship.cargo - sum(commander.cargo))
    if unit_price <= 0 or available <= 0 or free_bays <= 0 or commander.credits < unit_price:
        return

    quantity = min(available, free_bays, commander.credits // unit_price)
    if amount is not None:
        quantity = min(quantity, max(0, amount))
    if quantity <= 0:
        return

    commander.cargo[ware_id] += quantity
    commander.credits -= quantity * unit_price
    planet.trade_items[ware_id] -= quantity


def sell_good(ware_id: int, amount: int | None = None) -> None:
    """Sell up to the requested amount of a ware currently in the ship's cargo."""
    commander = c.GAME["commander"]
    planet = c.GAME["universe"].planets[commander.currentSystem]
    if ware_id not in e.Ware.enum():
        raise ValueError(f"Invalid ware ID: {ware_id}")

    quantity = commander.cargo[ware_id]
    if amount is not None:
        quantity = min(quantity, max(0, amount))
    unit_price = planet.trade_prices[ware_id]
    if quantity <= 0 or unit_price <= 0:
        return

    commander.cargo[ware_id] -= quantity
    commander.credits += quantity * unit_price
