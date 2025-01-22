import pygame as pg
import os


class SpriteObj:
    def __init__(self, game, path, pos, scale, shift):
        self.game = game
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HEIGHT = self.image.get_height()
        self.scale = scale

    def get_sprite(self):
        self.game.screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.get_sprite()