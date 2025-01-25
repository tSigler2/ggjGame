import pygame as pg
from test_idea.Game import Game
from test_idea.MapSlot import Space

class Map:
    def get_map(game):
        return [[Space(game, "grass.png", (i*50+365, j*50), (32, 32)) for j in range(11)] for i in range(11)]
