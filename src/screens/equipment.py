"""Equipment buying and selling screens."""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

import src.constants as c
import src.ui_actions as actions

from .screens import Screen

if TYPE_CHECKING:
    from src.screens.screen_manager import ScreenManager  # ruff:ignore[runtime-import-in-type-checking-block]


class BuyEquipment(Screen):

    """Shop interface for buying things like weapons and shields"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        """Show equipment available at this system and its purchase price."""
        self.table_frame = ttk.Frame(self)
        self.table_frame.columnconfigure(1, weight=1)

        sold_equipment = actions.get_equip_sold()
        for row, value in enumerate(sold_equipment):
            unavailable_marker, equipment_name, price = value

            if not unavailable_marker:
                ttk.Button(self.table_frame, text="Buy", command=actions.buy_equipment).grid(row=row, column=0)
            else:
                ttk.Label(self.table_frame, text="   ").grid(row=row, column=0)

            ttk.Label(self.table_frame, text=equipment_name).grid(row=row, column=1, sticky="w")
            ttk.Label(self.table_frame, text=price.capitalize()).grid(row=row, column=2, sticky="e")

        self.table_frame.pack(fill="x", expand=True)

        # Keep the price/status column at the right edge of the screen.
        self.credits_label = ttk.Label(self, text=actions.get_credits())
        self.credits_label.place(relx=1, rely=1, anchor="se")


class SellEquipment(Screen):

    """Shop interface for selling things like weapons and shields"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        """Show the equipment the ship can sell, grouped by equipment type."""
        self.table_frame = ttk.Frame(self)
        self.table_frame.columnconfigure(0, weight=1)
        for row, weight in enumerate((3, 0, 3, 0, 4)):
            self.table_frame.rowconfigure(row, weight=weight)

        weapon_frame = ttk.Frame(self.table_frame)
        weapon_frame.columnconfigure(1, weight=1)
        ttk.Button(weapon_frame, text="Sell", command=actions.sell_equipment).grid(row=0, column=0, sticky="w")
        ttk.Label(weapon_frame, text="Pulse laser").grid(row=0, column=1, sticky="w", padx=5 * c.SCALAR)
        ttk.Label(weapon_frame, text="1500 cr.").grid(row=0, column=2, sticky="e")
        weapon_frame.grid(row=0, column=0, sticky="new")

        tk.Frame(self.table_frame, background=c.FRG_HEX, height=2 * c.SCALAR).grid(
            row=1, column=0, sticky="ew"
        )

        ttk.Label(self.table_frame, text="No shields").grid(row=2, column=0, sticky="w", padx=22 * c.SCALAR)

        tk.Frame(self.table_frame, background=c.FRG_HEX, height=2 * c.SCALAR).grid(
            row=3, column=0, sticky="ew"
        )

        ttk.Label(self.table_frame, text="No gadgets").grid(row=4, column=0, sticky="w", padx=22 * c.SCALAR)
        self.table_frame.pack(fill="both", expand=True)

        self.credits_label = ttk.Label(self, text=actions.get_credits())
        self.credits_label.place(relx=1, rely=1, anchor="se")
