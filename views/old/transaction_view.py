import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


from graphic_primitives.box import Box
from graphic_primitives.colors import colors

class Link():
    def __init__(self, utxo, link_type):
        self.utxo = utxo
        self.link_type = link_type


class Transaction():
    LINK_TO_INPUT_TYPE  = 'LINK_TO_INPUT_TYPE'
    LINK_TO_OUTPUT_TYPE = 'LINK_TO_OUTPUT_TYPE'

    def __init__(self, topleft):
        self.w = 0.7
        self.h = 0.7
        self.d = 0.1
        self.x0 = topleft[0]
        self.y0 = topleft[1] -  self.h
        self.z0 = topleft[2]
        self.box = Box(self.x0,self.y0,self.z0, self.w,self.h,self.d, color = 'pale turquoise')
        self.links = []

    def link(self, utxo, link_type):
        self.links.append(Link(utxo,link_type))

    def alterColorsOfUtxos(self):
        for l in self.links:
            l.utxo.alterColor()

    def render(self):
        self.box.render()
        if len(self.links)>0:
            glBegin(GL_QUADS)
            for link in self.links:
                utxo = link.utxo
                if link.link_type == Transaction.LINK_TO_INPUT_TYPE:
                    c = colors['yellow']
                elif link.link_type == Transaction.LINK_TO_OUTPUT_TYPE:
                    c = colors['red']
                glColor3fv(c)
                glVertex3fv((self.x0+(self.w/2)-0.02,self.y0+(self.h/2),self.z0+(self.d/2)))
                glVertex3fv((self.x0+(self.w/2)+0.02,self.y0+(self.h/2),self.z0+(self.d/2)))
                glVertex3fv((utxo.x0+(utxo.w/2)+0.02,utxo.y0+(utxo.h/2),utxo.z0+(utxo.d/2)))
                glVertex3fv((utxo.x0+(utxo.w/2)-0.02,utxo.y0+(utxo.h/2),utxo.z0+(utxo.d/2)))
            glEnd()
            glBegin(GL_LINES)
            for link in self.links:
                utxo = link.utxo
                glColor3fv(colors['black'])
                glVertex3fv((self.x0+(self.w/2)-0.02,self.y0+(self.h/2),self.z0+(self.d/2)))
                glVertex3fv((self.x0+(self.w/2)+0.02,self.y0+(self.h/2),self.z0+(self.d/2)))
                glVertex3fv((utxo.x0+(utxo.w/2)+0.02,utxo.y0+(utxo.h/2),utxo.z0+(utxo.d/2)))
                glVertex3fv((utxo.x0+(utxo.w/2)-0.02,utxo.y0+(utxo.h/2),utxo.z0+(utxo.d/2)))
            glEnd()
