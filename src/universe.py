"""
    Universe Module

    This module houses the classes and functions for the game universe, which subsequently
    contains all the systems, their respective governments and traits.
"""

import logging
from math import floor, pow, sqrt
from random import choice, randint

from .constants import (
    GALAXYHEIGHT,
    GALAXYWIDTH,
    MAX_WORMHOLES,
    MIN_DISTANCE,
    SECTOR_DIAMETER,
    SOCIETAL_PRESSURE_PREVALENCE,
    SPECIAL_RESOURCE_PREVALENCE,
    Activity,
    Size,
    SocietalPressure,
    SpecialResource,
    TechLevel,
)
from .economy import PoliticalSystem, Ware

logger = logging.getLogger(__name__)

TMPGAMEDIFFICULTY = 1
PLANET_NAMES = {
    0: "Acamar",
    1: "Adahn",
    2: "Aldea",
    3: "Andevian",
    4: "Antedi",
    5: "Balosnee",
    6: "Baratas",
    7: "Bob",
    8: "Brax",
    9: "Bretel",
    10: "Calondia",
    11: "Campor",
    12: "Capelle",
    13: "Carzon",
    14: "Castor",
    15: "Cestus",
    16: "Cheron",
    17: "Courteney",
    18: "Daled",
    19: "Damast",
    20: "Davlos",
    21: "Deneb",
    22: "Deneva",
    23: "Devidia",
    24: "Draylon",
    25: "Drema",
    26: "Endor",
    27: "Esmee",
    28: "Exo",
    29: "Ferris",
    30: "Festen",
    31: "Fourmi",
    32: "Frolix",
    33: "Gemulon",
    34: "Guinifer",
    35: "Hades",
    36: "Hamlet",
    37: "Helena",
    38: "Hulst",
    39: "Iodine",
    40: "Iralius",
    41: "Janus",
    42: "Japori",
    43: "Jarada",
    44: "Jason",
    45: "Kaylon",
    46: "Khefka",
    47: "Kira",
    48: "Klaatu",
    49: "Klaestron",
    50: "Korma",
    51: "Kravat",
    52: "Krios",
    53: "Laertes",
    54: "Largo",
    55: "Lave",
    56: "Ligon",
    57: "Lowry",
    58: "Magrat",
    59: "Malcoria",
    60: "Melina",
    61: "Mentar",
    62: "Merik",
    63: "Mintaka",
    64: "Montor",
    65: "Mordan",
    66: "Myrthe",
    67: "Nelvana",
    68: "Nix",
    69: "Nyle",
    70: "Odet",
    71: "Og",
    72: "Omega",
    73: "Omphalos",
    74: "Orias",
    75: "Othello",
    76: "Parade",
    77: "Penthara",
    78: "Picard",
    79: "Pollux",
    80: "Quator",
    81: "Rakhar",
    82: "Ran",
    83: "Regulas",
    84: "Relva",
    85: "Rhymus",
    86: "Rochani",
    87: "Rubicum",
    88: "Rutia",
    89: "Sarpeidon",
    90: "Sefalla",
    91: "Seltrice",
    92: "Sigma",
    93: "Sol",
    94: "Somari",
    95: "Stakoron",
    96: "Styris",
    97: "Talani",
    98: "Tamus",
    99: "Tantalos",
    100: "Tanuga",
    101: "Tarchannen",
    102: "Terosa",
    103: "Thera",
    104: "Titan",
    105: "Torin",
    106: "Triacus",
    107: "Turkana",
    108: "Tyrus",
    109: "Umberlee",
    110: "Utopia",
    111: "Vadera",
    112: "Vagra",
    113: "Vandor",
    114: "Ventax",
    115: "Xenon",
    116: "Xerxes",
    117: "Yew",
    118: "Yojimbo",
    119: "Zalkon",
    120: "Zuul",
}
GOVERNMENTS = {
    PoliticalSystem.ANARCHY: PoliticalSystem(
        "Anarchy",
        0,
        Activity.ABSENT,
        Activity.SWARMS,
        Activity.MINIMAL,
        TechLevel.PRE_AGRICULTURAL,
        TechLevel.INDUSTRIAL,
        7,
        True,
        True,
        Ware.FOOD,
    ),
    PoliticalSystem.CAPITALIST: PoliticalSystem(
        "Capitalist",
        2,
        Activity.SOME,
        Activity.FEW,
        Activity.SWARMS,
        TechLevel.EARLY_INDUSTRIAL,
        TechLevel.HI_TECH,
        1,
        True,
        True,
        Ware.ORE,
    ),
    PoliticalSystem.COMMUNIST: PoliticalSystem(
        "Communist",
        6,
        Activity.ABUNDANT,
        Activity.MODERATE,
        Activity.MODERATE,
        TechLevel.AGRICULTURAL,
        TechLevel.INDUSTRIAL,
        5,
        True,
        True,
        Ware.NONE,
    ),
    PoliticalSystem.CONFEDERACY: PoliticalSystem(
        "Confederacy",
        5,
        Activity.MODERATE,
        Activity.SOME,
        Activity.MANY,
        TechLevel.AGRICULTURAL,
        TechLevel.POST_INDUSTRIAL,
        3,
        True,
        True,
        Ware.GAMES,
    ),
    PoliticalSystem.CORPORATE: PoliticalSystem(
        "Corporate",
        2,
        Activity.ABUNDANT,
        Activity.FEW,
        Activity.SWARMS,
        TechLevel.EARLY_INDUSTRIAL,
        TechLevel.HI_TECH,
        2,
        True,
        True,
        Ware.ROBOTS,
    ),
    PoliticalSystem.CYBERNETIC: PoliticalSystem(
        "Cybernetic",
        0,
        Activity.SWARMS,
        Activity.SWARMS,
        Activity.MANY,
        TechLevel.POST_INDUSTRIAL,
        TechLevel.HI_TECH,
        0,
        False,
        False,
        Ware.ORE,
    ),
    PoliticalSystem.DEMOCRACY: PoliticalSystem(
        "Democracy",
        4,
        Activity.SOME,
        Activity.FEW,
        Activity.MANY,
        TechLevel.RENAISSANCE,
        TechLevel.HI_TECH,
        2,
        True,
        True,
        Ware.GAMES,
    ),
    PoliticalSystem.DICTATORSHIP: PoliticalSystem(
        "Dictatorship",
        3,
        Activity.MODERATE,
        Activity.MANY,
        Activity.SOME,
        TechLevel.PRE_AGRICULTURAL,
        TechLevel.HI_TECH,
        2,
        True,
        True,
        Ware.NONE,
    ),
    PoliticalSystem.FASCIST: PoliticalSystem(
        "Fascist",
        7,
        Activity.SWARMS,
        Activity.SWARMS,
        Activity.MINIMAL,
        TechLevel.EARLY_INDUSTRIAL,
        TechLevel.HI_TECH,
        0,
        False,
        True,
        Ware.MACHINERY,
    ),
    PoliticalSystem.FEUDAL: PoliticalSystem(
        "Feudal",
        1,
        Activity.MINIMAL,
        Activity.ABUNDANT,
        Activity.FEW,
        TechLevel.PRE_AGRICULTURAL,
        TechLevel.RENAISSANCE,
        6,
        True,
        True,
        Ware.FIREARMS,
    ),
    PoliticalSystem.MILITARY: PoliticalSystem(
        "Military",
        7,
        Activity.SWARMS,
        Activity.ABSENT,
        Activity.ABUNDANT,
        TechLevel.MEDIEVAL,
        TechLevel.HI_TECH,
        0,
        False,
        True,
        Ware.ROBOTS,
    ),
    PoliticalSystem.MONARCHY: PoliticalSystem(
        "Monarchy",
        3,
        Activity.MODERATE,
        Activity.SOME,
        Activity.MODERATE,
        TechLevel.PRE_AGRICULTURAL,
        TechLevel.INDUSTRIAL,
        4,
        True,
        True,
        Ware.MEDICINE,
    ),
    PoliticalSystem.PACIFIST: PoliticalSystem(
        "Pacifist",
        7,
        Activity.FEW,
        Activity.MINIMAL,
        Activity.MANY,
        TechLevel.PRE_AGRICULTURAL,
        TechLevel.RENAISSANCE,
        1,
        True,
        False,
        Ware.NONE,
    ),
    PoliticalSystem.SOCIALIST: PoliticalSystem(
        "Socialist",
        4,
        Activity.FEW,
        Activity.MANY,
        Activity.SOME,
        TechLevel.PRE_AGRICULTURAL,
        TechLevel.INDUSTRIAL,
        6,
        True,
        True,
        Ware.NONE,
    ),
    PoliticalSystem.SATORI: PoliticalSystem(
        "Satori",
        0,
        Activity.MINIMAL,
        Activity.MINIMAL,
        Activity.MINIMAL,
        TechLevel.PRE_AGRICULTURAL,
        TechLevel.AGRICULTURAL,
        0,
        False,
        False,
        Ware.NONE,
    ),
    PoliticalSystem.TECHNOCRACY: PoliticalSystem(
        "Technocracy",
        1,
        Activity.ABUNDANT,
        Activity.SOME,
        Activity.ABUNDANT,
        TechLevel.EARLY_INDUSTRIAL,
        TechLevel.HI_TECH,
        2,
        True,
        True,
        Ware.WATER,
    ),
    PoliticalSystem.THEOCRACY: PoliticalSystem(
        "Theocracy",
        5,
        Activity.ABUNDANT,
        Activity.MINIMAL,
        Activity.MODERATE,
        TechLevel.PRE_AGRICULTURAL,
        TechLevel.EARLY_INDUSTRIAL,
        0,
        True,
        True,
        Ware.NARCOTICS,
    ),
}
TRADEITEMS = {
    Ware.WATER: Ware(
        "Water",
        TechLevel.PRE_AGRICULTURAL,
        TechLevel.PRE_AGRICULTURAL,
        TechLevel.MEDIEVAL,
        30,
        3,
        4,
        SocietalPressure.DROUGHT,
        SpecialResource.SWEETOCEANS,
        SpecialResource.DESERT,
        30,
        50,
        1,
    ),
    Ware.FURS: Ware(
        "Furs",
        TechLevel.PRE_AGRICULTURAL,
        TechLevel.PRE_AGRICULTURAL,
        TechLevel.PRE_AGRICULTURAL,
        250,
        10,
        10,
        SocietalPressure.COLD,
        SpecialResource.RICHFAUNA,
        SpecialResource.LIFELESS,
        230,
        280,
        5,
    ),
    Ware.FOOD: Ware(
        "Food",
        TechLevel.AGRICULTURAL,
        TechLevel.PRE_AGRICULTURAL,
        TechLevel.AGRICULTURAL,
        100,
        5,
        5,
        SocietalPressure.CROPFAILURE,
        SpecialResource.RICHSOIL,
        SpecialResource.POORSOIL,
        90,
        160,
        5,
    ),
    Ware.ORE: Ware(
        "Ore",
        TechLevel.MEDIEVAL,
        TechLevel.MEDIEVAL,
        TechLevel.RENAISSANCE,
        350,
        20,
        10,
        SocietalPressure.WAR,
        SpecialResource.MINERAL_RICH,
        SpecialResource.MINERAL_POOR,
        350,
        420,
        10,
    ),
    Ware.GAMES: Ware(
        "Games",
        TechLevel.RENAISSANCE,
        TechLevel.AGRICULTURAL,
        TechLevel.POST_INDUSTRIAL,
        250,
        -10,
        5,
        SocietalPressure.BOREDOM,
        SpecialResource.ARTISTIC,
        SpecialResource.NOTHING,
        160,
        270,
        5,
    ),
    Ware.FIREARMS: Ware(
        "Firearms",
        TechLevel.RENAISSANCE,
        TechLevel.AGRICULTURAL,
        TechLevel.INDUSTRIAL,
        1250,
        -75,
        100,
        SocietalPressure.WAR,
        SpecialResource.WARLIKE,
        SpecialResource.NOTHING,
        600,
        1100,
        25,
    ),
    Ware.MEDICINE: Ware(
        "Medicine",
        TechLevel.EARLY_INDUSTRIAL,
        TechLevel.AGRICULTURAL,
        TechLevel.POST_INDUSTRIAL,
        650,
        -20,
        10,
        SocietalPressure.PLAGUE,
        SpecialResource.SPECIALHERBS,
        SpecialResource.NOTHING,
        400,
        700,
        25,
    ),
    Ware.MACHINERY: Ware(
        "Machinery",
        TechLevel.EARLY_INDUSTRIAL,
        TechLevel.RENAISSANCE,
        TechLevel.INDUSTRIAL,
        900,
        -30,
        5,
        SocietalPressure.EMPLOYMENT,
        SpecialResource.NOTHING,
        SpecialResource.NOTHING,
        600,
        800,
        25,
    ),
    Ware.NARCOTICS: Ware(
        "Narrcotics",
        TechLevel.INDUSTRIAL,
        TechLevel.PRE_AGRICULTURAL,
        TechLevel.INDUSTRIAL,
        3500,
        -125,
        150,
        SocietalPressure.BOREDOM,
        SpecialResource.WEIRDMUSHROOMS,
        SpecialResource.NOTHING,
        2000,
        3000,
        50,
    ),
    Ware.ROBOTS: Ware(
        "Robots",
        TechLevel.POST_INDUSTRIAL,
        TechLevel.EARLY_INDUSTRIAL,
        TechLevel.HI_TECH,
        5000,
        -150,
        100,
        SocietalPressure.EMPLOYMENT,
        SpecialResource.NOTHING,
        SpecialResource.NOTHING,
        3500,
        5000,
        100,
    ),
}


