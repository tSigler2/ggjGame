import pygame as pg
import sys
import random


class Level2:
    def __init__(self, dims, fps=60):
        pg.init()
        self.width, self.height = dims
        self.fps = fps
        self.screen = pg.display.set_mode(dims)
        pg.display.set_caption("Level 2: Pole Position")
        self.clock = pg.time.Clock()

        # Colors
        self.colors = {
            "road": (50, 50, 50),
            "grass": (0, 150, 0),
            "line": (255, 255, 255),
            "car": (0, 0, 255),
            "obstacle": (255, 0, 0),
        }

        # Road properties
        self.road_width = 300
        self.segment_length = 10
        self.segments = 100
        self.curves = [0] * self.segments
        self.scroll = 0
        self.generate_curves()

        # Player car
        self.car = {"width": 30, "height": 50, "x_offset": 0, "speed": 2.5}
        self.car["y"] = self.height - 100

        # Obstacles
        self.obstacles = []
        self.spawn_timer = 0
        self.spawn_delay = 60

        # Game variables
        self.running = True

    def generate_curves(self):
        curve_amplitude = 2
        for i in range(self.segments):
            if i % 20 == 0:
                curve_amplitude = random.choice([-2, 0, 2])
            self.curves[i] = curve_amplitude

    def project_road(self):
        for i in range(self.segments - 1, 0, -1):
            perspective = self.height / (i + 1)
            road_width = perspective * (self.road_width / self.height)
            curve_offset = sum(self.curves[:i]) * perspective
            x1 = self.width // 2 - road_width + curve_offset
            x2 = self.width // 2 + road_width + curve_offset
            y1 = self.height - i * self.segment_length + self.scroll
            y2 = self.height - (i - 1) * self.segment_length + self.scroll

            if y1 >= 0 and y2 >= 0:
                pg.draw.polygon(
                    self.screen,
                    self.colors["road"],
                    [(x1, y1), (x2, y1), (x2, y2), (x1, y2)],
                )
                if i % 10 == 0:
                    lane_x = (x1 + x2) // 2
                    pg.draw.line(
                        self.screen, self.colors["line"], (lane_x, y1), (lane_x, y2), 2
                    )

    def spawn_obstacle(self):
        if self.spawn_timer >= self.spawn_delay:
            position = random.uniform(-0.8, 0.8)
            self.obstacles.append([position, self.segments - 1])
            self.spawn_timer = 0

    def update_obstacles(self):
        self.obstacles = [o for o in self.obstacles if o[1] > 0]
        for obstacle in self.obstacles:
            obstacle[1] -= 1
            obs_x = (
                self.width // 2
                + sum(self.curves[: obstacle[1]])
                - (self.car["width"] / 2)
            )
            if (
                5 < self.segments - obstacle[1] < 15
                and abs(self.car["x_offset"] - obs_x) < self.car["width"]
            ):
                self.running = False

    def handle_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.car["x_offset"] -= self.car["speed"]
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.car["x_offset"] += self.car["speed"]

    def draw_car(self):
        car_x = self.width // 2 + self.car["x_offset"]
        pg.draw.rect(
            self.screen,
            self.colors["car"],
            (
                car_x - self.car["width"] // 2,
                self.car["y"] - self.car["height"],
                self.car["width"],
                self.car["height"],
            ),
        )

    def show_game_over(self):
        font = pg.font.Font(None, 74)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)
        pg.display.flip()
        pg.time.wait(3000)

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.handle_input()
            self.scroll += 2
            if self.scroll >= self.segment_length:
                self.scroll = 0
                self.curves.pop(0)
                self.curves.append(random.choice([-1, 0, 1]))

            self.spawn_timer += 1
            self.spawn_obstacle()
            self.update_obstacles()

            self.screen.fill(self.colors["grass"])
            self.project_road()
            self.draw_car()
            pg.display.flip()
            self.clock.tick(self.fps)

        self.show_game_over()


if __name__ == "__main__":
    game = Level2((800, 600))
    game.run()
