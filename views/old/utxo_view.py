import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from graphic_primitives.box import Box

class Utxo():
    def __init__(self, topleft, color='blue', useImage=False):
        self.w = 0.7
        self.h = 0.7
        self.d = 0.1
        self.x0 = topleft[0]
        self.y0 = topleft[1] -  self.h
        self.z0 = topleft[2]
        self.color = color
        self.box = Box(self.x0,self.y0,self.z0, self.w,self.h,self.d, color = color)

    def render(self):
        self.box.render()
    
    def alterColor(self):
        if self.color == 'blue':
            self.color = 'red'
        elif self.color == 'red':
            self.color = 'blue'
        self.box.setColor(self.color)

