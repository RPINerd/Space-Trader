"""
    Screens module

    Defines the elements that make up an individual screen in the game
"""

import logging
import tkinter as tk
from tkinter import ttk

from src.constants import BKG_HEX, FRG_HEX, INTERNAL_RES, SCALAR

logger = logging.getLogger(__name__)


class Heading(ttk.Frame):

    def __init__(self, parent, heading: str):
        self.parent = parent
        super().__init__(parent)
        self.heading = heading
        self.create_widgets()
        self.pack()

    def create_widgets(self):

        self.heading = ttk.Label(self, text=self.heading, style="Title.TLabel")
        self.heading.pack(side="left")

        self.b = ttk.Button(
            self,
            text="B",
            width=2,
            # height=1,
            command=lambda: self.shortcut_trigger(self, "B"),
        )
        self.b.pack(side="right")
        self.s = ttk.Button(
            self,
            text="S",
            width=2,
            # height=1,
            command=lambda: self.shortcut_trigger(self, "S"),
        )
        self.s.pack(side="right")
        self.y = ttk.Button(
            self,
            text="Y",
            width=2,
            # height=1,
            command=lambda: self.shortcut_trigger(self, "Y"),
        )
        self.y.pack(side="right")
        self.w = ttk.Button(
            self,
            text="W",
            width=2,
            # height=1,
            command=lambda: self.shortcut_trigger(self, "W"),
        )
        self.w.pack(side="right")

        self.underline = tk.Canvas(self, width=INTERNAL_RES * SCALAR, height=2, bg=FRG_HEX)
        self.underline.pack(side="bottom", expand=True, fill="x")

    def shortcut_trigger(event, self, key):
        # print(f"self type: {type(self)}\nself: {self}")
        # print(f"event type: {type(event)}\nevent: {event}, key: {key}")
        # for attrib in getattr(event, "__dict__", {}):
        #     print(f"attrib: {attrib}")
        logger.debug("Shortcut triggered: %s", key)
        self.parent.manager.go_to_screen(key)


class Screen(ttk.Frame):

    def __init__(self, parent, screen_title: str, manager) -> None:
        self.manager = manager
        self.screen_title = screen_title
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=1, relheight=1)

        self.header = Heading(self, self.screen_title)

        # Bind the game shortcut keys
        self.bind_all("<KeyPress-b>", self.change_screen)
        self.bind_all("<KeyPress-s>", self.change_screen)
        self.bind_all("<KeyPress-y>", self.change_screen)
        self.bind_all("<KeyPress-e>", self.change_screen)
        self.bind_all("<KeyPress-q>", self.change_screen)
        self.bind_all("<KeyPress-p>", self.change_screen)
        self.bind_all("<KeyPress-k>", self.change_screen)
        self.bind_all("<KeyPress-i>", self.change_screen)
        self.bind_all("<KeyPress-c>", self.change_screen)
        self.bind_all("<KeyPress-g>", self.change_screen)
        self.bind_all("<KeyPress-w>", self.change_screen)
        self.bind_all("<KeyPress-o>", self.change_screen)

        self.create_widgets()

    def change_screen(self, event):
        logger.debug("Changing screen to %s", event.keysym)
        self.manager.go_to_screen(event.keysym.upper())

    def create_widgets(self):
        # ! Placeholder id frame
        self.id_frame = ttk.Frame(self)
        ttk.Label(self.id_frame, text=self.screen_title, justify="center").pack(fill="x", expand=True)
        ttk.Label(self.id_frame, text="Not Implemented", justify="center").pack(fill="x", expand=True)
        self.id_frame.pack(fill="both", expand=True)


class Popup(ttk.Frame):

    def __init__(self, parent, title, content: ttk.Frame, height: int = INTERNAL_RES * SCALAR):
        super().__init__(parent, bg=BKG_HEX, height=height, width=INTERNAL_RES * SCALAR)
        self.pack(expand=True, fill="both")
        self.title = title
        self.content = content
        self.create_widgets()

    def create_widgets(self):
        self.title = ttk.Label(self, text=self.title)
        self.title.pack()
        self.message = ttk.Label(self, text=self.message)
        self.message.pack()
        self.ok = ttk.Button(self, text="OK", command=self.destroy)
        self.ok.pack()
