import os
import pygame as pg
from MapSlot import Space


class Map:
    @staticmethod
    def get_map(game):
        # Construct the absolute path for Sand_tile.png
        asset_path = os.path.join(os.path.dirname(__file__), "Assets", "Sand_tile.png")

        return [
            [
                Space(game, asset_path, (i * 64 + 288, j * 64), (64, 64))
                for j in range(11)
            ]
            for i in range(11)
        ]
