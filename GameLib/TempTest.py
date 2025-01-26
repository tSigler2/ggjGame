# File: GameLib\Test.py
import pygame as pg
import sys
from GameLib.TempEnemy import Enemy


class Test:
    def __init__(self, dims):
        pg.init()
        self.width, self.height = dims
        self.screen = pg.display.set_mode(dims)
        pg.display.set_caption("Enemy Pathfinding Test")
        self.clock = pg.time.Clock()
        self.tile_size = 40
        self.running = True
        self.show_path = False  # Debugging toggle

        # Map Configuration
        self.map_matrix = [
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "M", "M", "M", "M", "M", "M", "M", "M", "M", "0"],
            ["0", "M", "0", "0", "0", "0", "0", "0", "0", "M", "0"],
            ["0", "M", "0", "H", "H", "H", "M", "M", "0", "M", "0"],
            ["0", "M", "0", "H", "H", "H", "M", "0", "0", "M", "0"],
            ["0", "M", "0", "H", "H", "H", "M", "0", "M", "M", "0"],
            ["0", "M", "0", "0", "0", "0", "M", "0", "0", "M", "0"],
            ["0", "M", "M", "M", "0", "0", "M", "M", "0", "M", "0"],
            ["0", "0", "0", "M", "M", "M", "M", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
        ]
        self.colors = {
            "0": (194, 178, 128),  # Sand
            "H": (139, 69, 19),  # House
            "M": (255, 0, 255),  # Magenta
        }

        # Setup Enemies
        self.enemies = [
            Enemy(100, (0, 0), (4, 4), self.map_matrix, enemy_speed=6),
            Enemy((100, 0, 0), (4, 4), self.map_matrix, enemy_speed=3),
            Enemy(100, (0, 0), (4, 4), self.map_matrix, enemy_speed=1),
        ]

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def draw_map(self):
        for row_idx, row in enumerate(self.map_matrix):
            for col_idx, tile in enumerate(row):
                x, y = col_idx * self.tile_size, row_idx * self.tile_size
                pg.draw.rect(
                    self.screen,
                    self.colors[tile],
                    (x, y, self.tile_size, self.tile_size),
                )

    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.move()
            if self.show_path:
                for px, py in enemy.path:
                    pg.draw.circle(
                        self.screen,
                        (0, 255, 0),
                        (
                            px * self.tile_size + self.tile_size // 2,
                            py * self.tile_size + self.tile_size // 2,
                        ),
                        self.tile_size // 8,
                    )
            ex, ey = enemy.get_position()
            pg.draw.circle(
                self.screen,
                (255, 255, 255),
                (
                    ex * self.tile_size + self.tile_size // 2,
                    ey * self.tile_size + self.tile_size // 2,
                ),
                self.tile_size // 4,
            )

    def run(self):
        while self.running:
            self.handle_events()
            self.screen.fill((0, 0, 0))
            self.draw_map()
            self.draw_enemies()
            pg.display.flip()
            self.clock.tick(10)

        pg.quit()
        sys.exit()
