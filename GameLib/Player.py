# File: GameLib\Player.py
from collections import deque
import pygame as pg
import os
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

        if not os.path.exists(init_sprite):
            print(f"Error: File '{init_sprite}' not found.")
            sys.exit(1)
        self.sprite = pg.image.load(init_sprite).convert_alpha()

        # Ensure pos is a list, not a tuple, to allow mutation
        self.pos = list(pos)  # Changed from tuple to list
        print(f"Type of self.pos before move: {type(self.pos)}")
        self.x, self.y = self.pos  # Unpack from the list
        self.h, self.w = self.sprite.get_height(), self.sprite.get_width()
        self.coords = coords

        self.speed = 3  # Adjusted movement speed
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

        # Initialize velocity attributes
        self.vel_x = 0
        self.vel_y = 0

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

        print(f"Pos initialized as: {self.pos}")

        # self.pos = list(pos)  # Changed from tuple to list

        # Move up
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.pos[1] -= self.speed  # Move up based on speed
        # Move down
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.pos[1] += self.speed  # Move down based on speed
        # Move left
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.pos[0] -= self.speed  # Move left based on speed
        # Move right
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.pos[0] += self.speed  # Move right based on speed

        
        # Prevent the player from going off the screen
        self.x = max(
            258, min(961, self.pos[0])
        )  # Constrain left and right between 288 and 991
        self.y = max(
            -38, min(651, self.pos[1])
        )  # Constrain top and bottom between 8 and 711

        #Bug-Fix assignment here
        self.pos = (self.map[0][0].x, self.map[0][0].y)

        # Debug print statements for the boundaries
        if self.game.debug_mode:
            print(
                f"Left boundary: {self.radius}, Right boundary: {self.game.width - self.radius}"
            )
            print(
                f"Up boundary: {self.radius}, Down boundary: {self.game.height - self.radius}"
            )

        # Update the player position based on the new values
        self.x, self.y = self.pos  # Update x, y position values

        # Handle attack based on mouse button press
        if mouse_buttons[0]:
            mouse_pos = pg.mouse.get_pos()
            if self.countdown >= 2000:
                self.countdown = 0
                self.attack_anim_trigger = 6  # Trigger the attack animation
            for enemy in self.game.enemyManager.enemy_list:
                if (
                    enemy.rect.collidepoint(mouse_pos)
                    and abs(self.coords[0] - enemy.position[0])
                    + abs(self.coords[1] - enemy.position[1])
                    <= 2
                ):
                    enemy.update_health(-1)

    def move(self):
        # Update player position based on velocity
        self.pos[0] += self.vel_x * self.game.delta_time
        self.pos[1] += self.vel_y * self.game.delta_time
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
        self.move()  # Move the player based on velocity

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

        # Display velocity for debugging
        speed_text = f"Speed X: {self.vel_x:.2f} Y: {self.vel_y:.2f}"
        text_surface = self.game.font.render(speed_text, True, (255, 255, 255))
        self.game.screen.blit(text_surface, (10, 10))  # Adjust position as needed

        self.draw(self.sprite)
