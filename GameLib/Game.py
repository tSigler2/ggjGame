# Re-work this later
import pygame
import sys
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()

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


# Game objects
class GameObject:
    def __init__(self, x, y, color, health):
        self.x = x
        self.y = y
        self.color = color
        self.health = health

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )


class GoblinShark(GameObject):
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


# Game class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Squirrely Pop: The Last Stand")
        self.running = True
        self.clock = pygame.time.Clock()
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.goblin_shark = GoblinShark(GRID_SIZE // 2, GRID_SIZE // 2)
        self.house = House(GRID_SIZE // 2, GRID_SIZE // 2)
        self.squirrels = []
        self.corals = []

    def spawn_squirrel(self):
        x, y = random.choice(
            [
                (0, random.randint(0, GRID_SIZE - 1)),
                (GRID_SIZE - 1, random.randint(0, GRID_SIZE - 1)),
                (random.randint(0, GRID_SIZE - 1), 0),
                (random.randint(0, GRID_SIZE - 1), GRID_SIZE - 1),
            ]
        )
        self.squirrels.append(Squirrel(x, y))

    def draw_grid(self):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.goblin_shark.move(0, -1)
        if keys[K_s]:
            self.goblin_shark.move(0, 1)
        if keys[K_a]:
            self.goblin_shark.move(-1, 0)
        if keys[K_d]:
            self.goblin_shark.move(1, 0)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.goblin_shark.attack(self.squirrels)

    def update(self):
        self.house.produce_sand_dollars()

        for squirrel in self.squirrels:
            squirrel.move_toward_target(self.house)

        for coral in self.corals:
            coral.attack(self.squirrels)

        self.squirrels = [s for s in self.squirrels if s.health > 0]

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()

        self.house.draw(self.screen)
        self.goblin_shark.draw(self.screen)

        for squirrel in self.squirrels:
            squirrel.draw(self.screen)

        for coral in self.corals:
            coral.draw(self.screen)

        # Draw below-grid menu
        pygame.draw.rect(self.screen, GRAY, (0, SCREEN_WIDTH, SCREEN_WIDTH, 100))
        font = pygame.font.Font(None, 36)
        sand_dollars_text = font.render(
            f"Sand Dollars: {self.house.sand_dollars}", True, WHITE
        )
        self.screen.blit(sand_dollars_text, (10, SCREEN_WIDTH + 10))

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
