"""Ship, equipment, and crew service actions."""

import inspect
import logging

import src.constants as c
import src.economy as e

logger = logging.getLogger(__name__)


def buy_fuel() -> None:
    """Logic for buying fuel at the current system"""
    logger.debug("Buying fuel!")
    current_ship: e.Ship = c.GAME["commander"].ship
    full_tank = current_ship.fuel_cost * (current_ship.tank_capacity - current_ship.fuel)
    if full_tank > c.GAME["commander"].credits:
        logger.warning("Not enough credits to buy fuel!")
        return
    current_ship.fuel = current_ship.tank_capacity
    c.GAME["commander"].credits -= full_tank
    logger.info("Fuel bought successfully!")


def repair() -> None:
    """Repair the current ship."""
    logger.warning(f"{inspect.currentframe().f_code.co_name} is not implememented yet.")


def buy_pod() -> None:
    """Buy an escape pod."""
    logger.warning(f"{inspect.currentframe().f_code.co_name} is not implememented yet.")


def buy_ship() -> None:
    """Buy a ship."""
    logger.warning(f"{inspect.currentframe().f_code.co_name} is not implememented yet.")


def get_equip_sold() -> list[str]:
    """Make an list of equipment sold by the current system, with 'x' for ones not sold"""
    current_system_tech = c.GAME["universe"].planets[c.GAME["commander"].currentSystem].tech_level
    sold_equipment: list[tuple[str, str, str]] = []
    for equips in [e.WEAPONS, e.SHIELDS, e.GADGETS]:
        for equip in equips.values():
            if equip.tech_level == e.TechLevel.UNAVAILABLE:
                continue
            if equip.tech_level <= current_system_tech:
                sold_equipment.append(("", equip.name, f"{equip.price} cr."))
            else:
                sold_equipment.append(("x", equip.name, "not sold"))
    return sold_equipment


def buy_equipment() -> None:
    """Buy ship equipment."""
    logger.warning(f"{inspect.currentframe().f_code.co_name} is not implememented yet.")


def sell_equipment() -> None:
    """Sell ship equipment."""
    logger.warning(f"{inspect.currentframe().f_code.co_name} is not implememented yet.")


def hire_crew() -> None:
    """Hire a crew member."""
    logger.warning(f"{inspect.currentframe().f_code.co_name} is not implememented yet.")


def fire_crew() -> None:
    """Fire a crew member."""
    logger.warning(f"{inspect.currentframe().f_code.co_name} is not implememented yet.")
