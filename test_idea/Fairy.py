import pygame as pg
import math
import heapq
from Game import Game
from MapSlot import Space

class Fairy:
    def __init__(self, game, path, init_spawn_rate, growth_rate, coords, move_speed):
        self.game = game
        self.sprite = pg.image.load(file).convert_alpha()

        self.x, self.y = coords

        self.spawn_rate = init_spawn_rate
        self.growth_rate = growth_rate

        self.move_speed = self.move_speed
        self.move_delta = 0

    def move(self, new_coords):
        self.x, self.y = newcoords

    def path_find(self):
        goal = (0, 0)

        node_list = [(self.x, self.y)]

        came_from = {}


