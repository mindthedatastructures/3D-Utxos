

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from graphic_primitives.colors import colors

import math

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

sq3o2 = math.sqrt(3)/2

class SegmentView():
    # Vertical: True
    def __init__(self,x,y,z,size,orientation = True):
        self.enable= True
        self.orientation = orientation
        self.size = size
        self.x = x
        self.y = y
        self.z = z
        self.updateVertices()

    def setPos(self,x,y,z):
        (self.x, self.y, self.z) = (x,y,z)

    def updateVertices(self):
        if self.orientation:
            self.points = [
                (self.x,self.y,self.z),
                (self.x-0.5*self.size, self.y-sq3o2*self.size, self.z),
                (self.x-0.5*self.size, self.y-(2+sq3o2)*self.size, self.z),
                (self.x+0.5*self.size, self.y-sq3o2*self.size, self.z),
                (self.x+0.5*self.size, self.y-sq3o2*self.size, self.z),
                (self.x+0.5*self.size, self.y-(2+sq3o2)*self.size, self.z),
                (self.x, self.y-2*(1+sq3o2)*self.size, self.z),
                (self.x-0.5*self.size, self.y-(2+sq3o2)*self.size ,self.z)
            ]
        else:
            self.points = [
                (self.x,self.y,self.z),
                (self.x+sq3o2*self.size,       self.y-0.5*self.size, self.z),
                (self.x+(2+sq3o2)*self.size,   self.y-0.5*self.size, self.z),
                (self.x+sq3o2*self.size,       self.y+0.5*self.size, self.z),
                (self.x+sq3o2*self.size,       self.y+0.5*self.size, self.z),
                (self.x+(2+sq3o2)*self.size,   self.y+0.5*self.size, self.z),
                (self.x+2*(1+sq3o2)*self.size, self.y,               self.z),
                (self.x+(2+sq3o2)*self.size ,  self.y-0.5*self.size, self.z)
            ]


    def renderS(self):
        if not self.enable:
            return

        glColor3fv((1,0,0))
        for p in self.points:
            glVertex3fv(p)
    def renderL(self):
        None
    def render(self):
        if not self.enable:
            return
        glBegin(GL_QUADS)
        self.renderS()
        glEnd()


class NumberView():
    # s * k_w = w
    # s * k_h = h
    margin=1/50
    k_w = 2+4*sq3o2+4*margin
    k_h = 4+6*sq3o2+5*margin


    def __init__(self,x,y,z,size):
        self.offset = 0.05
        self.x=x
        self.y=y
        self.z=z
        self.w = size
        self.h = self.w*NumberView.k_h/NumberView.k_w
        self.d = 0

        self.s = self.w/NumberView.k_w
        self.margin = NumberView.margin * self.s
        self.sq3o2 = sq3o2 * self.s

        self.updatePoints()
        self.initSegments()

    def initSegments(self):
        # TOP
        self.s1=SegmentView(
            self.x+2*self.margin+self.sq3o2,
            self.y+self.h+ - self.margin-self.sq3o2,
            self.z+self.offset,
            self.s,
            orientation = False)
        # UP LEFT
        self.s2=SegmentView(
            self.x+self.margin+self.sq3o2,
            self.y+self.h+ - 2*self.margin-self.sq3o2,
            self.z+self.offset,
            self.s,
            orientation = True)
        # UP RIGHT
        self.s3=SegmentView(
            self.x+self.w - self.margin- self.sq3o2,
            self.y+self.h+ - 2*self.margin-self.sq3o2,
            self.z+self.offset,
            self.s,
            orientation = True)
        # MIDDLE
        self.s4=SegmentView(
            self.x+2*self.margin+self.sq3o2,
            self.y+self.h/2,
            self.z+self.offset,
            self.s,
            orientation = False)
        # DOWN LEFT
        self.s5=SegmentView(
            self.x+self.margin+self.sq3o2,
            self.y+self.h+ - 2*self.margin-3*self.sq3o2 - 2*self.s,
            self.z+self.offset,
            self.s,
            orientation = True)

        # DOWN RIGHT
        self.s6=SegmentView(
            self.x+self.w - self.margin- self.sq3o2,
            self.y+self.h+ - 2*self.margin-3*self.sq3o2 - 2*self.s,
            self.z+self.offset,
            self.s,
            orientation = True)

        # MIDDLE
        self.s7=SegmentView(
            self.x+2*self.margin+self.sq3o2,
            self.y+self.h+ - 2*self.margin-5*self.sq3o2 - 4*self.s,
            self.z+self.offset,
            self.s,
            orientation = False)

        self.segments = [self.s1, self.s2,self.s3, self.s4, self.s5, self.s6, self.s7]

    def setY(self,y):
        self.y = y

    def setNumber(self,n):
        if n == '-':
            (self.s1.enable,self.s2.enable,self.s3.enable,self.s4.enable,self.s5.enable,self.s6.enable,self.s7.enable) = \
                (False, False, False, True, False, False, False)
            return
        self.s1.enable = n not in [1,4]
        self.s2.enable = n not in [1,2,3,7]
        self.s3.enable = n not in [5,6]
        self.s4.enable = n not in [0,1,7]
        self.s5.enable = n in [0,2,6,8]
        self.s6.enable = n != 2
        self.s7.enable = n not in [1,4,7]

    def setPos(self,x,y,z):
        (self.x,self.y,self.z) = (x,y,z)
        self.updatePoints()
        self.updateSegments()

    def updatePoints(self):
        self.points = (
            (self.x,self.y, self.z),
            (self.x,self.y+self.h, self.z),
            (self.x+self.w,self.y+self.h, self.z),
            (self.x+self.w,self.y, self.z)
            )

    def updateSegments(self):
        self.s1.setPos(
            self.x+2*self.margin+self.sq3o2,
            self.y+self.h+ - self.margin-self.sq3o2,
            self.z+self.offset
            )
        # UP LEFT
        self.s2.setPos(
            self.x+self.margin+self.sq3o2,
            self.y+self.h+ - 2*self.margin-self.sq3o2,
            self.z+self.offset
            )
        # UP RIGHT
        self.s3.setPos(
            self.x+self.w - self.margin- self.sq3o2,
            self.y+self.h+ - 2*self.margin-self.sq3o2,
            self.z+self.offset
            )
        # MIDDLE
        self.s4.setPos(
            self.x+2*self.margin+self.sq3o2,
            self.y+self.h/2,
            self.z+self.offset
            )
        # DOWN LEFT
        self.s5.setPos(
            self.x+self.margin+self.sq3o2,
            self.y+self.h+ - 2*self.margin-3*self.sq3o2 - 2*self.s,
            self.z+self.offset
            )

        # DOWN RIGHT
        self.s6.setPos(
            self.x+self.w - self.margin- self.sq3o2,
            self.y+self.h+ - 2*self.margin-3*self.sq3o2 - 2*self.s,
            self.z+self.offset
            )

        # MIDDLE
        self.s7.setPos(
            self.x+2*self.margin+self.sq3o2,
            self.y+self.h+ - 2*self.margin-5*self.sq3o2 - 4*self.s,
            self.z+self.offset
            )
        [s.updateVertices() for s in self.segments]


    def renderS(self):
        glColor3fv((0,0,0))
        [glVertex3fv(p) for p in self.points]
        [s.renderS() for s in self.segments]

    def renderL(self):
        None
    def render(self):
        glBegin(GL_QUADS)
        self.renderS()
        glEnd()

