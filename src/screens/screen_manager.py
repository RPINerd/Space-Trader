"""
    Screen Manager Module

    Manages the different screens in the game and handles navigation between them.
"""
import logging
import tkinter as tk

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

    """Manages the different screens in the game and handles navigation between them"""

    def __init__(self, window: tk.Tk) -> None:
        """"""
        self.window = window
        self.current_screen = "I"

    def get_screen(self, screen: Screen) -> object:
        """Returns the screen object associated with the given screen key"""
        if not isinstance(screen, str):
            raise TypeError(f"Expected string for screen, got {type(screen)}")
        if screen not in self.screens:
            raise KeyError(f"Key {screen} not found in screens")
        return self.screens[screen]

    def go_to_screen(self, key: str) -> None:
        """Use a key shortcut to switch to a different screen"""
        try:
            screen = self.screens[key]
            screen.tkraise()
            on_show = getattr(screen, "on_show", None)
            if on_show is not None:
                on_show()
        except KeyError:
            raise KeyError(f"Key {key} not found in screens")
        except AttributeError:
            raise AttributeError(f"{self.screens} at {key} does not have a tkraise method")
        except Exception as e:
            raise Exception(f"Unexpected error in go_to_screen: {e}")
        else:
            logger.debug("Switched to screen %s (%s)", key, self.screens[key])

    def build_screens(self) -> None:
        """Simply builds the dictionary of possible screens and their associated classes"""
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
