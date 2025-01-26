import pygame as pg
from GameLib.TempEnemy import Enemy
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
            self.enemy_list.append(Enemy(0, init_spot, self.game.map))
        elif side == "bottom" and not self.game.map[10][init_spot].occupied:
            self.enemy_list.append(Enemy(10, init_spot, self.game.map))
        elif side == "left" and not self.game.map[init_spot][0].occupied:
            self.enemy_list.append(Enemy(init_spot, 0, self.game.map))
        elif side == "right" and not self.game.map[init_spot][10].occupied:
            self.enemy_list.append(Enemy(init_spot, 10, self.game.map))

    def updateEnemies(self):
        for enemy in self.enemy_list:
            enemy.update()  # assuming the Enemy class has an update method
            if enemy.is_destroyed():  # check if the enemy should be removed
                self.enemy_list.remove(enemy)

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
