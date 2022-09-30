
import json
import time

class CameraManager():
    def __init__(self, camera_matrix):
        self.camera_matrix = camera_matrix
        self.lastTime = -1
        self.animator = None
        self.names = []
        self.current_camera_name = ''
        self.current_camera_index = ''
        self.lock = False
        with open('camera.json','r') as f:
            self.camera_configs = json.loads(f.read())
        for c in self.camera_configs['cameras']:
            self.names.append(c['name'])

    def setAnimator(self, animator):
        self.animator = animator

    def loadInit(self):
        self.camera_matrix._m = self.camera_configs['cameras'][0]['val']
        self.current_camera_name = self.camera_configs['cameras'][0]['name']
        self.current_camera_index = 0

    def getCameraByName(self,name):
        for c in self.camera_configs['cameras']:
            if c['name'] == name:
                return c['val']
        return None
        return self.camera_configs['cameras'][name]['val']


    def m_key_pressed(self):
        if self.lock:
            return
        if time.time() - self.lastTime <1:
            return
        self.current_camera_index = (self.current_camera_index+1) % len(self.names)
        self.current_camera_name = self.names[self.current_camera_index]
        print(f"Loading Camera: {self.current_camera_name}")
        self.lock = True
        self.animator.startCameraAnimation(2, self.current_camera_name, after=[lambda:self.unlock()])

    def unlock(self):
        self.lock=False


    def l_key_pressed(self):
        if time.time() - self.lastTime <1:
            return
        self.lastTime = time.time()
        i = len(self.camera_configs['cameras'])
        val = self.camera_matrix._m
        name = f"Camera#{i}"

        with open('camera.json','r') as f:
            self.camera_configs = json.loads(f.read())

        print(f"Storing Camera {name}")
        self.camera_configs['cameras'].append({'name':name,'val':val})
        with open('camera.json','w') as f:
            f.write(json.dumps(self.camera_configs, indent = 4))




