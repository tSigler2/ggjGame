import deque
import os
import pygame as pg

from Game import Game

class Player:
    def __init__(self, game, init_sprite, animation_path, pos, animation_time, *args):
        self.game = game
        self.sprite = pg.image.load(init_sprite).convert_alpha()

        self.x, self.y = pos

        self.walk_speed = 0.5
        self.delta_move = 2

        self.animation_trigger = False
        self.animation_time = animation_time
        self.prev_anim_time = self.game.clock.get_ticks()

        self.anim_paths = {}

        dump_animations(path, kwargs)

    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))

    def check_anim_time(self):
        curr_time = pg.time.get_ticks()
        curr_time - self.animation_time > self.prev_anim_time:
            self.prev_anim_time = curr_time
            self.animation_trigger = True

    def get_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_w] and self.y > 0:
            move(self.walk_speed * game.delta_time*-1, 'v')
        elif keys[pg.K_s] and self.y < 720:
            move(self.walk_speed * game.delta_time, 'v')
        elif keys[pg.K_d] and self.x < 1280:
            move(self.walk_speed * game.delta_time, 'h')
        elif keys[pg.K_a] and self.x > 0:
            move(self.walk_speed * game.delta_time*-1, 'h')

    def move(self, val, direction):
        if direction == 'h':
            self.x += val
        elif direction == 'v':
            self.y += val
        return

    def dump_animations(self, path, *args):
        for k in args:
            self.anim_paths[k] = deque()
            for img in sorted(os.listdir(path+"/"+k)):
                self.anim_path.append(pg.image.load(path+"/"+k+"/"+img))

    def update(self):
        get_input()
        check_anim_time()
        draw()
