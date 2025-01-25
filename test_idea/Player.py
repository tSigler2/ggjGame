from collections import deque
import os
import pygame as pg

class Player:
    def __init__(self, game, init_sprite, animation_path, pos, animation_time, coords, *args):
        self.game = game
        self.sprite = pg.image.load(init_sprite).convert_alpha()

        self.x, self.y = pos
        self.h, self.w = self.sprite.get_height(), self.sprite.get_width()
        self.coords = coords

        self.delta_move = 200
        self.prev_move_time = self.game.clock.get_time()

        self.animation_trigger = False
        self.animation_time = animation_time
        self.prev_anim_time = self.game.clock.get_time()

        self.anim_paths = {}

        self.dump_animations(animation_path, args)

    def draw(self):
        self.game.screen.blit(self.sprite, (self.x, self.y))

    def check_anim_time(self):
        curr_time = pg.time.get_ticks()
        if curr_time - self.animation_time > self.prev_anim_time:
            self.prev_anim_time = curr_time
            self.animation_trigger = True

    def get_input(self):
        keys = pg.key.get_pressed()
        curr_time = pg.time.get_ticks()

        if keys[pg.K_w] and self.coords[1] > 0 and (curr_time - self.prev_move_time) >= self.delta_move:
            self.prev_move_time = curr_time
            self.coords[1] -= 1
            self.move((self.game.map[self.coords[0]][self.coords[1]].x, self.game.map[self.coords[0]][self.coords[1]].y))
        elif keys[pg.K_s] and self.coords[1] < 10 and (curr_time - self.prev_move_time) >= self.delta_move:
            self.prev_move_time = curr_time
            self.coords[1] += 1
            self.move((self.game.map[self.coords[0]][self.coords[1]].x, self.game.map[self.coords[0]][self.coords[1]].y))
        elif keys[pg.K_d] and self.coords[0] < 10 and (curr_time - self.prev_move_time) >= self.delta_move:
            self.prev_move_time = curr_time
            self.coords[0] += 1
            self.move((self.game.map[self.coords[0]][self.coords[1]].x, self.game.map[self.coords[0]][self.coords[1]].y))
        elif keys[pg.K_a] and self.coords[0] > 0 and (curr_time - self.prev_move_time) >= self.delta_move:
            self.prev_move_time = curr_time
            self.coords[0] -= 1
            self.move((self.game.map[self.coords[0]][self.coords[1]].x, self.game.map[self.coords[0]][self.coords[1]].y))

    def move(self, val):
            self.x, self.y = val

    def dump_animations(self, path, *args):
        for k in args[0]:
            self.anim_paths[k] = deque()
            for img in sorted(os.listdir(path+"/"+k)):
                self.anim_path.append(pg.image.load(path+"/"+k+"/"+img))

    def update(self):
        self.get_input()
        self.check_anim_time()
        self.draw()
