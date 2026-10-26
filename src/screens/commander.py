"""Commander, ship, personnel, and quest screens."""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

import src.ui_actions as actions

from .screens import Screen

if TYPE_CHECKING:
    from src.screens.screen_manager import ScreenManager  # ruff:ignore[runtime-import-in-type-checking-block]


class CommanderInfo(Screen):

    """View the current commanders stats/skills/etc"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:  # ruff:ignore[too-many-statements]
        """"""
        # Pull the data for the current commander's info
        commander_info = actions.get_commander_info()

        # First frame is the Name: {name}
        self.name_frame = ttk.Frame(self)
        self.name_title = ttk.Label(self.name_frame, text="Name:")
        self.name_label = ttk.Label(self.name_frame, text=commander_info["name"])
        self.name_title.pack(side="left")
        self.name_label.pack(side="left")
        self.name_frame.pack()

        # Divides the remainder stats down the middle
        self.halfway_frame = ttk.Frame(self)
        self.left_half = ttk.Frame(self.halfway_frame)
        self.right_half = ttk.Frame(self.halfway_frame)

        # Top grid of the left half is the skills
        self.skill_grid = ttk.Frame(self.left_half)
        self.skill_grid.rowconfigure(0, weight=1)
        self.skill_grid.rowconfigure(1, weight=1)
        self.skill_grid.rowconfigure(2, weight=1)
        self.skill_grid.rowconfigure(3, weight=1)
        self.skill_grid.columnconfigure(0, weight=1)
        self.skill_grid.columnconfigure(1, weight=1)

        self.pilot_title = ttk.Label(self.skill_grid, text="Pilot:")
        self.pilot_label = ttk.Label(self.skill_grid, text=commander_info["pilot"])
        self.fighter_title = ttk.Label(self.skill_grid, text="Fighter:")
        self.fighter_label = ttk.Label(self.skill_grid, text=commander_info["fighter"])
        self.trader_title = ttk.Label(self.skill_grid, text="Trader:")
        self.trader_label = ttk.Label(self.skill_grid, text=commander_info["trader"])
        self.engineer_title = ttk.Label(self.skill_grid, text="Engineer:")
        self.engineer_label = ttk.Label(self.skill_grid, text=commander_info["engineer"])

        self.pilot_title.grid(row=0, column=0)
        self.pilot_label.grid(row=0, column=1)
        self.fighter_title.grid(row=1, column=0)
        self.fighter_label.grid(row=1, column=1)
        self.trader_title.grid(row=2, column=0)
        self.trader_label.grid(row=2, column=1)
        self.engineer_title.grid(row=3, column=0)
        self.engineer_label.grid(row=3, column=1)

        self.skill_grid.pack()

        # Bottom half for the left side is a few titles
        self.lower_left_frame = ttk.Frame(self.left_half)
        self.networth_title = ttk.Label(self.lower_left_frame, text="Net Worth:")
        self.rep_label = ttk.Label(self.lower_left_frame, text="Reputation:")
        self.record_label = ttk.Label(self.lower_left_frame, text="Police Record:")
        self.difficulty_label = ttk.Label(self.lower_left_frame, text="Difficulty:")

        self.networth_title.pack()
        self.rep_label.pack()
        self.record_label.pack()
        self.difficulty_label.pack()

        self.lower_left_frame.pack()
        self.left_half.pack(side="left")

        # Right top grid is kills, time played, cash, debt
        self.right_top_grid = ttk.Frame(self.right_half)
        self.right_top_grid.rowconfigure(0, weight=1)
        self.right_top_grid.rowconfigure(1, weight=1)
        self.right_top_grid.rowconfigure(2, weight=1)
        self.right_top_grid.rowconfigure(3, weight=1)
        self.right_top_grid.columnconfigure(0, weight=1)
        self.right_top_grid.columnconfigure(1, weight=1)

        self.kills_title = ttk.Label(self.right_top_grid, text="Kills:")
        self.kills_label = ttk.Label(self.right_top_grid, text=commander_info["kills"])
        self.time_title = ttk.Label(self.right_top_grid, text="Time Played:")
        self.time_label = ttk.Label(self.right_top_grid, text=commander_info["time"])
        self.cash_title = ttk.Label(self.right_top_grid, text="Cash:")
        self.cash_label = ttk.Label(self.right_top_grid, text=commander_info["cash"])
        self.debt_title = ttk.Label(self.right_top_grid, text="Debt:")
        self.debt_label = ttk.Label(self.right_top_grid, text=commander_info["debt"])

        self.kills_title.grid(row=0, column=0)
        self.kills_label.grid(row=0, column=1)
        self.time_title.grid(row=1, column=0)
        self.time_label.grid(row=1, column=1)
        self.cash_title.grid(row=2, column=0)
        self.cash_label.grid(row=2, column=1)
        self.debt_title.grid(row=3, column=0)
        self.debt_label.grid(row=3, column=1)

        self.right_top_grid.pack()

        # Bottom right is the net worth, reputation, police record, and difficulty values
        self.lower_right_frame = ttk.Frame(self.right_half)

        self.networth_label = ttk.Label(self.lower_right_frame, text=commander_info["net_worth"])
        self.rep_label = ttk.Label(self.lower_right_frame, text=commander_info["rep"])
        self.record_label = ttk.Label(self.lower_right_frame, text=commander_info["record"])
        self.difficulty_label = ttk.Label(self.lower_right_frame, text=commander_info["difficulty"])

        self.networth_label.pack()
        self.rep_label.pack()
        self.record_label.pack()
        self.difficulty_label.pack()

        self.lower_right_frame.pack()
        self.right_half.pack(side="right")

        self.halfway_frame.pack()

        # Bottom of the screen has context buttons to switch to questlog, ship info, and special cargo
        self.context_buttons_frame = ttk.Frame(self)
        self.quest_button = ttk.Button(
            self.context_buttons_frame,
            text="Quests",
            command=lambda: self.manager.go_to_screen("L"),
        )
        self.ship_info_button = ttk.Button(
            self.context_buttons_frame,
            text="Ship",
            command=lambda: self.manager.go_to_screen("A"),
        )
        self.special_cargo_button = ttk.Button(
            self.context_buttons_frame,
            text="Special Cargo",
            command=lambda: self.manager.go_to_screen("U"),
        )

        self.quest_button.pack(side="left")
        self.ship_info_button.pack(side="left")
        self.special_cargo_button.pack(side="left")

        self.context_buttons_frame.pack(side="bottom", expand=True)


class ShipInfo(Screen):

    """View the current ship's stats and equipment"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        """"""
        # Bottom of the screen has context buttons to switch to commander status, questlog, and special cargo
        self.context_buttons_frame = ttk.Frame(self)
        self.commander_status_button = ttk.Button(
            self.context_buttons_frame,
            text="Status",
            command=lambda: self.manager.go_to_screen("C"),
        )
        self.quest_button = ttk.Button(
            self.context_buttons_frame,
            text="Quests",
            command=lambda: self.manager.go_to_screen("L"),
        )
        self.special_cargo_button = ttk.Button(
            self.context_buttons_frame,
            text="Special Cargo",
            command=lambda: self.manager.go_to_screen("U"),
        )

        self.commander_status_button.pack(side="left")
        self.quest_button.pack(side="left")
        self.special_cargo_button.pack(side="left")

        self.context_buttons_frame.pack(side="bottom", expand=True)


