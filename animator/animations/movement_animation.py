
from animator.IAnimation import IAnimation

class MovementAnimation(IAnimation):

    def __init__(self, o, t0, duration, pos0, pos1, after=[]):
        self.o = o
        self.t0 = t0
        self.duration = duration
        self.pos0 = pos0
        self.pos1 = pos1
        (self.o.x, self.o.y, self.o.z) = pos0
        self.o.updateBox()
        self.hasEnded_v=False
        self.after = after

    def animate(self, now):
        delta_t = (now-self.t0)/self.duration
        if delta_t >= 1:
            (self.o.x, self.o.y, self.o.z) = pos1
            return
        x = self.pos0[0]+(self.pos1[0]-self.pos0[0])*delta_t
        y = self.pos0[1]+(self.pos1[1]-self.pos0[1])*delta_t
        z = self.pos0[2]+(self.pos1[2]-self.pos0[2])*delta_t
        self.o.setPos(x,y,z)
        self.o.updateBox()

    def loadEndPositionForPhase(self):
        (self.o.x, self.o.y, self.o.z) = self.pos1
        
    def hasEnded(self, now):
        if self.hasEnded_v:
            return True
        self.hasEnded_v = self.t0 + self.duration < now
        if self.hasEnded_v:
            self.loadEndPositionForPhase()
        self.o.updateBox()

        return self.hasEnded_v

    def after_animation_listeners(self):
        for a in self.after:
            a()
