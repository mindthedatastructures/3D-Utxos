
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from graphic_primitives.colors import colors

import math




class Clock():
    def __init__(self,x0,y0,z0,radius, resolution = 25):
        self.points = []
        self.resolution = resolution

        delta = 2*math.pi / resolution
        pi_over_2 = math.pi /2
        for i in range(resolution):
            x1 = x0 + radius*math.cos(-i*delta + pi_over_2)
            y1 = y0 + radius*math.sin(-i*delta + pi_over_2)
            self.points.append((x1,y1,z0))
        self.center = (x0,y0,z0)
        self.percent = 0

        self.green = self.getColor('green')
        self.red = self.getColor('red')

    def getColor(self,color):
        if type(color) == str:
            return colors[color]
        else:
            return color


    def setPercentage(self,percent):
        self.percent=percent

    def renderL(self):
        if False:
            if self.white_borders:
                glColor3fv((1,1,1))
            else:
                glColor3fv((0,0,0))
            glBegin(GL_LINES)
            for edge in edges:
                for vertex in edge:
                    glVertex3fv(self.verticies[vertex])
            glEnd()
            
    def renderS(self):
        switch_point = int(self.percent * self.resolution/ 100)
        glColor3fv(self.green)
        for i in range(0, switch_point):
            glVertex3fv(self.points[i])
            glVertex3fv(self.points[(i+1)%self.resolution])
            glVertex3fv(self.center)
            glVertex3fv(self.center)
        glColor3fv(self.red)
        for i in range(switch_point, self.resolution):
            glVertex3fv(self.points[i])
            glVertex3fv(self.points[(i+1)%self.resolution])
            glVertex3fv(self.center)
            glVertex3fv(self.center)

