import pygame as pg


class CollidableObj:
<<<<<<< HEAD
    def __init__(self, dims):
=======
    def __init__(self, game, dims):
        self.x, self.y, self.width, self.height = pos
        self.game = game
>>>>>>> ed329b3 (Current Work)
        self.rect = pg.Rect(dims)

    def check_collision(self, *other_rects):
        return self.rect.collidelist(other_rects) != -1