class Planet:  # noqa: PLR0904 (too many public methods)

    """
    Object representing a single planet in the game world.

    name - planet name
    x - x coordinate of the planet
    y - y coordinate of the planet
    size - planet size
    tech_level - tech level of the planet
    government - political system type of the planet
    soci_pressure - current pressure on the planet
    special_resource - current special resource of the planet
    quest_system - whether the planet is a quest host
    trade_items - items available for trade on the planet
    #? count_down - countdown
    visited - whether the planet has been visited
    #? shipyard_id - id of the shipyard in the system
    """

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        size: int,
        government: PoliticalSystem,
        tech_level: int,
        soci_pressure: int,
        special_resource: int,
    ) -> None:
        """"""
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.government = government
        self.tech_level = tech_level
        self.soci_pressure = soci_pressure
        self.special_resource = special_resource
        self.quest_system = False
        self.trade_items = [0] * 10
        self.count_down = 0
        self.visited = False
        self.shipyard_id = None

        self.initialize_trade_items()

    # Basic Info Interfaces
    def __str__(self) -> str:
        """"""
        return self.name

    def __repr__(self) -> str:
        """Provides a string representation of the planet for debugging purposes"""
        repr_str = f"{self.name} ({self.x}, {self.y}), \
            {Size.name(self.size)}, {self.get_government_name()}, \
            {self.get_tech_level()}, {SpecialResource.name(self.special_resource)}, \
            {self.soci_pressure}, {self.government.law}, {self.government.crime}"
        return repr_str

    def pprint(self) -> str:
        """Provides a pretty print string of the planet info for the system info screen"""
        return f"""---------------
        Planet: {self.name} at ({self.x}, {self.y})\n \
        Size: {Size.name(self.size)}\n \
        Tech Level: {self.tech_level}\n \
        Government: {self.get_government_name()}\n \
        Resources: {SpecialResource.name(self.special_resource)}\n \
        Police: {self.government.law}\n \
        Pirates: {self.government.crime}\n \
        Pressure: {self.soci_pressure}\n \
        ---------------
        """

    @staticmethod
    def system_info_headers() -> list[str]:
        """Reference for making window"""
        # ? Maybe should be in a "UI" data module?
        return [
            "Name:",
            "Size:",
            "Tech level:",
            "Government:",
            "Resources:",
            "Police:",
            "Pirates:",
        ]

    def system_info(self) -> list[str]:
        """"""
        return [
            self.name,
            Size.name(self.size),
            TechLevel.name(self.tech_level),
            self.get_government_name(),
            SpecialResource.name(self.special_resource),
            Activity.name(self.government.law),
            Activity.name(self.government.crime),
        ]

    def get_location(self) -> tuple[int, int]:
        """"""
        return (self.x, self.y)

    def get_size(self) -> int:
        """"""
        return self.size

    def get_tech_level(self) -> int:
        """"""
        return self.tech_level

    def set_visited(self) -> None:
        """"""
        self.visited = True

    def set_tech_level(self, value: int) -> None:
        """"""
        self.tech_level = value

    def dest_is_ok(self) -> bool:
        """
        Check if the destination is reachable with the current fuel level

        Also account for wormholes

        Returns:
            bool: whether the destination is reachable
        """
        raise NotImplementedError("Planet.dest_is_ok not implemented")
        # comm = Game.current_game.commander
        # return self != comm.current_system and (
        #     self.get_distance() <= comm.ship.fuel or Functions.wormhole_exists(comm.current_system, self)
        # )

    def get_distance(self, target_planet=None):
        return int(floor(sqrt(pow(self.x - target_planet.x, 2) + pow(self.y - target_planet.y, 2))))

    # Political Interfaces
    # TODO maybe change to alter_ and handle political shift logic here
    def set_govt_type(self, value: PoliticalSystem) -> None:
        """"""
        self.government = value

    def get_govt_type(self) -> PoliticalSystem:
        """"""
        return self.government

    def get_government_name(self) -> str:
        """"""
        return str(self.government)

    # Economic Interfaces
    def get_pressure(self) -> int:
        """
        Societal pressures:

        0 = under no particular pressure; Uneventful
        1 = at war; Ore and Weapons in demand
        2 = ravaged by a plague; Medicine in demand
        3 = suffering from a drought; Water in demand
        4 = suffering from extreme boredom; Games and Narcotics in demand
        5 = suffering from a cold spell; Furs in demand
        6 = suffering from a crop failure; Food in demand
        7 = lacking enough workers; Machinery and Robots in demand
        """
        return self.soci_pressure

    def set_pressure(self, value: int) -> None:
        """"""
        self.soci_pressure = value

    def get_special_resource(self) -> int:
        """
        Special resources:

        0 = Nothing Special
        1 = Mineral Rich
        2 = Mineral Poor
        3 = Desert
        4 = Sweetwater Oceans
        5 = Rich Soil
        6 = Poor Soil
        7 = Rich Fauna
        8 = Lifeless
        9 = Weird Mushrooms
        10 = Special Herbs
        11 = Artistic Populace
        12 = Warlike Populace
        """
        if self.visited:
            return self.special_resource
        # TODO maybe not random here?
        self.special_resource = SpecialResource.random()
        return self.special_resource

    def initialize_trade_items(self) -> None:
        """Set the starting quantity of each trade good for the planet"""
        for item_id in Ware.enum():

            # Make sure the item is allowed to be traded
            if not self.is_item_traded(item_id):
                self.trade_items[item_id] = 0
            else:
                # Quantity is dictated by the planet tech level, size, and a bit of randomness
                self.trade_items[item_id] = (self.size + 1) * (
                    randint(9, 14) - abs(TRADEITEMS[item_id].tech_level_max - self.tech_level)
                )

            # Because of the enormous profitssss possible,
            # there shouldn't be too many robots or narcotics available
            if item_id >= Ware.NARCOTICS:
                self.trade_items[item_id] = (
                    (self.trade_items[item_id] * (5 - TMPGAMEDIFFICULTY)) / (6 - TMPGAMEDIFFICULTY)
                ) + 1

            # Adjust for special resources and societal pressures
            if self.special_resource == TRADEITEMS[item_id].special_resource_drop:
                self.trade_items[item_id] = self.trade_items[item_id] * 4 / 3
            if self.special_resource == TRADEITEMS[item_id].special_resource_hike:
                self.trade_items[item_id] = self.trade_items[item_id] * 3 / 4
            if self.soci_pressure == TRADEITEMS[item_id].pressure:
                self.trade_items[item_id] /= 5

            # Another small random factor
            self.trade_items[item_id] = self.trade_items[item_id] - randint(1, 10) + randint(1, 10)

            # Finally just make sure it's not negative
            self.trade_items[item_id] = max(self.trade_items[item_id], 0)

    def is_item_traded(self, item: int) -> bool:
        """
        Given an item ID, check with the planets political system to see if it can be traded

        Args:
            item (int): item ID to check

        Returns:
            bool: whether the item can be traded
        """
        if item not in {Ware.FIREARMS, Ware.NARCOTICS}:
            return True

        if item == Ware.FIREARMS:
            return self.government.firearms_ok()

        if item == Ware.NARCOTICS:
            return self.government.drugs_ok()

        raise ValueError(f"Item ID {item} not valid!")

    def item_used(self, item: Ware) -> bool:
        """"""
        raise NotImplementedError(f"Planet.item_used not implemented. Item: {item}")
        # return (
        #     (item.item_type != d.NARCOTICS or self.get_political_system().is_drugs_ok())
        #     and (item.item_type != d.FIREARMS or self.get_political_system().is_firearms_ok())
        #     and self.tech_level.cast_to_int() >= item.tech_usage.cast_to_int()
        # )

    def get_inventory(self) -> list[int]:
        """"""
        return self.trade_items

    # Misc Interfaces
    # TODO implement
    def get_mercenaries_for_hire(self) -> list:
        """
        Get a list of mercenaries available for hire on the planet

        Source code:

            Commander			cmdr		= Game.CurrentGame.Commander;
            CrewMember[]	mercs		= Game.CurrentGame.Mercenaries;
            ArrayList			forHire	= new ArrayList(3);

            for (int i = 1; i < mercs.Length; i++)
            {
                if (mercs[i].CurrentSystem == cmdr.CurrentSystem && !cmdr.Ship.HasCrew(mercs[i].Id))
                    forHire.Add(mercs[i]);
            }

            return (CrewMember[])forHire.ToArray(typeof(CrewMember));
        """
        raise NotImplementedError("Planet.get_mercenaries_for_hire not implemented")
        # cmdr = Game.current_game.commander
        # return [
        #     merc
        #     for merc in Game.current_game.mercenaries.values()
        #     if merc.is_mercenary() and merc.current_system == cmdr.current_system and not cmdr.ship.has_crew(merc.id)
        # ]

    def is_quest_system(self) -> bool:
        """Check whether the planet is a quest system or not"""
        return self.quest_system

    def set_quest_system(self, value: bool) -> None:
        """Set whether the planet is a quest system or not"""
        self.quest_system = value

    # TODO implement
    def show_quest_button(self) -> None:
        """
        Soruce code:

        public bool ShowSpecialButton()
        {
        Game	game	= Game.CurrentGame;
        bool	show	= false;

        switch (SpecialEventType)
        {
                case SpecialEventType.Artifact:
                case SpecialEventType.Dragonfly:
                case SpecialEventType.Experiment:
                case SpecialEventType.Jarek:
                        show	= game.Commander.PoliceRecordScore >= Consts.PoliceRecordScoreDubious;
                        break;
                case SpecialEventType.ArtifactDelivery:
                        show	= game.Commander.Ship.ArtifactOnBoard;
                        break;
                case SpecialEventType.CargoForSale:
                        show	= game.Commander.Ship.FreeCargoBays >= 3;
                        break;
                case SpecialEventType.DragonflyBaratas:
                        show	= game.QuestStatusDragonfly > SpecialEvent.StatusDragonflyNotStarted &&
                        game.QuestStatusDragonfly < SpecialEvent.StatusDragonflyDestroyed;
                        break;
                case SpecialEventType.DragonflyDestroyed:
                        show	= game.QuestStatusDragonfly == SpecialEvent.StatusDragonflyDestroyed;
                        break;
                case SpecialEventType.DragonflyMelina:
                        show	= game.QuestStatusDragonfly > SpecialEvent.StatusDragonflyFlyBaratas &&
                        game.QuestStatusDragonfly < SpecialEvent.StatusDragonflyDestroyed;
                        break;
                case SpecialEventType.DragonflyRegulas:
                        show	= game.QuestStatusDragonfly > SpecialEvent.StatusDragonflyFlyMelina &&
                        game.QuestStatusDragonfly < SpecialEvent.StatusDragonflyDestroyed;
                        break;
                case SpecialEventType.DragonflyShield:
                case SpecialEventType.ExperimentFailed:
                case SpecialEventType.Gemulon:
                case SpecialEventType.GemulonFuel:
                case SpecialEventType.GemulonInvaded:
                case SpecialEventType.Lottery:
                case SpecialEventType.ReactorLaser:
                case SpecialEventType.PrincessQuantum:
                case SpecialEventType.SculptureHiddenBays:
                case SpecialEventType.Skill:
                case SpecialEventType.SpaceMonster:
                case SpecialEventType.Tribble:
                        show	= true;
                        break;
                case SpecialEventType.EraseRecord:
                case SpecialEventType.Wild:
                        show	= game.Commander.PoliceRecordScore < Consts.PoliceRecordScoreDubious;
                        break;
                case SpecialEventType.ExperimentStopped:
                        show	= game.QuestStatusExperiment > SpecialEvent.StatusExperimentNotStarted &&
                    game.QuestStatusExperiment < SpecialEvent.StatusExperimentPerformed;
                        break;
                case SpecialEventType.GemulonRescued:
                        show	= game.QuestStatusGemulon > SpecialEvent.StatusGemulonNotStarted &&
                        game.QuestStatusGemulon < SpecialEvent.StatusGemulonTooLate;
                        break;
                case SpecialEventType.Japori:
                        show	= game.QuestStatusJapori						== SpecialEvent.StatusJaporiNotStarted &&
                        game.Commander.PoliceRecordScore	>= Consts.PoliceRecordScoreDubious;
                        break;
                case SpecialEventType.JaporiDelivery:
                        show	= game.QuestStatusJapori == SpecialEvent.StatusJaporiInTransit;
                        break;
                case SpecialEventType.JarekGetsOut:
                        show	= game.Commander.Ship.JarekOnBoard;
                        break;
                case SpecialEventType.Moon:
                        show	= game.QuestStatusMoon == SpecialEvent.StatusMoonNotStarted &&
                        game.Commander.Worth >  SpecialEvent.MoonCost * .8;
                        break;
                case SpecialEventType.MoonRetirement:
                        show	= game.QuestStatusMoon == SpecialEvent.StatusMoonBought;
                        break;
                case SpecialEventType.Princess:
                        show	= game.Commander.PoliceRecordScore	>= Consts.PoliceRecordScoreLawful &&
                        game.Commander.ReputationScore		>= Consts.ReputationScoreAverage;
                        break;
                case SpecialEventType.PrincessCentauri:
                        show	= game.QuestStatusPrincess >= SpecialEvent.StatusPrincessFlyCentauri &&
                        game.QuestStatusPrincess <= SpecialEvent.StatusPrincessFlyQonos;
                        break;
                case SpecialEventType.PrincessInthara:
                        show	= game.QuestStatusPrincess >= SpecialEvent.StatusPrincessFlyInthara &&
                        game.QuestStatusPrincess <= SpecialEvent.StatusPrincessFlyQonos;
                        break;
                case SpecialEventType.PrincessQonos:
                        show	= game.QuestStatusPrincess == SpecialEvent.StatusPrincessRescued &&
                                !game.Commander.Ship.PrincessOnBoard;
                        break;
                case SpecialEventType.PrincessReturned:
                        show	= game.Commander.Ship.PrincessOnBoard;
                        break;
                case SpecialEventType.Reactor:
                        show	= game.QuestStatusReactor						== SpecialEvent.StatusReactorNotStarted &&
                        game.Commander.PoliceRecordScore	<  Consts.PoliceRecordScoreDubious &&
                        game.Commander.ReputationScore		>= Consts.ReputationScoreAverage;
                        break;
                case SpecialEventType.ReactorDelivered:
                        show	= game.Commander.Ship.ReactorOnBoard;
                        break;
                case SpecialEventType.Scarab:
                        show	= game.QuestStatusScarab					== SpecialEvent.StatusScarabNotStarted &&
                                                        game.Commander.ReputationScore	>= Consts.ReputationScoreAverage;
                        break;
                case SpecialEventType.ScarabDestroyed:
                case SpecialEventType.ScarabUpgradeHull:
                        show	= game.QuestStatusScarab == SpecialEvent.StatusScarabDestroyed;
                        break;
                case SpecialEventType.Sculpture:
                        show	= game.QuestStatusSculpture					== SpecialEvent.StatusSculptureNotStarted &&
                        game.Commander.PoliceRecordScore	<  Consts.PoliceRecordScoreDubious &&
                        game.Commander.ReputationScore		>= Consts.ReputationScoreAverage;
                        break;
                case SpecialEventType.SculptureDelivered:
                        show	= game.QuestStatusSculpture	== SpecialEvent.StatusSculptureInTransit;
                        break;
                case SpecialEventType.SpaceMonsterKilled:
                        show	= game.QuestStatusSpaceMonster == SpecialEvent.StatusSpaceMonsterDestroyed;
                        break;
                case SpecialEventType.TribbleBuyer:
                        show	= game.Commander.Ship.Tribbles > 0;
                        break;
                case SpecialEventType.WildGetsOut:
                        show	= game.Commander.Ship.WildOnBoard;
                        break;
                default:
                        break;
        }

        return show;
        }
        """
        raise NotImplementedError("Planet.show_quest_button not implemented")


