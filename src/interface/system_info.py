"""
    Space Trader (PalmOS) | RPINerd, 2024

    Basic system information screen
"""

import pygame

from ..constants import GameStateID
from .renderer import Header, TextRender, TitleBar
from .state import State


class SystemInfo(State):

    def __init__(self, game) -> None:
        self.game = game
        self.head_font: pygame.font.Font = game.font_sm_bold
        self.font: pygame.font.Font = game.font_sm
        super().__init__(game)

    def handle_events(self, event: pygame.event) -> None:
        if event.type == pygame.QUIT:
            self.game.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.game.current_state = GameStateID.SPLASH
            if event.key == pygame.K_ESCAPE:
                self.game.current_state = GameStateID.SPLASH

    def update(self, actions) -> None:
        pass

    def render(self, canvas: pygame.Surface) -> pygame.Surface:
        canvas.fill((240, 240, 240))

        # Draw the header
        header = Header(canvas)
        header.render()
        title = TitleBar("System Info", self.head_font, canvas)
        title.render()

        # Category headers
        categories: list[TextRender] = []
        categories.append(TextRender("Name:", (1, 18), self.head_font))
        categories.append(TextRender("Size:", (1, 38), self.head_font))
        categories.append(TextRender("Tech Level:", (1, 58), self.head_font))
        categories.append(TextRender("Government:", (1, 78), self.head_font))
        categories.append(TextRender("Resources:", (1, 98), self.head_font))
        categories.append(TextRender("Police:", (1, 118), self.head_font))
        categories.append(TextRender("Pirates:", (1, 138), self.head_font))

        for category in categories:
            category.draw(canvas)

        return canvas
