"""System information and navigation chart screens."""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

import src.constants as c
from src.actions.information import get_system_info
from src.actions.trade import buy_news
from src.constants import Size, TechLevel
from src.universe import Planet

from .screens import Screen

if TYPE_CHECKING:
    from src.screens.screen_manager import ScreenManager  # ruff:ignore[runtime-import-in-type-checking-block]


class SystemInfo(Screen):

    """The system info screen; appears immediately after warp to a new system"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        """"""
        system_info, pressure = get_system_info()

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
        ttk.Button(self.shortcut_frame, text="News", command=buy_news).pack(side="left")
        self.shortcut_frame.pack(side="top", fill="both", expand=True)


class ShortRange(Screen):

    """Short Range Chart; where player selects nearby system to warp to"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        """Create the zoomed chart of systems near the current system."""
        self.universe = c.GAME["universe"]
        commander = c.GAME["commander"]
        self.current_planet = self.universe.planets[commander.currentSystem]
        self.selected_planet = self.current_planet
        self.chart_width = 140 * c.SCALAR
        self.chart_height = 140 * c.SCALAR
        self.chart_scale = self.chart_width / (2 * c.MAX_DISTANCE)

        self.map_canvas = tk.Canvas(
            self,
            bg=c.BKG_HEX,
            width=self.chart_width,
            height=self.chart_height,
            highlightthickness=0,
        )
        self.map_canvas.pack(side="top", padx=3 * c.SCALAR)
        self.map_canvas.bind("<Button-1>", self._on_map_click)
        self._redraw_chart()

    def on_show(self) -> None:
        """Refresh the chart when returning to it after changing systems."""
        commander = c.GAME["commander"]
        current_planet = self.universe.planets[commander.currentSystem]
        if current_planet != self.current_planet:
            self.selected_planet = current_planet
        self._redraw_chart()

    @staticmethod
    def _is_in_chart(planet: Planet, center: Planet) -> bool:
        """Return whether a system falls inside the short-range chart bounds."""
        return (
            abs(planet.x - center.x) <= c.MAX_DISTANCE
            and abs(planet.y - center.y) <= c.MAX_DISTANCE
        )

    def _chart_position(self, planet: Planet) -> tuple[float, float]:
        """Map a system's coordinates to its position on the centered chart."""
        center_x = self.chart_width / 2
        center_y = self.chart_height / 2
        return (
            center_x + (planet.x - self.current_planet.x) * self.chart_scale,
            center_y + (planet.y - self.current_planet.y) * self.chart_scale,
        )

    @staticmethod
    def _is_click_near_system(click_x: float, click_y: float, system_x: float, system_y: float) -> bool:
        """Return whether a click falls within the small system-marker hit area."""
        margin = 4 * c.SCALAR
        return (click_x - system_x) ** 2 + (click_y - system_y) ** 2 <= margin**2

    def _redraw_chart(self) -> None:
        """Draw nearby systems, their names, and the current fuel range."""
        commander = c.GAME["commander"]
        self.current_planet = self.universe.planets[commander.currentSystem]
        nearby_planets = [
            planet
            for planet in self.universe.planets.values()
            if self._is_in_chart(planet, self.current_planet)
        ]
        self.map_canvas.delete("all")

        center_x, center_y = self._chart_position(self.current_planet)
        radius = commander.ship.fuel * self.chart_scale
        self.map_canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            outline=c.FRG_HEX,
        )

        # Draw labels first so every system marker remains visible.
        for planet in nearby_planets:
            x, y = self._chart_position(planet)
            self.map_canvas.create_text(
                x,
                y - 2 * c.SCALAR,
                text=planet.name,
                anchor="s",
                font=("Palm Pilot Small", 14),
                fill=c.FRG_HEX,
            )

        for planet in nearby_planets:
            x, y = self._chart_position(planet)
            self.map_canvas.create_rectangle(
                x - c.SCALAR,
                y - c.SCALAR,
                x + c.SCALAR,
                y + c.SCALAR,
                fill=c.FRG_HEX,
                outline=c.FRG_HEX,
            )

        selected_x, selected_y = self._chart_position(self.selected_planet)
        arm = 4 * c.SCALAR
        self.map_canvas.create_line(
            selected_x - arm,
            selected_y,
            selected_x + arm,
            selected_y,
            fill=c.FRG_HEX,
        )
        self.map_canvas.create_line(
            selected_x,
            selected_y - arm,
            selected_x,
            selected_y + arm,
            fill=c.FRG_HEX,
        )

    def _on_map_click(self, event: tk.Event) -> None:
        """Select a system only when the click lands near its marker."""
        clickable_planets = [
            planet
            for planet in self.universe.planets.values()
            if self._is_in_chart(planet, self.current_planet)
            and self._is_click_near_system(
                event.x,
                event.y,
                *self._chart_position(planet),
            )
        ]
        if not clickable_planets:
            return

        self.selected_planet = min(
            clickable_planets,
            key=lambda planet: (self._chart_position(planet)[0] - event.x) ** 2
            + (self._chart_position(planet)[1] - event.y) ** 2,
        )
        c.GAME["target_system"] = self.selected_planet
        self.manager.go_to_screen("T")


