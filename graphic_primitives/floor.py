import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from graphic_primitives.colors import colors

RED   = (1,0,0)
GREEN = (0,1,0)
BLUE  = (0,0,1)

class Floor():
    def __init__(self):
        None

    def renderS(self):
        glColor3fv(colors['brown'])
        
        glVertex3fv((0,0,0))
        glVertex3fv((0,0,100))
        glVertex3fv((100,0,100))
        glVertex3fv((100,0,0))
    def renderL(self):
        None
