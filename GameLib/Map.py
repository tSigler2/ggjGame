import os
import pygame as pg
from GameLib.MapSlot import Space


class Map:
    @staticmethod
    def get_map(game):
        # Construct the absolute path for Sand_tile.png
        asset_path = os.path.join(os.path.dirname(__file__), "Assets", "Sand_tile.png")

        # Calculate offsets dynamically based on screen dimensions
        grid_start_x = (game.width - 11 * 50) // 2  # Center the grid horizontally
        grid_start_y = (game.height - 11 * 50) // 2  # Center the grid vertically

        return [
            [
                Space(
                    game, asset_path, (i * 50 + grid_start_x, j * 50 + grid_start_y), (32, 32)
                )
                for j in range(11)
            ]
            for i in range(11)
        ]
