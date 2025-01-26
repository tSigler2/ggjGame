import pygame as pg
import os
from Sprite.MultiAnimatedSprite import MultiAnimatedSprite
from collections import deque

class Coral(MultiAnimatedSprite):
    def __init__(self, game, health, coords, damage, path, animation_time, *args):
        super().__init__(game, path, coords, 1, 0, animation_time, args)
        self.game = game
        self.health = health
        self.damage = damage
        self.x, self.y = coords

        self.animations = {}
        self.dump_animations(path, args[0])
        self.animation_trigger = False
        self.curr_deque = self.animation['std']
        self.prev_anim_time = pg.time.get_ticks()
        self.anim_trigger = False
        

    def dump_animations(self, path, *args):
        for k in args[0]:
            self.anim_paths[k] = deque()
            full_path = os.path.join(
                path, k
            )  # Correctly construct the full path to the folder

            # Check if the directory exists
            if os.path.exists(full_path):
                for img in sorted(os.listdir(full_path)):
                    if img.endswith(".png"):  # Make sure to only load PNG files
                        self.anim_paths[k].append(
                            pg.image.load(os.path.join(full_path, img))
                        )
            else:
                print(
                    f"Warning: '{full_path}' directory not found, skipping animation loading."
                )

    def damage(self):
        dam_list = []

        if (
            self.game.map[self.x - 1][self.y - 1].occupied
            and self.game.map[self.x - 1][self.y - 1].occupant != self.game.player
            and self.game.map[self.x - 1][self.y - 1].occupant != self.game.house
        ):
            dam_list.append((self.x - 1, self.y - 1))
        if (
            self.game.map[self.x][self.y - 1].occupied
            and self.game.map[self.x][self.y - 1].occupant != self.game.player
            and self.game.map[self.x][self.y - 1].occupant != self.game.house
        ):
            dam_list.append((self.x, self.y - 1))
        if (
            self.game.map[self.x + 1][self.y - 1].occupied
            and self.game.map[self.x + 1][self.y - 1].occupant != self.game.player
            and self.game.map[self.x + 1][self.y - 1].occupant != self.game.house
        ):
            dam_list.append((self.x + 1, self.y - 1))
        if (
            self.game.map[self.x - 1][self.y].occupied
            and self.game.map[self.x - 1][self.y].occupant != self.game.player
            and self.game.map[self.x - 1][self.y].occupant != self.game.house
        ):
            dam_list.append((self.x - 1, self.y))
        if (
            self.game.map[self.x + 1][self.y].occupied
            and self.game.map[self.x + 1][self.y].occupant != self.game.player
            and self.game.map[self.x + 1][self.y].occupant != self.game.house
        ):
            dam_list.append((self.x + 1, self.y))
        if (
            self.game.map[self.x - 1][self.y + 1].occupied
            and self.game.map[self.x - 1][self.y + 1].occupant != self.game.player
            and self.game.map[self.x - 1][self.y + 1].occupant != self.game.house
        ):
            dam_list.append((self.x - 1, self.y + 1))
        if (
            self.game.map[self.x][self.y + 1].occupied
            and self.game.map[self.x][self.y + 1].occupant != self.game.player
            and self.game.map[self.x][self.y + 1].occupant != self.game.house
        ):
            dam_list.append((self.x, self.y + 1))
        if (
            self.game.map[self.x + 1][self.y + 1].occupied
            and self.game.map[self.x + 1][self.y + 1].occupant != self.game.player
            and self.game.map[self.x + 1][self.y + 1].occupant != self.game.house
        ):
            dam_list.append((self.x + 1, self.y + 1))

        for sq in dam_list:
            self.game.map[sq[0]][sq[1]].occupant.take_damage(1)

    def take_damage(self, val):
        self.health -= 1
    
    def check_anim_time(self):
       curr_time = pg.time.get_ticks()

       if curr_time - self.prev_anim_time >= self.anim_time:
           self.prev_anim_time = curr_time
           self.anim_tigger = True

    def update(self):
        self.check_anim_time()

        if self.anim_trigger:
            self.curr_deque.rotate(-1)
            self.anim_trigger = False
        self.game.screen.blit(self.curr_deque[0], (self.x, self.y))

        self.damage()
