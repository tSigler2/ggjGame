import pygame as pg
from GameLib.Sprite.TempMultiAnimatedSprite import MultiAnimatedSprite

class Coral(MultiAnimatedSprite):
    def __init__(self, game, health, coords, damage, path, animation_time, *args):
        super().__init__(game, path, coords, 1, 0, animationed_time, args)
        self.game = game
        self.health = health
        self.damage = damage
        self.x, self.y = coords

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

    def update(self):
        self.animate()
        self.damage()
