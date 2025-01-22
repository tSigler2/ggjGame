import pygame as pg
from collections import deque
import os
from Sprite import SpriteObj


class AnimatedSprite(SpriteObj):
    def __init__(
        self,
        game,
        path="Assets/static_sprites/candlebra.png",
        pos=(10.5, 3.5),
        scale=0.7,
        shift=0.27,
        animation_time=120,
    ):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        self.check_anim_time()
        self.animate()
        super().update()

    def get_images(self, path):
        images = deque()

        for file in sorted(os.listdir(path)):
            if os.path.isfile(os.path.join(path, file)) and file != ".DS_Store":
                img = pg.image.load(path + "/" + file).convert_alpha()
                images.append(img)

        return images

    def check_anim_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        # I thought it should be `self.animation_time_prev` instead of `self.animation_trigger`
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def animate(self):
        if self.animation_trigger:
            self.images.rotate(-1)
            # images is not a local or global variable, so I thought it should be self.images
            self.image = self.images[0]
