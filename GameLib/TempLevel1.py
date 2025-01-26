import pygame as pg
import sys


class Level1:
    def __init__(self, dims, fps=60):
        pg.init()
        self.width, self.height = dims
        self.fps = fps
        self.screen = pg.display.set_mode(dims)
        pg.display.set_caption("Roll around, brother")
        self.clock = pg.time.Clock()

        # Circle (player) properties
        self.circle_pos = [
            self.width // 2,
            self.height // 2,
        ]  # this sets the starting position
        self.circle_radius = 20
        self.circle_color = (
            0,
            255,
            0,
        )  # this is the circle's color (0, 255, 0 is green)
        self.speed = 5  # movement speed

    def handle_input(self):
        keys = pg.key.get_pressed()  # this gets the keys pressed

        if keys[pg.K_UP] or keys[pg.K_w]:  # Move up
            self.circle_pos[1] -= self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:  # Move down
            self.circle_pos[1] += self.speed
        if keys[pg.K_LEFT] or keys[pg.K_a]:  # Move left
            self.circle_pos[0] -= self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:  # Move right
            self.circle_pos[0] += self.speed

        # This prevents the circle from going off the screen
        self.circle_pos[0] = max(
            self.circle_radius, min(self.width - self.circle_radius, self.circle_pos[0])
        )
        self.circle_pos[1] = max(
            self.circle_radius,
            min(self.height - self.circle_radius, self.circle_pos[1]),
        )

    def update(self):
        self.screen.fill((0, 0, 0))  # this sets the background color (black is 0, 0, 0)

        # this draws the circle
        pg.draw.circle(
            self.screen, self.circle_color, self.circle_pos, self.circle_radius
        )

        pg.display.flip()  # this refreshes the display

    def run(self):
        while True:
            for event in pg.event.get():  # this handles events like quitting
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.handle_input()  # this handles the input game state
            self.update()  # this handles the update game state

            self.clock.tick(self.fps)  # this caps the frame rate
