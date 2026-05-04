"""
    Constants Module

    Game constants, to be imported by other modules.
"""

from random import randint

# Player Game Instance
GAME = {}


# Display
INTERNAL_RES = 160
HALF_RES = INTERNAL_RES // 2
BKG_COLOR = (134, 134, 104)
BKG_HEX = "#868668"
FRG_COLOR = (0, 0, 0)
FRG_HEX = "#000000"
CIRCLE_XY = (14, 14)
SCALAR = 3

# Galaxy
GALAXYWIDTH = 154
GALAXYHEIGHT = 110
MIN_DISTANCE = 7
MAX_DISTANCE = 20
WORMHOLE_DISTANCE = 25
SECTOR_DIAMETER = 13
MAX_WORMHOLES = 6

# Economy
START_CREDITS = 1000
INTEREST_RATE = 0.1
DEBT_WARN = 75000
DEBT_LIMIT = 100000
INSURANCE_RATE = 0.0025
MAX_NOCLAIM = 90

# Character
MAXTRIBBLES = 100000
MAXSKILL = 10
SKILLBONUS = 3
CLOAKBONUS = 2
BOUNTYMOD = 1000  # Price paid by govt for each neg police point

MERCENARYNAMES = {
    1: "Alyssa",
    2: "Armatur",
    3: "Bentos",
    4: "C2U2",
    5: "Chi'Ti",
    6: "Crystal",
    7: "Dane",
    8: "Deirdre",
    9: "Doc",
    10: "Draco",
    11: "Iranda",
    12: "Jeremiah",
    13: "Jujubal",
    14: "Krydon",
    15: "Luis",
    16: "Mercedez",
    17: "Milete",
    18: "Muri-L",
    19: "Mystyc",
    20: "Nandi",
    21: "Orestes",
    22: "Pancho",
    23: "PS37",
    24: "Quarck",
    25: "Sosumi",
    26: "Uma",
    27: "Wesley",
    28: "Wonton",
    29: "Yorvick",
    30: "Zeethibal",  # anagram of Elizabeth
}


class Activity:

    """Enum-esque class to associate an int with an activity level"""

    ABSENT = 0
    MINIMAL = 1
    FEW = 2
    SOME = 3
    MODERATE = 4
    MANY = 5
    ABUNDANT = 6
    SWARMS = 7
    UNAVAILABLE = 100

    NAMES = (
        "Absent",
        "Minimal",
        "Few",
        "Some",
        "Moderate",
        "Many",
        "Abundant",
        "Swarms",
        "Unavailable",
    )

    @classmethod
    def name(cls, activity: int) -> str:
        """
        Provides the name of the activity level

        Raises:
            ValueError on invalid index given
        """
        if activity < 0 or activity >= len(cls.NAMES):
            raise ValueError(f"Invalid activity: {activity}")
        return cls.NAMES[activity]


class TechLevel:

    """Enum-esque class to associate an int with a tech level"""

    PRE_AGRICULTURAL = 0
    AGRICULTURAL = 1
    MEDIEVAL = 2
    RENAISSANCE = 3
    EARLY_INDUSTRIAL = 4
    INDUSTRIAL = 5
    POST_INDUSTRIAL = 6
    HI_TECH = 7
    UNAVAILABLE = 8

    NAMES = (
        "Pre-Agricultural",
        "Agricultural",
        "Medieval",
        "Renaissance",
        "Early Industrial",
        "Industrial",
        "Post-Industrial",
        "Hi-Tech",
        "Unavailable",
    )

    @classmethod
    def name(cls, tech: int) -> str:
        """
        Provides the name of the tech level

        Raises:
            ValueError on invalid index given
        """
        if tech < 0 or tech >= len(cls.NAMES):
            raise ValueError(f"Invalid tech level: {tech}")
        return cls.NAMES[tech]


