import pygame as pg
import sys
import random


class Level2:
    def __init__(self, dims, fps=60):
        pg.init()  # initialize pygame
        self.width, self.height = dims
        self.fps = fps
        self.screen = pg.display.set_mode(dims)  # set up the screen
        pg.display.set_caption("Level 2: Pole Position")  # game window title
        self.clock = pg.time.Clock()  # for controlling the frame rate

        # Road properties
        self.road_width = 400  # wider road
        self.road_color = (0, 0, 0)  # black road
        self.grass_color = (0, 150, 0)  # green grass
        self.line_color = (255, 255, 0)  # yellow lane markers

        # Player properties
        self.car_width = 40
        self.car_height = 70
        self.car_x = self.width // 2  # start centered
        self.car_y = self.height - 100
        self.car_color = (0, 0, 255)
        self.car_speed = 3  # player speed
        self.max_offset = 150  # max offset from the road center
        self.player_offset = 0  # player's horizontal offset

        # Road variables
        self.segments = 200  # total road segments
        self.segment_length = 15  # height of each road segment
        self.road = []  # list for road data
        self.scroll_position = 0  # how far the road has scrolled
        self.speed = 0  # player speed (acceleration and deceleration)
        self.max_speed = 5  # max speed
        self.acceleration_rate = 0.05  # acceleration rate
        self.deceleration_rate = 0.03  # deceleration rate

        self.generate_road()  # generate the road

        # Camera properties
        self.camera_offset = 0  # camera offset for panning

        # Game variables
        self.running = True  # game loop flag

    def generate_road(self):
        self.road = [0]  # starting curve
        for _ in range(self.segments - 1):
            curve_change = random.choice([-1, 0, 1])  # random curve
            self.road.append(self.road[-1] + curve_change)

    def draw_road(self):
        base_y = self.height
        curve_accumulation = 0  # total horizontal curve offset
        scale = 1  # perspective scaling factor

        for i in range(len(self.road) - 1, -1, -1):
            curve_accumulation += self.road[i]

            # calculate perspective scaling for current and next segments
            scale_current = scale
            scale_next = scale * 1.05

            # calculate road widths
            road_width_current = scale_current * self.road_width
            road_width_next = scale_next * self.road_width

            # screen coordinates for road edges
            x1 = (
                self.width // 2
                + curve_accumulation
                - road_width_current / 2
                + self.player_offset * scale_current
                - self.camera_offset
            )
            x2 = (
                self.width // 2
                + curve_accumulation
                + road_width_current / 2
                + self.player_offset * scale_current
                - self.camera_offset
            )
            x3 = (
                self.width // 2
                + curve_accumulation
                - road_width_next / 2
                + self.player_offset * scale_next
                - self.camera_offset
            )
            x4 = (
                self.width // 2
                + curve_accumulation
                + road_width_next / 2
                + self.player_offset * scale_next
                - self.camera_offset
            )

            # vertical positions
            y1 = base_y - self.segment_length * scale_current
            y2 = base_y

            # draw grass (background) - make it wider
            grass_width = 2 * road_width_current  # wider grass
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

            # draw road segment
            pg.draw.polygon(
                self.screen, self.road_color, [(x1, y1), (x2, y1), (x4, y2), (x3, y2)]
            )
            base_y = y1

            # add lane markers every 10th segment
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

            scale *= 0.95  # reduce scale to simulate perspective

    def handle_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.player_offset -= self.car_speed  # move left
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.player_offset += self.car_speed  # move right
        if self.player_offset < -self.max_offset:  # limit left offset
            self.player_offset = -self.max_offset
        elif self.player_offset > self.max_offset:  # limit right offset
            self.player_offset = self.max_offset

        # acceleration and deceleration
        if keys[pg.K_UP] or keys[pg.K_w]:
            if self.speed < self.max_speed:
                self.speed += self.acceleration_rate
        else:
            if self.speed > 0:
                self.speed -= self.deceleration_rate

    def update_camera(self):
        road_curve = self.road[
            int(self.scroll_position) % len(self.road)
        ]  # get road curve
        self.camera_offset += road_curve * 0.1  # adjust camera based on curve

        # limit camera panning
        if self.camera_offset > 100:
            self.camera_offset = 100
        elif self.camera_offset < -100:
            self.camera_offset = -100

    def draw_player(self):
        car_x = self.width // 2 + self.player_offset  # player's x position
        pg.draw.rect(
            self.screen,
            self.car_color,
            (car_x - self.car_width // 2, self.car_y, self.car_width, self.car_height),
        )

    def update_scroll(self):
        self.scroll_position += self.speed  # update scrolling position
        if self.scroll_position >= self.segment_length:
            self.scroll_position -= self.segment_length
            self.road.pop(0)  # remove old segment
            curve_change = random.choice([-1, 0, 1])  # random curve
            self.road.append(self.road[-1] + curve_change)  # add new segment

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False  # quit game on close

            # game logic
            self.handle_input()
            self.update_camera()
            self.update_scroll()

            # drawing
            self.screen.fill((135, 206, 235))  # sky blue background
            self.draw_road()
            self.draw_player()

            pg.display.flip()  # update display
            self.clock.tick(self.fps)  # control frame rate

        pg.quit()  # quit pygame
        sys.exit()  # exit program


if __name__ == "__main__":
    game = Level2((800, 600))
    game.run()
