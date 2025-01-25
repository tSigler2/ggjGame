import pygame as pg
# from AnimatedSprite import AnimatedSprit
from GameLib.Sprite.AnimatedSprite import AnimatedSprite
from collections import deque
import os


class MultiAnimatedSprite(AnimatedSprite):
    def __init__(self, game, path, pos, scale, shift, animation_time, *args):
        super().__init__(game, path, pos, scale, shift, animation_time)
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

    def dump_animations(animation_list):
        print(animation_list)  # replace this with actual logic
