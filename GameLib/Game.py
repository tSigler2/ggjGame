# File: GameLib\Game.py
import pygame as pg
import sys
from pygame.locals import *
from GameLib.Player import *
from GameLib.House import *
from GameLib.Menu.Button import Button
from GameLib.Map import *
from GameLib.Util.Sound import SoundManager
from GameLib.EnemyManager import EnemyManager
from GameLib.CoralManager import CoralManager
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

        self.background = pg.transform.scale(
            pg.image.load("GameLib/Assets/background.png").convert_alpha(), dims
        )

        self.running = False
        self.font = pg.font.SysFont("Consolas", 25)

        self.start_button = Button(150, 400, 150, 50)
        self.options_button = Button(350, 400, 150, 50)
        self.frame_count = 0

    def init(self):
        self.map = Map.get_map(self)

        # Get the directory where the current script is located
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Initialize music
        music_file = "Squirrely Pop MainTheme.mp3"
        music_path = os.path.join(base_dir, "Assets", "music", music_file)

        if not os.path.exists(music_path):
            print(f"Error: Music file '{music_file}' not found.")
            sys.exit(1)

        self.music = pg.mixer.Sound(music_path)
        self.music.play(loops=-1)  # Play the music on a loop

        # Player setup
        walk_dir = os.path.join(base_dir, "Assets", "player", "walk")
        walk_images = [
            os.path.join(walk_dir, f)
            for f in sorted(os.listdir(walk_dir))
            if f.endswith(".png")
        ]

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
            "attack",
        )

        # Load the house sprite
        house_sprite_path = os.path.join(base_dir, "Assets", "House.png")
        if not os.path.exists(house_sprite_path):
            print(f"Error: File '{house_sprite_path}' not found.")
            sys.exit(1)

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

        self.enemyManager = EnemyManager(self, 900, 5000)

        # Initialize the sound manager
        sounds_dir = os.path.join(base_dir, "Assets", "sounds")
        self.sound_manager = SoundManager(sounds_dir)

        self.coral_manager = CoralManager(self)

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
            self.screen.blit(self.background, (0, 0))
            self.draw_map()
            self.player.update()
            self.house.update()
            self.enemyManager.update()
            self.coral_manager.update_coral()
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
