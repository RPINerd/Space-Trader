"""
    Screen Manager Module

    Manages the different screens in the game and handles navigation between them.
"""
import logging

from .gamescreens import (
    AvgPrices,
    Bank,
    BuyCargo,
    BuyEquipment,
    BuyShip,
    CommanderInfo,
    LongRange,
    Personnel,
    Quests,
    SellCargo,
    SellEquipment,
    ShipInfo,
    Shipyard,
    ShortRange,
    SpecialCargo,
    SystemInfo,
    TargetSystem,
)
from .screens import Screen

logger = logging.getLogger(__name__)

SCREENS = {
    "I": {
        "name": "system_info",
        "title": "System Info",
        "class": SystemInfo,
    },
    "B": {
        "name": "buy_cargo",
        "title": "Buy Cargo",
        "class": BuyCargo,
    },
    "S": {
        "name": "sell_cargo",
        "title": "Sell Cargo",
        "class": SellCargo,
    },
    "Y": {
        "name": "shipyard",
        "title": "Shipyard",
        "class": Shipyard,
    },
    "W": {
        "name": "short_range_chart",
        "title": "Short Range Chart",
        "class": ShortRange,
    },
    "E": {
        "name": "buy_equipment",
        "title": "Buy Equipment",
        "class": BuyEquipment,
    },
    "Q": {
        "name": "sell_equipment",
        "title": "Sell Equipment",
        "class": SellEquipment,
    },
    "P": {
        "name": "personnel",
        "title": "Personnel",
        "class": Personnel,
    },
    "K": {
        "name": "bank",
        "title": "Bank",
        "class": Bank,
    },
    "C": {
        "name": "commander_status",
        "title": "Commander Status",
        "class": CommanderInfo,
    },
    "G": {
        "name": "galactic_chart",
        "title": "Galactic Chart",
        "class": LongRange,
    },
    "O": {
        "name": "options",
        "title": "Options",
        "class": None,
    },
}


class ScreenManager:

    def __init__(self, window):
        self.window = window
        self.current_screen = "I"

    def get_screen(self, screen):
        return self.screens[screen]

    def go_to_screen(self, key):
        try:
            self.screens[key].tkraise()
        except KeyError:
            raise KeyError(f"Key {key} not found in screens")
        except AttributeError:
            # self.screens[key].place(x=0, y=0, relwidth=1, relheight=1)
            raise AttributeError(f"{self.screens} at {key} does not have a tkraise method")
        except Exception as e:
            raise Exception(f"Unexpected error in go_to_screen: {e}")
        else:
            logger.debug("Switched to screen %s (%s)", key, self.screens[key])

    def build_screens(self):
        self.screens: dict[str, Screen] = {
            "I": SystemInfo(self.window, "System Info", self),
            "B": BuyCargo(self.window, "Buy Cargo", self),
            "S": SellCargo(self.window, "Sell Cargo", self),
            "Y": Shipyard(self.window, "Shipyard", self),
            "W": ShortRange(self.window, "Short Range Chart", self),
            "E": BuyEquipment(self.window, "Buy Equipment", self),
            "Q": SellEquipment(self.window, "Sell Equipment", self),
            "P": Personnel(self.window, "Personnel", self),
            "K": Bank(self.window, "Bank", self),
            "C": CommanderInfo(self.window, "Character Info", self),
            "G": LongRange(self.window, "Long Range Chart", self),
            "L": Quests(self.window, "Quests", self),
            "A": ShipInfo(self.window, "Ship Info", self),
            "U": SpecialCargo(self.window, "Special Cargo", self),
            "T": TargetSystem(self.window, "Target System", self),
            "V": AvgPrices(self.window, "Average Prices", self),
            "Z": BuyShip(self.window, "Buy Ship", self),
        }
