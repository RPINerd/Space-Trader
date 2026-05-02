"""
    Commander Module

    Handles the players stats, skills and progress through the game as well as crew info.
"""

import random

from .constants import INSURANCE_RATE, INTEREST_RATE, MAXSKILL, MERCENARYNAMES, CombatReputation, CriminalRecord, Skills
from .economy import SHIPS, Ship


class Commander:

    """Player stats, skills and progress through the game"""

    def __init__(self, name: str, pilot_skill: int, fighter_skill: int, trader_skill: int, engineer_skill: int) -> None:
        """"""
        self.name = name
        self.pilotSkill = pilot_skill
        self.fighterSkill = fighter_skill
        self.traderSkill = trader_skill
        self.engineerSkill = engineer_skill
        self.credits = 1000
        self.debt = 0
        self.ship = SHIPS[Ship.GNAT]
        self.kills = 0
        self.reputation = 0
        self.policeRecord = 0
        self.timePlayed = 0
        self.currentSystem = random.randint(0, 120)

    def __str__(self) -> str:
        """Returns the name of the commander"""
        return self.name

    def pprint(self) -> str:
        """Pretty print of the commander stats"""
        return f"Name: {self.name}\n \
            Skills: {self.pilotSkill}/{self.fighterSkill}/{self.traderSkill}/{self.engineerSkill}\n \
            Credits: {self.credits}\n \
            Debt: {self.debt}\n \
            Ship: {self.ship.name}\n \
            Kills: {self.kills}\n \
            Reputation: {self.reputation}\n \
            Police Record: {self.policeRecord}\n \
            Time Played: {self.timePlayed}"

    def get_net_worth(self) -> int:
        """Returns the net worth of the commander"""
        # TODO include moon value eventually
        return self.credits + self.ship.get_value() - self.debt

    def get_reputation(self) -> str:
        """Returns the string repr of the reputation of the commander"""
        return CombatReputation.get_reputation_string(self.reputation)

    def get_police_record(self) -> str:
        """Returns the string repr of the police record of the commander"""
        return CriminalRecord.get_record_string(self.policeRecord)

    def pay_interest(self) -> None:
        """Calculates the interest on current debt and pays it"""
        debt_interest = 0
        if self.debt > 0:
            debt_interest = max(1, self.debt * INTEREST_RATE)
            if self.credits > debt_interest:
                self.credits -= debt_interest
            else:
                self.debt += debt_interest - self.credits
                self.credits = 0
        self.debt *= 1.1

    def pay_insurance(self) -> None:
        """Calculates the insurance on the ship and pays it"""
        # ! AI generated placeholder
        insurance = self.ship.get_value() * INSURANCE_RATE
        if self.credits > insurance:
            self.credits -= insurance
        else:
            self.debt += insurance - self.credits
            self.credits = 0

    def get_debt(self) -> int:
        """Returns the current debt of the commander"""
        return self.debt

    def improve_skill(self, skill: int, improvement: int) -> None:
        """
        Improves the skill of the commander by the given amount.

        Args:
            skill (int): The skill to improve. 0 = Pilot, 1 = Fighter, 2 = Trader, 3 = Engineer
            improvement (int): The amount to improve the skill by.

        Raises:
            ValueError: If the skill is not in the range [0-3]
        """
        if skill == Skills.PILOT:
            self.pilotSkill = min(self.pilotSkill + improvement, MAXSKILL)
        elif skill == Skills.FIGHTER:
            self.fighterSkill = min(self.fighterSkill + improvement, MAXSKILL)
        elif skill == Skills.TRADER:
            self.traderSkill = min(self.traderSkill + improvement, MAXSKILL)
        elif skill == Skills.ENGINEER:
            self.engineerSkill = min(self.engineerSkill + improvement, MAXSKILL)
        else:
            raise ValueError(f"Invalid skill type, expected [0-3] but got {skill}!")

    def deteriorate_skill(self, skill: int, deterioration: int) -> None:
        """
        Deteriorates the skill of the commander by the given amount.

        Args:
            skill (int): The skill to deteriorate. 0 = Pilot, 1 = Fighter, 2 = Trader, 3 = Engineer
            deterioration (int): The amount to deteriorate the skill by.

        Raises:
            ValueError: If the skill is not in the range [0-3]
        """
        if skill == Skills.PILOT:
            self.pilotSkill = max(self.pilotSkill - deterioration, 1)
        elif skill == Skills.FIGHTER:
            self.fighterSkill = max(self.fighterSkill - deterioration, 1)
        elif skill == Skills.TRADER:
            self.traderSkill = max(self.traderSkill - deterioration, 1)
        elif skill == Skills.ENGINEER:
            self.engineerSkill = max(self.engineerSkill - deterioration, 1)
        else:
            raise ValueError(f"Invalid skill type, expected [0-3] but got {skill}!")


class Crew:

    """Handles the mercenaries and crew members of the ship."""

    def __init__(self, id: int) -> None:
        """"""
        self.id = id
        self.pilotSkill = None
        self.fighterSkill = None
        self.traderSkill = None
        self.engineerSkill = None
        self.currentSystem = None

    def __str__(self) -> str:
        """Returns the name of the crew member"""
        return MERCENARYNAMES[self.id]

    def __repr__(self) -> str:
        """Returns the id of the crew member"""
        return str(self.id)

    def get_salary(self) -> int:
        """
        I think special crewmembers are free? Or something like that

        return Consts.SpecialCrewMemberIds.Contains(Id) || Id == CrewMemberId.Zeethibal ? 0 :

        Returns:
            int: The salary of the crew member
        """
        return sum([self.pilotSkill, self.fighterSkill, self.traderSkill, self.engineerSkill]) * 3

    def get_skills(self) -> list[int]:
        """Returns the skills of the crew member as a list"""
        return [self.pilotSkill, self.fighterSkill, self.traderSkill, self.engineerSkill]

    def mod_random_skill(self, amount: int) -> None:
        """
        Modifies a random skill by the given amount.

        The value can be negative, but the skill will not go below 1 or above {MAXSKILL}.

        TODO In source, looks like there is some recalculation done as well
        int	curTrader = Game.CurrentGame.Commander.Ship.Trader;
        Skills[skill] += amount;
        if (Game.CurrentGame.Commander.Ship.Trader != curTrader)
            Game.CurrentGame.RecalculateBuyPrices(Game.CurrentGame.Commander.CurrentSystem);

        Args:
            amount (int): The amount to modify the skill by. Can be negative.
        """
        skill_attrs = ["pilotSkill", "fighterSkill", "traderSkill", "engineerSkill"]
        eligible = [i for i, s in enumerate(self.get_skills()) if 1 <= s + amount <= MAXSKILL]

        if not eligible:
            return

        idx = random.choice(eligible)
        setattr(self, skill_attrs[idx], self.get_skills()[idx] + amount)
        # TODO: if traderSkill changed, RecalculateBuyPrices for current system (see source note above)
