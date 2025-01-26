# File: GameLib\Player.py
from collections import deque
import pygame as pg
import os
import sys


class Player:
    def __init__(
        self,
        game,
        health,
        range,
        init_sprite,
        animation_path,
        pos,
        position,
        animation_time,
        coords,
        money,
        *args,
    ):
        self.game = game
        self.health = health
        self.range = range
        self.clock = pg.time.Clock()
        self.countdown = 0

        if not os.path.exists(init_sprite):
            print(f"Error: File '{init_sprite}' not found.")
            sys.exit(1)
        self.sprite = pg.image.load(init_sprite).convert_alpha()

        self.x, self.y = pos
        self.h, self.w = self.sprite.get_height(), self.sprite.get_width()
        self.coords = coords
        self.pos = list(position)

        self.speed = 5  # Adjusted movement speed
        self.prev_move_time = self.game.clock.get_time()

        self.animation_trigger = False
        self.animation_time = animation_time
        self.prev_anim_time = self.game.clock.get_time()

        self.anim_paths = {}

        self.dump_animations(animation_path, args)

        self.radius = 20  # set the player's radius here

        self.health = health
        self.money = money

    def draw(self):
        self.game.screen.blit(self.sprite, (self.x, self.y))

    def respawn_player(self):
        self.x, self.y = self.game.house.pos

    def get_money(self, val):
        self.money += val
        return self.money

    def check_anim_time(self):
        curr_time = pg.time.get_ticks()
        if curr_time - self.animation_time > self.prev_anim_time:
            self.prev_anim_time = curr_time
            self.animation_trigger = True

    def take_damage(self, damage):
        self.health -= damage

        if self.health <= 0:
            self.respawn_player()

    def get_input(self):
        keys = pg.key.get_pressed()  # Get all the keys currently pressed
        curr_time = pg.time.get_ticks()

        if (keys[pg.K_w] or keys[pg.K_UP]) and (  # Move up
            curr_time - self.prev_move_time
        ) >= 100:
            self.prev_move_time = curr_time
            self.y -= self.speed
        if (keys[pg.K_s] or keys[pg.K_DOWN]) and (  # Move down
            curr_time - self.prev_move_time
        ) >= 100:
            self.prev_move_time = curr_time
            self.y += self.speed
        if (keys[pg.K_d] or keys[pg.K_RIGHT]) and (  # Move right
            curr_time - self.prev_move_time
        ) >= 100:
            self.prev_move_time = curr_time
            self.x += self.speed
        if (keys[pg.K_a] or keys[pg.K_LEFT]) and (  # Move left
            curr_time - self.prev_move_time
        ) >= 100:
            self.prev_move_time = curr_time
            self.x -= self.speed

    def move(self, val):
        self.x, self.y = val

    def dump_animations(self, path, *args):
        for k in args[0]:
            self.anim_paths[k] = deque()
            full_path = os.path.join(path, k)

            if os.path.exists(full_path):
                for img in sorted(os.listdir(full_path)):
                    if img.endswith(".png"):
                        self.anim_paths[k].append(
                            pg.image.load(os.path.join(full_path, img))
                        )
            else:
                print(
                    f"Warning: '{full_path}' directory not found, skipping animation loading."
                )

    def update(self):
        self.get_input()
        self.check_anim_time()

        self.dt = self.clock.tick()
        self.countdown += self.dt

        if self.countdown > 50000:
            self.respawn_player()
            self.countdown = 0

        if self.animation_trigger:
            self.animation_trigger = False
            walk_frames = self.anim_paths.get("walk", [])
            if walk_frames:
                current_frame = walk_frames.popleft()
                walk_frames.append(current_frame)
                self.sprite = current_frame

        self.draw()
