import sys
import os
import pygame as pg

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from GameLib.Sprite.TempSprite import SpriteObj


class Button(SpriteObj):
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)
        self.color = (0, 0, 255)

    def draw(self, surface):

        pg.draw.rect(surface, self.color, self.rect)

    def isClicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
