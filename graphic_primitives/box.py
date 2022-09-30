import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from graphic_primitives.colors import colors

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

class Box():
    def __init__(self,x0,y0,z0,w,h,d, color='green', drawLines =True, drawSurfaces=True, white_borders=False):
        self.updateVertices(x0,y0,z0,w,h,d)
        self.setColor(color)
        self.drawLines = drawLines
        self.drawSurfaces = drawSurfaces
        self.white_borders = white_borders

    def updateVertices(self,x0,y0,z0,w,h,d):
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

    def setColor(self,color):
        if type(color) == str:
            self.color = colors[color]
        else:
            self.color = color

    def renderS(self):
        if self.drawSurfaces:
            glColor3fv(self.color)
            for surface in surfaces:
                x = 0
                for vertex in surface:
                    x+=1
                    glVertex3fv(self.verticies[vertex])
        
    def renderL(self):
        if self.white_borders:
            glColor3fv((1,1,1))
        else:
            glColor3fv((0,0,0))
        for edge in edges:
            for vertex in edge:
                glVertex3fv(self.verticies[vertex])


class Cube(Box):
    def __init__(self):
        super().__init__(-1,-1,-1,2,2,2)
