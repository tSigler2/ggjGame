import pygame as pg

class CollidableObj:
    def __init__(self, dims):
        self.x, self.y, self.width, self.height = pos
        self.rect = pg.Rect(dims)

    def check_collision(self, *otherRects):
        return self.rect.collidelist(otherRects)

