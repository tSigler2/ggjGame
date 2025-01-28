import pygame as pg


class Tile:
    """
    The Tile class represents a single tile on the map.
    """

    def __init__(self, game, x: int, y: int, width: int, height: int, image_path: str):
        """
        Initialize the tile.

        Args:
            game: The main game object.
            x: X-coordinate of the tile.
            y: Y-coordinate of the tile.
            width: Width of the tile.
            height: Height of the tile.
            image_path: Path to the tile's image.
        """
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = pg.Rect(x, y, width, height)
        self.occupied = False
        self.occupant = None  # Entity occupying the tile (e.g., player, enemy, coral)

    def draw(self):
        """
        Draw the tile on the screen.
        """
        self.game.screen.blit(self.image, (self.x, self.y))

    def update(self):
        """
        Update the tile's state (e.g., draw the tile and its occupant).
        """
        self.draw()
        if self.occupant:
            self.occupant.draw()
