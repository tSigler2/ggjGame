import pygame as pg
from collections import deque
from Sprite.MultiAnimatedSprite import MultiAnimatedSprite
import os


class Coral(MultiAnimatedSprite):
    """
    The Coral class represents a coral entity in the game.
    It can be planted, moved, and attacks squirrels within its range.
    """

    def __init__(
        self,
        game,
        health: int,
        coords: tuple,
        damage: int,
        path: str,
        animation_time: int,
        *animation_sets,
    ):
        """
        Initialize the coral.

        Args:
            game: The main game object.
            health: The coral's initial health.
            coords: The coral's grid coordinates (x, y).
            damage: The damage dealt by the coral per attack.
            path: Base path for animation assets.
            animation_time: Time between animation frames.
            *animation_sets: Animation sets (e.g., "std").
        """
        super().__init__(game, path, coords, 1, 0, animation_time, animation_sets)
        self.health = health
        self.damage = damage
        self.coords = coords  # Grid coordinates (x, y)
        self.attack_interval = 1000  # Time between attacks in milliseconds
        self.last_attack_time = 0  # Timestamp of the last attack

        # Load animations
        self.animations = self.load_animations(path, animation_sets)
        self.current_animation = "std"  # Default animation
        self.animation_trigger = False

        # Set initial position
        self.x, self.y = self.game.map[coords[0]][coords[1]].x, self.game.map[coords[0]][coords[1]].y

    def load_animations(self, path: str, animation_sets: tuple) -> dict:
        """
        Load animations from the specified path.

        Args:
            path: Base path for animation assets.
            animation_sets: Names of animation sets (e.g., "std").

        Returns:
            A dictionary of animation sets, where each set is a deque of images.
        """
        animations = {}
        for animation_set in animation_sets:
            full_path = os.path.join(path, animation_set)
            if not os.path.exists(full_path):
                print(f"Warning: Animation path '{full_path}' not found. Skipping.")
                continue

            images = deque()
            for file in sorted(os.listdir(full_path)):
                if file.endswith((".png", ".jpg")):
                    img = pg.image.load(os.path.join(full_path, file)).convert_alpha()
                    images.append(img)
            animations[animation_set] = images

        return animations

    def take_damage(self, damage: int):
        """
        Reduce the coral's health by the specified amount.

        Args:
            damage: Amount of damage to take.
        """
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        """
        Handle the coral's death by removing it from the game.
        """
        self.game.map[self.coords[0]][self.coords[1]].occupied = False
        self.game.map[self.coords[0]][self.coords[1]].occupant = None
        self.game.coral_manager.remove_coral(self)

    def attack(self):
        """
        Attack all squirrels within the coral's range.
        """
        current_time = pg.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_interval:
            self.last_attack_time = current_time

            # Check all tiles within range (orthogonal and diagonal)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue  # Skip the coral's own tile

                    x, y = self.coords[0] + dx, self.coords[1] + dy
                    if 0 <= x < len(self.game.map) and 0 <= y < len(self.game.map[0]):
                        tile = self.game.map[x][y]
                        if tile.occupied and tile.occupant != self.game.player and tile.occupant != self.game.house:
                            tile.occupant.take_damage(self.damage)

    def move(self, new_coords: tuple):
        """
        Move the coral to new grid coordinates.

        Args:
            new_coords: New grid coordinates (x, y).
        """
        # Clear the current tile
        self.game.map[self.coords[0]][self.coords[1]].occupied = False
        self.game.map[self.coords[0]][self.coords[1]].occupant = None

        # Update coordinates and position
        self.coords = new_coords
        self.x, self.y = self.game.map[new_coords[0]][new_coords[1]].x, self.game.map[new_coords[0]][new_coords[1]].y

        # Occupy the new tile
        self.game.map[new_coords[0]][new_coords[1]].occupied = True
        self.game.map[new_coords[0]][new_coords[1]].occupant = self

    def update(self):
        """
        Update the coral's state, including attacks and animations.
        """
        self.attack()
        self.update_animations()
        self.draw(self.sprite)

    def update_animations(self):
        """
        Update the coral's animations based on the current state.
        """
        if self.animation_trigger:
            self.animation_trigger = False
            self.animations[self.current_animation].rotate(-1)
            self.sprite = self.animations[self.current_animation][0]