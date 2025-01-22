import pygame as pg
from AnimatedSprite import AnimatedSprite
from collections import deque
import os

class MultiAnimatedSprite(AnimatedSprite):
    def __init__(self, game, path, pos, scale, shift, animation_time, **kwargs):
        super().__init__(game, path, pos, scale, shift, animation_time)

        animation_paths = {}

        for k in kwargs:
            animation_paths[k] = deque()
            for file in sorted(os.listdir(kwargs[k])):
                if os.path.isfile(kwargs[k]) and file != '.DS_Store':
                    animation_paths[k].append(pg.image.load(kwargs[k]+file).convert_alpha())

    def switchSpriteSet(self, animation_set):
        self.images = self.animatation_paths[animation_set]
