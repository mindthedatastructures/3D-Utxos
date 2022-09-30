SCREEN_SIZE = (1980, 1080)

from math import radians 

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

from gameobjects.matrix44 import *
from gameobjects.vector3 import *

from commands.commands import CommandManager
from commands.command_receiver import CommandReceiver

from http_request_model_info.http_request_model_info_server import HttpRequestModelInfoServer

from camera_manager.camera_manager import CameraManager
from views.old.color_palette import ColorPalette
from graphic_primitives.axis import Axis
from graphic_primitives.floor import Floor
from graphic_primitives.box import Cube
from graphic_primitives.box import Box
from graphic_primitives.sphere import Sphere

from graphic_primitives.number_view import NumberView
from graphic_primitives.letter_view import LetterView

from views.old.color_palette import ColorPalette
from views.old.living_board_view import LivingBoardView
from views.old.transaction_view import Transaction
from views.old.block_view import Block
from views.old.utxo_view import Utxo
import model.models as models
import edit_parts.edit_parts as editparts
from views.view_manager import ViewManager
from animator.animator import Animator

from PIL import Image

import time
import signal

import os, json



###### Handling Close
to_close_list = []
running=True

def handler_exit(signum, frame):
    global running
    running = False
    for t in to_close_list:
        t.close()
    pygame.quit()
    exit(0)

signal.signal(signal.SIGINT, handler_exit) # This is to close the log file when the tests fail
######


def resize(width, height):
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width)/height, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    
    glEnable(GL_DEPTH_TEST)
    
    glShadeModel(GL_FLAT)
    glClearColor(1.0, 1.0, 1.0, 0.0)

    glEnable(GL_COLOR_MATERIAL)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)        
    glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))    
    glLightfv(GL_LIGHT0, GL_AMBIENT,  (0, 1.5, 1, 0))

    

def run():
    with open('config.json', 'r') as f:
        configs = json.loads(f.read())

    camera_matrix = Matrix44()
    camera_manager = CameraManager(camera_matrix)
    animator = Animator(configs, camera_manager)
    camera_manager.setAnimator(animator)


    scene_model = models.Scene.generate(configs)
    view_manager = ViewManager()
    view_manager.initBoardViewObjects()
    view_manager.other_objects.append(Axis())

    for i in range(10):
        a = NumberView(7+i*1.1,23,3,1)
        a.setNumber(i)
        view_manager.other_objects.append(a)
    a = NumberView(7+10*1.1,23,3,1)
    a.setNumber('-')
    view_manager.other_objects.append(a)

    i=0
    for l in 'abcdefghijklmnopqrstuvwxyz':
        a=LetterView(7+i,20,3,1)
        view_manager.other_objects.append(a)
        a.setLetter(l)
        i+=1






    # view_manager.other_objects.append(SegmentView(7.1,7.1,3,1, False))
    # view_manager.other_objects.append(ColorPalette())
    view_manager.other_objects.append(Floor())
    scene_edit_part = editparts.SceneEditPart.generate(scene_model, view_manager, animator, configs)
    scene_edit_part.initObjectViews()

    command_manager = CommandManager(scene_edit_part)
    commands_receiver = CommandReceiver(command_manager)
    to_close_list.append(commands_receiver)

        
    center=(0,0,4)
    radius=1.0
    ratev=80
    rateh = 20

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, OPENGL|DOUBLEBUF)

    resize(*SCREEN_SIZE)
    init()
    
    clock = pygame.time.Clock()    
    
    # glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))    
    # glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))


    # Camera transform matrix
    camera_matrix.translate = (10.0, .6, 10.0)



    http_server = HttpRequestModelInfoServer(scene_model, animator, camera_matrix, configs)
    to_close_list.append(http_server)

    # Initialize speeds and directions
    rotation_direction = Vector3()
    rotation_speed = radians(90.0)
    movement_direction = Vector3()
    movement_speed = 5.0    

