import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from graphic_primitives.box import Box
from graphic_primitives.colors import colors


class Echantillon():
    def __init__(self, index, color, topleft):
        self.index = index
        self.color = color
        self.topleft = topleft
        self.w = 0.7
        self.h = 0.7
        self.d = 0.1
        self.x0 = topleft[0]
        self.y0 = topleft[1] -  self.h
        self.z0 = topleft[2]

        self.box = Box(self.x0,self.y0,self.z0, self.w,self.h,self.d, color = color)

    def render(self):
        self.box.render()


class ColorPalette():
    def __init__(self):
        self.x0 = 10
        self.y0 = 0
        self.z0 = 20
        self.w  = 18
        self.h  = 18
        self.d  = 1
        self.offsetx = 0.15
        self.offsety = 0.15
        self.paddingx = 0.3
        self.paddingy = 0.3
        self.echsPerLine = 16

        self.echw = 0.7
        self.echh = 0.7
        self.echs = []

        index = 0
        for name, val in colors.items():
            self.addEchantillon(index, val)

        self.box = Box(self.x0,self.y0,self.z0,self.w,self.h,self.d, color=(0,0,0))

    def addEchantillon(self, index, color):
        index = len(self.echs)
        x = self.x0 + self.offsetx +(index%self.echsPerLine) * (self.echw+self.paddingx)
        y = self.y0 + self.h -self.offsety - int(index/self.echsPerLine) * (self.echh+self.paddingy)
        z = self.z0 + self.d
        topleft = (x,y,z)
        dimensions = (0.7, 0.7, 0.1)

        ech = Echantillon(index, color, topleft)
        self.echs.append(ech)

    def render(self):
        self.box.render()
        for u in self.echs:
            u.render()
