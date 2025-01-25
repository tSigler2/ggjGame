import pygame as pg
from AnimatedSprite import AnimatedSprite


class Enemy(AnimatedSprite):
    def __init__(self, game):
        self.game = game
        self.health = 100
        self.speed = 5
        self.range = 10
        
