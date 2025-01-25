# File: GameLib\test.py
import pygame as pg
import sys
from GameLib.enemy import Enemy


class Test:
    def __init__(self, dims=(600, 600), grid_size=11):
        pg.init()
        self.width, self.height = dims
        self.cell_size = self.width // grid_size
        self.grid_size = grid_size
        self.screen = pg.display.set_mode(dims)
        pg.display.set_caption("Pathfinding Test")
        self.clock = pg.time.Clock()

        self.maze = [
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", "#", "#", "#", " ", "#", "#", "#", " ", " "],
            [" ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " "],
            [" ", "#", "#", " ", "#", " ", "#", "#", "#", "#", " "],
            [" ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", "#", " ", " ", " ", "#", "#", " "],
            [" ", "#", " ", "#", "#", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", "#", "#", "#", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        ]

        # make the maze to a grid of 0 (empty) and 1 (obstacle)
        self.grid = self.convert_maze_to_grid()

        # put the house in the center of the maze
        self.house = (grid_size // 2, grid_size // 2)

        # spawn the enemy at the top-left corner
        self.enemy = Enemy(0, 0, self.cell_size)
        self.enemy.path = self.enemy.pathfinding(self.grid, (0, 0), self.house)

    def convert_maze_to_grid(self):
        # Convert the maze into a grid of 0's and 1's
        grid = []
        for row in self.maze:
            grid_row = []
            for cell in row:
                if cell == "#":  # Obstacle
                    grid_row.append(1)
                else:  # Empty space or house
                    grid_row.append(0)
            grid.append(grid_row)
        return grid

    def draw_grid(self):
        # Draw the grid with obstacles, empty spaces, and the house
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                color = (255, 255, 255)  # Default empty space (white)
                if self.grid[row][col] == 1:
                    color = (50, 50, 50)  # Obstacle (dark gray)
                elif (row, col) == self.house:
                    color = (0, 255, 0)  # House (green)
                pg.draw.rect(
                    self.screen,
                    color,
                    (
                        col * self.cell_size,
                        row * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

    def update(self):
        if self.enemy.path:
            next_pos = self.enemy.path.pop(0)
            self.enemy.x, self.enemy.y = next_pos

    def draw(self):
        self.screen.fill((0, 0, 0))  # background color
        self.draw_grid()
        self.enemy.draw(self.screen)
        pg.display.flip()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.update()
            self.draw()
            self.clock.tick(5)  # slow down


if __name__ == "__main__":
    game = Test()
    game.run()
