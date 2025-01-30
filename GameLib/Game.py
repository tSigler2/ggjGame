# File: GameLib\Game.py
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

# Colors
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

        # Game objects
        self.grid = [
            [None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)
        ]  # 11x11 grid
        self.player = Player(
            GRID_SIZE // 2, GRID_SIZE // 2
        )  # Player starts in the center
        self.house = House(GRID_SIZE // 2, GRID_SIZE // 2)  # House starts in the center
        self.squirrels = []  # List of squirrels (enemies)
        self.corals = []  # List of corals (defensive structures)
        self.sand_dollars = 0  # Sand dollar counter

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

        # Update squirrels
        for squirrel in self.squirrels:
            squirrel.move_toward_target(self.house)

        # Update corals
        for coral in self.corals:
            coral.attack(self.squirrels)

        # Remove dead squirrels
        self.squirrels = [s for s in self.squirrels if s.health > 0]

    def draw(self, surface):
        """
        Draw the game state.

        Args:
            surface: The surface to draw on (internal surface).
        """
        surface.fill(BLACK)  # Clear the screen

        # Draw the grid
        self.draw_grid(surface)

        # Draw the house
        self.house.draw(surface)

        # Draw the player
        self.player.draw(surface)

        # Draw squirrels
        for squirrel in self.squirrels:
            squirrel.draw(surface)

        # Draw corals
        for coral in self.corals:
            coral.draw(surface)

        # Draw the sand dollar counter
        self.draw_sand_dollar_counter(surface)

    def draw_grid(self, surface):
        """
        Draw the 11x11 grid on the surface.

        Args:
            surface: The surface to draw on (internal surface).
        """
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pg.Rect(
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )
                pg.draw.rect(surface, WHITE, rect, 1)  # Draw grid lines

    def draw_sand_dollar_counter(self, surface):
        """
        Draw the sand dollar counter bar at the bottom of the screen.

        Args:
            surface: The surface to draw on (internal surface).
        """
        # Draw the bar background
        pg.draw.rect(
            surface,
            GRAY,
            (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100),
        )

        # Draw the sand dollar counter text
        font = pg.font.SysFont("Consolas", 24)
        text_surface = font.render(f"Sand Dollars: {self.sand_dollars}", True, WHITE)
        surface.blit(
            text_surface,
            (10, SCREEN_HEIGHT - 80),
        )

    def handle_events(self, event):
        """
        Handle user input events.
        """
        keys = pg.key.get_pressed()

        # Player movement
        if keys[pg.K_w]:
            self.player.move(0, -1)
        if keys[pg.K_s]:
            self.player.move(0, 1)
        if keys[pg.K_a]:
            self.player.move(-1, 0)
        if keys[pg.K_d]:
            self.player.move(1, 0)

        # Player attack
        if keys[pg.K_SPACE]:
            self.player.attack(self.squirrels)

        # Quit the game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def run(self):
        """
        Run the game loop.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw(self.internal_surface)
            pg.display.flip()
            self.clock.tick(FPS)


class Player:
    """
    The Player class represents the player character.
    """

    def __init__(self, x, y):
        """
        Initialize the player.

        Args:
            x: Initial x-coordinate on the grid.
            y: Initial y-coordinate on the grid.
        """
        self.x = x
        self.y = y
        self.color = BLUE
        self.health = 5
        self.energy = 5

    def move(self, dx, dy):
        """
        Move the player on the grid.

        Args:
            dx: Change in x-coordinate.
            dy: Change in y-coordinate.
        """
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            self.x = new_x
            self.y = new_y

    def attack(self, squirrels):
        """
        Attack squirrels within range.

        Args:
            squirrels: List of squirrels to attack.
        """
        for squirrel in squirrels:
            if abs(squirrel.x - self.x) <= 1 and abs(squirrel.y - self.y) <= 1:
                squirrel.health -= 0.5

    def draw(self, surface):
        """
        Draw the player on the screen.

        Args:
            surface: The surface to draw on (internal surface).
        """
        pg.draw.rect(
            surface,
            self.color,
            (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )


class House:
    """
    The House class represents the player's house.
    """

    def __init__(self, x, y):
        """
        Initialize the house.

        Args:
            x: Initial x-coordinate on the grid.
            y: Initial y-coordinate on the grid.
        """
        self.x = x
        self.y = y
        self.color = RED
        self.health = 10
        self.sand_dollars = 0
        self.timer = 0

    def produce_sand_dollars(self):
        """
        Produce sand dollars over time.
        """
        self.timer += 1
        if self.timer >= FPS * 10:  # 10 seconds
            self.sand_dollars += 1
            self.timer = 0

    def draw(self, surface):
        """
        Draw the house on the screen.

        Args:
            surface: The surface to draw on (internal surface).
        """
        pg.draw.rect(
            surface,
            self.color,
            (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )


class Squirrel:
    """
    The Squirrel class represents an enemy.
    """

    def __init__(self, x, y):
        """
        Initialize the squirrel.

        Args:
            x: Initial x-coordinate on the grid.
            y: Initial y-coordinate on the grid.
        """
        self.x = x
        self.y = y
        self.color = GRAY
        self.health = 1
        self.timer = 0

    def move_toward_target(self, target):
        """
        Move the squirrel toward the target (house).

        Args:
            target: The target to move toward (house).
        """
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

    def draw(self, surface):
        """
        Draw the squirrel on the screen.

        Args:
            surface: The surface to draw on (internal surface).
        """
        pg.draw.rect(
            surface,
            self.color,
            (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )


class Coral:
    """
    The Coral class represents a defensive structure.
    """

    def __init__(self, x, y):
        """
        Initialize the coral.

        Args:
            x: Initial x-coordinate on the grid.
            y: Initial y-coordinate on the grid.
        """
        self.x = x
        self.y = y
        self.color = GREEN
        self.health = 10
        self.range = 1

    def attack(self, squirrels):
        """
        Attack squirrels within range.

        Args:
            squirrels: List of squirrels to attack.
        """
        for squirrel in squirrels:
            if (
                abs(squirrel.x - self.x) <= self.range
                and abs(squirrel.y - self.y) <= self.range
            ):
                squirrel.health -= 1

    def draw(self, surface):
        """
        Draw the coral on the screen.

        Args:
            surface: The surface to draw on (internal surface).
        """
        pg.draw.rect(
            surface,
            self.color,
            (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )
