"""
    Program | RPINerd, 10/22/26

    Description for program
"""

import inspect
import logging
from random import choice, randint

import src.constants as c
from src import universe

logger = logging.getLogger(__name__)


def _resolve_target(
    target: int | universe.Planet | None, planets: dict[int, universe.Planet]
) -> tuple[int | None, universe.Planet | None]:
    if isinstance(target, int):
        return target, planets.get(target)
    if target is None:
        return None, None

    target_id = next((planet_id for planet_id, planet in planets.items() if planet is target), None)
    return target_id, target if target_id is not None else None


def _within_fuel_range(via_singularity: bool, wormhole_jump: bool, distance: int, fuel: int) -> bool:
    return via_singularity or wormhole_jump or 0 < distance <= fuel


def shuffle_system_status() -> None:
    """The status of systems should change over time, call this on arrival to update all the systems"""
    """Pseudo

    for system in galaxy
        if system.status isn't uneventful
            system.status = uneventful if rand(100) < 15
        elif rand(100) < 15
            system.status = random status
    """
    logger.warning("System status shuffle not implemented yet")


def prep_for_warp(via_singularity: bool = False) -> None:
    """Validate and prepare the commander and ship for a warp."""
    game = c.GAME
    commander = game["commander"]
    ship = commander.ship
    game_universe = game["universe"]
    target_id, target_planet = _resolve_target(game.get("target_system"), game_universe.planets)

    if target_id is None or target_planet is None:
        logger.warning("Warp cancelled: no valid target system selected")
        return

    current_id = commander.currentSystem
    if target_id == current_id:
        logger.warning("Warp cancelled: target system is the current system")
        return

    wormhole_jump = universe.wormhole_exists(game_universe.wormholes, current_id, target_id)
    distance = game_universe.planets[current_id].get_distance(target_planet)
    available_fuel = min(ship.fuel, ship.tank_capacity)

    if not _within_fuel_range(via_singularity, wormhole_jump, distance, available_fuel):
        logger.warning("Warp cancelled: target system is outside fuel range")
        return

    # TODO: If Wild is aboard, require a weapon or let the player leave him behind.

    if commander.debt > c.DEBT_LIMIT:
        logger.warning("Warp cancelled: debt is too large for travel")
        return

    # TODO: Sum the daily salaries for hired crew once crew membership is modeled.
    mercenary_cost = 0
    insurance_cost = commander.get_insurance_payment()
    wormhole_tax = ship.fuel_cost * 25 if wormhole_jump else 0
    travel_cost = mercenary_cost + insurance_cost + wormhole_tax
    if travel_cost > commander.credits:
        logger.warning("Warp cancelled: not enough credits for travel costs")
        return

    if not via_singularity:
        commander.credits -= travel_cost
        if commander.insurance:
            commander.noClaimDays += 1

    # TODO: Refill installed shields to their type's maximum strength.
    """
    for (i=0; i<MAXSHIELD; ++i)
	{
		if (Ship.Shield[i] < 0)
			break;
		Ship.ShieldStrength[i] = Shieldtype[Ship.Shield[i]].Power;
	}
    """
    game["arrived_via_wormhole"] = via_singularity or wormhole_jump
    if not game["arrived_via_wormhole"]:
        ship.fuel -= min(distance, available_fuel)

    # TODO: Reset transient news events before recording this trip's events.
    """
    {resetNewsEvents()}

    if not a wormhole jump
        {PayInterest()}
        {IncDays(1)}  this is a counter of playtime for score calc
        if insurance owned
            increment the no-claim warp count
    else
        {addNewsEvent(ARRIVALVIASINGULARITY)}
    """
    if not via_singularity:
        commander.pay_interest()
        commander.timePlayed += 1
        # TODO: Advance quest timers along with the play-time counter.
    else:
        # TODO: Add the arrival-via-singularity news event.
        pass

    game["clicks"] = 21
    game["raided"] = False
    game["inspected"] = False
    game["litter_warning"] = False

    # TODO: Grow monster hull by 5%, capped at its ship type's hull strength.
    """
    monster_hull = (monster_hull * 105) / 100
    if (MonsterHull > Shiptype[SpaceMonster.Type].HullStrength)
		MonsterHull = Shiptype[SpaceMonster.Type].HullStrength
	"""
    # TODO: Apply passive police-record changes based on time and difficulty.
    """
    if (Days%3 == 0)
	{
		if (PoliceRecordScore > CLEANSCORE)
			--PoliceRecordScore;
	}
	if (PoliceRecordScore < DUBIOUSSCORE)
		if (Difficulty <= NORMAL)
			++PoliceRecordScore;
		else if (Days%Difficulty == 0)
			++PoliceRecordScore
    """
    game["possible_to_go_through_rip"] = True

    game_universe.update_trade_prices()

    travel()


def travel() -> None:
    """This is the rough logic of everything that can happen during the transit process"""
    logger.warning(f"{inspect.currentframe().f_code.co_name} is not functionally implememented yet.")

    # TODO these are likely properties to be stored elsewhere, here just for code translation ease
    POSSIBLE_TO_GO_THROUGH_RIP = False
    EXPERIMENT_STATUS = 12
    FABRIC_RIP_PROB = 1
    CLICKS = 21

    if POSSIBLE_TO_GO_THROUGH_RIP and EXPERIMENT_STATUS == 12 and FABRIC_RIP_PROB > 0 and (randint(0, 100) < FABRIC_RIP_PROB or FABRIC_RIP_PROB == 25):
        # Query player if they wish to travel rift
        warp_target = choice(universe.Universe.planets)
    POSSIBLE_TO_GO_THROUGH_RIP = False

    pirate, trader, police, mantis = False
