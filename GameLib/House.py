from collections import deque
import os
import pygame as pg
import sys


class House:
    def __init__(
        self,
        game,
        health,
        init_sprite,
        animation_path,
        pos,
        animation_time,
        coords,
        *args,
    ):
        self.game = game
        self.health = health
        self.range = range
        self.clock = pg.time.Clock()
        self.countdown = 0

        # Check if the sprite file exists before loading it
        if not os.path.exists(init_sprite):
            print(f"Error: File '{init_sprite}' not found.")
            sys.exit(1)  # Exit the program if the file is not found

        self.sprite = pg.image.load(init_sprite).convert_alpha()

        self.x, self.y = pos
        self.pos = pos
        self.h, self.w = self.sprite.get_height(), self.sprite.get_width()
        self.coords = coords

        self.delta_move = 200
        self.prev_move_time = self.game.clock.get_time()

        self.animation_trigger = False
        self.animation_time = animation_time
        self.prev_anim_time = self.game.clock.get_time()
        self.health = health

        self.countdown = 0

    def draw(self):
        self.game.screen.blit(self.sprite, (self.x, self.y))
    
    def respawn_player(self):
        self.game.player.pos = self.pos

    def respawn_player(self):
        self.game.player.pos = self.pos

    def give_money(self):
        self.money_value = self.game.player.get_money(1)
        print("Money Value: " + str(self.money_value))

    def update(self):
        self.draw()

        dt = self.clock.tick()
        self.countdown += dt

        if self.countdown > 10000:
            self.give_money()
            self.countdown = 0  # reset it to 0 so you can count again

        if self.health == 0:
            self.respawn_player
