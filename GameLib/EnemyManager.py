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
        self.rate = (init_spawn_rate/(1 + math.log10(self.game.frame_count/self.update_interval)))

    def spawn(self):
        init_spot = r.randint(0, 11)
        if r.randint(0, 2) == 0:
            if r.randint(0, 2) == 0 and not self.game.map[0][init_spot].occupied:
                self.enemy_list.append(Enemy(0, (init_spot)), self.game.map))
            elif not self.game.map[10][init_spot].occupied:
                self.enemy_list.append(Enemy(10, (init_spot)), self.game.map))
        else:
            if r.randint(0, 2) == 0 and not self.game.map[init_spot][0].occupied:
                self.enemy_list.append(Enemy((init_spot), 0), self.game.map))
            elif not self.game.map[init_spot][10].occupied:
                self.enemy_list.append(Enemy((init_spot), 10), self.game.map))

    def updateEnemyies(self):
        for enemy in self.enemyList:
            enemy.
