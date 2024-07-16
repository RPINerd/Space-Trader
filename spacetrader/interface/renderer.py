import pygame
from pygame.locals import Color


class TextRender:
    """
    A self aware object that can render itself to the screen.
    """

    def __init__(self, text, pos, **options):
        self.text = text
        self.pos = pos

        self.fontname = "../fonts/palm-pilot-small.ttf"
        self.fontsize = 10
        self.fontcolor = Color("black")
        self.set_font()
        self.render()

    def set_font(self):
        """Set the font from its name and size."""
        self.font = pygame.font.Font(self.fontname, self.fontsize)

    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos