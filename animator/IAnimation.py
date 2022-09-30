

class IAnimation():
    def __init__(self):
        None
    def setInitialTime(self,init_t):
        self.init_t = init_t

    def animate(self, now):
        None

    def hasEnded(self, now):
        return False
    
    def after_animation_listeners(self):
        None
