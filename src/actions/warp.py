"""
    Program | RPINerd, 10/22/26

    Description for program
"""

import inspect
import logging
from random import choice, randint

from src import universe

logger = logging.getLogger(__name__)


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
    """
    This function coordinates all the processes that take place once the player clicks on the Warp button

    Args:
        via_singularity (bool): whether travel is occuring through a wormhole or not
    """
    logger.warning(f"{inspect.currentframe().f_code.co_name} is not implememented yet.")

    # The following pseudocode summary is a direct port of the step by step functions from the original source codes 'DoWarp()'

    # 1. If Wild is aboard, the ship must be armed
    # If not armed, player must choose whether to say goodbye to Wild or not

    # 2. Check if the players debt is too large to travel
    # TODO need to fill out more details on this

    # 3. Verify enough money to pay for mercenaries currently hired

    # 4. Verify enough money for current insurance payment

    # 5. If attempting to travel via wormhole, calulate tax and make sure there is enough money

    # 6. If all above checks do not raise any warnings, deduct the funds from the player account

    """
    At this point looks to be some sort of sheild reset?

    for (i=0; i<MAXSHIELD; ++i)
	{
		if (Ship.Shield[i] < 0)
			break;
		Ship.ShieldStrength[i] = Shieldtype[Ship.Shield[i]].Power;
	}
    """

    # 7. Process fuel and distance
    # TODO GetFuel() function translation
    """
    if wormhole jump
        distance = 0
        arrived_via_worm = true
    else
        distance = dist(current_system, target_system)
        ship.fuel -= min(distance, {GetFuel() function})
        arrived_via_worm = false
    """

    # 8. Handle news and insurance things

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

    # 9. Init some travel variables

    """
    clicks = 21
    raided = false
    inspected = false
    litter_warning = false
    """

    # 10. Grow the monster
    monster_hull = (monster_hull * 105) / 100
    """
    if (MonsterHull > Shiptype[SpaceMonster.Type].HullStrength)
		MonsterHull = Shiptype[SpaceMonster.Type].HullStrength
	"""

    # 11. Update passive changes to police record

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

    # TODO not sure what this is about yet
    possible_to_go_through_rip = True

    # TODO expound upon
    # {DeterminePrices(WarpSystem)}

    # Travel()


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
