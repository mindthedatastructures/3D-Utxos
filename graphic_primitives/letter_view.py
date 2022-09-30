

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from graphic_primitives.colors import colors

import math
values = {
    'a':[False,True,True,False,True,False,False,True,True,True,True,True,True,False,False,True,True,False,False,True],
    'b':[True,True,True,False,True,False,False,True,True,True,True,False,True,False,False,True,True,True,True,False],
    'c':[False,True,True,True,True,False,False,False,True,False,False,False,True,False,False,False,False,True,True,True],
    'd':[True,True,True,False,True,False,False,True,True,False,False,True,True,False,False,True,True,True,True,False],
    'e':[True,True,True,True,True,False,False,False,True,True,True,False,True,False,False,False,True,True,True,True],
    'f':[True,True,True,True,True,False,False,False,True,True,True,False,True,False,False,False,True,False,False,False],
    'g':[False,True,True,True,True,False,False,False,True,False,True,True,True,False,False,True,False,True,True,True],
    'h':[True,False,False,True,True,False,False,True,True,True,True,True,True,False,False,True,True,False,False,True],
    'i':[False,True,True,True,False,False,True,False,False,False,True,False,False,False,True,False,False,True,True,True],
    'j':[False,False,False,True,False,False,False,True,False,False,False,True,True,False,False,True,False,True,True,False],
    'k':[True,False,False,True,True,False,True,False,True,True,False,False,True,False,True,False,True,False,False,True],
    'l':[True,False,False,False,True,False,False,False,True,False,False,False,True,False,False,False,True,True,True,True],
    'm':[True,False,False,True,True,True,True,True,True,True,True,True,True,False,False,True,True,False,False,True],
    'n':[True,False,False,True,True,True,False,True,True,False,True,True,True,False,False,True,True,False,False,True],
    'o':[False,True,True,False,True,False,False,True,True,False,False,True,True,False,False,True,False,True,True,False],
    'p':[True,True,True,False,True,False,False,True,True,True,True,False,True,False,False,False,True,False,False,False],
    'q':[False,True,True,False,True,False,False,True,True,False,False,True,True,False,True,True,False,True,True,True],
    'r':[True,True,True,False,True,False,False,True,True,True,True,False,True,False,True,False,True,False,False,True],
    's':[False,True,True,True,True,False,False,False,False,True,True,False,False,False,False,True,True,True,True,False],
    't':[False,True,True,True,False,False,True,False,False,False,True,False,False,False,True,False,False,False,True,False],
    'u':[True,False,False,True,True,False,False,True,True,False,False,True,True,False,False,True,True,True,True,True],
    'v':[True,False,False,True,True,False,False,True,True,False,False,True,False,True,True,False,False,True,True,False],
    'w':[True,False,False,True,True,False,False,True,True,True,True,True,False,True,True,False,False,True,True,False],
    'x':[True,False,False,True,True,False,False,True,False,True,True,False,True,False,False,True,True,False,False,True],
    'y':[True,False,False,True,True,False,False,True,False,True,True,False,False,False,True,False,False,False,True,False],
    'z':[True,True,True,True,False,False,False,True,False,False,True,False,False,True,False,False,True,True,True,True],
    ' ':[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
}



sq3o2 = math.sqrt(3)/2

class PixelView():
    # Vertical: True
    def __init__(self,x,y,z,size):
        self.enable= False
        self.size = size
        self.x = x
        self.y = y
        self.z = z
        self.updateVertices()

    def updateVertices(self):
        self.points = [
            (self.x,self.y,self.z),
            (self.x+self.size,self.y,self.z),
            (self.x+self.size,self.y+self.size,self.z),
            (self.x,self.y+self.size,self.z),
        ]
     


    def renderL(self):
        None
    def renderS(self):
        if not self.enable:
            return
        glColor3fv((0,1,0))
        for p in self.points:
            glVertex3fv(p)

class LetterView():
    # s * k_w = w
    # s * k_h = h
    margin=0.2

    def __init__(self,x,y,z,size):
        self.offset = 0.05
        self.x=x
        self.y=y
        self.z=z
        self.w = size
        self.h = size
        self.d = 0

        self.s = self.w/(5+2*LetterView.margin)
        self.margin = LetterView.margin * self.s

        self.updatePoints()
        self.initPixels()


    def initPixels(self):
        self.pixels = []
        for y in range(5):
            for x in range(4):
                a=PixelView(
                    self.x+self.margin+x*self.s,
                    self.y+self.margin+y*self.s,
                    self.z+self.offset,
                    self.s
                    )
                self.pixels.append(a)
    def setLetter(self,val):
        for y in range(5):
            for x in range(4):
                i = 4*y+x
                j= 4*(4-y)+x
                self.pixels[j].enable = values[val.lower()][i]
        
    def updatePoints(self):
        self.points = (
            (self.x,self.y, self.z),
            (self.x,self.y+self.h, self.z),
            (self.x+self.w,self.y+self.h, self.z),
            (self.x+self.w,self.y, self.z)
            )


    def renderL(self):
        None
    def renderS(self):
        glColor3fv((0,0,0))
        for p in self.points:
            glVertex3fv(p)
        for s in self.pixels:
            s.renderS()

    def render(self):
        glBegin(GL_QUADS)
        self.renderS()
        glEnd()

        # if self.drawLines:
        #     if self.white_borders:
        #         glColor3fv((1,1,1))
        #     else:
        #         glColor3fv((0,0,0))
        #     glBegin(GL_LINES)
        #     for edge in edges:
        #         for vertex in edge:
        #             glVertex3fv(self.verticies[vertex])
        #     glEnd()

class DisplayView():
    def __init__(self, x,y,z,text, size):
        self.x = x
        self.y = y
        self.z = z
        self.w = size*len(text)
        self.h = size
        self.d = 0
        self.letters=[]

        for i,l in enumerate(text):
            let = LetterView(x+i*size,y,z,size)
            let.setLetter(l)
            self.letters.append(let)
    def renderS(self):
        for l in self.letters:
            l.renderS()
