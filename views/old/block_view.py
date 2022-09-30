import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from graphic_primitives.box import Box
from views.old.utxo_view import Utxo


class Block():
    def __init__(self, topleft):
        self.w = 3
        self.h = 0.5
        self.d = 3
        self.x0 = topleft[0]
        self.y0 = topleft[1] -  self.h
        self.z0 = topleft[2]
        self.box = Box(self.x0,self.y0,self.z0, self.w,self.h,self.d, color = 'dark orange')
        self.links = []

    def render(self):
        self.box.render()
