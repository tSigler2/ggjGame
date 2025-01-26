import pygame as pg
import sys
from pygame.locals import *
from GameLib.Player import *
from GameLib.House import *
from GameLib.Menu.Button import Button
from GameLib.Map import *
from GameLib.Util.Sound import SoundManager
import os


class Game:
    def __init__(self, dims, fps=60):
        pg.init()
        self.width, self.height = dims
        self.fps = fps
        self.screen = pg.display.set_mode(dims)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.glob_event = pg.USEREVENT
        self.glob_trigger = False
        pg.time.set_timer(self.glob_event, 40)
        self._end = False

        self.running = False
        self.font = pg.font.SysFont("Consolas", 25)

        self.start_button = Button(150, 400, 150, 50)
        self.options_button = Button(350, 400, 150, 50)
        self.frame_count = 0

        # Ensure self.assets_dir is set
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(base_dir, "Assets")

    def init(self):
        self.map = Map.get_map(self)

        # Updated grid offsets for alignment based on tile size of 64
        tile_size = 64
        grid_start_x = (self.width - 11 * tile_size) // 2
        grid_start_y = (self.height - 11 * tile_size) // 2

        center_x, center_y = 5, 5  # Grid center

        house_position = (
            grid_start_x + center_x * tile_size,
            grid_start_y + center_y * tile_size,
        )

        house_sprite_path = os.path.join(self.assets_dir, "house", "house.png")
        self.house = House(
            self,
            health=100,
            init_sprite=house_sprite_path,
            animation_path="path_to_animation",
            pos=house_position,
            animation_time=200,
            coords=[(0, 0)],
        )

        walk_dir = os.path.join(self.assets_dir, "player", "walk")
        walk_images = sorted(
            [
                os.path.join(walk_dir, f)
                for f in os.listdir(walk_dir)
                if f.endswith(".png")
            ]
        )

        if not walk_images:
            print(f"Error: No images found in '{walk_dir}' for walking animation.")
            sys.exit(1)

        self.player = Player(
            self,
            5,
            3,
            walk_images[0],
            "GameLib/Assets/player",
            (self.map[0][0].x, self.map[0][0].y),
            120,
            [0, 0],
            0,
            "walk",
        )

    def check_events(self):
        self.glob_trigger = False
        self.click = False
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif e.type == self.glob_event:
                self.glob_trigger = True

    # File: GameLib\Game.py (Updated draw_map method)

    def draw_map(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                self.map[i][j].draw()

                # Commented out the red lines for debugging purposes
                # rect = pg.Rect(
                #     self.map[i][j].x, self.map[i][j].y, 64, 64
                # )
                # pg.draw.rect(self.screen, (255, 0, 0), rect, 1)

                # Draw green dot at the center of each tile
                #center_x = self.map[i][j].x + 64 // 2
                #center_y = self.map[i][j].y + 64 // 2
                #pg.draw.circle(self.screen, (0, 255, 0), (center_x, center_y), 3)

    def run(self):
        self.init()
        self.game()

    def update(self):
        self.frame_count += 1
        pg.display.flip()
        self.delta_time = self.clock.tick(self.fps)
        pg.display.set_caption(f"SquirrelyPop")

    def handle_input(self):
        keys = pg.key.get_pressed()  # Get the keys pressed

        # Move up
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.player.pos[1] -= self.player.speed
        # Move down
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.player.pos[1] += self.player.speed
        # Move left
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.player.pos[0] -= self.player.speed
        # Move right
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.player.pos[0] += self.player.speed

        # Prevent the player from going off the screen
        self.player.pos[0] = max(
            self.player.radius, min(self.width - self.player.radius, self.player.pos[0])
        )
        self.player.pos[1] = max(
            self.player.radius,
            min(self.height - self.player.radius, self.player.pos[1]),
        )

    def game(self):
        self.running = True
        while self.running:
            self.screen.fill((0, 0, 0))
            self.draw_map()
            self.handle_input()  # Call handle_input to move the player
            self.player.update()
            self.house.update()
            self.check_events()
            self.update()

    def options(self):
        self.running = True
        while self.running:
            self.screen.fill((0, 0, 0))
            self.draw_text(
                "Press ESC for Main Menu",
                self.font,
                (255, 255, 255),
                self.screen,
                int(self.width / 2) - 160,
                20,
            )
            self.check_events()
            self.update()

    def run(self):
        self.init()
        self.game()


if __name__ == "__main__":
    # Pass the paths to assets and sounds as parameters
    assets_dir = "Assets"
    sounds_dir = os.path.join(assets_dir, "sounds")
    game = Game((1280, 720), assets_dir=assets_dir, sounds_dir=sounds_dir)
    game.run()