class Universe:

    """Responsible for managing the game world, including planet locations and attributes."""

    def __init__(self, shuffle: bool = True) -> None:
        """
        Generate the universe for the game, including planet attributes and locations.

        The C source does re-suffle without re-checking minimum distances, so post-shuffle positions are not
            guaranteed to satisfy the placement invariant.

        Args:
            shuffle (bool): When True (default), randomise planet name-to-position assignments after placement.
        """
        self.planets: dict[int, Planet] = {}
        self.wormholes: list = [0] * MAX_WORMHOLES
        logger.info("Generating Universe...")
        self.generate_planets()
        if shuffle:
            self.extra_planet_shuffle()

    def generate_planets(self) -> None:
        """Generate the planets for the game world."""
        for id, planet_name in PLANET_NAMES.items():

            planet_size = randint(0, 5)
            planet_govt = choice(GOVERNMENTS)

            # TODO can transition this to a choice of valid_tech_levels
            tech_level = randint(planet_govt.minTech, planet_govt.maxTech)

            # As per the original code, ~15% of planets have no societal pressure
            if randint(1, 100) <= SOCIETAL_PRESSURE_PREVALENCE:
                soci_pressure = SocietalPressure.NONE
            else:
                soci_pressure = randint(1, 7)

            # As per the original code, ~40% of planets have no special resource
            if randint(1, 100) <= SPECIAL_RESOURCE_PREVALENCE:
                special_resource = SpecialResource.NOTHING
            else:
                special_resource = randint(1, 12)

            # Generate system position
            x, y = self.pick_valid_xy(id)

            new_planet = Planet(
                planet_name, x, y, planet_size, planet_govt, tech_level, soci_pressure, special_resource
            )

            self.planets[id] = new_planet

    def pick_valid_xy(self, id: int) -> tuple[int, int]:
        """
        Pick a valid x, y coordinate for a new planet

        This first pass is as close a 1:1 translation as possible,
        there is likely a good way to refactor this, if nothing else as a
        good exercise in algorithm design!
        """
        x: int = 0
        y: int = 0

        # Place the first planet somewhere in the center of the galaxy
        if id < len(self.wormholes):
            x = int(((GALAXYWIDTH * (1 + 2 * (id % 3))) / 6) - randint(-SECTOR_DIAMETER + 1, SECTOR_DIAMETER))
            y = int(((GALAXYHEIGHT * (1 if id < 3 else 3)) / 4) - randint(-SECTOR_DIAMETER + 1, SECTOR_DIAMETER))
            self.wormholes[id] = id
            return (x, y)

        valid = False
        while not valid:
            x = randint(1, GALAXYWIDTH)
            y = randint(1, GALAXYHEIGHT)

            close_found = False
            too_close = False
            j = 0
            while j < id and not too_close:

                system_distance = planet_distance(self.planets[j].get_location(), x, y)

                # Minimum distance between any two systems not to be accepted.
                if system_distance <= MIN_DISTANCE**2:
                    too_close = True

                # There should be at least one system which is close enough.
                if system_distance < SECTOR_DIAMETER**2:
                    close_found = True

                j += 1

            valid = close_found and not too_close

        return (x, y)

    def extra_planet_shuffle(self) -> None:
        """
        This function is responsible for shuffling the planets around the universe.

        Apparently without this extra step, the planets with names at the beginning
        of the alphabet are all clustered in the center of the galaxy.
        """
        for planet in self.planets.values():
            i = randint(0, len(self.planets) - 1)
            if not wormhole_exists(self.wormholes, i, -1):
                planet.x, self.planets[i].x = self.planets[i].x, planet.x
                planet.y, self.planets[i].y = self.planets[i].y, planet.y
                hole = self.wormholes.index(i) if i in self.wormholes else -1
                if hole >= 0:
                    self.wormholes[hole] = i

        # Randomize wormhole order
        for wh in self.wormholes:
            new_index = randint(0, len(self.wormholes) - 1)
            wh, self.wormholes[new_index] = self.wormholes[new_index], wh


