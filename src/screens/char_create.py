"""Character creation screen"""
import logging
import tkinter as tk
from tkinter import ttk

from ..commander import Commander
from ..constants import BKG_HEX, FRG_HEX, GAME, Difficulty

logger = logging.getLogger(__name__)


class StatAdjuster(ttk.Frame):

    """A frame that contains a label, a decrement button, a value label, and an increment button."""

    def __init__(self, parent, label_text: str, initial_value: int, row: int, column: int, **kwargs: dict) -> None:
        """"""
        super().__init__(parent, **kwargs)

        global points_pool
        self.value = tk.IntVar(value=initial_value)
        self.label = ttk.Label(self, text=label_text)
        self.decrement = ttk.Button(self, text="-", command=self.decrement_value)
        self.value_label = ttk.Label(self, textvariable=self.value)
        self.increment = ttk.Button(self, text="+", command=self.increment_value)

        self.label.grid(row=row, column=column)
        self.decrement.grid(row=row, column=column + 1)
        self.value_label.grid(row=row, column=column + 2)
        self.increment.grid(row=row, column=column + 3)

    def get_value(self) -> int:
        """Returns the current value of the stat adjuster."""
        return self.value.get()

    def decrement_value(self) -> None:
        """Decrements the value of the stat adjuster if possible."""
        if self.value.get() == 1:
            return
        self.value.set(max(self.value.get() - 1, 1))
        points_pool.set(points_pool.get() + 1)

    def increment_value(self) -> None:
        """Increments the value of the stat adjuster if possible."""
        if points_pool.get() == 0 or self.value.get() == 10:
            return
        self.value.set(min(self.value.get() + 1, 10))
        points_pool.set(points_pool.get() - 1)


class CreateCommander(ttk.Frame):

    """The screen for creating a new commander."""

    def __init__(self, parent) -> None:
        self.parent = parent
        super().__init__(parent)
        """Initializes the CreateCommander screen and places it on the parent window."""
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets for the CreateCommander screen."""
        # Initial values
        self.cmdr_name = tk.StringVar(value="Jameson")
        self.diff_current_value = 2
        global points_pool
        points_pool = tk.IntVar(value=0)

        # Title Bar
        self.header = ttk.Label(
            self,
            text="New Commander",
            style="Title.TLabel",
            # font=("Palm Pilot Bold", 28),
            anchor="center",
            background=FRG_HEX,
            foreground=BKG_HEX,
        )
        self.header.pack(expand=True, fill="x")

        # Commander name
        self.name_frame = ttk.Frame(self)
        self.name_label = ttk.Label(self.name_frame, text="Name:")
        self.name_entry = ttk.Entry(self.name_frame, textvariable=self.cmdr_name)
        self.name_label.pack(side="left")
        self.name_entry.pack(side="left")

        # Game difficulty selection
        self.difficulty_frame = ttk.Frame(self)
        self.difficulty_label = ttk.Label(self.difficulty_frame, text="Difficulty:")
        self.difficulty_dec = ttk.Button(self.difficulty_frame, style="TButton", text="-", command=self.dec_difficulty)
        self.difficulty_current = ttk.Label(
            self.difficulty_frame,
            text=Difficulty.name(self.diff_current_value),
        )
        self.difficulty_inc = ttk.Button(self.difficulty_frame, text="+", command=self.inc_difficulty)
        self.difficulty_label.pack(side="left")
        self.difficulty_dec.pack(side="left")
        self.difficulty_current.pack(side="left")
        self.difficulty_inc.pack(side="left")

        # Skill points allocation grid
        self.skills_frame = ttk.Frame(self)
        self.points_label = ttk.Label(self.skills_frame, text="Skill Points:")
        self.points_current = ttk.Label(self.skills_frame, textvariable=points_pool)
        self.pilot_skill = StatAdjuster(self.skills_frame, "Pilot:", 5, 0, 0)
        self.fighter_skill = StatAdjuster(self.skills_frame, "Fighter:", 5, 1, 0)
        self.trader_skill = StatAdjuster(self.skills_frame, "Trader:", 5, 2, 0)
        self.engineer_skill = StatAdjuster(self.skills_frame, "Engineer:", 5, 3, 0)

        self.points_label.pack(expand=True, fill="x")
        self.points_current.pack(expand=True, fill="x")
        self.pilot_skill.pack(expand=True, fill="x")
        self.fighter_skill.pack(expand=True, fill="x")
        self.trader_skill.pack(expand=True, fill="x")
        self.engineer_skill.pack(expand=True, fill="x")

        # Button to start the game
        self.start_button = ttk.Button(self, text="OK", command=self.cmdr_create, width=15)

        self.name_frame.pack(expand=True, fill="x")
        self.difficulty_frame.pack(expand=True, fill="x")
        self.skills_frame.pack(expand=True, fill="x")
        self.start_button.pack(expand=True)

    def dec_difficulty(self) -> None:
        """Decreases the difficulty of the game."""
        logger.debug("Decreasing difficulty")
        logger.debug("Current value: %s", self.diff_current_value)
        new_difficulty = max(self.diff_current_value - 1, 0)
        logger.debug("New value: %s", new_difficulty)
        if new_difficulty == 0:
            self.difficulty_dec["state"] = "disabled"
        self.difficulty_inc["state"] = "enabled"
        self.difficulty_current["text"] = Difficulty.name(new_difficulty)
        self.diff_current_value = new_difficulty

    def inc_difficulty(self) -> None:
        """Increases the difficulty of the game."""
        logger.debug("Increasing difficulty")
        logger.debug("Current value: %s", self.diff_current_value)
        new_difficulty = min(self.diff_current_value + 1, 4)
        logger.debug("New value: %s", new_difficulty)
        if new_difficulty == 4:
            self.difficulty_inc["state"] = "disabled"
        self.difficulty_dec["state"] = "enabled"
        self.difficulty_current["text"] = Difficulty.name(new_difficulty)
        self.diff_current_value = new_difficulty

    def cmdr_create(self) -> None:
        """
        Creates a new commander based on the inputted values

        # TODO Show a message box for invalid submissions
        """
        if points_pool.get() != 0:
            logger.warning("Commander creation failed: unspent skill points remaining")
            return
        if self.cmdr_name.get() == "":
            logger.warning("Commander creation failed: no name entered")
            return
        cmdr = Commander(
            self.cmdr_name.get(),
            self.pilot_skill.get_value(),
            self.fighter_skill.get_value(),
            self.trader_skill.get_value(),
            self.engineer_skill.get_value(),
        )
        GAME["commander"] = cmdr
        GAME["difficulty"] = self.diff_current_value
        logger.debug("Created commander: %s", cmdr.pprint())
        self.destroy()
        self.parent.manager.build_screens()
