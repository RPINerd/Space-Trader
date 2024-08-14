"""
    Space Trader (PalmOS) | RPINerd, 2024

    Character creation screen
"""

import tkinter as tk
from tkinter import ttk

import pygame

from ..commander import Commander
from ..constants import BKG_COLOR, CIRCLE_XY, FRG_COLOR, HALF_RES, INTERNAL_RES, Difficulty, GameStateID
from .renderer import Button, TextInput, TextRender
from .state import State


class StatAdjuster(ttk.Frame):
    """
    A frame that contains a label, a decrement button, a value label, and an increment button.
    """

    def __init__(self, master, label_text, initial_value, row, column, **kwargs):
        super().__init__(master, **kwargs)

        self.value = tk.IntVar(value=initial_value)

        self.label = ttk.Label(self, text=label_text)
        self.decrement = ttk.Button(self, text="-", command=self.decrement_value)
        self.value_label = ttk.Label(self, textvariable=self.value)
        self.increment = ttk.Button(self, text="+", command=self.increment_value)

        self.label.grid(row=row, column=column)
        self.decrement.grid(row=row, column=column + 1)
        self.value_label.grid(row=row, column=column + 2)
        self.increment.grid(row=row, column=column + 3)

    def decrement_value(self):
        self.value.set(max(self.value.get() - 1, 1))

    def increment_value(self):
        self.value.set(min(self.value.get() + 1, 10))


