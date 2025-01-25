import pygame as pg
import sys
from pygame.locals import *
from Player import *
from Menu.Button import Button
from Map import *
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

        self.click = False
        self.running = False
        self.font = pg.font.SysFont("Consolas", 25)

        self.start_button = Button(150, 400, 150, 50)
        self.options_button = Button(350, 400, 150, 50)

    def init(self):
        self.map = Map.get_map(self)

        # Check if the sprite file exists before creating the Player
        player_sprite_path = "ball.png"
        if not os.path.exists(player_sprite_path):
            print(f"Error: File '{player_sprite_path}' not found.")
            sys.exit(1)  # Exit the program if the file is not found

        self.player = Player(
            self,
            player_sprite_path,
            "Assets",
            (self.map[0][0].x, self.map[0][0].y),
            120,
            [0, 0],
            "xxx"
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
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    self.click = True
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.running = False
    
    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, 1, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_obj, text_rect)

    def main_menu(self):
        while True:
            self.screen.fill((0,0,0))
 
            mx, my = pg.mouse.get_pos()

            self.start_button.draw(self.screen)
            self.options_button.draw(self.screen)

            if self.start_button.isClicked((mx, my)):
                self.game()

            if self.options_button.isClicked((mx, my)):
                self.options()

            self.draw_text('Glasscord GGJ Game 2025', self.font, (255, 255, 255), self.screen, int(self.width  / 2) - 160, 20)
            self.draw_text('Start Game', self.font, (255, 255, 255), self.screen, 155, 415)
            self.draw_text('Options', self.font, (255, 255, 255), self.screen, 375, 415)

            self.check_events()
            self.update()

    def draw_map(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                self.map[i][j].draw()
            
    def update(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(self.fps)
        pg.display.set_caption(f'GGJ PyGame Game')
    
    def game(self):
        
        self.running = True

        while self.running:
            self.screen.fill((0,0,0))
            self.draw_map()
            self.player.update()
            self.check_events()
            self.update()

    def options(self):
        
        self.running = True

        while self.running:
            self.screen.fill((0,0,0))
            self.draw_text('Press ESC for Main Menu', self.font, (255, 255, 255), self.screen, int(self.width  / 2) - 160, 20)

            self.check_events()
            self.update()
            
    def run(self):
        self.init()
        self.main_menu()

if __name__ == '__main__':
    game = Game((1280, 720))
    game.run()

