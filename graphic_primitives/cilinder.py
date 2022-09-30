import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import math

points = None
def getPoints(top,radius,ratev,rateh):
    points=[]
    for i in range(ratev):
        if i == 0:
            res = [(top[0],top[1],top[2])]*rateh
        elif i == ratev-1:
            res = [(top[0],top[1],top[2]-2*radius)]*rateh
        else:
            z_center = top[2] - radius
            z = top[2]-(i*2*radius/(ratev-1))
            r_h = math.sqrt(radius**2 - (z-z_center)**2)
            x=top[0]
            y = r_h+top[1]
            cosx = math.cos(2*math.pi/rateh)
            sinx = math.sin(2*math.pi/rateh)
            res = []
            for j in range(rateh):
                res.append((x+0,y+0,z+0))
                oldx=x
                x =  ((x-top[0])*cosx + (y-top[1])*sinx)+top[0]
                y = (-(oldx-top[0])*sinx + (y-top[1])*cosx)+top[1]
        points.append(res)
    return points


COLOR_TYPE_SINGLE=1

class Cilinder():
    def __init__(self, pointA, pointB, radius, ratev=10, rateh = 10,color=(0,0,1)):
        self.pointA = pointB
        self.center = center
        self.radius = radius
        self.ratev = ratev
        self.rateh = rateh
        self.color=color
        self.points = None

    def getPoints(self,top,radius,ratev,rateh):
        points=[]
        for i in range(ratev):
            if i == 0:
                res = [(top[0],top[1],top[2])]*rateh
            elif i == ratev-1:
                res = [(top[0],top[1],top[2]-2*radius)]*rateh
            else:
                z_center = top[2] - radius
                z = top[2]-(i*2*radius/(ratev-1))
                r_h = math.sqrt(radius**2 - (z-z_center)**2)
                x=top[0]
                y = r_h+top[1]
                cosx = math.cos(2*math.pi/rateh)
                sinx = math.sin(2*math.pi/rateh)
                res = []
                for j in range(rateh):
                    res.append((x+0,y+0,z+0))
                    oldx=x
                    x =  ((x-top[0])*cosx + (y-top[1])*sinx)+top[0]
                    y = (-(oldx-top[0])*sinx + (y-top[1])*cosx)+top[1]
            points.append(res)
        return points

    def renderS(self):
        points=self.getPoints(top,self.radius,self.ratev,self.rateh)
        for i in range(self.ratev-1):
            points_prev=points[i]
            points_next=points[i+1]
            for j in range(self.rateh):
                glColor3fv(self.color)
                glVertex3fv(points_prev[j])
                glVertex3fv(points_next[j])
                glVertex3fv(points_next[(j+1)%self.rateh])
                glVertex3fv(points_prev[(j+1)%self.rateh])
