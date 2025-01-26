from collections import deque
import pygame as pg
import os
import sys
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

        if not os.path.exists(init_sprite):
            print(f"Error: File '{init_sprite}' not found.")
            sys.exit(1)
        self.sprite = pg.image.load(init_sprite).convert_alpha()

        # Ensure pos is a list, not a tuple, to allow mutation
        self.pos = list(pos)  # Changed from tuple to list
        self.x, self.y = self.pos  # Unpack from the list
        self.h, self.w = self.sprite.get_height(), self.sprite.get_width()
        self.coords = coords

        self.speed = 5  # Adjusted movement speed
        self.prev_move_time = self.game.clock.get_time()

        self.animation_trigger = False
        self.animation_time = animation_time
        self.prev_anim_time = self.game.clock.get_time()

        self.anim_paths = {}

        self.dump_animations(animation_path, args)

        self.radius = 20  # Set the player's radius here

        self.health = health
        self.money = money

        # Attack variables
        self.attack_anim_trigger = 0
        self.attack_in_progress = False

    def draw(self, sprite=None):
        """Draw the player sprite on the screen."""
        if sprite:
            self.game.screen.blit(sprite, (self.x, self.y))
        else:
            self.game.screen.blit(self.sprite, (self.x, self.y))

    def respawn_player(self):
        self.x, self.y = self.game.house.pos
        self.pos = [self.x, self.y]  # Update pos list when respawning

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
        mouse_buttons = pg.mouse.get_pressed()
        curr_time = pg.time.get_ticks()

        if (keys[pg.K_w] or keys[pg.K_UP]) and (  # Move up
            curr_time - self.prev_move_time
        ) >= 100:
            self.prev_move_time = curr_time
            self.pos[1] -= self.speed  # Update y in pos list

        if (keys[pg.K_s] or keys[pg.K_DOWN]) and (  # Move down
            curr_time - self.prev_move_time
        ) >= 100:
            self.prev_move_time = curr_time
            self.pos[1] += self.speed  # Update y in pos list

        if (keys[pg.K_d] or keys[pg.K_RIGHT]) and (  # Move right
            curr_time - self.prev_move_time
        ) >= 100:
            self.prev_move_time = curr_time
            self.pos[0] += self.speed  # Update x in pos list

        if (keys[pg.K_a] or keys[pg.K_LEFT]) and (  # Move left
            curr_time - self.prev_move_time
        ) >= 100:
            self.prev_move_time = curr_time
            self.coords[0] -= 1
            self.move(
                (
                    self.game.map[self.coords[0]][self.coords[1]].x,
                    self.game.map[self.coords[0]][self.coords[1]].y,
                )
            )
        if mouse_buttons[0]:
            if self.countdown >= 2000:
                self.countdown = 0
                self.attack_anim_trigger = 6  # Trigger the attack animation

    def move(self, val):
        self.pos = list(val)  # Ensure the new position is a list
        self.x, self.y = self.pos  # Update x and y

    def dump_animations(self, path, *args):
        for k in args[0]:
            self.anim_paths[k] = deque()
            full_path = os.path.join(path, k)
            print(full_path, type(full_path))

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
            print(self.anim_paths)
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
                current_frame = walk_frames.popleft()
                walk_frames.append(current_frame)
                self.sprite = current_frame  # Set the current frame as the sprite

        self.draw(self.sprite)
