import pygame as pg
from collections import deque
import os

from Sprite.Sprite import SpriteObj



class AnimatedSprite(SpriteObj):
    def __init__(self, game, path, pos, scale, shift, animation_time):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.images = self.get_images(path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        self.check_anim_time()
        self.animate()
        super().update()

    def get_images(self, path):
        images = deque()
        for file in sorted(os.listdir(path)):
            if file.endswith((".png", ".jpg")):
                img = pg.image.load(os.path.join(path, file)).convert_alpha()
                images.append(img)
        return images

    def check_anim_time(self):
        current_time = pg.time.get_ticks()
        if current_time - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = current_time
            self.animation_trigger = True

    def animate(self):
        if self.animation_trigger:
            self.images.rotate(-1)
            # images is not a local or global variable, so I thought it should be self.images
            self.image = self.images[0]
