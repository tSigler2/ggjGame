import pygame as pg
from GameLib.Enemy import Enemy
import sys

class Test:
    def __init__(self, dims, fps=60):
        pg.init()
        self.width, self.height = dims
        self.fps = fps
        self.screen = pg.display.set_mode(dims)
        pg.display.set_caption("Test")
        self.clock = pg.time.Clock()

        self.enemy = Enemy(350, 200, 150, 50)
    

    def update(self):
        self.screen.fill((0, 0, 0))  # this sets the background color (black is 0, 0, 0)
        self.enemy.draw(self.screen)


        pg.display.flip()  # this refreshes the display

    def run(self):
        while True:
            for event in pg.event.get():  # this handles events like quitting
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.update()  # this handles the update game state

            self.clock.tick(self.fps)  # this caps the frame rate