class CreateCommander(ttk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        # Initial values
        self.cmdr_name = tk.StringVar(value="Jameson")
        self.diff_current_value = 2
        self.points_pool = tk.IntVar(value=16)
        self.pilot_points = tk.IntVar(value=1)
        self.fighter_points = tk.IntVar(value=1)
        self.trader_points = tk.IntVar(value=1)
        self.engineer_points = tk.IntVar(value=1)

        # Title Bar
        self.header = ttk.Label(self, text="New Commander", font=("Helvetica", 8))
        self.header.pack()

        # Commander name
        self.name_frame = ttk.Frame(self)
        self.name_label = ttk.Label(self.name_frame, text="Name:")
        self.name_entry = ttk.Entry(self.name_frame, textvariable=self.cmdr_name)
        self.name_label.pack(side="left")
        self.name_entry.pack(side="left")

        # Game difficulty selection
        self.difficulty_frame = ttk.Frame(self)
        self.difficulty_label = ttk.Label(self.difficulty_frame, text="Difficulty:")
        self.difficulty_dec = ttk.Button(self.difficulty_frame, text="-", command=self.dec_difficulty)
        self.difficulty_current = ttk.Label(
            self.difficulty_frame,
            text="Normal",
        )
        self.difficulty_inc = ttk.Button(self.difficulty_frame, text="+", command=self.inc_difficulty)
        self.difficulty_label.pack(side="left")
        self.difficulty_dec.pack(side="left")
        self.difficulty_current.pack(side="left")
        self.difficulty_inc.pack(side="left")

        # Skill points allocation grid

        self.skills_frame = ttk.Frame(self)
        self.points_label = ttk.Label(self.skills_frame, text="Skill Points:")
        self.pilot_skill = StatAdjuster(self.skills_frame, "Pilot:", 1, 0, 0)
        self.fighter_skill = StatAdjuster(self.skills_frame, "Fighter:", 1, 1, 0)
        self.trader_skill = StatAdjuster(self.skills_frame, "Trader:", 1, 2, 0)
        self.engineer_skill = StatAdjuster(self.skills_frame, "Engineer:", 1, 3, 0)

        self.points_label.pack(expand=True, fill="x")
        self.pilot_skill.pack(expand=True, fill="x")
        self.fighter_skill.pack(expand=True, fill="x")
        self.trader_skill.pack(expand=True, fill="x")
        self.engineer_skill.pack(expand=True, fill="x")

        # self.skills_frame = ttk.Frame(self, height=55, width=80)

        # self.points_label = ttk.Label(self.skills_frame, text="Skill Points:", justify="left")
        # self.pilot_label = ttk.Label(self.skills_frame, text="Pilot:", justify="left")
        # self.fighter_label = ttk.Label(self.skills_frame, text="Fighter:", justify="left")
        # self.trader_label = ttk.Label(self.skills_frame, text="Trader:", justify="left")
        # self.engineer_label = ttk.Label(self.skills_frame, text="Engineer:", justify="left")

        # self.pilot_dec = ttk.Button(self.skills_frame, text="-", width=2, command=self.dec_pilot)
        # self.pilot_inc = ttk.Button(self.skills_frame, text="+", width=2, command=self.inc_pilot)
        # self.fighter_dec = ttk.Button(self.skills_frame, text="-", width=2, command=self.dec_fighter)
        # self.fighter_inc = ttk.Button(self.skills_frame, text="+", width=2, command=self.inc_fighter)
        # self.trader_dec = ttk.Button(self.skills_frame, text="-", width=2, command=self.dec_trader)
        # self.trader_inc = ttk.Button(self.skills_frame, text="+", width=2, command=self.inc_trader)
        # self.engineer_dec = ttk.Button(self.skills_frame, text="-", width=2, command=self.dec_engineer)
        # self.engineer_inc = ttk.Button(self.skills_frame, text="+", width=2, command=self.inc_engineer)

        # self.points_current = ttk.Label(self.skills_frame, textvariable=self.points_pool)
        # self.points_current.grid(row=0, column=1)
        # self.pilot_current = ttk.Label(self.skills_frame, textvariable=self.pilot_points)
        # self.pilot_current.grid(row=1, column=2)
        # self.fighter_current = ttk.Label(self.skills_frame, textvariable=self.fighter_points)
        # self.fighter_current.grid(row=2, column=2)
        # self.trader_current = ttk.Label(self.skills_frame, textvariable=self.trader_points)
        # self.trader_current.grid(row=3, column=2)
        # self.engineer_current = ttk.Label(self.skills_frame, textvariable=self.engineer_points)
        # self.engineer_current.grid(row=4, column=2)

        # self.points_label.grid(row=0, column=0, columnspan=2)
        # self.points_current.grid(row=0, column=2)

        # self.pilot_label.grid(row=1, column=0, sticky="nsew")
        # self.pilot_dec.grid(row=1, column=1, sticky="nsew")
        # self.pilot_current.grid(row=1, column=2, sticky="nsew")
        # self.pilot_inc.grid(row=1, column=3, sticky="nsew")

        # self.fighter_label.grid(row=2, column=0, sticky="nsew")
        # self.fighter_dec.grid(row=2, column=1, sticky="nsew")
        # self.fighter_current.grid(row=2, column=2, sticky="nsew")
        # self.fighter_inc.grid(row=2, column=3, sticky="nsew")

        # self.trader_label.grid(row=3, column=0)
        # self.trader_dec.grid(row=3, column=1)
        # self.trader_current.grid(row=3, column=2)
        # self.trader_inc.grid(row=3, column=3)

        # self.engineer_label.grid(row=4, column=0)
        # self.engineer_dec.grid(row=4, column=1)
        # self.engineer_current.grid(row=4, column=2)
        # self.engineer_inc.grid(row=4, column=3)

        # Button to start the game
        self.start_button = ttk.Button(self, text="OK", command=self.cmdr_create, width=15)

        self.name_frame.pack(expand=True, fill="x")
        self.difficulty_frame.pack(expand=True)
        self.skills_frame.pack(expand=True, fill="x")
        self.start_button.pack(expand=True)

    def dec_difficulty(self) -> None:
        self.diff_current_value
        diff_current_value = max(self.diff_current_value - 1, 0)
        if diff_current_value == 0:
            self.difficulty_dec["state"] = "disabled"
        self.difficulty_inc["state"] = "enabled"
        self.difficulty_current["text"] = Difficulty.name(diff_current_value)

    def inc_difficulty(self) -> None:
        self.diff_current_value
        diff_current_value = min(self.diff_current_value + 1, 4)
        if diff_current_value == 4:
            self.difficulty_inc["state"] = "disabled"
        self.difficulty_dec["state"] = "enabled"
        self.difficulty_current["text"] = Difficulty.name(diff_current_value)

    def refill_pool(self) -> None:
        pts = self.points_pool.get()
        pts += 1
        self.points_pool.set(pts)

    def spend_pool(self) -> bool:
        pts = self.points_pool.get()
        if pts == 0:
            return False
        pts -= 1
        self.points_pool.set(pts)
        return True

    def dec_pilot(self) -> None:
        pts = self.pilot_points.get()
        if pts - 1 > 0:
            self.refill_pool()
            pts -= 1
            self.pilot_points.set(pts)

    def inc_pilot(self) -> None:
        pts = self.pilot_points.get()
        if pts == 10:
            return
        if self.spend_pool():
            pts += 1
            self.pilot_points.set(pts)

    def dec_fighter(self) -> None:
        pts = self.fighter_points.get()
        if pts - 1 > 0:
            self.refill_pool()
            pts -= 1
            self.fighter_points.set(pts)

    def inc_fighter(self) -> None:
        pts = self.fighter_points.get()
        if pts == 10:
            return
        if self.spend_pool():
            pts += 1
            self.fighter_points.set(pts)

    def dec_trader(self) -> None:
        pts = self.trader_points.get()
        if pts - 1 > 0:
            self.refill_pool()
            pts -= 1
            self.trader_points.set(pts)

    def inc_trader(self) -> None:
        pts = self.trader_points.get()
        if pts == 10:
            return
        if self.spend_pool():
            pts += 1
            self.trader_points.set(pts)

    def dec_engineer(self) -> None:
        pts = self.engineer_points.get()
        if pts - 1 > 0:
            self.refill_pool()
            pts -= 1
            self.engineer_points.set(pts)

    def inc_engineer(self) -> None:
        pts = self.engineer_points.get()
        if pts == 10:
            return
        if self.spend_pool():
            pts += 1
            self.engineer_points.set(pts)

    def cmdr_create(self):
        cmdr = Commander(
            self.cmdr_name.get(),
            self.pilot_points.get(),
            self.fighter_points.get(),
            self.trader_points.get(),
            self.engineer_points.get(),
        )
        print(cmdr.pprint())
        self.destroy()


class CharacterCreation(State):

    def __init__(self, game) -> None:
        self.game = game
        self.head_font: pygame.font.Font = game.font_sm_bold
        self.font: pygame.font.Font = game.font_sm
        super().__init__(game)

        self._cmdr_name = "Jameson"
        self._cmdr_input = TextInput(55, 20, 80, self.font)
        self.sprite_group = pygame.sprite.Group(self._cmdr_input)
        self._curr_difficulty = 2
        self._curr_points = 16
        self._curr_pilot = 1
        self._curr_fighter = 1
        self._curr_trader = 1
        self._curr_engineer = 1

        self._inc_difficulty = Button("+", (HALF_RES + 40, 48), CIRCLE_XY, self.font)
        self._dec_difficulty = Button("-", (HALF_RES - 20, 48), CIRCLE_XY, self.font)

        self._inc_pilot = Button("+", (HALF_RES + 10, 80), CIRCLE_XY, self.font)
        self._dec_pilot = Button("-", (HALF_RES - 20, 80), CIRCLE_XY, self.font)
        self._inc_fighter = Button("+", (HALF_RES + 10, 92), CIRCLE_XY, self.font)
        self._dec_fighter = Button("-", (HALF_RES - 20, 92), CIRCLE_XY, self.font)
        self._inc_trader = Button("+", (HALF_RES + 10, 104), CIRCLE_XY, self.font)
        self._dec_trader = Button("-", (HALF_RES - 20, 104), CIRCLE_XY, self.font)
        self._inc_engineer = Button("+", (HALF_RES + 10, 116), CIRCLE_XY, self.font)
        self._dec_engineer = Button("-", (HALF_RES - 20, 116), CIRCLE_XY, self.font)

        self._buttons = [
            self._inc_difficulty,
            self._dec_difficulty,
            self._inc_pilot,
            self._dec_pilot,
            self._inc_fighter,
            self._dec_fighter,
            self._inc_trader,
            self._dec_trader,
            self._inc_engineer,
            self._dec_engineer,
        ]
        self._curr_values = [
            self._curr_points,
            self._curr_pilot,
            self._curr_fighter,
            self._curr_trader,
            self._curr_engineer,
        ]

    def handle_events(self, event: pygame.event) -> None:
        if event.type == pygame.QUIT:
            self.game.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.game.running = False
            if event.key == pygame.K_ESCAPE:
                self.game.current_state = GameStateID.SPLASH
            if event.key == pygame.K_RETURN:
                self.game.current_state = GameStateID.SYSTEM_INFO
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for index, button in enumerate(self._buttons):
                if button.is_clicked(event.pos) and index < 2:
                    if button.text == "+":
                        self._curr_difficulty += 1
                    elif button.text == "-":
                        self._curr_difficulty -= 1
                    else:
                        raise ValueError(f"Invalid button text! Expected '+' or '-' but got {button.text}")
                elif button.is_clicked(event.pos) and index >= 2:
                    if button.text == "+":
                        self._curr_points -= 1
                        self._curr_values[index // 2] += 1
                    elif button.text == "-":
                        self._curr_points += 1
                        self._curr_values[index // 2] -= 1
                    else:
                        raise ValueError(f"Invalid button text! Expected '+' or '-' but got {button.text}")
        self.sprite_group.update(event)

    def update(self, actions) -> None:
        pass

    def render(self, canvas: pygame.Surface) -> pygame.Surface:

        # Background
        canvas.fill(BKG_COLOR)

        # Border
        pygame.draw.rect(
            canvas,
            FRG_COLOR,
            pygame.Rect(1, 1, INTERNAL_RES - 2, INTERNAL_RES - 2),
            2,
            border_radius=3,
        )

        # Header
        pygame.draw.rect(
            canvas,
            FRG_COLOR,
            pygame.Rect(3, 1, INTERNAL_RES - 6, 14),
        )
        header_text = TextRender(
            "New Commander", (INTERNAL_RES // 2, 8), self.head_font, ref="center", fontcolor=BKG_COLOR
        )
        header_text.draw(canvas)

        prompt_text: list[TextRender] = []
        prompt_text.append(TextRender("Name:", (10, 20), self.font))
        prompt_text.append(TextRender("Difficulty:", (10, 40), self.font))
        prompt_text.append(TextRender("Skill Points:", (10, 65 + 14 * 0), self.font))
        prompt_text.append(TextRender("Pilot:", (10, 65 + 14 * 1), self.font))
        prompt_text.append(TextRender("Fighter:", (10, 65 + 14 * 2), self.font))
        prompt_text.append(TextRender("Trader:", (10, 65 + 14 * 3), self.font))
        prompt_text.append(TextRender("Engineer:", (10, 65 + 14 * 4), self.font))

        for text in prompt_text:
            text.draw(canvas)

        # Buttons
        for button in self._buttons:
            button.draw(canvas)

        # Draw the current values
        self.sprite_group.draw(canvas)
        difficulty_text = TextRender(Difficulty.name(self._curr_difficulty), (HALF_RES, 40), self.font)
        difficulty_text.draw(canvas)
        for idx, value in enumerate(self._curr_values):
            value_text = TextRender(str(value), (HALF_RES, 65 + (idx * 14)), self.font)
            value_text.draw(canvas)

        return canvas