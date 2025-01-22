import pygame as pg


class CollidableObj:
    def __init__(self, dims):
        self.rect = pg.Rect(dims)

    def check_collision(self, *other_rects):
        return self.rect.collidelist(other_rects) != -1
