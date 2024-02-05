from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

"""
-GRID SIMULATION-
Originally written by L.Kaminski

A program simulating 'Grid,' a 3-dimensional digital space designed to create structures. it's based heavily off
'The Grid' from Tron.

HOW IT WORKS, STEP BY STEP
----------
1. Upon boot, three things are created; the Player, the Grid, and BASIS, the first true structure.
2. BASIS is the base structure for all the structures that come after it. it's a blank cube, that's placed
underneath the world and used as a duplicatable entity.
3. The Grid, every frame, is locked into a static enabled state, position, size, and rotation. You cannot modify or delete The Grid.
4. The player is given two abilities: The ability to move, and omnipotency. (I'm serious.)
The player's detailed abilities are as follows:
-Free range of movement, albiet with gravity
-The ability to create and transform 'structures,' which i'll explain in a minute
-The ability to delete structures.
5. 'Structures' are 3D objects that the player creates from the matter of the grid. The options are:
-Cube
-Torus
-Spike/Diamond
-Torus
6. Grid is a live program. Once you leave, everything you create is erased permanently, and you cannot retrieve it.
"""

app = Ursina()#define app

player = FirstPersonController()#init player

#preworked settings/preloaded assets
grid = Entity(model='plane', texture='resource_grid', collider='mesh', scale=10000, texture_scale=(10000,10000))
basis = Entity(model='cube', texture='resource_structure', collider='mesh', scale=2, y=-2)
sky = Sky()
sky.texture = 'resource_skybox'
player.cursor.color=color.cyan
player.y = 10
camera.clip_plane_far = 1000
window.fps_counter.enabled = False
window.entity_counter.enabled = False
window.collider_counter.enabled = False
window.exit_button.visible = False

#variable pool
buildingnum = 0
rising = False
heightmodlevel = 5
scalemodlevel = 1
modelnum = 1
selectedmodel = 'cube'
animationtime = 1
defaultheight = 0.2
incrementer = 1

#audio pool
creator = Audio(sound_file_name='create.wav', autoplay=False, volume=0.3)
destroyer = Audio(sound_file_name='destroy.wav', autoplay=False, volume=0.3)
modifier = Audio(sound_file_name='modify.wav', autoplay=False, volume=0.3)
up = Audio(sound_file_name='up.wav', autoplay=False, volume=0.3)
down = Audio(sound_file_name='down.mp3', autoplay=False, volume=0.3)
nudge = Audio(sound_file_name='nudge.wav', autoplay=False, volume=0.3)
ambience = Audio(sound_file_name='cyber.mp3', autoplay=False, loop=True, volume=0.6)
ambience.play()

window.fullscreen=True

def update():
    global modelnum
    global selectedmodel
    global grid
    global defaultheight
    global incrementer
    grid.scale = 10000
    grid.enable()
    grid.position = (0, 0, 0)

#sprinting
    if held_keys['shift']:
        player.speed = 14
    if not held_keys['shift']:
        player.speed = 7

#increment modifier
    if held_keys['control']:
        incrementer = 10
    if not held_keys['control']:
        incrementer = 1

#structure creation functions
def make_structure():
    try:
        basis2 = duplicate(basis, model='cube', x=mouse.world_point.x, z=mouse.world_point.z, y=defaultheight, rotation=(0,0,0), scale_y=0)
        basis2.animate_scale_y(10, duration=animationtime, curve=curve.linear, loop=False)
        creator.play()
    except AttributeError:
        pass

def make_spike_structure():
    try:
        basis2 = duplicate(basis, model='diamond', collider='mesh', x=mouse.world_point.x, z=mouse.world_point.z, y=defaultheight, rotation=(0,0,0), scale_y=0)
        basis2.animate_scale_y(10, duration=animationtime, curve=curve.linear, loop=False)
        creator.play()
    except AttributeError:
        pass

def make_cylinder_structure():
    try:
        basis2 = duplicate(basis, model='cylinder.obj', texture='resource_cylinder', collider='mesh', x=mouse.world_point.x, z=mouse.world_point.z, y=defaultheight, rotation=(0,0,0), scale_y=0)
        basis2.animate_scale_y(10, duration=animationtime, curve=curve.linear, loop=False)
        creator.play()
    except AttributeError:
        pass

def make_torus_structure():
    basis2 = duplicate(basis, model='torus', collider='mesh', x=mouse.world_point.x, z=mouse.world_point.z, y=defaultheight, rotation=(0,0,0), scale_y=0)
    basis2.animate_scale_y(10, duration=animationtime, curve=curve.linear, loop=False)
    creator.play()

