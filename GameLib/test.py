import pygame as pg
import sys
from GameLib.enemy import Enemy

# Setup Pygame
pg.init()

# Display
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Enemy Pathfinding Test")

# Map Configuration
tile_size = 40
map_matrix = [
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

colors = {
    "0": (194, 178, 128),  # Sand (light beige)
    "H": (139, 69, 19),  # House (brown))
    "M": (255, 0, 255),  # Coral (magenta)
}

# Setup Enemy
start_position = (0, 0)
goal = (4, 4)
enemy = Enemy(start_position, goal, map_matrix)

# Game Loop
clock = pg.time.Clock()
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen

    # Draw Map
    for row_idx, row in enumerate(map_matrix):
        for col_idx, tile in enumerate(row):
            x, y = col_idx * tile_size, row_idx * tile_size
            pg.draw.rect(
                screen,
                colors[tile],
                (x, y, tile_size, tile_size),
            )

    # Move Enemy
    enemy.move()
    enemy_position = enemy.get_position()
    ex, ey = enemy_position
    pg.draw.circle(
        screen,
        (255, 255, 255),  # White for enemy
        (ex * tile_size + tile_size // 2, ey * tile_size + tile_size // 2),
        tile_size // 4,
    )

    # Event Handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Update Display
    pg.display.flip()

    # Frame rate
    clock.tick(10)

pg.quit()
sys.exit()
