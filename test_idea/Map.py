import pygame as pg
from Game import Game
from MapSlot import Space


def get_map(game):
    return [[Space(game, "grass.png", (i*50+365, j*50), (32, 32)) for j in range(11)] for i in range(11)]
