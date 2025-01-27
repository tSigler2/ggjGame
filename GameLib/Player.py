import os
import pygame as pg
from collections import deque
from Sprite.MultiAnimatedSprite import MultiAnimatedSprite


class Player(MultiAnimatedSprite):
    """
    The Player class represents the player character in the game.
    It handles movement, attacks, animations, and interactions with the game world.
    """

    def __init__(
        self,
        game,
        health: int,
        range: int,
        init_sprite: str,
        animation_path: str,
        pos: tuple,
        animation_time: int,
        coords: tuple,
        money: int,
        *animation_sets,
    ):
        """
        Initialize the player.

        Args:
            game: The main game object.
            health: The player's initial health.
            range: The player's attack range.
            init_sprite: Path to the initial sprite image.
            animation_path: Base path for animation assets.
            pos: Initial position (x, y) of the player.
            animation_time: Time between animation frames.
            coords: Initial grid coordinates of the player.
            money: Initial amount of money.
            *animation_sets: Animation sets (e.g., "walk", "attack").
        """
        super().__init__(
            game, animation_path, pos, 1, 0, animation_time, animation_sets
        )
        self.health = health
        self.range = range
        self.money = money
        self.coords = coords  # Grid coordinates (x, y)
        self.attack_cooldown = 2000  # Cooldown between attacks in milliseconds
        self.last_attack_time = 0  # Timestamp of the last attack
        self.coral_toggle = False  # Toggle for placing coral instead of attacking

        # Load initial sprite
        if not os.path.exists(init_sprite):
            raise FileNotFoundError(f"Initial sprite file '{init_sprite}' not found.")
        self.sprite = pg.image.load(init_sprite).convert_alpha()

        # Animation setup
        self.animations = self.load_animations(animation_path, animation_sets)
        self.current_animation = "walk"  # Default animation
        self.animation_trigger = False

    def load_animations(self, path: str, animation_sets: tuple) -> dict:
        """
        Load animations from the specified path.

        Args:
            path: Base path for animation assets.
            animation_sets: Names of animation sets (e.g., "walk", "attack").

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

    def handle_input(self):
        """
        Handle player input for movement and actions.
        """
        keys = pg.key.get_pressed()
        mouse_buttons = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()

        # Movement
        if keys[pg.K_w] and self.coords[1] > 0:
            self.move((self.coords[0], self.coords[1] - 1))
        if keys[pg.K_s] and self.coords[1] < 10:
            self.move((self.coords[0], self.coords[1] + 1))
        if keys[pg.K_a] and self.coords[0] > 0:
            self.move((self.coords[0] - 1, self.coords[1]))
        if keys[pg.K_d] and self.coords[0] < 10:
            self.move((self.coords[0] + 1, self.coords[1]))

        # Attack or place coral
        if mouse_buttons[0]:  # Left mouse button
            self.handle_attack_or_coral(mouse_pos)

    def move(self, new_coords: tuple):
        """
        Move the player to new grid coordinates.

        Args:
            new_coords: New grid coordinates (x, y).
        """
        self.coords = new_coords
        tile = self.game.map[new_coords[0]][new_coords[1]]
        self.x, self.y = tile.x, tile.y

    def handle_attack_or_coral(self, mouse_pos: tuple):
        """
        Handle player attack or coral placement based on mouse input.

        Args:
            mouse_pos: Current mouse position (x, y).
        """
        current_time = pg.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            self.trigger_attack_animation()

            if not self.coral_toggle:
                self.attack_enemies(mouse_pos)
            else:
                self.place_coral(mouse_pos)

    def attack_enemies(self, mouse_pos: tuple):
        """
        Attack enemies within range of the mouse click.

        Args:
            mouse_pos: Current mouse position (x, y).
        """
        for enemy in self.game.enemyManager.enemy_list:
            if enemy.rect.collidepoint(mouse_pos):
                enemy.take_damage(1)

    def place_coral(self, mouse_pos: tuple):
        """
        Place coral at the clicked tile.

        Args:
            mouse_pos: Current mouse position (x, y).
        """
        coords = self.get_tile_coords(mouse_pos)
        if coords:
            self.game.coral_manager.add_coral(5, 2, coords, "Assets/coral", 120, "std")

    def get_tile_coords(self, mouse_pos: tuple) -> tuple:
        """
        Get the grid coordinates of the tile at the mouse position.

        Args:
            mouse_pos: Current mouse position (x, y).

        Returns:
            Grid coordinates (x, y) of the tile, or None if no tile is found.
        """
        for x, row in enumerate(self.game.map):
            for y, tile in enumerate(row):
                if tile.rect.collidepoint(mouse_pos):
                    return (x, y)
        return None

    def take_damage(self, damage: int):
        """
        Reduce the player's health by the specified amount.

        Args:
            damage: Amount of damage to take.
        """
        self.health -= damage
        if self.health <= 0:
            self.respawn()

    def respawn(self):
        """Respawn the player at the house's position."""
        self.coords = self.game.house.coords
        self.x, self.y = self.game.house.x, self.game.house.y
        self.health = 5  # Reset health

    def update(self):
        """
        Update the player's state, including input handling and animations.
        """
        self.handle_input()
        self.update_animations()
        self.draw(self.sprite)

    def update_animations(self):
        """
        Update the player's animations based on the current state.
        """
        if self.animation_trigger:
            self.animation_trigger = False
            self.animations[self.current_animation].rotate(-1)
            self.sprite = self.animations[self.current_animation][0]

    def trigger_attack_animation(self):
        """
        Trigger the attack animation and set the current animation to "attack".
        """
        self.current_animation = "attack"
        self.animation_trigger = True