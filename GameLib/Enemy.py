# File: GameLib\enemy.py
import pygame as pg
from heapq import heappush, heappop


class Enemy:
    def __init__(self, x, y, size, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.path = []

    def draw(self, screen):
        pg.draw.rect(
            screen,
            self.color,
            (self.x * self.size, self.y * self.size, self.size, self.size),
        )

    """
        This is A* pathfinding algorithm.
        - grid: 2D list representing the maze
        - start: (row, col) tuple of the start position
        - end: (row, col) tuple of the target position
        - return: List of (row, col) tuples representing the path
    """

    def pathfinding(self, grid, start, end):
        def heuristic(a, b):
            # Manhattan distance
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_set = []
        heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, end)}

        while open_set:
            _, current = heappop(open_set)

            if current == end:
                # Reconstruct the path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]  # Return the reversed path

            # Check neighbors (up, down, left, right)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)

                # Make sure the neighbor is within bounds and not an obstacle
                if (
                    0 <= neighbor[0] < len(grid)
                    and 0 <= neighbor[1] < len(grid[0])
                    and grid[neighbor[0]][neighbor[1]]
                    == 0  # Check for empty space (not obstacle)
                ):
                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                        heappush(open_set, (f_score[neighbor], neighbor))

        return []  # No path found, return empty list
