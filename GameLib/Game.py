import pygame as pg
import random

# Initialize Pygame
pg.init()

# Constants
GRID_SIZE = 11
CELL_SIZE = 50
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = SCREEN_WIDTH + 100  # Extra space for the menu
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Game:
    """
    The Game class handles the main game logic, including initialization, updates, and rendering.
    """

    def __init__(self, main):
        """
        Initialize the game.

        Args:
            main: The Main class instance (used to access shared resources like screen and clock).
        """
        self.main = main
        self.internal_surface = main.internal_surface
        self.clock = main.clock
        self.running = True

        # Constants
        self.grid_size = 11
        self.cell_size = self.internal_surface.get_width() // self.grid_size
        self.screen_width = self.internal_surface.get_width()
        self.screen_height = self.internal_surface.get_height()

        # Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (169, 169, 169)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)

        # Game objects
        self.grid = [
            [None for _ in range(self.grid_size)] for _ in range(self.grid_size)
        ]
        self.goblin_shark = GoblinShark(self.grid_size // 2, self.grid_size // 2)
        self.house = House(self.grid_size // 2, self.grid_size // 2)
        self.squirrels = []
        self.corals = []

    def init(self):
        """
        Initialize game-specific resources (e.g., player, enemies, map).
        """
        pass

    def update(self):
        """
        Update the game state.
        """
        self.house.produce_sand_dollars()

        for squirrel in self.squirrels:
            squirrel.move_toward_target(self.house)

        for coral in self.corals:
            coral.attack(self.squirrels)

        self.squirrels = [s for s in self.squirrels if s.health > 0]

    def draw(self, surface):
        """
        Draw the game state.

        Args:
            surface: The surface to draw on (internal surface).
        """
        surface.fill(BLACK)
        self.draw_grid(surface)

        self.house.draw(surface)
        self.goblin_shark.draw(surface)

        for squirrel in self.squirrels:
            squirrel.draw(surface)

        for coral in self.corals:
            coral.draw(surface)

        # Draw below-grid menu
        pg.draw.rect(
            surface, GRAY, (0, self.screen_height - 20, self.screen_width, 20)
        )
        font = pg.font.SysFont("Consolas", 16)
        sand_dollars_text = font.render(
            f"Sand Dollars: {self.house.sand_dollars}", True, WHITE
        )
        surface.blit(sand_dollars_text, (10, self.screen_height - 18))

    def draw_grid(self, surface):
        """
        Draw the grid on the surface.

        Args:
            surface: The surface to draw on (internal surface).
        """
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                rect = pg.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pg.draw.rect(surface, WHITE, rect, 1)

    def handle_events(self):
        """
        Handle user input events.
        """
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.goblin_shark.move(0, -1)
        if keys[pg.K_s]:
            self.goblin_shark.move(0, 1)
        if keys[pg.K_a]:
            self.goblin_shark.move(-1, 0)
        if keys[pg.K_d]:
            self.goblin_shark.move(1, 0)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.goblin_shark.attack(self.squirrels)

    def run(self):
        """
        Run the game loop.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw(self.internal_surface)
            pg.display.flip()
            self.clock.tick(self.main.fps)


class GameObject:
    """
    The GameObject class represents a generic game object.
    """

    def __init__(self, x, y, color, health):
        self.x = x
        self.y = y
        self.color = color
        self.health = health

    def draw(self, surface):
        pg.draw.rect(
            surface,
            self.color,
            (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )


class GoblinShark(GameObject):
    """
    The GoblinShark class represents the player character.
    """

    def __init__(self, x, y):
        super().__init__(x, y, BLUE, 5)
        self.energy = 5
        self.cooldown = 0  # Cooldown for planting/moving corals

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            self.x = new_x
            self.y = new_y

    def attack(self, squirrels):
        for squirrel in squirrels:
            if abs(squirrel.x - self.x) <= 1 and abs(squirrel.y - self.y) <= 1:
                squirrel.health -= 0.5


class House(GameObject):
    """
    The House class represents the player's house.
    """

    def __init__(self, x, y):
        super().__init__(x, y, RED, 10)
        self.sand_dollars = 0
        self.timer = 0

    def produce_sand_dollars(self):
        self.timer += 1
        if self.timer >= FPS * 10:  # 10 seconds
            self.sand_dollars += 1
            self.timer = 0


class Squirrel(GameObject):
    """
    The Squirrel class represents an enemy.
    """

    def __init__(self, x, y):
        super().__init__(x, y, GRAY, 1)
        self.timer = 0

    def move_toward_target(self, target):
        if self.timer < FPS * 2:  # Move every 2 seconds
            self.timer += 1
            return

        self.timer = 0
        dx = target.x - self.x
        dy = target.y - self.y

        if abs(dx) > abs(dy):
            self.x += 1 if dx > 0 else -1
        else:
            self.y += 1 if dy > 0 else -1


class Coral(GameObject):
    """
    The Coral class represents a defensive structure.
    """

    def __init__(self, x, y):
        super().__init__(x, y, GREEN, 10)
        self.range = 1

    def attack(self, squirrels):
        for squirrel in squirrels:
            if (
                abs(squirrel.x - self.x) <= self.range
                and abs(squirrel.y - self.y) <= self.range
            ):
                squirrel.health -= 1
