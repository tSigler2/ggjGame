import pygame as pg

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .CollidableObj import CollidableObj
from .MoveableObj import MoveableObj
from Sprite.MultiAnimatedSprite import MultiAnimatedSprite

class Player(MultiAnimatedSprite, MoveableObj, CollidableObj):
    def __init__(self, game, path, dims, pos, velocity, scale, shift, animation_time, standard_anim, **kwargs):
        MultiAnimatedSprite.__init__(game, path, pos, scale, shift, animation_time, standard_anim, kwargs)
        MoveableObj.__init__(game, pos, velocity)
        CollidableObj.__init__(game, dims)

    def get_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            if self.dy > 0:
                self.dy *= -1
            self.move('v')

            if

        if keys[pg.K_s]:
            if self.dy < 0:
                self.dy *= -1
            self.move('v')

        if keys[pg.K_a]:
            if self.dx > 0:
                self.dx *= -1
            self.move('h')

        if keys[pg.K_d]:
            if self.dx < 0:
                self.dx *= -1
            self.move('h')

    def update(self, anim_set, coll_check_list, direction):
        self.switchSpriteSet(self.animation_path)


