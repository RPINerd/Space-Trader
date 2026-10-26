"""Cargo trading screens."""

import logging
import tkinter as tk
from random import randint
from tkinter import ttk
from typing import TYPE_CHECKING

from src.actions.finance import get_credits
from src.actions.trade import buy_good, get_bays, get_ware_list, sell_good

from .screens import Screen

if TYPE_CHECKING:
    from src.screens.screen_manager import ScreenManager  # ruff:ignore[runtime-import-in-type-checking-block]

logger = logging.getLogger(__name__)


class AvgPrices(Screen):

    """Display average prices of trade goods that are available in system"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        logger.debug("Initializing AvgPrices screen, the parent class is %s", type(parent))
        super().__init__(parent, screen_title, manager)


class BuyCargo(Screen):

    """Interface for buying trade goods"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        """"""
        self.table_frame = ttk.Frame(self)
        for i, value in enumerate(get_ware_list()):
            ttk.Button(self.table_frame, text=randint(0, 42)).grid(row=i, column=0)
            ttk.Label(self.table_frame, text=value).grid(row=i, column=1)
            ttk.Button(self.table_frame, text="Max", command=buy_good).grid(row=i, column=2)
            ttk.Label(self.table_frame, text="1234 cr.").grid(row=i, column=3)
        self.table_frame.pack(fill="x", expand=True)

        # Current bays
        self.bays_label = ttk.Label(self, text=get_bays())
        self.bays_label.place(relx=0, rely=1, anchor="sw")

        # Current credits
        self.credits_label = ttk.Label(self, text=get_credits())
        self.credits_label.place(relx=1, rely=1, anchor="se")


class SellCargo(Screen):

    """Interface for selling trade goods"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        """"""
        self.table_frame = ttk.Frame(self)
        for i, value in enumerate(get_ware_list()):
            ttk.Button(self.table_frame, text="0").grid(row=i, column=0)
            ttk.Label(self.table_frame, text=value).grid(row=i, column=1)
            ttk.Button(self.table_frame, text="All", command=sell_good).grid(row=i, column=2)
            ttk.Label(self.table_frame, text="15cr").grid(row=i, column=3)
        self.table_frame.pack(fill="x", expand=True)

        # Current bays
        self.bays_label = ttk.Label(self, text=get_bays())
        self.bays_label.place(relx=0, rely=1, anchor="sw")

        # Current credits
        self.credits_label = ttk.Label(self, text=get_credits())
        self.credits_label.place(relx=1, rely=1, anchor="se")
