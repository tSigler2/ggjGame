import pygame as pg


class Enemy:
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)
        #self.game = game
        self.health = 100
        self.speed = 5
        self.range = 10
        self.color = (0, 0, 255)
        
    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect)
    
