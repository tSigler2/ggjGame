import pygame as pg

from MoveableObj import MoveableObj
from CollidableObj import CollidableObj


class StdEntity(MoveableObj, CollidableObj):
    def __init__(self, game, dims, velocity):
        # __init__ was missing self
        MoveableObj.__init__(self, game, (dims[0], dims[1]), velocity)
        CollidableObj.__init__(self, dims)
