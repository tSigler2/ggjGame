import pygame as pg


class Entity:
    """
    The base Entity class combines collision detection and movement functionality.
    """

    def __init__(self, game, pos: tuple, velocity: tuple, dims: tuple):
        """
        Initialize the entity.

        Args:
            game: The main game object.
            pos: Initial position (x, y) of the entity.
            velocity: Initial velocity (dx, dy) of the entity.
            dims: Dimensions (width, height) of the entity for collision detection.
        """
        self.game = game
        self.x, self.y = pos
        self.dx, self.dy = velocity
        self.width, self.height = dims
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

    def move(self, delta_time: float):
        """
        Move the entity based on its velocity and delta time.

        Args:
            delta_time: Time since the last frame (used for smooth movement).
        """
        self.x += self.dx * delta_time
        self.y += self.dy * delta_time
        self.rect.topleft = (self.x, self.y)

    def check_collision(self, other_rects: list) -> bool:
        """
        Check for collisions with a list of other rects.

        Args:
            other_rects: List of pygame.Rect objects to check for collisions.

        Returns:
            True if a collision is detected, False otherwise.
        """
        return self.rect.collidelist(other_rects) != -1

    def update(self, delta_time: float):
        """
        Update the entity's state (e.g., movement, collision detection).

        Args:
            delta_time: Time since the last frame.
        """
        self.move(delta_time)
