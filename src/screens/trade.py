"""Cargo trading screens."""

import logging
import tkinter as tk
from tkinter import simpledialog, ttk
from typing import TYPE_CHECKING

import src.constants as c
from src.actions.finance import get_credits
from src.actions.trade import (
    buy_good,
    get_bays,
    get_ware_list,
    sell_good,
)

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
        commander = c.GAME["commander"]
        planet = c.GAME["universe"].planets[commander.currentSystem]
        self.table_frame = ttk.Frame(self)
        self.stock_buttons = []
        self.price_labels = []
        for i, value in enumerate(get_ware_list()):
            stock_button = ttk.Button(
                self.table_frame,
                text=str(int(planet.trade_items[i])),
                command=lambda ware_id=i: self._prompt_buy_amount(ware_id),
                width=4,
            )
            stock_button.grid(row=i, column=0)
            self.stock_buttons.append(stock_button)
            ttk.Label(self.table_frame, text=value).grid(row=i, column=1)
            ttk.Button(self.table_frame, text="Max", command=lambda ware_id=i: self._buy_good(ware_id)).grid(
                row=i, column=2
            )
            price_label = ttk.Label(self.table_frame, text=self._price_text(planet.trade_prices[i]))
            price_label.grid(row=i, column=3)
            self.price_labels.append(price_label)
        self.table_frame.pack(fill="x", expand=True)

        # Current bays
        self.bays_label = ttk.Label(self, text=get_bays())
        self.bays_label.place(relx=0, rely=1, anchor="sw")

        # Current credits
        self.credits_label = ttk.Label(self, text=get_credits())
        self.credits_label.place(relx=1, rely=1, anchor="se")

    @staticmethod
    def _price_text(price: int) -> str:
        return f"{price} cr." if price > 0 else "not sold"

    def _buy_good(self, ware_id: int, amount: int | None = None) -> None:
        buy_good(ware_id, amount)
        commander = c.GAME["commander"]
        planet = c.GAME["universe"].planets[commander.currentSystem]
        self.stock_buttons[ware_id].configure(text=str(int(planet.trade_items[ware_id])))
        self.bays_label.configure(text=get_bays())
        self.credits_label.configure(text=get_credits())

    def _prompt_buy_amount(self, ware_id: int) -> None:
        amount = simpledialog.askinteger(
            "Buy Cargo",
            f"How many {get_ware_list()[ware_id]} do you want to buy?",
            parent=self,
            minvalue=1,
        )
        if amount is not None:
            self._buy_good(ware_id, amount)


class SellCargo(Screen):

    """Interface for selling trade goods"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        """"""
        commander = c.GAME["commander"]
        planet = c.GAME["universe"].planets[commander.currentSystem]
        self.table_frame = ttk.Frame(self)
        self.cargo_buttons = []
        self.price_labels = []
        for i, value in enumerate(get_ware_list()):
            cargo_button = ttk.Button(
                self.table_frame,
                text=str(commander.cargo[i]),
                command=lambda ware_id=i: self._prompt_sell_amount(ware_id),
                width=4,
            )
            cargo_button.grid(row=i, column=0)
            self.cargo_buttons.append(cargo_button)
            ttk.Label(self.table_frame, text=value).grid(row=i, column=1)
            ttk.Button(self.table_frame, text="All", command=lambda ware_id=i: self._sell_good(ware_id)).grid(
                row=i, column=2
            )
            price_label = ttk.Label(self.table_frame, text=self._price_text(planet.trade_prices[i]))
            price_label.grid(row=i, column=3)
            self.price_labels.append(price_label)
        self.table_frame.pack(fill="x", expand=True)

        # Current bays
        self.bays_label = ttk.Label(self, text=get_bays())
        self.bays_label.place(relx=0, rely=1, anchor="sw")

        # Current credits
        self.credits_label = ttk.Label(self, text=get_credits())
        self.credits_label.place(relx=1, rely=1, anchor="se")

    @staticmethod
    def _price_text(price: int) -> str:
        return f"{price} cr." if price > 0 else "no trade"

    def _sell_good(self, ware_id: int, amount: int | None = None) -> None:
        sell_good(ware_id, amount)
        commander = c.GAME["commander"]
        self.cargo_buttons[ware_id].configure(text=str(commander.cargo[ware_id]))
        self.bays_label.configure(text=get_bays())
        self.credits_label.configure(text=get_credits())

    def _prompt_sell_amount(self, ware_id: int) -> None:
        amount = simpledialog.askinteger(
            "Sell Cargo",
            f"How many {get_ware_list()[ware_id]} do you want to sell?",
            parent=self,
            minvalue=1,
        )
        if amount is not None:
            self._sell_good(ware_id, amount)
