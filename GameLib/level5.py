import pygame as pg
import sys
import random
from queue import PriorityQueue


class Level5:
    def __init__(self, dims, fps=60):
        pg.init()
        self.width, self.height = dims
        self.fps = fps
        self.screen = pg.display.set_mode(dims)
        pg.display.set_caption("Green Field with Maze")
        self.clock = pg.time.Clock()

        # Tile and Map Properties
        self.tile_size = 40
        self.map_matrix = [
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "M", "M", "M", "M", "M", "M", "M", "M", "0"],
            ["0", "M", "0", "0", "0", "0", "0", "0", "M", "0"],
            ["0", "M", "0", "H", "H", "H", "M", "0", "M", "0"],
            ["0", "M", "0", "H", "H", "H", "M", "0", "M", "0"],
            ["0", "M", "0", "H", "H", "H", "M", "0", "M", "0"],
            ["0", "M", "0", "0", "0", "0", "M", "0", "0", "0"],
            ["0", "M", "M", "M", "M", "M", "M", "M", "M", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
        ]
        self.colors = {
            "0": (34, 139, 34),  # Green (Grass)
            "H": (139, 69, 19),  # Brown (House)
            "M": (255, 0, 0),  # Red (Mushroom)
        }

        # Enemy Properties
        self.enemies = []
        self.spawn_rate = 120  # Spawn an enemy every 120 frames
        self.enemy_color = (255, 255, 255)  # White
        self.frame_count = 0
        self.enemy_speed = 3  # Adjust this to control the speed of the enemies

        # Pathfinding Properties
        self.goal = (4, 4)  # Center of the house

    def draw_map(self):
        for row_idx, row in enumerate(self.map_matrix):
            for col_idx, tile in enumerate(row):
                x, y = col_idx * self.tile_size, row_idx * self.tile_size
                pg.draw.rect(
                    self.screen,
                    self.colors[tile],
                    (x, y, self.tile_size, self.tile_size),
                )
                if tile == "M":  # Draw mushrooms as circles
                    pg.draw.circle(
                        self.screen,
                        (255, 255, 255),
                        (x + self.tile_size // 2, y + self.tile_size // 2),
                        self.tile_size // 3,
                    )

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def astar(self, start, goal):
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while not open_set.empty():
            _, current = open_set.get()

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if (
                    0 <= neighbor[1] < len(self.map_matrix)  # Check rows first
                    and 0 <= neighbor[0] < len(self.map_matrix[0])  # Then columns
                    and self.map_matrix[neighbor[1]][neighbor[0]]
                    != "M"  # Corrected access
                ):
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(
                            neighbor, goal
                        )
                        open_set.put((f_score[neighbor], neighbor))
        return []

    def spawn_enemy(self):
        start_x = random.choice([0, len(self.map_matrix[0]) - 1])
        start_y = random.choice([0, len(self.map_matrix) - 1])
        start = (start_x, start_y)
        path = self.astar(start, self.goal)
        if path:
            self.enemies.append({"path": path, "index": 0, "move_counter": 0})

    def update_enemies(self):
        for enemy in self.enemies:
            enemy["move_counter"] += 1
            if enemy["move_counter"] >= self.enemy_speed:
                enemy["move_counter"] = 0
                if enemy["index"] < len(enemy["path"]) - 1:
                    enemy["index"] += 1

    def draw_enemies(self):
        for enemy in self.enemies:
            if enemy["index"] < len(enemy["path"]):
                x, y = enemy["path"][enemy["index"]]
                pg.draw.circle(
                    self.screen,
                    self.enemy_color,
                    (
                        x * self.tile_size + self.tile_size // 2,
                        y * self.tile_size + self.tile_size // 2,
                    ),
                    self.tile_size // 4,
                )

    def update(self):
        self.screen.fill((0, 0, 0))  # Black background
        self.draw_map()
        self.update_enemies()
        self.draw_enemies()
        pg.display.flip()  # Refresh display

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.frame_count += 1
            if self.frame_count % self.spawn_rate == 0:
                self.spawn_enemy()

            self.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    level5 = Level5((800, 600))
    level5.run()
