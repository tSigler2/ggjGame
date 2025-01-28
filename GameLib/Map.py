import os
from Tile import Tile


class Map:
    """
    The Map class manages a grid of tiles.
    """

    def __init__(self, game, tile_size: int, map_matrix: list, tile_images: dict):
        """
        Initialize the map.

        Args:
            game: The main game object.
            tile_size: Size of each tile (width and height).
            map_matrix: 2D list representing the map layout.
            tile_images: Dictionary mapping tile types to image paths.
        """
        self.game = game
        self.tile_size = tile_size
        self.map_matrix = map_matrix
        self.tile_images = tile_images
        self.tiles = self.load_tiles()

    def load_tiles(self) -> list:
        """
        Load tiles based on the map matrix and tile images.

        Returns:
            A 2D list of Tile objects.
        """
        tiles = []
        for row_idx, row in enumerate(self.map_matrix):
            tile_row = []
            for col_idx, tile_type in enumerate(row):
                x = col_idx * self.tile_size
                y = row_idx * self.tile_size
                image_path = self.tile_images.get(tile_type, "Assets/default_tile.png")
                tile = Tile(self.game, x, y, self.tile_size, self.tile_size, image_path)
                tile_row.append(tile)
            tiles.append(tile_row)
        return tiles

    def draw(self):
        """
        Draw the entire map.
        """
        for row in self.tiles:
            for tile in row:
                tile.draw()

    def update(self):
        """
        Update the map and its tiles.
        """
        self.draw()
