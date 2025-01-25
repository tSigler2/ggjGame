# File: test_idea\Fairy.py
import sys
import pygame as pg
import math
import heapq
from Game import Game
from test_idea.MapSlot import Space
import os


class Fairy:
    def __init__(self, game, path, init_spawn_rate, growth_rate, coords, move_speed):
        self.game = game
        # Check if the sprite file exists
        if not os.path.exists(path):
            print(f"Error: File '{path}' not found.")
            sys.exit(1)  # Exit the program if the file is not found
        self.sprite = pg.image.load(path).convert_alpha()
        self.x, self.y = coords
        self.spawn_rate = init_spawn_rate
        self.growth_rate = growth_rate
        self.move_speed = move_speed
        self.move_delta = 0

    def move(self, new_coords):
        self.x, self.y = new_coords

    def path_find(self):
        goal = (0, 0)

        node_list = [(self.x, self.y)]

        came_from = {}
