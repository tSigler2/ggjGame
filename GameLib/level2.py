import pygame as pg
import sys
import random


class Level2:
    def __init__(self, dims, fps=60):
        pg.init()  # initialize pygame
        self.width, self.height = dims  # set screen dimensions
        self.fps = fps  # frames per second
        self.screen = pg.display.set_mode(dims)  # create the display window
        pg.display.set_caption("Level 2: Pole Position-like")  # set window title
        self.clock = pg.time.Clock()  # for controlling game frame rate

        # Road properties
        self.road_width = 500  # road width
        self.road_color = (0, 0, 0)  # black road color
        self.grass_color = (0, 150, 0)  # green grass color
        self.line_color = (255, 255, 0)  # yellow lane markers

        # Player properties
        self.car_width = 40  # car width
        self.car_height = 70  # car height
        self.car_x = self.width // 2  # start car centered
        self.car_y = self.height - 100  # place car near bottom
        self.car_color = (0, 0, 255)  # blue car color
        self.car_speed = 3  # car speed

        # Road variables
        self.segments = 200  # total number of road segments
        self.segment_length = 15  # height of each road segment
        self.road = []  # list to store road curve data
        self.scroll_position = 0  # tracks how far road has scrolled
        self.player_offset = 0  # player's horizontal position relative to road

        self.generate_road()  # generate road's curve data

        # Game variables
        self.running = True  # game running state

    def generate_road(self):
        """Generate the road's curvature data."""
        self.road = [0]  # starting with no curve
        for _ in range(self.segments - 1):
            curve_change = random.choice([-1, 0, 1])  # random curve direction
            self.road.append(self.road[-1] + curve_change)  # apply curve change

    def draw_road(self):
        """Draw the road with perspective and curvature."""
        base_y = self.height  # start drawing from the bottom
        curve_accumulation = 0  # total horizontal curve offset
        scale = 1  # perspective scaling factor

        for i in range(
            len(self.road) - 1, -1, -1
        ):  # loop through road segments in reverse
            curve_accumulation += self.road[i]  # accumulate the curve offset

            scale_current = scale  # current segment scale
            scale_next = scale * 1.05  # next segment will be slightly larger

            road_width_current = (
                scale_current * self.road_width
            )  # calculate width of current segment
            road_width_next = (
                scale_next * self.road_width
            )  # calculate width of next segment

            # calculate x coordinates for road edges
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

            y1 = (
                base_y - self.segment_length * scale_current
            )  # top of the current segment
            y2 = base_y  # bottom of the current segment

            # Draw grass (background)
            grass_width = 4 * road_width_current  # make grass wider than the road
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

            # Draw road segment
            pg.draw.polygon(
                self.screen, self.road_color, [(x1, y1), (x2, y1), (x4, y2), (x3, y2)]
            )
            base_y = y1  # update base_y for next segment

            # Add lane markers
            if i % 10 == 0:  # add lane markers every 10th segment
                lane_marker_x1 = (x1 + x2) / 2  # middle of left lane
                lane_marker_x2 = (x3 + x4) / 2  # middle of right lane
                pg.draw.line(
                    self.screen,
                    self.line_color,
                    (lane_marker_x1, y1),
                    (lane_marker_x2, y2),
                    2,
                )

            scale *= 0.95  # reduce scale to simulate perspective

    def handle_input(self):
        """Handle player input."""
        keys = pg.key.get_pressed()  # get all key states
        if keys[pg.K_LEFT] or keys[pg.K_a]:  # move left
            self.player_offset -= self.car_speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:  # move right
            self.player_offset += self.car_speed

    def draw_player(self):
        """Draw the player's car."""
        car_x = self.width // 2 + self.player_offset  # calculate car's x position
        pg.draw.rect(
            self.screen,
            self.car_color,
            (car_x - self.car_width // 2, self.car_y, self.car_width, self.car_height),
        )

    def update_scroll(self):
        """Update the scrolling position of the road."""
        self.scroll_position += 2  # move the road down a little
        if self.scroll_position >= self.segment_length:
            self.scroll_position -= (
                self.segment_length
            )  # reset scroll if exceeded segment length
            self.road.pop(0)  # remove the first segment
            curve_change = random.choice([-1, 0, 1])  # add a new curve
            self.road.append(self.road[-1] + curve_change)  # append new curve

    def run(self):
        """Main game loop."""
        while self.running:
            # Event handling
            for event in pg.event.get():
                if event.type == pg.QUIT:  # quit game if window is closed
                    self.running = False

            # Game logic
            self.handle_input()  # handle player input
            self.update_scroll()  # update the road scroll position

            # Drawing
            self.screen.fill((135, 206, 235))  # fill screen with sky blue background
            self.draw_road()  # draw the road
            self.draw_player()  # draw the car

            pg.display.flip()  # update the display
            self.clock.tick(self.fps)  # control the frame rate

        pg.quit()  # quit pygame
        sys.exit()  # exit the program


if __name__ == "__main__":
    game = Level2((800, 600))  # initialize game with screen size
    game.run()  # start the game loop