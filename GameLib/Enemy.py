from queue import PriorityQueue
from collections import deque
from GameLib.Sprite.MultiAnimatedSprite import MultiAnimatedSprite
import os
import pygame as pg


class Enemy(MultiAnimatedSprite):
    def __init__(
        self,
        game,
        health,
        start_position,
        goal,
        map_matrix,
        path,
        animation_time,
        *args,
        enemy_speed=3,
    ):
        self.anim_paths = {}
        self.dump_animations(path, args)
        self.animation_time = animation_time
        self.animation_trigger = False

        self.game = game
        self.health = health
        self.position = start_position
        self.x, self.y = (
            self.game.map[self.position[0]][self.position[1]].x,
            self.game.map[self.position[0]][self.position[1]].y,
        )
        self.goal = goal
        self.map_matrix = map_matrix
        self.enemy_speed = enemy_speed
        self.path = []
        self.prev_anim_time = pg.time.get_ticks()
        self.index = 0
        self.curr_deque = self.anim_paths["walk"]
        self.move_counter = 0
        self.find_path()
        self.rect = pg.Rect(self.x, self.y, 50, 50)

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

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def take_damage(self, damage):
        self.health -= damage

        if self.health <= 0:
            self.game.map[self.position[0]][self.position[1]].occupied = False
            self.game.map[self.position[0]][self.position[1]].occupant = None
            self.kill()
            self.game.player.get_money(1)

    def astar(self):
        open_set = PriorityQueue()
        open_set.put((0, self.position))
        came_from = {}
        g_score = {self.position: 0}
        f_score = {self.position: self.heuristic(self.position, self.goal)}

        while not open_set.empty():
            _, current = open_set.get()

            if current == self.goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                self.path = path
                return

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if (
                    0 <= neighbor[1] < len(self.map_matrix)
                    and 0 <= neighbor[0] < len(self.map_matrix[0])
                    and self.map_matrix[neighbor[1]][neighbor[0]] != "M"
                ):
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(
                            neighbor, self.goal
                        )
                        open_set.put((f_score[neighbor], neighbor))

    def move(self):
        self.move_counter += 1
        if self.move_counter >= self.enemy_speed:
            self.move_counter = 0
            if self.index < len(self.path) - 1:
                self.index += 1
                self.position = self.path[self.index]

    def get_position(self):
        return self.position

    def find_path(self):
        self.astar()

    def check_anim_time(self):
        curr_time = pg.time.get_ticks()
        if curr_time - self.animation_time > self.prev_anim_time:
            self.prev_anim_time = curr_time
            self.animation_trigger = True

    def animate(self):
        curr_sprite = self.curr_deque[0]
        self.curr_deque.rotate(-1)
        self.game.screen.blit(curr_sprite, (self.x, self.y))

    def update_health(self, val):
        self.health -= val

    def update(self):
        self.check_anim_time()

        if (
            self.position == (5, 6)
            or self.position == (7, 6)
            or self.position == (6, 5)
            or self.position == (6, 7)
        ):
            self.curr_deque = self.anim_paths["attack"]
        else:
            self.curr_deque = self.anim_paths["walk"]
            self.move()

        if self.animation_trigger:
            self.animate()

            if self.curr_deque == self.anim_paths["attack"]:
                self.game.house.health -= 1