class Size:

    """Enum-esque class to associate an int with a size"""

    TINY = 0
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    HUGE = 4
    GARGANTUAN = 5

    NAMES = ("Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan")

    @classmethod
    def name(cls, size: int) -> str:
        """
        Provides the name of the size

        Raises:
            ValueError on invalid index given
        """
        if size < 0 or size >= len(cls.NAMES):
            raise ValueError(f"Invalid size: {size}")
        return cls.NAMES[size]


SPECIAL_RESOURCE_PREVALENCE = 40


class SpecialResource:

    """Enum-esque class to associate an int with a special resource"""

    NOTHING = 0
    MINERAL_RICH = 1
    MINERAL_POOR = 2
    DESERT = 3
    SWEETOCEANS = 4
    RICHSOIL = 5
    POORSOIL = 6
    RICHFAUNA = 7
    LIFELESS = 8
    WEIRDMUSHROOMS = 9
    SPECIALHERBS = 10
    ARTISTIC = 11
    WARLIKE = 12

    NAMES = (
        "Nothing special",  # Uneventful
        "Mineral rich",  # produce Ore
        "Mineral poor",  # Ore in demand
        "Desert",  # Water in demand
        "Sweetwater oceans",  # produce Water
        "Rich soil",  # produce Food
        "Poor soil",  # Food in demand
        "Rich fauna",  # produce Fur
        "Lifeless",  # Water and Food in demand
        "Weird mushrooms",  # produce Narcotics
        "Special herbs",  # produce Narcotics
        "Artistic populace",  # Narcotics in demand
        "Warlike populace",  # Weapons in demand
    )

    @classmethod
    def name(cls, resource: int) -> str:
        """
        Provides the name of the special resource

        Raises:
            ValueError on invalid index given
        """
        if resource < 0 or resource >= len(cls.NAMES):
            raise ValueError(f"Invalid resource: {resource}")
        return cls.NAMES[resource]

    @staticmethod
    def random() -> int:
        """Gives the index value of a random special resource"""
        return randint(1, 12)


SOCIETAL_PRESSURE_PREVALENCE = 15


class SocietalPressure:

    """Enum-esque class to associate an int with a societal pressure"""

    NONE = 0
    WAR = 1
    PLAGUE = 2
    DROUGHT = 3
    BOREDOM = 4
    COLD = 5
    CROPFAILURE = 6
    EMPLOYMENT = 7

    NAMES = (
        "under no particular pressure",  # Uneventful
        "at war",  # Ore and Weapons in demand
        "ravaged by a plague",  # Medicine in demand
        "suffering from a drought",  # Water in demand
        "suffering from extreme boredom",  # Games and Narcotics in demand
        "suffering from a cold spell",  # Furs in demand
        "suffering from a crop failure",  # Food in demand
        "lacking enough workers",  # Machinery and Robots in demand
    )

    @classmethod
    def name(cls, pressure: int) -> str:
        """
        Provides the flavor text of the societal pressure

        Args:
            pressure: int

        Raises:
            ValueError on invalid index given

        Returns:
            str: Flavor text for the corresponding societal pressure
        """
        if pressure < 0 or pressure >= len(cls.NAMES):
            raise ValueError(f"Invalid pressure: {pressure}")
        return cls.NAMES[pressure]

    @staticmethod
    def random() -> int:
        """Gives the index value of a random societal pressure"""
        return randint(1, 7)


# Character
class Skills:

    """Enum-esque class to associate an int with a skill"""

    NONE = 0
    PILOT = 1
    FIGHTER = 2
    TRADER = 3
    ENGINEER = 4


class Difficulty:

    """Enum-esque class to associate an int with a difficulty level"""

    BEGINNER = 0
    EASY = 1
    NORMAL = 2
    HARD = 3
    IMPOSSIBLE = 4

    NAMES = ("Beginner", "Easy", "Normal", "Hard", "Impossible")

    @classmethod
    def name(cls, difficulty: int) -> str:
        """
        Provides the name of the difficulty level

        Args:
            difficulty: int

        Raises:
            ValueError on invalid index given

        Returns:
            str: Name of the difficulty level
        """
        if difficulty < 0 or difficulty >= len(cls.NAMES):
            raise ValueError(f"Invalid difficulty: {difficulty}")
        return cls.NAMES[difficulty]


