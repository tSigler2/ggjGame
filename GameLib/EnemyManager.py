from Enemy import Enemy
import random as r
import math


class EnemyManager:
    """
    The EnemyManager class manages all enemy instances in the game.
    It handles spawning, updating, and removing enemies.
    """

    def __init__(self, game, init_spawn_rate: int, update_interval: int):
        """
        Initialize the enemy manager.

        Args:
            game: The main game object.
            init_spawn_rate: Initial spawn rate (in frames).
            update_interval: Interval for recalculating spawn rate (in frames).
        """
        self.game = game
        self.init_spawn_rate = init_spawn_rate
        self.update_interval = update_interval
        self.spawn_rate = init_spawn_rate  # Current spawn rate
        self.enemies = []  # List of active enemy instances
        self.frame_count = 0  # Frame counter for spawn timing
        self.last_spawn_frame = 0  # Frame count of the last spawn

    def spawn_enemy(self):
        """
        Spawn a new enemy at a random edge of the map.
        """
        # Randomly choose a side to spawn the enemy
        side = r.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x, y = r.randint(0, 10), 0
        elif side == "bottom":
            x, y = r.randint(0, 10), 10
        elif side == "left":
            x, y = 0, r.randint(0, 10)
        elif side == "right":
            x, y = 10, r.randint(0, 10)

        # Ensure the spawn tile is not occupied
        if not self.game.map[x][y].occupied:
            enemy = Enemy(
                game=self.game,
                health=10,
                start_position=(x, y),
                goal=(5, 5),  # Target the center of the map
                map_matrix=self.game.map_matrix,
                path="Assets/enemy",
                animation_time=120,
                "walk",
                "attack",
                enemy_speed=3,
            )
            self.enemies.append(enemy)
            self.game.map[x][y].occupied = True
            self.game.map[x][y].occupant = enemy

    def remove_enemy(self, enemy):
        """
        Remove an enemy from the game.

        Args:
            enemy: The enemy instance to remove.
        """
        if enemy in self.enemies:
            self.enemies.remove(enemy)
            self.game.map[enemy.position[0]][enemy.position[1]].occupied = False
            self.game.map[enemy.position[0]][enemy.position[1]].occupant = None

    def update_spawn_rate(self):
        """
        Update the spawn rate based on the current frame count.
        """
        self.spawn_rate = self.init_spawn_rate / (
            1 + math.log10(max(1, self.frame_count / self.update_interval))
        )

    def update_enemies(self):
        """
        Update all active enemies in the game.
        """
        enemies_to_remove = []
        for enemy in self.enemies:
            enemy.update()
            if enemy.health <= 0:
                enemies_to_remove.append(enemy)

        # Remove dead enemies
        for enemy in enemies_to_remove:
            self.remove_enemy(enemy)

    def update(self):
        """
        Update the enemy manager, including spawning and updating enemies.
        """
        self.frame_count += 1

        # Recalculate spawn rate periodically
        if self.frame_count % self.update_interval == 0:
            self.update_spawn_rate()

        # Spawn new enemies based on the spawn rate
        if self.frame_count - self.last_spawn_frame >= self.spawn_rate:
            self.spawn_enemy()
            self.last_spawn_frame = self.frame_count

        # Update all enemies
        self.update_enemies()