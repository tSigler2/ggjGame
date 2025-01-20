import pygame as pg
import sys

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

    def check_events(self):
        self.glob_trigger = False
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif e.type == self.glob_event:
                self.glob_trigger = True

    def update(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(self.fps)
        pg.display.set_caption(f'GGJ PyGame Game')


    def run(self):
        while not self._end:
            self.check_events()
            self.update()

if __name__ == '__main__':
    game = Game((640, 480))
    game.run()

