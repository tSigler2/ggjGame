import pygame as pg


class MoveableObj:
    def __init__(self, game, pos, velocity):
        self.game = game
        self.x, self.y = pos
        self.dx, self.dy = velocity

    def move(self, *directions):
        if "h" in directions:
            self.x += self.dx * self.game.delta_time
        if "v" in directions:
            self.y += self.dy * self.game.delta_time
