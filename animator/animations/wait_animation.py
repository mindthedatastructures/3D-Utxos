
from animator.IAnimation import IAnimation

class WaitAnimation(IAnimation):

    def __init__(self, t0, duration, after=[]):
        self.t0 = t0
        self.duration = duration
        self.hasEnded_v=False
        self.after = after

    def animate(self, now):
        None
        
        
    def hasEnded(self, now):
        if self.hasEnded_v:
            return True
        self.hasEnded_v = self.t0 + self.duration < now
        return self.hasEnded_v

    def after_animation_listeners(self):
        for a in self.after:
            a()
