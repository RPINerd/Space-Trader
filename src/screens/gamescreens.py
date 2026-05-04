"""
    Game Screens Module

    Defines the various screens that make up the game, such as the system info screen, shipyard, etc.
"""

from random import randint
from tkinter import ttk

import src.ui_actions as actions

from .screens import Screen

FUEL_STATUS = "You have fuel to fly {0} parsecs."
FULL_TANK = "Your tank cannot hold more fuel."
HULL_STATUS = "Your hull strength is at {0}%."
FULL_HULL = "No repairs are needed."
SHIP_SALES = "No new ships are for sale."
ESCAPE_POD = "No escape pods are for sale."
NO_QUARTER = "No quarters available"
NO_HIRE = "No one for hire"


class SystemInfo(Screen):

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)

    def create_widgets(self):

        system_info, pressure = actions.get_system_info()

        # Info Frame
        self.info_frame = ttk.Frame(self)
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.columnconfigure(1, weight=1)
        info_headings = ["Name:", "Size:", "Tech Level:", "Government:", "Resources:", "Police:", "Pirates:"]
        for i, heading in enumerate(info_headings):
            ttk.Label(self.info_frame, text=heading, style="Heading.TLabel", justify="left").grid(
                row=i, column=0, sticky="ew"
            )
        # ! Placeholder content
        for i, stat in enumerate(system_info):
            ttk.Label(self.info_frame, text=stat, justify="left").grid(row=i, column=1, sticky="ew")
        self.info_frame.pack(fill="x", expand=True)

        # Pressure Frame
        self.pressure_frame = ttk.Frame(self)
        ttk.Label(self.pressure_frame, text=pressure).grid(row=0, column=0)
        self.pressure_frame.pack(side="top", fill="both", expand=True)

        # Shortcut Frame
        self.shortcut_frame = ttk.Frame(self)
        ttk.Button(self.shortcut_frame, text="News", command=actions.buy_news).pack(side="left")
        self.shortcut_frame.pack(side="top", fill="both", expand=True)

    def change_screen(self, event):
        # TODO probably can be a super method
        pass


class ShortRange(Screen):

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)


class LongRange(Screen):

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)


class TargetSystem(Screen):

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)


class AvgPrices(Screen):

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)


class BuyCargo(Screen):

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        self.table_frame = ttk.Frame(self)
        for i, value in enumerate(actions.get_ware_list()):
            ttk.Button(self.table_frame, text=randint(0, 42)).grid(row=i, column=0)
            ttk.Label(self.table_frame, text=value).grid(row=i, column=1)
            ttk.Button(self.table_frame, text="Max", command=actions.buy_good).grid(row=i, column=2)
            ttk.Label(self.table_frame, text="1234 cr.").grid(row=i, column=3)
        self.table_frame.pack(fill="x", expand=True)

        # Current bays
        self.bays_label = ttk.Label(self, text=actions.get_bays())
        self.bays_label.place(relx=0, rely=1, anchor="sw")

        # Current credits
        self.credits_label = ttk.Label(self, text=actions.get_credits())
        self.credits_label.place(relx=1, rely=1, anchor="se")


class SellCargo(Screen):

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        self.table_frame = ttk.Frame(self)
        for i, value in enumerate(actions.get_ware_list()):
            ttk.Button(self.table_frame, text="0").grid(row=i, column=0)
            ttk.Label(self.table_frame, text=value).grid(row=i, column=1)
            ttk.Button(self.table_frame, text="All", command=actions.sell_good).grid(row=i, column=2)
            ttk.Label(self.table_frame, text="15cr").grid(row=i, column=3)
        self.table_frame.pack(fill="x", expand=True)

        # Current bays
        self.bays_label = ttk.Label(self, text=actions.get_bays())
        self.bays_label.place(relx=0, rely=1, anchor="sw")

        # Current credits
        self.credits_label = ttk.Label(self, text=actions.get_credits())
        self.credits_label.place(relx=1, rely=1, anchor="se")


class BuyEquipment(Screen):

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        self.table_frame = ttk.Frame(self)

        sold_equipment = actions.get_equip_sold()
        for i, value in enumerate(sold_equipment):

            sold = value[0] == ""
            # First column are Buy buttons for each equipment
            if sold:
                ttk.Button(self.table_frame, text="Buy", command=actions.buy_equipment).grid(row=i, column=0)
            else:
                ttk.Label(self.table_frame, text="   ").grid(
                    row=i,
                    column=0,
                )

            # Second column is the equipment name
            ttk.Label(self.table_frame, text=value[1]).grid(row=i, column=1, sticky="w")

            # Third column is the cost for each equipment
            ttk.Label(self.table_frame, text=value[2]).grid(row=i, column=2)

        self.table_frame.pack(fill="x", expand=True)

        # Current credits
        self.credits_label = ttk.Label(self, text=actions.get_credits())
        self.credits_label.place(relx=1, rely=1, anchor="se")


class SellEquipment(Screen):

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)


class Bank(Screen):

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)

    def create_widgets(self):

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

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)

    def create_widgets(self):

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

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)


class CommanderInfo(Screen):

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)

    def create_widgets(self):

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

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)

    def create_widgets(self):

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

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)

    def create_widgets(self):

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

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)


class Quests(Screen):

    def __init__(self, parent, screen_title, manager) -> None:
        super().__init__(parent, screen_title, manager)

    def create_widgets(self):

        # commander_info = actions.get_commander_info()
        # quests = commander_info["quests"]
        # if not quests:
        quests = ["There are no open quests."]

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
