import pygame as pg
from StdObj.MoveableObj import MoveableObj
from StdObj.CollidableObj import CollidableObj


class StdEntity(MoveableObj, CollidableObj):
    def __init__(self, game, dims, velocity):
        MoveableObj.__init__(self, game, dims[:2], velocity)
        CollidableObj.__init__(self, dims)
