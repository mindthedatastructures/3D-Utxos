
from animator.animations.movement_animation import MovementAnimation
from animator.animations.validation_animation import ValidationAnimation
from animator.animations.load_block_animation import LoadBlockAnimation
from animator.animations.wait_animation import WaitAnimation
from animator.animations.camera_animation import CameraAnimation

import time

class Animator():

    def __init__(self, configs, camera_manager):
        self.animations = []
        self.configs = configs
        self.camera_manager = camera_manager
        self.debug = 0

    def loadAnimation(self, o, duration, pos0, pos1, after=[]):
        a = MovementAnimation(o, time.time(), duration, pos0, pos1, after)
        self.animations.append(a)

    def startValidationAnimation(self, validator_edit_part, link_holder_ep, duration, after=[]):
        a = ValidationAnimation(validator_edit_part, link_holder_ep, time.time(), duration, after)
        self.animations.append(a)

    def startBlockToBlockchainAnimation(self, scene_edit_part, after=[]):
        a = LoadBlockAnimation(self, time.time(), self.configs, scene_edit_part, after)
        self.animations.append(a)

    def loadWaitAnimation(self, duration, after=[]):
        a = WaitAnimation(time.time(), duration, after)
        self.animations.append(a)

    def startCameraAnimation(self, duration, camera_name, after=[]):
        a = CameraAnimation(time.time(), duration, camera_name, self.camera_manager, after)
        self.animations.append(a)


    def addAnimation(self, now,animation):
        animation.setStartingTime(now)
        self.animations.append(animation)

    def animate(self):
        now = time.time()
        toRemove = []
        for a in self.animations:
            if a.hasEnded(now):
                a.after_animation_listeners()
                toRemove.append(a)
                continue
            a.animate(now)
        for a in toRemove:
            self.debug += 1
            self.animations.remove(a)


