
from animator.IAnimation import IAnimation

class CameraAnimation(IAnimation):

    def __init__(self, t0, duration, camera_name, camera_manager, after=[]):
        self.t0 = t0
        self.duration = duration
        self.camera_name = camera_name
        self.camera_manager = camera_manager
        self.hasEnded_v=False
        self.after = after
        self.cam0 = self.camera_manager.camera_matrix._m.copy()
        self.cam1 = self.camera_manager.getCameraByName(camera_name)

    def animate(self, now):
        delta_t = (now-self.t0)/self.duration
        _m = self.camera_manager.camera_matrix._m
        for i in range(16):
            _m[i] = self.cam0[i] + (self.cam1[i]-self.cam0[i])*delta_t
        
    def hasEnded(self, now):
        if self.hasEnded_v:
            return True
        self.hasEnded_v = self.t0 + self.duration < now
        return self.hasEnded_v

    def after_animation_listeners(self):
        for a in self.after:
            a()