def planet_distance(planet: tuple[int, int], x2: int, y2: int) -> float:
    """
    Calculate the distance between a planet and a point.

    Args:
        planet (tuple[int, int]): tuple containing the x and y coordinates of the planet
        x2 (int): x coordinate of point 2
        y2 (int): y coordinate of point 2

    Returns:
        float: distance between the planet and the point
    """
    return distance(planet[0], planet[1], x2, y2)


def distance(x1: int, y1: int, x2: int, y2: int) -> float:
    """
    Calculate the distance between two points.

    Args:
        x1 (int): x coordinate of point 1
        y1 (int): y coordinate of point 1
        x2 (int): x coordinate of point 2
        y2 (int): y coordinate of point 2

    Returns:
        float: distance between the two points
    """
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def wormhole_exists(wormholes: list[int], a: int, b: int) -> bool:
    """
    Check if a wormhole exists at the given coordinates.

    Args:
        wormholes (list[int]): list of wormholes
        a (int): first wormhole
        b (int): second wormhole, or -1 if only checking for any wormhole at a

    Returns:
        bool: True if wormhole exists, False otherwise
    """
    # TODO bit of a mess, probably should have small separate functions for each check
    if a in wormholes:

        if b < 0:
            return True

        index = wormholes.index(a)
        if index < MAX_WORMHOLES - 1:
            if wormholes[index + 1] == b:
                return True
        elif wormholes[0] == b:
            return True

    return False
