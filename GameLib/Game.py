import pygame as pg
import sys
from pygame.locals import *
from Player import *
from house import *
from Menu.Button import Button
from Map import *
from Util.Sound import SoundManager
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
        self.glob_tigger = False
        pg.time.set_timer(self.glob_event, 40)
        self._end = False

        self.running = False
        self.font = pg.font.SysFont("Consolas", 25)

        self.start_button = Button(150, 400, 150, 50)
        self.options_button = Button(350, 400, 150, 50)
        self.frame_count = 0

    def init(self):
        self.map = Map.get_map(self)

        # Get the directory where the current script is located
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Build the path to the player sprite file and check if it exists
        player_sprite_path = os.path.join(
            base_dir, "Assets", "player", "walk", "JimmyWalkcycle1.png"
        )
        if not os.path.exists(player_sprite_path):
            print(f"Error: File '{player_sprite_path}' not found.")
            sys.exit(1)  # Exit the program if the file is not found

        self.player = Player(
            self,
            5,
            3,
            player_sprite_path,
            "Assets",
            (self.map[0][0].x, self.map[0][0].y),
            120,
            [0, 0],
            0,
            0,
            "xxx",
        )

        # Build the path to the 'Assets' folder and load the house sprite
        assets_dir = os.path.join(base_dir, "Assets")
        house_sprite_path = os.path.join(assets_dir, "House.png")
        if not os.path.exists(house_sprite_path):
            print(f"Error: File '{house_sprite_path}' not found.")
            sys.exit(1)  # Exit the program if the file is not found

        self.house = House(
            self,
            5,
            house_sprite_path,
            "Assets",
            (self.map[5][5].x, self.map[5][5].y),
            120,
            [5, 5],
            "xxx",
        )

        # Build the path to the 'Assets/sounds' folder and initialize the sound manager
        sounds_dir = os.path.join(base_dir, "Assets", "sounds")
        self.sound_manager = SoundManager(sounds_dir)

    def check_events(self):
        self.glob_trigger = False
        self.click = False
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif e.type == self.glob_event:
                self.glob_trigger = True

    def draw_map(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                self.map[i][j].draw()

    def update(self):
        self.frame_count += 1
        pg.display.flip()
        self.delta_time = self.clock.tick(self.fps)
        pg.display.set_caption(f"SquirrelyPop")

    def game(self):
        self.running = True
        while self.running:
            self.screen.fill((0, 0, 0))
            self.draw_map()
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
    game = Game((1280, 720))
    game.run()
