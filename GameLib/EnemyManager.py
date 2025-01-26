import pygame as pg
from GameLib.Enemy import Enemy
import math
import random as r


class EnemyManager:
    def __init__(self, game, init_spawn_rate, update_interval):
        self.game = game
        self.init_spawn_rate = init_spawn_rate
        self.update_interval = update_interval
        self.rate = self.init_spawn_rate

        self.frame_count = 0
        self.last_spawn_frame = 0

        self.enemy_list = []

    def rate_calc(self):
        # update the spawn rate based on frame count and update interval
        self.rate = self.init_spawn_rate / (
            1 + math.log10(max(1, self.game.frame_count / self.update_interval))
        )

    def spawn(self):
        init_spot = r.randint(0, 10)  # Random spot in a 11x11 grid
        side = r.choice(["top", "bottom", "left", "right"])  # choose a side to spawn

        if side == "top" and not self.game.map[0][init_spot].occupied:
            self.enemy_list.append(Enemy(self.game, 10, (0, init_spot), (6, 6), self.game.map, "GameLib/Assets/squirrel", 120, "attack", "walk", enemy_speed=3))
        elif side == "bottom" and not self.game.map[10][init_spot].occupied:
            self.enemy_list.append(Enemy(self.game, 10, (10, init_spot), (6, 6), self.game.map, "GameLib/Assets/squirrel", 120, "attack", "walk", enemy_speed=3))
        elif side == "left" and not self.game.map[init_spot][0].occupied:
            self.enemy_list.append(
                Enemy(
                    self.game,
                    10,
                    (init_spot, 0),
                    (6, 6),
                    self.game.map,
                    "GameLib/Assets/squirrel",
                    120,
                    "attack",
                    "walk",
                    enemy_speed=3
                )
            )
        elif side == "right" and not self.game.map[init_spot][10].occupied:
            self.enemy_list.append(
                Enemy(
                    self.game,
                    10,
                    (init_spot, 10),
                    (6, 6),
                    self.game.map,
                    "GameLib/Assets/squirrel",
                    120,
                    "attack",
                    "walk",
                    enemy_speed=3
                )
            )

    def updateEnemies(self):
        destroy_list = []
        for enemy in range(len(self.enemy_list)):
            self.enemy_list[
                enemy
            ].update()  # assuming the Enemy class has an update method
            if (
                self.enemy_list[enemy].health <= 0
            ):  # check if the enemy should be removed
                destroy_list.append(enemy)

        for enemy in destroy_list:
            self.game.map[enemy.position[0]][enemy.position[1]].occupied = False
            self.game.map[enemy.position[0]][enemy.position[1]].occupant = None
            self.enemy_list.pop(enemy)

    def update(self):
        self.frame_count += 1

        # recalculate spawn rate periodically
        if self.frame_count % self.update_interval == 0:
            self.rate_calc()

        # spawn new enemies based on the spawn rate
        if self.frame_count - self.last_spawn_frame >= self.rate:
            self.spawn()
            self.last_spawn_frame = self.frame_count

        self.updateEnemies()
