import os
import pygame as pg
from GameLib.MapSlot import Space


class Map:
    @staticmethod
    def get_map(game):
        asset_path = os.path.join(os.path.dirname(__file__), "Assets", "Sand_tile.png")

        tile_size = 64  # Updated tile size
        grid_start_x = (game.width - 11 * tile_size) // 2
        grid_start_y = (game.height - 11 * tile_size) // 2

        map_grid = []
        for row in range(11):
            grid_row = []
            for col in range(11):
                x = grid_start_x + col * tile_size
                y = grid_start_y + row * tile_size
                grid_row.append(Space(game, asset_path, (x, y), (tile_size, tile_size)))
            map_grid.append(grid_row)

        return map_grid
