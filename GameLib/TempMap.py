import os
import pygame as pg
from GameLib.TempMapSlot import Space


class Map:
    @staticmethod
    def get_map(game):
        # Construct the absolute path for Sand_tile.png
        asset_path = os.path.join(os.path.dirname(__file__), "Assets", "Sand_tile.png")

        return [
            [
                Space(game, asset_path, (i * 50 + 365, j * 50), (32, 32))
                for j in range(11)
            ]
            for i in range(11)
        ]