class LongRange(Screen):

    """Also known as the Galactic chart"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        """"""
        commander = c.GAME["commander"]
        self.universe = c.GAME["universe"]
        self.current_planet = self.universe.planets[commander.currentSystem]
        self.selected_planet = self.current_planet

        self.map_canvas = tk.Canvas(
            self,
            bg=c.BKG_HEX,
            width=c.GALAXYWIDTH * c.SCALAR,
            height=c.GALAXYHEIGHT * c.SCALAR,
            highlightthickness=0,
        )
        self.map_canvas.pack(side="top", padx=3 * c.SCALAR)
        self.map_canvas.bind("<Button-1>", self._on_map_click)

        self.info_frame = ttk.Frame(self)
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.columnconfigure(1, weight=1)
        self.info_frame.columnconfigure(2, weight=1)
        self.name_label = ttk.Label(self.info_frame, anchor="w")
        self.distance_label = ttk.Label(self.info_frame, anchor="center")
        self.find_button = ttk.Button(self.info_frame, text="Find", width=6)
        self.description_label = ttk.Label(self.info_frame, anchor="w")
        self.name_label.grid(row=0, column=0, sticky="ew")
        self.distance_label.grid(row=0, column=1, sticky="ew")
        self.find_button.grid(row=0, column=2, sticky="e")
        self.description_label.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.info_frame.pack(fill="x", padx=2 * c.SCALAR)

        self._redraw_chart()

    def _redraw_chart(self) -> None:
        """Redraw planets, current fuel range, and selected-system details."""
        commander = c.GAME["commander"]
        self.current_planet = self.universe.planets[commander.currentSystem]
        self.map_canvas.delete("all")
        for planet in self.universe.planets.values():
            x, y = planet.x * c.SCALAR, planet.y * c.SCALAR
            self.map_canvas.create_rectangle(
                x - c.SCALAR,
                y - c.SCALAR,
                x + c.SCALAR,
                y + c.SCALAR,
                fill=c.FRG_HEX,
                outline=c.FRG_HEX,
            )

        center_x = self.current_planet.x * c.SCALAR
        center_y = self.current_planet.y * c.SCALAR
        radius = commander.ship.fuel * c.SCALAR
        self.map_canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            outline=c.FRG_HEX,
        )

        selected_x = self.selected_planet.x * c.SCALAR
        selected_y = self.selected_planet.y * c.SCALAR
        arm = 4 * c.SCALAR
        self.map_canvas.create_line(
            selected_x - arm, selected_y, selected_x + arm, selected_y, fill=c.FRG_HEX
        )
        self.map_canvas.create_line(
            selected_x, selected_y - arm, selected_x, selected_y + arm, fill=c.FRG_HEX
        )

        distance = self.current_planet.get_distance(self.selected_planet)
        self.name_label.configure(text=self.selected_planet.name)
        self.distance_label.configure(text=f"{distance} parsecs")
        self.description_label.configure(
            text=(
                f"{Size.name(self.selected_planet.size)} "
                f"{TechLevel.name(self.selected_planet.tech_level)} "
                f"{self.selected_planet.get_government_name()} State"
            )
        )

    def _on_map_click(self, event: tk.Event) -> None:
        """Select the planet nearest the clicked map position."""
        self.selected_planet = min(
            self.universe.planets.values(),
            key=lambda planet: (planet.x - event.x / c.SCALAR) ** 2
            + (planet.y - event.y / c.SCALAR) ** 2,
        )
        self._redraw_chart()


class TargetSystem(Screen):

    """Display info known about the current targeted system"""

    def __init__(self, parent: tk.Misc, screen_title: str, manager: ScreenManager) -> None:
        """"""
        super().__init__(parent, screen_title, manager)

    def create_widgets(self) -> None:
        """Create fields for the currently targeted system's known information."""
        self.info_frame = ttk.Frame(self)
        self.info_labels: list[ttk.Label] = []
        for row, heading in enumerate(Planet.system_info_headers()):
            ttk.Label(self.info_frame, text=heading, style="Heading.TLabel", justify="left").grid(
                row=row, column=0, sticky="ew"
            )
            value_label = ttk.Label(self.info_frame, justify="left")
            value_label.grid(row=row, column=1, sticky="ew")
            self.info_labels.append(value_label)
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.columnconfigure(1, weight=1)
        self.info_frame.pack(fill="x", expand=True)
        self.on_show()

    def on_show(self) -> None:
        """Refresh the displayed details for the current target system."""
        target_planet = c.GAME.get("target_system")
        if target_planet is None:
            commander = c.GAME["commander"]
            target_planet = c.GAME["universe"].planets[commander.currentSystem]
        for label, value in zip(self.info_labels, target_planet.system_info(), strict=True):
            label.configure(text=value)