class CriminalRecord:

    """Enum-esque class to associate an int with a criminal record"""

    PSYCHOPATH = 0
    VILLAIN = 1
    CRIMINAL = 2
    CROOK = 3
    DUBIOUS = 4
    CLEAN = 5
    LAWFUL = 6
    TRUSTED = 7
    LIKED = 8
    HERO = 9
    ERRNO = 10

    NAMES = (
        "Psychopath",
        "Villain",
        "Criminal",
        "Crook",
        "Dubious",
        "Clean",
        "Lawful",
        "Trusted",
        "Liked",
        "Hero",
        "ERRNO",
    )

    SCORES = (
        -100,
        -70,
        -30,
        -10,
        -5,
        0,
        5,
        10,
        25,
        75,
        100,
    )

    @staticmethod
    def get_record_string(record: int) -> str:
        """Provides the name of the criminal record"""
        return CriminalRecord.NAMES[record]


class CombatReputation:

    """Enum-esque class to associate an int with a combat reputation"""

    HARMLESS = 0
    MOSTLY_HARMLESS = 1
    POOR = 2
    AVERAGE = 3
    ABOVE_AVERAGE = 4
    COMPETENT = 5
    DANGEROUS = 6
    DEADLY = 7
    ELITE = 8
    BORG = 9

    NAMES = (
        "Harmless",
        "Mostly Harmless",
        "Poor",
        "Average",
        "Above Average",
        "Competent",
        "Dangerous",
        "Deadly",
        "Elite",
        "Borg",
    )

    SCORES = (
        0,
        10,
        20,
        40,
        80,
        150,
        300,
        600,
        1500,
        3000,
    )

    @staticmethod
    def get_reputation_string(reputation: int) -> str:
        """Provides the name of the combat reputation"""
        return CombatReputation.NAMES[reputation]


# TODO Unknown values/usage
SCOREATTACKPIRATE = 0
SCOREATTACKPOLICE = -3
SCOREATTACKTRADER = -2
SCORECAUGHTWITHWILD = -4
SCOREFLEEPOLICE = -2
SCOREKILLCAPTAIN = 100
SCOREKILLPIRATE = 1
SCOREKILLPOLICE = -6
SCOREKILLTRADER = -4
SCOREPLUNDERPIRATE = -1
SCOREPLUNDERTRADER = -2
SCORETRAFFICKING = -1

SHIPTEMPLATESEPARATOR = "----------------------------"

STARTCLICKS = 20
MAXFUELTANKS = 20
FUELCOMPACTORTANKS = 3
HULLUPGRADE = 50
MAXSHIP = 9
MAXSLOTS = 5
FLEACONVERSIONCOST = 500
PODTRANSFERCOST = 200

IMAGESPERSHIP = 4
SHIPIMGOFFSETNORMAL = 0
SHIPIMGOFFSETDAMAGE = 1
SHIPIMGOFFSETSHIELD = 2
SHIPIMGOFFSETSHEILDDAMAGE = 3
SHIPIMGUSEDEFAULT = -1
ENCOUNTERIMGALIEN = 0
ENCOUNTERIMGPIRATE = 1
ENCOUNTERIMGPOLICE = 2
ENCOUNTERIMGSPECIAL = 3
ENCOUNTERIMGTRADER = 4

STORYPROBABILITY = 50 / 8
FABRICRIPINITIALPROBABILITY = 25

DIRECTIONUP = 0
DIRECTIONDOWN = 1
DIRECTIONLEFT = 2
DIRECTIONRIGHT = 3

DISRUPTORSYSTEMSMULTIPLIER = 3
