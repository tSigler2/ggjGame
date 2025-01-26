import pygame as pg
from Coral import Coral

class CoralManager:
    def __init__(self, game):
        self.game = game
        self.coral_list = []

    def add_coral(self, health, coords, damage, path, animation_time, *args):
        self.coral_list.append(Coral(self.game, health, coords, damage, path, animation_time, args))

    def update_coral(self):
        kill_list = []
        for coral in range(len(self.coral_list)):
            if self.coral_list[coral].health <= 0:
                kill.list.append(coral)
            else:
                coral.update()

        for k in kill_list:
            coral_list.pop(k)
