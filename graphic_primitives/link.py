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

class Link():
    def __init__(self, color='magenta', radius = 0.5, onlyLines =False):
        self.verticies = None
        self.setColor(color)
        self.onlyLines = onlyLines
        self.radius = radius

    def updateVertices(self,x0,y0,z0,x1,y1,z1):
        radius = self.radius
        self.verticies = (
            (x0+radius,y0-radius, z0),
            (x0+radius,y0+radius, z0),
            (x0-radius,y0+radius, z0),
            (x0-radius,y0-radius, z0),
            (x1+radius,y1-radius, z1),
            (x1+radius,y1+radius, z1),
            (x1-radius,y1+radius, z1),
            (x1-radius,y1-radius, z1),
            )

    def setColor(self,color):
        if type(color) == str:
            self.color = colors[color]
        else:
            self.color = color

    def renderS(self):
        if not self.verticies:
            return
        if not self.onlyLines:
            glColor3fv(self.color)
            for surface in surfaces:
                x = 0
                for vertex in surface:
                    x+=1
                    glVertex3fv(self.verticies[vertex])

    def renderL(self):
        if not self.verticies:
            return
        glColor3fv((0,0,0))
        for edge in edges:
            for vertex in edge:
                glVertex3fv(self.verticies[vertex])

    def render(self):
        if not self.verticies:
            return
        if not self.onlyLines:
            glBegin(GL_QUADS)
            self.renderS()
            glEnd()

        glBegin(GL_LINES)
        self.renderL()
        glEnd()
