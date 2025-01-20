import pygame as pg
import os

class SpriteObj:
    def __init__(self, game, path='Assets/static_sprites/candlebra.png', pos=(10.5, 3.5), scale=0.7, shift=0.27):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width()//2
        self.IMAGE_RATIO = self.IMAGE_WIDTH/self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale

    def get_sprite(self):
        self.game.screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.get_sprite()
