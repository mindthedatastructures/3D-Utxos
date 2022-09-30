import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from graphic_primitives.box import Box
from views.old.utxo_view import Utxo

class LivingBoardView():
    offsetx = 0.15
    offsety = 0.15
    paddingx = 0.3
    paddingy = 0.3
    utxow = 0.7
    utxoh = 0.7
    def __init__(self, topleft, dimensions, utxosPerLine):
        self.utxosPerLine = utxosPerLine
        self.x0 = topleft[0]
        self.y0 = topleft[1]
        self.z0 = topleft[2]
        self.w  = dimensions[0]
        self.h  = dimensions[1]
        self.d  = dimensions[2]

        self.utxos = []
        self.box = Box(self.x0,self.y0,self.z0,self.w,self.h,self.d, color='dark green')

    def addUtxo(self):
        index = len(self.utxos)
        x = self.x0 + LivingBoardView.offsetx +(index%self.utxosPerLine) * (LivingBoardView.utxow+LivingBoardView.paddingx)
        y = self.y0 + self.h -LivingBoardView.offsety - int(index/self.utxosPerLine) * (LivingBoardView.utxoh+LivingBoardView.paddingy)
        z = self.z0 + self.d
        topleft = (x,y,z)
        utxo = Utxo(topleft)
        self.utxos.append((index,utxo,topleft))

    def render(self):
        self.box.render()
        for u in self.utxos:
            u[1].render()







