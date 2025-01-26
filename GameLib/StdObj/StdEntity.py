import pygame as pg
from GameLib.StdObj.MoveableObj import MoveableObj
from GameLib.StdObj.CollidableObj import CollidableObj


class StdEntity(MoveableObj, CollidableObj):
    def __init__(self, game, dims, velocity):
        MoveableObj.__init__(self, game, dims[:2], velocity)
        CollidableObj.__init__(self, dims)
