"""Banking, shipyard, and ship purchasing screens."""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING

import src.economy as e
import src.ui_actions as actions
from src.constants import Size

from .screens import Screen

if TYPE_CHECKING:
    from src.screens.screen_manager import ScreenManager  # ruff:ignore[runtime-import-in-type-checking-block]

FUEL_STATUS = "You have fuel to fly {0} parsecs."
FULL_TANK = "Your tank cannot hold more fuel."
HULL_STATUS = "Your hull strength is at {0}%."
FULL_HULL = "No repairs are needed."
SHIP_SALES = "No new ships are for sale."
ESCAPE_POD = "No escape pods are for sale."
NO_QUARTER = "No quarters available"
NO_HIRE = "No one for hire"


class Bank(Screen):

    """Bank interface for managing loans and insurance"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        """"""
        # Loan Frame
        self.loan_frame = ttk.Frame(self)
        ttk.Label(self.loan_frame, text="Loan").pack()

        self.loan_grid = ttk.Frame(self.loan_frame)
        ttk.Label(self.loan_grid, text="Current debt:").grid(row=0, column=0, sticky="w")
        ttk.Label(self.loan_grid, text=actions.get_debt()).grid(row=0, column=1, sticky="w")
        ttk.Label(self.loan_grid, text="Maximum loan:").grid(row=1, column=0)
        ttk.Label(self.loan_grid, text=actions.get_max_loan()).grid(row=1, column=1)

        self.loan_grid.pack(expand=True, fill="x")
        ttk.Button(self.loan_frame, text="Get Loan", command=actions.get_loan).pack()
        self.loan_frame.pack(expand=True, fill="x")

        # Insurance Frame
        self.insurance_frame = ttk.Frame(self)
        ttk.Label(self.insurance_frame, text="Insurance").pack()

        self.insurance_grid = ttk.Frame(self.insurance_frame)
        ttk.Label(self.insurance_grid, text="Current ship:").grid(row=0, column=0)
        ttk.Label(self.insurance_grid, text="No-claim:").grid(row=1, column=0)
        ttk.Label(self.insurance_grid, text="Costs:").grid(row=2, column=0)
        ttk.Label(self.insurance_grid, text=actions.get_ship_value()).grid(row=0, column=1)
        ttk.Label(self.insurance_grid, text=actions.get_no_claim()).grid(row=1, column=1)
        ttk.Label(self.insurance_grid, text=actions.get_insurance_rate()).grid(row=2, column=1)

        self.insurance_grid.pack(expand=True, fill="x")
        ttk.Button(self.insurance_frame, text="Buy Insurance", command=actions.buy_insurance).pack()
        self.insurance_frame.pack(expand=True, fill="x")

        # Current credits
        self.credits_label = ttk.Label(self, text=actions.get_credits())
        self.credits_label.place(relx=1, rely=1, anchor="se")


class Shipyard(Screen):

    """Hopefully self explanatory"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        """"""
        # Fuel Frame
        self.fuel_frame = ttk.Frame(self)
        ttk.Label(self.fuel_frame, text=FUEL_STATUS.format(0), font=("Palm Pilot Small", 14)).pack()
        ttk.Button(self.fuel_frame, text="Refuel", command=actions.buy_fuel).pack()
        self.fuel_frame.pack(side="top", fill="both", expand=True)

        # Hull Frame
        self.hull_frame = ttk.Frame(self)
        ttk.Label(self.hull_frame, text=HULL_STATUS.format(0), font=("Palm Pilot Small", 14)).pack()
        ttk.Button(self.hull_frame, text="Repair", command=actions.repair).pack()
        self.hull_frame.pack(side="top", fill="both", expand=True)

        # Escape Pod Frame
        self.escape_pod_frame = ttk.Frame(self)
        ttk.Label(self.escape_pod_frame, text=ESCAPE_POD, font=("Palm Pilot Small", 14)).pack()
        ttk.Button(self.escape_pod_frame, text="Buy Escape Pod", command=actions.buy_pod).pack()
        self.escape_pod_frame.pack(side="top", fill="both", expand=True)

        # Ship Sales Frame
        self.ship_sales_frame = ttk.Frame(self)
        ttk.Label(self.ship_sales_frame, text=SHIP_SALES, font=("Palm Pilot Small", 14)).pack()
        ttk.Button(self.ship_sales_frame, text="Buy Ship", command=actions.buy_ship).pack()
        self.ship_sales_frame.pack(side="top", fill="both", expand=True)


class BuyShip(Screen):

    """Specific sub-menu for purchasing a new ship"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        """Show purchasable ships with prices and specifications."""
        ship_names = e.Ship.sale_lst()
        ships_for_sale = [ship for ship in e.SHIPS.values() if ship.name in ship_names]

        self.table_frame = ttk.Frame(self)
        self.table_frame.columnconfigure(1, weight=1)
        for row, ship in enumerate(ships_for_sale):
            ttk.Button(self.table_frame, text="Buy", command=actions.buy_ship).grid(row=row, column=0)
            ttk.Label(self.table_frame, text=ship.name).grid(row=row, column=1, sticky="w")
            ttk.Button(
                self.table_frame,
                text="Info",
                command=lambda selected_ship=ship: self.show_ship_info(selected_ship),
            ).grid(row=row, column=2)
            ttk.Label(self.table_frame, text=f"{ship.price} cr.").grid(row=row, column=3, sticky="e")

        self.table_frame.pack(fill="x", expand=True)

        self.credits_label = ttk.Label(self, text=actions.get_credits())
        self.credits_label.place(relx=1, rely=1, anchor="se")

    @staticmethod
    def show_ship_info(ship: e.Ship) -> None:
        """Display the selected ship's specifications."""
        details = (
            f"Size: {Size.name(ship.size)}\n"
            f"Hull: {ship.hull}\n"
            f"Cargo: {ship.cargo} bays\n"
            f"Crew: {ship.crew}\n"
            f"Fuel: {ship.fuel} parsecs\n"
            f"Weapon slots: {ship.weapon_slots}\n"
            f"Shield slots: {ship.shield_slots}\n"
            f"Gadget slots: {ship.gadget_slots}\n"
            f"Price: {ship.price} cr."
        )
        messagebox.showinfo(ship.name, details)
