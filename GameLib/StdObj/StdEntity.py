import pygame as pg

from MoveableObj import MoveableObj
from CollidableObj import CollidableObj

class StdEntity(MoveableObj, CollidableObj):
    def __init__(self, game, dims, velocity):
        MoveableObj.__init__(game, (dims[0], dims[1]). velocity)
        CollidableObj.__init(dims)
