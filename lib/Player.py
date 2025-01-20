import pygame as pg

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = P_POS
        self.health = P_MAX_HEALTH

    def movement(self):
        speed = P_SPEED * self.game.delta_time
        dx, dy = 0, 0

        keys = pg.key.get_pressed()
        
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
