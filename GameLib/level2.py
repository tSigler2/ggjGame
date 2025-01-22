import pygame as pg
import sys
import random


class Level2:
    def __init__(self, dims, fps=60):
        pg.init()
        pg.font.init()  # Ensure font module is initialized
        self.width, self.height = dims
        self.fps = fps
        self.screen = pg.display.set_mode(dims)
        pg.display.set_caption("Level 2: Pole Position")
        self.clock = pg.time.Clock()
        # road properties
        self.road_width = self.width // 2
        self.road_x = (self.width - self.road_width) // 2
        self.road_color = (50, 50, 50)
        self.line_color = (255, 255, 255)
        self.line_width = 5
        # player car
        self.car_width = 40
        self.car_height = 60
        self.car_x = self.width // 2
        self.car_y = self.height - 100
        self.car_color = (0, 0, 255)  # blue car
        self.car_speed = 8
        # obstacles
        self.obstacles = []
        self.obstacle_width = 40
        self.obstacle_height = 60
        self.obstacle_color = (255, 0, 0)  # red cars
        self.obstacle_speed = 6
        self.spawn_timer = 0
        self.spawn_delay = 30  # frames between obstacle spawns
        # game variables
        self.running = True
        self.font = pg.font.Font(None, 74)  # Create font during initialization

    def spawn_obstacle(self):
        # spawn an obstacle at a random position on the road
        obstacle_x = random.randint(
            self.road_x + 10, self.road_x + self.road_width - self.obstacle_width - 10
        )
        obstacle_y = -self.obstacle_height  # start off-screen
        self.obstacles.append([obstacle_x, obstacle_y])

    def handle_input(self):
        keys = pg.key.get_pressed()  # get the keys pressed
        # move the car left and right
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.car_x -= self.car_speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.car_x += self.car_speed
        # keep the car within the road bounds
        self.car_x = max(
            self.road_x + 10,
            min(self.road_x + self.road_width - self.car_width - 10, self.car_x),
        )

    def update_obstacles(self):
        # move obstacles down the screen
        for obstacle in self.obstacles:
            obstacle[1] += self.obstacle_speed
        # remove obstacles that are off the screen
        self.obstacles = [obs for obs in self.obstacles if obs[1] < self.height]
        # check for collisions
        for obstacle in self.obstacles:
            if (
                self.car_x < obstacle[0] + self.obstacle_width
                and self.car_x + self.car_width > obstacle[0]
                and self.car_y < obstacle[1] + self.obstacle_height
                and self.car_y + self.car_height > obstacle[1]
            ):
                self.running = False  # end the game on collision

    def draw(self):
        self.screen.fill((0, 150, 0))  # clear the screen with a green background
        # draw the road
        pg.draw.rect(
            self.screen, self.road_color, (self.road_x, 0, self.road_width, self.height)
        )
        # draw dashed lines on the road
        for y in range(0, self.height, 40):
            pg.draw.line(
                self.screen,
                self.line_color,
                (self.width // 2, y),
                (self.width // 2, y + 20),
                self.line_width,
            )
        # draw the player's car
        pg.draw.rect(
            self.screen,
            self.car_color,
            (self.car_x, self.car_y, self.car_width, self.car_height),
        )
        # draw obstacles
        for obstacle in self.obstacles:
            pg.draw.rect(
                self.screen,
                self.obstacle_color,
                (obstacle[0], obstacle[1], self.obstacle_width, self.obstacle_height),
            )
        pg.display.flip()  # update the display

    def run(self):
        while self.running:
            # handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            # game logic
            self.handle_input()
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_obstacle()
                self.spawn_timer = 0
            self.update_obstacles()
            # draw everything
            self.draw()
            self.clock.tick(self.fps)  # cap the frame rate
        self.show_game_over()  # end the game

    def show_game_over(self):
        # Ensure no crashes when showing game-over
        try:
            text = self.font.render(
                "GAME OVER", True, (255, 0, 0)
            )  # red game over text
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(text, text_rect)
            pg.display.flip()
            pg.time.wait(3000)  # wait for 3 seconds before exiting
        except Exception as e:
            print(f"Error in game over screen: {e}")
        finally:
            pg.quit()
            sys.exit()


if __name__ == "__main__":
    game = Level2((800, 600))
    game.run()
