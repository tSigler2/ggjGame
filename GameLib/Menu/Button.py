import sys
import os
import pygame as pg

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Sprite.Sprite import SpriteObj


class Button(SpriteObj):
    def __init__(self, game, path, pos, scale, shift):
        super().__init__(game, path, pos, scale, shift)

    def check_overlap(self):
        pos = pg.mouse.get_pos()
        if self.x <= pos[0] <= (self.x + self.IMAGE_WIDTH) and self.y <= pos[1] <= (
            self.y + self.IMAGE_HEIGHT
        ):
            return True
        return False
