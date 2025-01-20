import pygame as pg
from AnimatedSprite import AnimatedSprite

class Player(AnimatedSprite):
    def __init__(self, game):
        self.game = game
        self.x, self.y = P_POS
        self.health = P_MAX_HEALTH

    def movement(self):
        speed = P_SPEED * self.game.delta_time

        keys = pg.key.get_pressed()
        
        if keys[pg.K_w]:
            pass
        if keys[pg.K_s]:
            pass
        if keys[pg.K_d]:
            pass
        if keys[pg.K_a]:
            pass

    def update(self):
        self.movement()
        super().update()