class SpecialCargo(Screen):

    """View special cargo items (i.e. quest items)"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        """"""
        # Bottom of the screen has context buttons to switch to commander status, ship info, and questlog
        self.context_buttons_frame = ttk.Frame(self)
        self.commander_status_button = ttk.Button(
            self.context_buttons_frame,
            text="Status",
            command=lambda: self.manager.go_to_screen("C"),
        )
        self.ship_info_button = ttk.Button(
            self.context_buttons_frame,
            text="Ship",
            command=lambda: self.manager.go_to_screen("A"),
        )
        self.quest_button = ttk.Button(
            self.context_buttons_frame,
            text="Quests",
            command=lambda: self.manager.go_to_screen("L"),
        )

        self.commander_status_button.pack(side="left")
        self.ship_info_button.pack(side="left")
        self.quest_button.pack(side="left")

        self.context_buttons_frame.pack(side="bottom", expand=True)


class Personnel(Screen):

    """View any hired crew and their stats"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)


class Quests(Screen):

    """View any active quests"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        """"""
        quests = actions.get_quests()

        for _, quest in enumerate(quests):
            ttk.Label(self, text=quest).pack()

        # Bottom of the screen has context buttons to switch to commander status, ship info, and special cargo
        self.context_buttons_frame = ttk.Frame(self)
        self.commander_status_button = ttk.Button(
            self.context_buttons_frame,
            text="Status",
            command=lambda: self.manager.go_to_screen("C"),
        )
        self.ship_info_button = ttk.Button(
            self.context_buttons_frame,
            text="Ship",
            command=lambda: self.manager.go_to_screen("A"),
        )
        self.special_cargo_button = ttk.Button(
            self.context_buttons_frame,
            text="Special Cargo",
            command=lambda: self.manager.go_to_screen("U"),
        )

        self.commander_status_button.pack(side="left")
        self.ship_info_button.pack(side="left")
        self.special_cargo_button.pack(side="left")

        self.context_buttons_frame.pack(side="bottom", expand=True)
