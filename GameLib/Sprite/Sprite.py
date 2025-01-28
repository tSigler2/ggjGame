import pygame as pg
import os


class Sprite:
    """
    The base Sprite class handles loading and drawing a single image.
    """

    def __init__(self, game, path: str, pos: tuple, scale: float = 1.0):
        """
        Initialize the sprite.

        Args:
            game: The main game object.
            path: Path to the sprite image.
            pos: Initial position (x, y) of the sprite.
            scale: Scale factor for the sprite (default: 1.0).
        """
        self.game = game
        self.x, self.y = pos
        self.scale = scale

        if not os.path.exists(path):
            raise FileNotFoundError(f"Sprite file '{path}' not found.")
        self.image = pg.image.load(path).convert_alpha()
        self.image = pg.transform.scale(
            self.image,
            (int(self.image.get_width() * scale), int(self.image.get_height() * scale)),
        )

    def draw(self):
        """
        Draw the sprite on the screen.
        """
        self.game.screen.blit(self.image, (self.x, self.y))

    def update(self):
        """
        Update the sprite's state (can be overridden by subclasses).
        """
        self.draw()
