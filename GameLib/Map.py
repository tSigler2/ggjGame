import pygame as pg
from MapSlot import Space


class Map:
    @staticmethod
    def get_map(game):
        return [
            [
                Space(game, "Assets/Sand_tile.png", (i * 50 + 365, j * 50), (32, 32))
                for j in range(11)
            ]
            for i in range(11)
        ]
