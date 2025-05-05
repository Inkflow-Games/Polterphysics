"""
Polterphysics
main.py

A script that demonstrates the functionality of the game's physics engine
Features include:
- Object movement with applied forces
- Collision detection with the ground
- Debugging display of object position
- Two controllable objects (balls) to collide with each other

Last Updated: Feb 2025
Python Version: 3.12.9
Dependencies: pygame, core.physics_engine, objects.object
"""

import pygame
from pygame.math import Vector2
import pygame.transform
from core.physics_engine import PhysicsEngine
from core.collision import *
from core.force_calculator import *
from objects.object import *
from utils.math_utils import *
from utils.vector_utils import *
from core.input_handler import *
from objects.mincircle import welzl
from objects.Quadtree import RectangleQ,Quadtree
import core.level_manager as level_manager
import json
from core.sound import *
from random import randint

# Initialize Pygame
pygame.init()
pygame.mixer.init() #to play music


# Initialize physics engine
physics_engine = PhysicsEngine()

# Clock to control frame rate
clock = pygame.time.Clock()
running = True

clicked_object = None # Will stock the object that will receive the vector from the user
vectors_applied = False # Defines if all the vectors created by the user have been applied



# Initialize Pygame
pygame.init()
pygame.mixer.init() #to play music


# Get the size of the screen
display_info = pygame.display.Info()

# Configure the window in full screen
display_width, display_height = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((display_width, display_height-10))
pygame.display.set_caption("Physics Engine Test")
pictureBackground = pygame.image.load("data/background/back1.png")
pictureBackground = pygame.transform.scale(pictureBackground, (display_width, display_height))
pictureOption = pygame.image.load("data/background/back1-tuto.png")
pictureOption = pygame.transform.scale(pictureOption, (display_width, display_height))


# Initialize physics engine
physics_engine = PhysicsEngine()
bounding_box = RectangleQ(-1000,-1000,3400,2200)
quadtree = Quadtree(bounding_box,7)
# Clock to control frame rate
clock = pygame.time.Clock()
running = True

# Dictionary to track key states : ONLY "SPACE" to pause the game
key_state = {
    pygame.K_SPACE: False,
}

# Ground level (just above the bottom of the window) --> Pass ground_level as display_height - 20 (or whatever your ground level is)
ground_level = display_height - 20

level_manager.load_scene(0, display_width, display_height,physics_engine)

game_state = "menu"


# Main game loop
while running:

    new_scene = level_manager.current_scene #verify if we changed of scene
    running_scene = new_scene
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else :
            if GetMouseInput(event):  # Get the click input
                click = True

    # Get key states for the first object (Arrow keys)
    keys = pygame.key.get_pressed()

    # Check if we pause the game with space
    if keys[pygame.K_SPACE] and not key_state[pygame.K_SPACE] :
        key_state[pygame.K_SPACE] = True
        if game_state == 'paused' :
            game_state = 'running'
        elif  game_state == 'running': 
            game_state = "paused"


    # Reset key state when key is released
    for key in key_state:
        if not keys[key]:
            key_state[key] = False

    if game_state == "paused":
        
        vectors_applied = False # Allows for the application of the vectors at the moment game_state = "running"
        
        # Main mechanic : application of the vectors by the user
        clicked_object = vector_application(event, physics_engine.objects, clicked_object, quadtree)


    if game_state == "running" : # Define the state when the physics engine is active
        dt = clock.get_time() / 100.0  # Convert milliseconds to a suitable scale'
        
        # to change : Need comments from Clement
        for elements in physics_engine.objects:
            quadtree.insert(elements)        
        interactions = quadtree.searchelements(physics_engine.objects)
        
        
        # Apply all the vectors entered by the user during transition from "paused" state to "running" state --> prevent vector stacking 
        if vectors_applied == False :
            for obj in physics_engine.objects :
                if (obj.applied_coords != [0,0]) and (obj.grabable == True) :
                    obj.shape.velocity += (Vector2(obj.applied_coords) /  obj.shape.mass) # Instant increase of the speed of the object   
            vectors_applied = True
        
        
        # Reset the vectors info and mouse position for all the objects loaded in the physics engine
        reset_level_vectors(physics_engine.objects) 
        for elements in physics_engine.objects :
            update_mouse(elements, Vector2(0,0))


        # to change : Need comments from Clement
        for interaction in interactions:
            if len(interaction) >= 2:
                for elms in interaction[1:]:
                    gjk = GJK2D(interaction[0],elms)
                    trig = gjk.detection()
                    stuff = gjk.EPA(trig)
                    if trig is not None:
                        gjk.find_contact_features(gjk.shape1,gjk.shape2,stuff)
                        gjk.resolve(stuff,dt)

        physics_engine.update(dt)  


    # Draw frame (display of the game)
    screen.fill((170, 170, 170))  # Clear screen
    if game_state == "menu" :
        screen.blit(pictureBackground, (0,0))
    if game_state == "options" : 
        screen.blit(pictureOption, (0,0))

    if game_state != "menu" and game_state != "options":
        screen.blit(level_manager.background, (360,0))
        for elements in physics_engine.objects:
            if (elements.name != "RightPanel" and elements.name != "LeftPanel") :
                elements.shape.draw(screen,(255,0,0)) # Draws the shape of the objects in red
        
        # to delete (?)
        # for elements in physics_engine.objects:
        #     if (elements.name != "RightPanel" and elements.name != "LeftPanel") :
        #         pygame.draw.circle(screen,(50,50,50),Vector2(elements.mincircle.x,elements.mincircle.y),elements.mincircle.radius,2) # Draws the outline of these objects  
        screen.blit(level_manager.text_list[0], (0.03 * display_width, 0.15 * display_height))
        screen.blit(level_manager.text_list[1], (0.03 * display_width, 0.25 * display_height))

        # Draws the vectors applied by the user, and display (at the moment) 20 positions at intervals of 0.1s :
        # change "False" in lines_and_positions by "True" in order to give the realistic equations for the movements of the objects
        if game_state == "paused" : 
            for obj in physics_engine.objects :
                lines_and_positions(physics_engine.objects,screen, game_state, False)


    # Draw all buttons in the correct order depending on the current scene, it loads the button as well
    new_scene = level_manager.current_scene 
    running_scene = new_scene
    for button in level_manager.button_list:
        if (pygame.mouse.get_pos()[0] < button.position[0] + button.width/2) and (pygame.mouse.get_pos()[0] > button.position[0] - button.width/2) and (pygame.mouse.get_pos()[1] < button.position[1] + button.height/2) and (pygame.mouse.get_pos()[1] > button.position[1] - button.height/2) :
            button.hover(screen)   
            if click :

                secret_sound = randint(0,50)
                if secret_sound == 30 :
                    play_sound_fx("data/Music/pwomp.wav")
                else :
                    play_sound_fx("data/Music/click.wav")
                button.is_pressed(display_width, display_height,physics_engine)
                game_state = button.game_state
                new_scene = level_manager.current_scene #verify if we changed of scene
                click = False
        elif button.image[14:] == "data\\Phantoms" :
            for elem in range (len(physics_engine.objects)) :
                if (physics_engine.objects[elem].name == button.action) and physics_engine.objects[elem].applied_coords != [0,0]:
                    button.hover(screen)

        else :
            button.draw(screen)

    pygame.display.flip()  # Refresh screen
    clock.tick(120)  # Limit FPS to 60

# Quit Pygame
pygame.quit()