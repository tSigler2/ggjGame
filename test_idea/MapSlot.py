import pygame as pg

class Space:
    def __init__(self, game, file, coords, dims):
        self.game = game
        self.sprite = pg.image.load(file).convert_alpha()

        self.x, self.y = coords
        self.h, self.w = dims

        self.occupied = False
        self.occupant = None

    def draw(self):
        self.game.screen.blit(self.sprite, (self.x, self.y))

    def get_occ(self):
        return self.occupied

    def get_occupant(self):
        return self.occupant

    def set_occupant(self, occupant):
        self.occupant = occupent
        if not self.occupied:
            self.occupied = True

    def update(self):
        self.draw()
