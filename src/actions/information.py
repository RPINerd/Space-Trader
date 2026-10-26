"""Read-only actions for system and commander information."""

import src.constants as c


def get_system_info() -> tuple[list[str], str]:
    """Pulls the current system information and pressure to be displayed on the system info screen"""
    current_planet = c.GAME["universe"].planets[c.GAME["commander"].currentSystem]

    sys_info = current_planet.system_info()

    # Format system pressure
    pressure = current_planet.get_pressure()
    pressure_str = f"System is {c.SocietalPressure.name(pressure)}"

    return sys_info, pressure_str


def get_commander_info() -> dict:
    """Returns a dictionary of the commander's information"""
    commander = c.GAME["commander"]
    return {
        "name": commander.name,
        "pilot": (commander.pilotSkill, commander.pilotSkill),
        "fighter": (commander.fighterSkill, commander.fighterSkill),
        "trader": (commander.traderSkill, commander.traderSkill),
        "engineer": (commander.engineerSkill, commander.engineerSkill),
        "kills": commander.kills,
        "time": commander.timePlayed,
        "cash": commander.credits,
        "debt": commander.debt,
        "net_worth": commander.get_net_worth(),
        "rep": commander.get_reputation(),
        "record": commander.get_police_record(),
        "difficulty": c.GAME["difficulty"],
    }


def get_quests() -> list[str]:
    """Return the open quests for the commander."""
    return ["There are no open quests."]
