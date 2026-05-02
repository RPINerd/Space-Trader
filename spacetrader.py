"""
    Space Trader (PalmOS) | RPINerd, 08/20/24

    An early space strategy RPG game inspired by Elite and Solar Wars for PalmOS.

    This file is the main game file. It shows the splash screen, creates the main window and starts the game.
"""

import configparser
import tkinter as tk
from pathlib import Path
from tkinter import ttk

import src.constants as c
from src.screens.char_create import CreateCommander
from src.screens.screen_manager import ScreenManager
from src.universe import Universe
from src.utils import FontManager


class SpaceTrader(tk.Tk):

    """"""

    def __init__(self, screen_x: int, screen_y: int) -> None:
        """"""
        super().__init__()
        self.title("Space Trader")
        self.resizable(False, False)
        self.geometry(self._center_window(screen_x, screen_y))
        self.bind_all("<KeyPress-Escape>", lambda _: self.quit())
        self._load_assets()
        self._build_styles()
        self.manager = ScreenManager(self)

        # TODO eventually check for existing game and load or start new game
        self.boot()

    @staticmethod
    def _center_window(screen_x: int, screen_y: int) -> str:
        """
        Builds a geometry string to center window on the monitor

        Args:
            screen_x (int): The width of the screen
            screen_y (int): The height of the screen

        Returns:
            str: A string to center the geometry of the window
        """
        res = c.INTERNAL_RES * c.SCALAR
        x_adj = int((screen_x / 2) - (res / 2))
        y_adj = int((screen_y / 2) - (res / 2))

        return f"{res!s}x{res!s}+{x_adj}+{y_adj}"

    def _load_assets(self) -> None:
        """Loads all game assets, currently just pointers to directories"""
        # Load the configuration file
        self.config = configparser.ConfigParser()
        self.config.read(Path("src/config") / "config.ini")

        # Load the directories for the game assets
        self.images = Path("assets/images/")
        self.resources = Path("assets/resources/")
        self.fonts = Path("assets/fonts/")
        self.data = Path("data")
        FontManager.load_font(self.fonts / "palm-pilot-small.ttf")
        FontManager.load_font(self.fonts / "palm-pilot-bold.ttf")
        FontManager.load_font(self.fonts / "palm-pilot-large.ttf")
        FontManager.load_font(self.fonts / "palm-pilot-large-bold.ttf")

    @staticmethod
    def _build_styles() -> None:
        """Builds the custom styles for the game"""
        normal_fontsize = int(-14 * c.SCALAR)
        title_fontsize = int(-16 * c.SCALAR)
        s = ttk.Style()
        s.theme_use("alt")
        s.configure(
            "TEntry", background=c.BKG_HEX, fieldbackground=c.BKG_HEX, font=("Palm Pilot Small", normal_fontsize)
        )
        s.configure("TFrame", background=c.BKG_HEX, font=("Palm Pilot Small", normal_fontsize))
        s.configure("TButton", background=c.BKG_HEX, font=("Palm Pilot Small", normal_fontsize))
        s.configure("TLabel", background=c.BKG_HEX, font=("Palm Pilot Small", normal_fontsize))
        s.configure(
            "Title.TLabel", background=c.FRG_HEX, foreground=c.BKG_HEX, font=("Palm Pilot Bold", title_fontsize)
        )
        s.configure("Heading.TLabel", background=c.BKG_HEX, font=("Palm Pilot Bold", normal_fontsize))

    def boot(self) -> None:
        """Starts the game"""
        CreateCommander(self).tkraise()


def splash() -> tuple[int, int]:
    """Splash screen"""
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.resizable(False, False)
    # Place the splash screen in the center
    screen_x = splash.winfo_screenwidth()
    screen_y = splash.winfo_screenheight()
    x_adj = int((screen_x / 2) - (160 / 2))
    y_adj = int((screen_y / 2) - (160 / 2))
    splash.geometry(f"160x160+{x_adj}+{y_adj}")

    splash_image = tk.PhotoImage(file=Path(Path.cwd() / "assets" / "images" / "splash.png"))
    splash_label = tk.Label(splash, image=splash_image)
    splash_label.pack(expand=True, fill="both")

    c.GAME["universe"] = Universe()
    splash.after(1000, lambda: [splash.destroy(), print("Splash screen closed")])
    splash.mainloop()

    # Return the monitor resolution just to reduce the re-polling in main window
    return screen_x, screen_y


def main() -> None:
    """Show the splash screen and start the game"""
    screen_x, screen_y = splash()
    window = SpaceTrader(screen_x, screen_y)
    window.mainloop()


if __name__ == "__main__":
    main()
