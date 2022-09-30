import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from graphic_primitives.colors import colors
from graphic_primitives.box import Box

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

class ValidatorBox():
    def __init__(self,x0,y0,z0,w,h,d, w1,h1,d1, color='green'):
        self.box = [None]*6
        w_col = (w-w1)/2
        h_cov = (h-h1)/2
        d_col = (d-d1)/2
        self.verticies = (
            (x0+w,y0, z0),
            (x0+w,y0+h, z0),
            (x0,y0+h, z0),
            (x0,y0, z0),
            (x0+w,y0, z0+d),
            (x0+w,y0+h, z0+d),
            (x0,y0, z0+d),
            (x0,y0+h, z0+d),
            )

        self.box[0] = Box(x0,y0,z0, w,h_cov,d, color, drawLines=False)
        self.box[1] = Box(x0,y0+h-h_cov,z0, w,h_cov,d, color, drawLines=False)
        self.box[2] = Box(x0,y0,z0, w_col,h,d_col, color, drawLines=False)
        self.box[3] = Box(x0,y0,z0+d-d_col, w_col,h,d_col, color, drawLines=False)
        self.box[4] = Box(x0+w-w_col,y0,z0, w_col,h,d_col, color, drawLines=False)
        self.box[5] = Box(x0+w-w_col,y0,z0+d-d_col, w_col,h,d_col, color, drawLines=False)

        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.w = w
        self.h = h
        self.d = d
        self.w_col = w_col
        self.h_cov = h_cov
        self.d_col = d_col

    def setColor(self,color):
        for b in self.box:
            b.setColor(color)



    def renderS(self):
        for b in self.box:
            b.renderS()
        glColor3fv((0,0,0))
    def render(self):
        for b in self.box:
            b.render()
        glColor3fv((0,0,0))

        glBegin(GL_LINES)
        self.renderL()
        glEnd()

        
    def renderL(self):
        for edge in edges:
            for vertex in edge:
                glVertex3fv(self.verticies[vertex])
        #holes
        glVertex3fv((self.x0+self.w_col, self.y0+self.h_cov,self.z0))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h_cov,self.z0))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h_cov,self.z0))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h-self.h_cov,self.z0))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h-self.h_cov,self.z0))
        glVertex3fv((self.x0+self.w_col, self.y0+self.h-self.h_cov,self.z0))
        glVertex3fv((self.x0+self.w_col, self.y0+self.h-self.h_cov,self.z0))
        glVertex3fv((self.x0+self.w_col, self.y0+self.h_cov,self.z0))

        glVertex3fv((self.x0+self.w_col, self.y0+self.h_cov,self.z0+self.d))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h_cov,self.z0+self.d))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h_cov,self.z0+self.d))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h-self.h_cov,self.z0+self.d))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h-self.h_cov,self.z0+self.d))
        glVertex3fv((self.x0+self.w_col, self.y0+self.h-self.h_cov,self.z0+self.d))
        glVertex3fv((self.x0+self.w_col, self.y0+self.h-self.h_cov,self.z0+self.d))
        glVertex3fv((self.x0+self.w_col, self.y0+self.h_cov,self.z0+self.d))

        glVertex3fv((self.x0, self.y0+self.h_cov,self.z0+self.d_col))
        glVertex3fv((self.x0, self.y0+self.h_cov,self.z0+self.d-self.d_col))
        glVertex3fv((self.x0, self.y0+self.h_cov,self.z0+self.d-self.d_col))
        glVertex3fv((self.x0, self.y0+self.h-self.h_cov,self.z0+self.d-self.d_col))
        glVertex3fv((self.x0, self.y0+self.h-self.h_cov,self.z0+self.d-self.d_col))
        glVertex3fv((self.x0, self.y0+self.h-self.h_cov,self.z0+self.d_col))
        glVertex3fv((self.x0, self.y0+self.h-self.h_cov,self.z0+self.d_col))
        glVertex3fv((self.x0, self.y0+self.h_cov,self.z0+self.d_col))

        glVertex3fv((self.x0+self.w, self.y0+self.h_cov,self.z0+self.d_col))
        glVertex3fv((self.x0+self.w, self.y0+self.h_cov,self.z0+self.d-self.d_col))
        glVertex3fv((self.x0+self.w, self.y0+self.h_cov,self.z0+self.d-self.d_col))
        glVertex3fv((self.x0+self.w, self.y0+self.h-self.h_cov,self.z0+self.d-self.d_col))
        glVertex3fv((self.x0+self.w, self.y0+self.h-self.h_cov,self.z0+self.d-self.d_col))
        glVertex3fv((self.x0+self.w, self.y0+self.h-self.h_cov,self.z0+self.d_col))
        glVertex3fv((self.x0+self.w, self.y0+self.h-self.h_cov,self.z0+self.d_col))
        glVertex3fv((self.x0+self.w, self.y0+self.h_cov,self.z0+self.d_col))

        # Internal Columns
        glVertex3fv((self.x0+self.w_col, self.y0+self.h_cov,self.z0+self.d_col))
        glVertex3fv((self.x0+self.w_col, self.y0+self.h_cov,self.z0+self.d-self.d_col))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h_cov,self.z0+self.d_col))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h_cov,self.z0+self.d-self.d_col))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h-self.h_cov,self.z0+self.d_col))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h-self.h_cov,self.z0+self.d-self.d_col))
        glVertex3fv((self.x0+self.w_col, self.y0+self.h-self.h_cov,self.z0+self.d_col))
        glVertex3fv((self.x0+self.w_col, self.y0+self.h-self.h_cov,self.z0+self.d-self.d_col))

        glVertex3fv((self.x0, self.y0+self.h_cov,self.z0+self.d_col))
        glVertex3fv((self.x0+self.w_col, self.y0+self.h_cov,self.z0+self.d_col))
        glVertex3fv((self.x0+self.w_col, self.y0+self.h_cov,self.z0+self.d_col))
        glVertex3fv((self.x0+self.w_col, self.y0+self.h_cov,self.z0))

        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h_cov,self.z0))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h_cov,self.z0+self.d_col))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h_cov,self.z0+self.d_col))
        glVertex3fv((self.x0+self.w, self.y0,self.z0+self.d_col))

        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h_cov,self.z0+self.d))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h_cov,self.z0+self.d-self.d_col))
        glVertex3fv((self.x0+self.w-self.w_col, self.y0+self.h_cov,self.z0+self.d-self.d_col))
        glVertex3fv((self.x0+self.w, self.y0,self.z0+self.d-self.d_col))

        glVertex3fv((self.x0+self.w_col, self.y0+self.h_cov,self.z0+self.d))
        glVertex3fv((self.x0+self.w_col, self.y0+self.h_cov,self.z0+self.d-self.d_col))
        glVertex3fv((self.x0+self.w_col, self.y0+self.h_cov,self.z0+self.d-self.d_col))
        glVertex3fv((self.x0, self.y0,self.z0+self.d-self.d_col))


