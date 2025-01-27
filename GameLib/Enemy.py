import pygame as pg
from collections import deque
from Sprite.MultiAnimatedSprite import MultiAnimatedSprite
import os


class Enemy(MultiAnimatedSprite):
    """
    The Enemy class represents an enemy entity in the game.
    It handles pathfinding, movement, attacks, and animations.
    """

    def __init__(
        self,
        game,
        health: int,
        start_position: tuple,
        goal: tuple,
        map_matrix: list,
        path: str,
        animation_time: int,
        *animation_sets,
        enemy_speed: int = 3,
    ):
        """
        Initialize the enemy.

        Args:
            game: The main game object.
            health: The enemy's initial health.
            start_position: The enemy's starting grid coordinates (x, y).
            goal: The enemy's target grid coordinates (x, y).
            map_matrix: The game's map matrix.
            path: Base path for animation assets.
            animation_time: Time between animation frames.
            *animation_sets: Animation sets (e.g., "walk", "attack").
            enemy_speed: The enemy's movement speed (default: 3).
        """
        super().__init__(game, path, start_position, 1, 0, animation_time, animation_sets)
        self.health = health
        self.position = start_position  # Grid coordinates (x, y)
        self.goal = goal  # Target grid coordinates (x, y)
        self.map_matrix = map_matrix  # Game map matrix
        self.enemy_speed = enemy_speed  # Movement speed
        self.path = []  # Path to follow (list of grid coordinates)
        self.move_counter = 0  # Counter for movement timing
        self.attack_range = 1  # Range for attacking the house or player
        self.damage = 1  # Damage dealt per attack

        # Load animations
        self.animations = self.load_animations(path, animation_sets)
        self.current_animation = "walk"  # Default animation
        self.animation_trigger = False

        # Set initial position
        self.x, self.y = self.game.map[start_position[0]][start_position[1]].x, self.game.map[start_position[0]][start_position[1]].y

        # Find initial path
        self.find_path()

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

    def heuristic(self, a: tuple, b: tuple) -> int:
        """
        Calculate the Manhattan distance between two grid coordinates.

        Args:
            a: First grid coordinates (x, y).
            b: Second grid coordinates (x, y).

        Returns:
            The Manhattan distance between the two coordinates.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self):
        """
        Find a path from the enemy's current position to the goal using A* algorithm.
        """
        open_set = []
        open_set.append((0, self.position))
        came_from = {}
        g_score = {self.position: 0}
        f_score = {self.position: self.heuristic(self.position, self.goal)}

        while open_set:
            _, current = open_set.pop(0)

            if current == self.goal:
                self.path = []
                while current in came_from:
                    self.path.append(current)
                    current = came_from[current]
                self.path.reverse()
                return

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if (
                    0 <= neighbor[0] < len(self.map_matrix)
                    and 0 <= neighbor[1] < len(self.map_matrix[0])
                    and self.map_matrix[neighbor[1]][neighbor[0]] != "M"
                ):
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, self.goal)
                        open_set.append((f_score[neighbor], neighbor))
                        open_set.sort(key=lambda x: x[0])

    def move(self):
        """
        Move the enemy along the calculated path.
        """
        self.move_counter += 1
        if self.move_counter >= self.enemy_speed and self.path:
            self.move_counter = 0
            next_position = self.path.pop(0)
            self.position = next_position
            self.x, self.y = self.game.map[next_position[0]][next_position[1]].x, self.game.map[next_position[0]][next_position[1]].y

    def attack(self):
        """
        Attack the house or player if within range.
        """
        if self.heuristic(self.position, self.goal) <= self.attack_range:
            self.game.house.take_damage(self.damage)
            self.current_animation = "attack"
        else:
            self.current_animation = "walk"

    def take_damage(self, damage: int):
        """
        Reduce the enemy's health by the specified amount.

        Args:
            damage: Amount of damage to take.
        """
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        """
        Handle the enemy's death by removing it from the game.
        """
        self.game.map[self.position[0]][self.position[1]].occupied = False
        self.game.map[self.position[0]][self.position[1]].occupant = None
        self.game.enemy_manager.remove_enemy(self)

    def update(self):
        """
        Update the enemy's state, including movement, attacks, and animations.
        """
        self.move()
        self.attack()
        self.update_animations()
        self.draw(self.sprite)

    def update_animations(self):
        """
        Update the enemy's animations based on the current state.
        """
        if self.animation_trigger:
            self.animation_trigger = False
            self.animations[self.current_animation].rotate(-1)
            self.sprite = self.animations[self.current_animation][0]