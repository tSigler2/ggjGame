import pygame as pg

# from AnimatedSprite import AnimatedSprit
from Sprite.AnimatedSprite import AnimatedSprite
from collections import deque
import os


class MultiAnimatedSprite(AnimatedSprite):
<<<<<<< HEAD
    def __init__(self, game, path, pos, scale, shift, animation_time, *args):
        super().__init__(game, path, pos, scale, shift, animation_time)
        args = args[0]
        self.animation_paths = {
            key: deque(
                pg.image.load(os.path.join(key, file)).convert_alpha()
                for file in sorted(os.listdir(key))
                if file.endswith((".png", ".jpg"))
            )
            for key in args
        }

    def switchSpriteSet(self, animation_set):
        if animation_set in self.animation_paths:
            self.images = self.animation_paths[animation_set]
=======
    def __init__(self, game, path, pos, scale, shift, animation_time, standard_anim, **kwargs):
        super().__init__(game, path, pos, scale, shift, animation_time)

        animation_paths = {}
        self.animation_path = standard_anim

        for k in kwargs:
            animation_paths[k] = deque()
            for file in sorted(os.listdir(kwargs[k])):
                if os.path.isfile(kwargs[k]) and file != '.DS_Store':
                    animation_paths[k].append(pg.image.load(kwargs[k]+file).convert_alpha())

    def switchSpriteSet(self, animation_set):
        self.images = self.animatation_paths[animation_set]
        self.update()
>>>>>>> ed329b3 (Current Work)