def make_building_structure():
    #goes unused
    basis2 = duplicate(basis, model='building', collider='mesh', x=mouse.world_point.x, z=mouse.world_point.z, y=defaultheight, rotation=(0,0,0), scale_y=0)
    basis2.animate_scale_y(10, duration=animationtime, curve=curve.linear, loop=False)
    creator.play()

#modifier/increment funcs
def mod_print_up():
    global heightmodlevel
    global incrementer
    heightmodlevel += incrementer
    up.play()
    indicator = Text(text=str(heightmodlevel), color=color.cyan)
    print(heightmodlevel)
    ass = Sequence(Wait(0.2), Func(indicator.disable), started=True)

def mod_print_down():
    global heightmodlevel
    global incrementer
    heightmodlevel -= incrementer
    down.play()
    indicator = Text(text=str(heightmodlevel), color=color.cyan)
    print(heightmodlevel)
    ass = Sequence(Wait(0.2), Func(indicator.disable), started=True)

def mod_scale_print_up():
    global scalemodlevel
    global incrementer
    scalemodlevel += incrementer
    up.play()
    indicator = Text(text=str(scalemodlevel), color=color.orange)
    print(scalemodlevel)
    ass = Sequence(Wait(0.2), Func(indicator.disable), started=True)

def mod_scale_print_down():
    global scalemodlevel
    global incrementer
    scalemodlevel -= incrementer
    down.play()
    indicator = Text(text=str(scalemodlevel), color=color.orange)
    print(scalemodlevel)
    ass = Sequence(Wait(0.2), Func(indicator.disable), started=True)

def modify_structure():
    global heightmodlevel
    try:
        mouse.hovered_entity.animate_scale_y(heightmodlevel, duration=animationtime, curve=curve.linear)
        modifier.play()
    except AttributeError:
        pass

def modify_structure_scale():
    global scalemodlevel
    try:
        mouse.hovered_entity.animate_scale(scalemodlevel, duration=animationtime, curve=curve.linear)
        modifier.play()
    except AttributeError:
        pass

#text string that controls the tooltips
controls = """
WASD - Move
Shift - Sprint
0 - Quit
1-4 - Create Structures
R - Mod Structure Height
U/I - Adjust Structure Width (X Axis, based on scale modifier)
T - Mod Structure Scale
Arrow Keys + (-/=/m) - Move/Rotate Structure Axis (based on height modifier)
V - Erase Structure
, / . - Height Mod Adjust Up/Down (Hold CTRL to +10)
[ / ] - Scale Mod Adjust Up/Down (Hold CTRL to +10)
"""

tooltips = Text(text=controls, origin=(-.5,.5), color=color.cyan, size=.010, x=-0.87, y=0.52)

#eraser func
def erase_structure():
    try:
        mouse.hovered_entity.disable()
        destroyer.play()
    except AttributeError:
        pass

#input handler
def input(key):
    if key == '0':
        quit()
    if key == '1':
        make_structure()
    if key == '2':
        make_spike_structure()
    if key == '3':
        make_cylinder_structure()
    if key == '4':
        make_torus_structure()
    if key == 'escape':
        if mouse.locked == True:
            mouse.locked = False
        elif mouse.locked == False:
            mouse.locked = True
    if key == 'r':
        modify_structure()
    if key == 'up arrow':
        try:
            mouse.hovered_entity.x += heightmodlevel
            nudge.play()
        except AttributeError:
            pass
    if key == 'down arrow':
        try:
            mouse.hovered_entity.x -= heightmodlevel
            nudge.play()
        except AttributeError:
            pass
    if key == 'left arrow':
        try:
            mouse.hovered_entity.z += heightmodlevel
            nudge.play()
        except AttributeError:
            pass
    if key == 'right arrow':
        try:
            mouse.hovered_entity.z -= heightmodlevel
            nudge.play()
        except AttributeError:
            pass
    if key == '=':
        try:
            mouse.hovered_entity.y += heightmodlevel
            nudge.play()
        except AttributeError:
            pass
    if key == 'm':
        try:
            mouse.hovered_entity.rotation_y += heightmodlevel
            nudge.play()
        except AttributeError:
            pass
    if key == '-':
        try:
            mouse.hovered_entity.y -= heightmodlevel
            nudge.play()
        except AttributeError:
            pass
    if key == 'u':
        try:
            mouse.hovered_entity.scale_x -= scalemodlevel
            nudge.play()
        except AttributeError:
            pass
    if key == 'i':
        try:
            mouse.hovered_entity.scale_x += scalemodlevel
            nudge.play()
        except AttributeError:
            pass
    if key == 't':
        modify_structure_scale()
    if key == '.':
        mod_print_up()
    if key == ',':
        mod_print_down()
    if key == ']':
        mod_scale_print_up()
    if key == '[':
        mod_scale_print_down()
    if key == 'v':
        erase_structure()

app.run()#init app