## Init Matrix
    camera_matrix.set(
        [ 0.997366,  -0.032816, 0.064688,  0 ],
        [ 0.024892,  0.992497,  0.119705,  0 ],
        [ -0.068131, -0.11778,  0.9907,    0 ],
        [ 7.538773,  1.296523,  14.00039,  1 ]
        )


    camera_manager.loadInit()

    glLoadMatrixd(camera_matrix.get_inverse().to_opengl())
    previous_r = 0

    mouse_pressed = False
    mouse_pressed_position = None
    while running:
        rotation_direction.set(0.0, 0.0, 0.0)
        movement_direction.set(0.0, 0.0, 0.0)
        for event in pygame.event.get():
            if event.type == QUIT:
                handler_exit
            if event.type == KEYUP and event.key == K_ESCAPE:
                return
            if event.type == MOUSEWHEEL:
                movement_direction.z = - 5*float(event.y)
            if event.type == MOUSEMOTION:
                if mouse_pressed == True:
                    rotation_direction.y = 0.2*float(mouse_pressed_position[0]-event.pos[0])
                    rotation_direction.x = 0.2*float(mouse_pressed_position[1]-event.pos[1])
                    mouse_pressed_position = event.pos
            if event.type == MOUSEBUTTONUP:
                mouse_pressed = False
            if event.type == MOUSEBUTTONDOWN:
                mouse_pressed = True
                mouse_pressed_position = event.pos

        # Clear the screen, and z-buffer
        glClearColor(0,0,0,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
                        
        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.
        
        pressed = pygame.key.get_pressed()

        if pressed[K_ESCAPE]:
            handler_exit(None, None)

        
        # Reset rotation and movement directions
        

        # if pressed[K_r]:
        #     now = time.time()
        #     if  now - previous_r > 0.5:
        #         previous_r = time.time()
        #         tx1.alterColorsOfUtxos()
        if pressed[K_t]:
            scene_model.print()

        # Modify direction vectors for key presses
        if pressed[K_LEFT]:
            rotation_direction.y = +1.0
        elif pressed[K_RIGHT]:
            rotation_direction.y = -1.0
        if pressed[K_UP]:
            rotation_direction.x = +1.0
        elif pressed[K_DOWN]:
            rotation_direction.x = -1.0
        if pressed[K_z]:
            rotation_direction.z = -1.0
        elif pressed[K_x]:
            rotation_direction.z = +1.0            
        if pressed[K_w]:
            movement_direction.z = -1.0
        elif pressed[K_s]:
            movement_direction.z = +1.0
        if pressed[K_a]:
            movement_direction.x = -1.0
        elif pressed[K_d]:
            movement_direction.x = +1.0
        if pressed[K_SPACE]:
            if pressed[K_LSHIFT] or pressed[K_RSHIFT]:
                movement_direction.y = -1.0
            else:
                movement_direction.y = +1.0
        if pressed[K_p]:
            print(camera_matrix)

        
        # Calculate rotation matrix and multiply by camera matrix    
        rotation = rotation_direction * rotation_speed * time_passed_seconds
        rotation_matrix = Matrix44.xyz_rotation(*rotation)        
        camera_matrix *= rotation_matrix
        
        # Calcluate movment and add it to camera matrix translate
        heading = Vector3(camera_matrix.forward)
        movement = heading * movement_direction.z * movement_speed
        movement = movement + Vector3(camera_matrix.right) * movement_direction.x * movement_speed
        movement = movement + Vector3(camera_matrix.up) * movement_direction.y * movement_speed
        camera_matrix.translate += movement * time_passed_seconds
        
        if pressed[K_l]:
            camera_manager.l_key_pressed()

        if pressed[K_m]:
            camera_manager.m_key_pressed()

        # Upload the inverse camera matrix to OpenGL
                
        # Light must be transformed as well
        glLight(GL_LIGHT0, GL_POSITION,  (0, 1.5, 1, 0)) 
                
        # Render the map
        animator.animate()
        glLoadMatrixd(camera_matrix.get_inverse().to_opengl())
        view_manager.render_all()

        # Show the screen
        pygame.display.flip()

def main(args):
    run()

if __name__ == '__main__':
    main([])