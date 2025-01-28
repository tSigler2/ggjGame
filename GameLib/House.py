import pygame as pg
import os


class House:
    """
    The House class represents the player's house in the game.
    It produces sand dollars, manages health, and handles game-over conditions.
    """

    def __init__(self, game, health: int, init_sprite: str, pos: tuple, coords: tuple):
        """
        Initialize the house.

        Args:
            game: The main game object.
            health: The house's initial health.
            init_sprite: Path to the initial sprite image.
            pos: Initial position (x, y) of the house.
            coords: Initial grid coordinates (x, y) of the house.
        """
        self.game = game
        self.health = health
        self.max_health = health  # Maximum health for reference
        self.coords = coords  # Grid coordinates (x, y)
        self.x, self.y = pos  # Screen position (x, y)
        self.sand_dollar_interval = (
            10000  # Time between sand dollar production (in milliseconds)
        )
        self.last_sand_dollar_time = 0  # Timestamp of the last sand dollar production

        # Load the house sprite
        if not os.path.exists(init_sprite):
            raise FileNotFoundError(f"House sprite file '{init_sprite}' not found.")
        self.sprite = pg.image.load(init_sprite).convert_alpha()

    def take_damage(self, damage: int):
        """
        Reduce the house's health by the specified amount.

        Args:
            damage: Amount of damage to take.
        """
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.game_over()

    def game_over(self):
        """
        Handle the game-over condition when the house's health reaches zero.
        """
        print("Game Over! The house has been destroyed.")
        self.game.running = False  # Stop the game loop

    def produce_sand_dollars(self):
        """
        Produce sand dollars at regular intervals.
        """
        current_time = pg.time.get_ticks()
        if current_time - self.last_sand_dollar_time >= self.sand_dollar_interval:
            self.last_sand_dollar_time = current_time
            self.game.player.get_money(1)  # Give the player 1 sand dollar
            print("Produced 1 sand dollar!")

    def draw(self):
        """
        Draw the house on the screen.
        """
        self.game.screen.blit(self.sprite, (self.x, self.y))

    def update(self):
        """
        Update the house's state, including sand dollar production and health checks.
        """
        self.produce_sand_dollars()
        self.draw()

        # Debugging: Display house health
        health_text = f"House Health: {self.health}"
        font = pg.font.SysFont("Consolas", 20)
        text_surface = font.render(health_text, True, (255, 255, 255))
        self.game.screen.blit(text_surface, (self.x, self.y - 20))
