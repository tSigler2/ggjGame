import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Sprite.Sprite import SpriteObj

class Button(SpriteObj):
    def __init__(self, game, path, pos, scale, shift):
        super().__init__(game, path, pos, scale, shift)

    def check_overlap(self):
        pos = pg.mouse.get_pos()

        if pos[0] >= self.x and pos[0] <= (self.x+self.width) and pos[1] >= self.y and pos[1] <= (self.y+self.height):
            return True
        return False
