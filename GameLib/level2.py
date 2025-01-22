import pygame as pg
import sys
import random


class Level2:
    def __init__(self, dims, fps=60):
        # Initialize PyGame and game variables
        pg.init()
        self.width, self.height = dims
        self.fps = fps
        self.screen = pg.display.set_mode(dims)
        pg.display.set_caption("Level 2: Pole Position")
        self.clock = pg.time.Clock()

        # Road properties
        self.road_width = 300
        self.road_color = (50, 50, 50)
        self.grass_color = (0, 150, 0)
        self.line_color = (255, 255, 255)

        # Player properties
        self.car_width = 40
        self.car_height = 70
        self.car_x = self.width // 2  # Start centered
        self.car_y = self.height - 100
        self.car_color = (0, 0, 255)
        self.car_speed = 3  # Player speed

        # Road variables
        self.segments = 200  # Total road segments
        self.segment_length = 15  # Vertical height of each road segment
        self.road = []  # List to store road segment data
        self.scroll_position = 0  # Tracks how far the road has scrolled
        self.player_offset = 0  # Player's horizontal offset relative to road

        self.generate_road()

        # Game variables
        self.running = True

    def generate_road(self):
        """Generate the road's curvature data."""
        self.road = [0]  # Starting curve
        for _ in range(self.segments - 1):
            curve_change = random.choice([-1, 0, 1])  # Random curve
            self.road.append(self.road[-1] + curve_change)

    def draw_road(self):
        """Draw the road with perspective and curvature."""
        base_y = self.height
        curve_accumulation = 0  # Total horizontal curve offset
        scale = 1  # Perspective scaling factor

        for i in range(len(self.road) - 1, -1, -1):
            curve_accumulation += self.road[i]

            # Perspective scaling for current and next segment
            scale_current = scale
            scale_next = scale * 1.05

            # Calculate road widths
            road_width_current = scale_current * self.road_width
            road_width_next = scale_next * self.road_width

            # Calculate screen coordinates for road edges
            x1 = (
                self.width // 2
                + curve_accumulation
                - road_width_current / 2
                + self.player_offset * scale_current
            )
            x2 = (
                self.width // 2
                + curve_accumulation
                + road_width_current / 2
                + self.player_offset * scale_current
            )
            x3 = (
                self.width // 2
                + curve_accumulation
                - road_width_next / 2
                + self.player_offset * scale_next
            )
            x4 = (
                self.width // 2
                + curve_accumulation
                + road_width_next / 2
                + self.player_offset * scale_next
            )

            # Calculate vertical positions
            y1 = base_y - self.segment_length * scale_current
            y2 = base_y

            # Draw road segment
            pg.draw.polygon(
                self.screen, self.road_color, [(x1, y1), (x2, y1), (x4, y2), (x3, y2)]
            )
            base_y = y1

            # Add lane markers
            if i % 10 == 0:
                lane_marker_x1 = (x1 + x2) / 2
                lane_marker_x2 = (x3 + x4) / 2
                pg.draw.line(
                    self.screen,
                    self.line_color,
                    (lane_marker_x1, y1),
                    (lane_marker_x2, y2),
                    2,
                )

            # Grass
            grass_width = 1.5 * road_width_current
            pg.draw.polygon(
                self.screen,
                self.grass_color,
                [
                    (x1 - grass_width, y1),
                    (x2 + grass_width, y1),
                    (x4 + grass_width, y2),
                    (x3 - grass_width, y2),
                ],
            )

            scale *= 0.95  # Reduce scale to simulate perspective

    def handle_input(self):
        """Handle player input."""
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.player_offset -= self.car_speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.player_offset += self.car_speed

    def draw_player(self):
        """Draw the player's car."""
        car_x = self.width // 2 + self.player_offset
        pg.draw.rect(
            self.screen,
            self.car_color,
            (car_x - self.car_width // 2, self.car_y, self.car_width, self.car_height),
        )

    def update_scroll(self):
        """Update the scrolling position of the road."""
        self.scroll_position += 2
        if self.scroll_position >= self.segment_length:
            self.scroll_position -= self.segment_length
            self.road.pop(0)
            curve_change = random.choice([-1, 0, 1])
            self.road.append(self.road[-1] + curve_change)

    def run(self):
        """Main game loop."""
        while self.running:
            # Event handling
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            # Game logic
            self.handle_input()
            self.update_scroll()

            # Drawing
            self.screen.fill((135, 206, 235))  # Sky blue background
            self.draw_road()
            self.draw_player()

            # Update the display
            pg.display.flip()
            self.clock.tick(self.fps)

        pg.quit()
        sys.exit()


if __name__ == "__main__":
    game = Level2((800, 600))
    game.run()
