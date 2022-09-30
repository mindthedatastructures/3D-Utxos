import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

RED   = (1,0,0)
GREEN = (0,1,0)
BLUE  = (0,0,1)

class Axis():
    def __init__(self):
        None

    def renderL(self):
        glColor3fv(RED)
        glVertex3fv((0,0,0))
        glVertex3fv((0,0,10))
        
        glColor3fv(GREEN)
        glVertex3fv((0,0,0))
        glVertex3fv((0,10,0))

        glColor3fv(BLUE)
        glVertex3fv((0,0,0))
        glVertex3fv((10,0,0))

    def renderS(self):
        None
    