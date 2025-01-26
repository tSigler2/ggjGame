# File: test_idea\Player.py
from collections import deque
import os
import pygame as pg
import sys
import math
from Sprite.MultiAnimatedSprite import MultiAnimatedSprite


class Player(MultiAnimatedSprite):
    def __init__(
        self,
        game,
        health,
        range,
        init_sprite,
        animation_path,
        pos,
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

        # Check if the sprite file exists before loading it
        if not os.path.exists(init_sprite):
            print(f"Error: File '{init_sprite}' not found.")
            sys.exit(1)  # Exit the program if the file is not found
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

        self.health = health
        self.money = money

        self.attack_anim_trigger = 0

        self.clock = pg.time.Clock()
        self.attack_in_progress = False
        self.countdown = 2000
        self.coral_toggle = False

    def draw(self, sprite):
        self.game.screen.blit(self.sprite, (self.x, self.y))

    def respawn_player(self):
        self.pos = self.game.house.pos

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
            self.respawn_player

    def get_input(self):
        keys = pg.key.get_pressed()
        mouse_buttons = pg.mouse.get_pressed()
        curr_time = pg.time.get_ticks()

        if (
            keys[pg.K_w]
            and self.coords[1] > 0
            and (curr_time - self.prev_move_time) >= self.delta_move
        ):
            self.prev_move_time = curr_time
            self.coords[1] -= 1
            self.move(
                (
                    self.game.map[self.coords[0]][self.coords[1]].x,
                    self.game.map[self.coords[0]][self.coords[1]].y,
                )
            )
        if (
            keys[pg.K_s]
            and self.coords[1] < 10
            and (curr_time - self.prev_move_time) >= self.delta_move
        ):
            self.prev_move_time = curr_time
            self.coords[1] += 1
            self.move(
                (
                    self.game.map[self.coords[0]][self.coords[1]].x,
                    self.game.map[self.coords[0]][self.coords[1]].y,
                )
            )
        if (
            keys[pg.K_d]
            and self.coords[0] < 10
            and (curr_time - self.prev_move_time) >= self.delta_move
        ):
            self.prev_move_time = curr_time
            self.coords[0] += 1
            self.move(
                (
                    self.game.map[self.coords[0]][self.coords[1]].x,
                    self.game.map[self.coords[0]][self.coords[1]].y,
                )
            )
        if (
            keys[pg.K_a]
            and self.coords[0] > 0
            and (curr_time - self.prev_move_time) >= self.delta_move
        ):
            self.prev_move_time = curr_time
            self.coords[0] -= 1
            self.move(
                (
                    self.game.map[self.coords[0]][self.coords[1]].x,
                    self.game.map[self.coords[0]][self.coords[1]].y,
                )
            )
        if mouse_buttons[0]:
            mouse_pos = pg.mouse.get_pos()
            if self.countdown >= 2000:
                self.countdown = 0
                self.attack_anim_trigger = 6  # Trigger the attack animation
            if not self.coral_toggle:
                for enemy in self.game.enemyManager.enemy_list:
                    if (
                        enemy.rect.collidepoint(mouse_pos)
                        and abs(self.coords[0] - enemy.position[0])
                        + abs(self.coords[1] - enemy.position[1])
                        <= 2
                    ):
                        enemy.update_health(-1)
            else:
                coords = None
                for x in range(len(self.game.map)):
                    for y in range(len(x)):
                        if y.collidepoint(mouse_pos):
                            coords = (x, y)
                            break
                    if coords != None:
                        break
                self.game.coral_manager.add_coral(5, 2, coords, "Assets/coral", 120, "std")

    def move(self, val):
        self.x, self.y = val

    def dump_animations(self, path, *args):
        for k in args[0]:
            self.anim_paths[k] = deque()
            full_path = os.path.join(
                path, k
            )  # Correctly construct the full path to the folder
            print(full_path, type(full_path))

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

    def update(self):
        self.get_input()

        if self.attack_in_progress == False:
            self.check_anim_time()

        dt = self.clock.tick()
        self.countdown += dt
        self.check_anim_time()

        self.dt = self.clock.tick()
        self.countdown += self.dt

        if self.countdown > 50000:
            self.respawn_player()
            self.countdown = 0

        if self.attack_anim_trigger > 0:
            self.attack_in_progress = True
            self.attack_anim_trigger -= 1
            attack_frame = self.anim_paths["attack"][0]
            self.anim_paths["attack"].rotate(-1)
            self.sprite = (
                attack_frame  # Update the sprite to the attack animation frame
            )

            if self.attack_anim_trigger == 0:
                self.attack_in_progress = False

        elif self.animation_trigger:
            self.animation_trigger = False  # Reset trigger
            # Loop through animation frames in the 'walk' group
            walk_frames = self.anim_paths.get("walk", [])
            if walk_frames:
                # Rotate through the frames for walking
                current_frame = walk_frames.popleft()
                walk_frames.append(
                    current_frame
                )  # Push frame to the back for next time
                self.sprite = current_frame  # Set the current frame as the sprite

        self.draw(self.sprite)
