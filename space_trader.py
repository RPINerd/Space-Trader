"""
    Space Trader (PalmOS) | RPINerd, 06/27/24

    An early strategy RPG game for PalmOS, Space Trader is a game where you are a
    freelance captain, buying and selling goods to make a profit, fending off pirates,
    dealing with sector police, and occasionally ending up on intergalactic quests.

    You can travel to different planets, each with their own economy for trade. You can
    also upgrade your ship, hire crew, and take on missions to make money.

    The game is over when you run out of money, your ship is destroyed or you
    retire with the spoils of your adventures.
"""

import configparser
import os

import pygame

from spacetrader.constants import GameStateID
from spacetrader.interface import commander, splash


class Game:
    """
    Class to represent the core game object.

    Handles the game loop, event handling, and rendering for each frame.

    Attributes:
        screen_width (int): The width of the game window.
        screen_height (int): The height of the game window.
        canvas (pygame.Surface): The surface to draw the game on.
        screen (pygame.Surface): The game window surface.
        config (configparser.ConfigParser): The configuration file for the game.
        running (bool): Flag to indicate if the game is running.
    """

    def __init__(self):

        # Initialize pygame
        pygame.init()

        # Load game assets
        self.load_assets()

        # Set up the game window
        self.screen_width = int(self.config["graphics"]["screen_width"])
        self.screen_height = int(self.config["graphics"]["screen_height"])
        self.canvas = pygame.Surface((160, 160))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Space Trader")
        pygame.display.set_icon(pygame.image.load("images/App.ico"))
        self.manager = GameStateManager(GameStateID.SPLASH)

        self.running = True

    def run(self):
        """
        Main game loop.
        """

        while self.running:
            self.handle_events()
            self.update()
            self.render()

    def render(self):
        """
        Transforms the current canvas to the desired resolution and then
        renders it to the screen.
        """

        transform = pygame.transform.scale(self.canvas, (self.screen_width, self.screen_height))
        self.screen.blit(transform, (0, 0))
        pygame.display.flip()
        self.clock.tick(30)

    def handle_events(self):
        """
        Handles all events in the event queue.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def load_assets(self):
        """
        Loads all game assets, currently just pointers to directories
        """

        # Load the configuration file
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join("config", "config.ini"))

        # Load the directories for the game assets
        self.images = os.path.join("images")
        self.resources = os.path.join("resources")
        # self.data = os.path.join("data")
        self.font_sm = pygame.font.Font("fonts/palm-pilot-small.ttf", 8)
        self.font_sm_bold = pygame.font.Font("fonts/palm-pilot-bold.ttf", 8)
        self.font_lg = pygame.font.Font("fonts/palm-pilot-large.ttf", 8)
        self.font_lg_bold = pygame.font.Font("fonts/palm-pilot-large-bold.ttf", 8)

    def update(self):
        self.splash_image = pygame.image.load("images/splash.jpg")
        self.canvas.blit(self.splash_image, (0, 0))


class GameStateManager:
    """
    Class to manage different game states.
    """

    def __init__(self, initial_state):
        self.state = initial_state
        self.previous_state = None

    def get_state(self) -> str:
        return self.state

    def set_state(self, new_state) -> None:
        """
        Set the current game state.

        param state: The new game state.
        """
        try:
            self.previous_state = self.state
            self.state = new_state
        except ValueError:
            print(f"Invalid state: {new_state}")

    def get_previous_state(self) -> str:
        return self.previous_state


def main():
    """ """

    space_trader = Game()
    while space_trader.running:
        space_trader.run()
    pygame.quit()


if __name__ == "__main__":

    main()
