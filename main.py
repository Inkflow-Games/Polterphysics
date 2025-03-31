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
from core.physics_engine import PhysicsEngine
from core.collision import resolve_collision
from core.force_calculator import *
from objects.object import Object
from utils.math_utils import *
from utils.vector_utils import *
from core.input_handler import *
from utils.math_utils import WIDTH, HEIGHT, FPS
import core.level_manager as level_manager
import json
from math import atan, degrees




# define the function somewhere else if possible (need the reference to the objects in order to work)
def reset_vectors_applied (vector1_cd, vector2_cd):# must give the Vector2 (=coordinates) of the vectors
    test_object.apply_force(-vector1_cd)
    second_object.apply_force(-vector2_cd)




clicked_object = None
last_clicked = None
vector_applied1 = False
vector_applied2 = False
vector1_coords = Vector2(0,0)
vector2_coords = Vector2(0,0)
vector1_angle = 0 #measures in degrees
vector2_angle = 0

test_position_x_before = 0
test_position_y_before = 0




# Initialize Pygame
pygame.init()
pygame.mixer.init() #to play music
click_sound = pygame.mixer.Sound("data/Music/click.wav")  #import the "click" sound


# Get the size of the screen
display_info = pygame.display.Info()

# Configure the window in full screen
display_width, display_height = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((display_width, display_height-100))
pygame.display.set_caption("Physics Engine Test")


# Initialize physics engine
physics_engine = PhysicsEngine()

# Create a test object (simulating a basketball)
test_object = Object(mass=0.6, position=(400, 100), radius=15, max_speed=700, bounciness=0.8, damping_coefficient=0.02)
physics_engine.add_object(test_object)

# Create a second test object (another basketball)
second_object = Object(mass=2, position=(600, 100), radius=25, max_speed=700, bounciness=0.07, damping_coefficient=0)
physics_engine.add_object(second_object)

# Clock to control frame rate
clock = pygame.time.Clock()
running = True

# Dictionary to track key states for the first object
key_state_1 = {
    pygame.K_RIGHT: False,
    pygame.K_LEFT: False,
    pygame.K_DOWN: False,
    pygame.K_UP: False
}

# Dictionary to track key states for the second object (ZQSD control)
key_state_2 = {
    pygame.K_d: False,
    pygame.K_q: False,
    pygame.K_s: False,
    pygame.K_z: False, 
    pygame.K_SPACE: False,
    pygame.K_a: False
}

# Ground level (just above the bottom of the window)
ground_level = display_height - 120

level_manager.load_scene(0, display_width, display_height)

game_state = "menu"



# Main game loop
while running:

    if game_state != "menu" and not pygame.mixer.music.get_busy() : #play music only ingame
        pygame.mixer.music.load("data/Music/login_test.mp3")  #play music when the game is running
        pygame.mixer.music.play(-1)  #-1 loop the music
    elif game_state == "menu" and pygame.mixer.music.get_busy() :
        pygame.mixer.music.stop() #stop music
        

    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else :
            if GetMouseInput(event):  # Get the click input
                click = True

    # Get key states for the first object (Arrow keys)
    keys = pygame.key.get_pressed()

    # Get key states for the second object (ZQSD keys)
    keys_2 = pygame.key.get_pressed()

    if game_state == "paused" : # only check input when the game is paused

        # Apply force to the first object (Arrow keys)
        if keys[pygame.K_RIGHT] and not key_state_1[pygame.K_RIGHT]:
            test_object.apply_force(Vector2(newton_to_force(30), 0))  # Apply force to the right
            key_state_1[pygame.K_RIGHT] = True

        if keys[pygame.K_LEFT] and not key_state_1[pygame.K_LEFT]:
            test_object.apply_force(Vector2(-newton_to_force(30), 0))  # Apply force to the left
            key_state_1[pygame.K_LEFT] = True

        if keys[pygame.K_DOWN] and not key_state_1[pygame.K_DOWN]:
            test_object.apply_force(Vector2(0, newton_to_force(30)))  # Apply force downward
            key_state_1[pygame.K_DOWN] = True

        if keys[pygame.K_UP] and not key_state_1[pygame.K_UP]:
            test_object.apply_force(Vector2(0, -newton_to_force(30)))  # Apply force upward
            key_state_1[pygame.K_UP] = True


        # Apply force to the second object (ZQSD keys)
        if keys_2[pygame.K_d] and not key_state_2[pygame.K_d]:
            second_object.apply_force(Vector2(newton_to_force(46), 0))
            key_state_2[pygame.K_d] = True

        if keys_2[pygame.K_q] and not key_state_2[pygame.K_q]:
            second_object.apply_force(Vector2(-newton_to_force(46), 0))
            key_state_2[pygame.K_q] = True

        if keys_2[pygame.K_s] and not key_state_2[pygame.K_s]:
            second_object.apply_force(Vector2(0, newton_to_force(46)))
            key_state_2[pygame.K_s] = True

        if keys_2[pygame.K_z] and not key_state_2[pygame.K_z]:
            second_object.apply_force(Vector2(0, -newton_to_force(46)))
            key_state_2[pygame.K_z] = True

    # Check if we pause the game with space
    if keys_2[pygame.K_SPACE] and not key_state_2[pygame.K_SPACE] :
        key_state_2[pygame.K_SPACE] = True
        if game_state == 'paused' :
            game_state = 'running'
            
            
        elif  game_state == 'running': 
            game_state = "paused"
        
    if keys_2[pygame.K_a] and not key_state_2[pygame.K_a] :
        key_state_2[pygame.K_a] = True
        reset_vectors_applied (vector1_coords, vector2_coords)

            


    # Reset key state when key is released
    for key in key_state_1:
        if not keys[key]:
            key_state_1[key] = False

    for key in key_state_2:
        if not keys_2[key]:
            key_state_2[key] = False
            
            
            
    if game_state == "paused":
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = pygame.mouse.get_pos()
            
            # Vérifier sur quel cercle on clique
            if is_point_in_circle(mouse_position, test_object.position, test_object.radius):
                clicked_object = test_object  # if click on the test_object
                if vector_applied1 == True :  # if we didn't apply a vector to test_object yet (in pause mode) 
                    force_vector = -vector1_coords
                    test_object.apply_force(force_vector)
                    vector_applied1 = False
                    vector1_coords = Vector2(0,0)
            elif is_point_in_circle(mouse_position, second_object.position, second_object.radius):
                clicked_object = second_object  # if click on second_object
                if vector_applied2 == True:
                    force_vector = -vector2_coords
                    second_object.apply_force(force_vector)
                    vector_applied2 = False
                    vector2_coords = Vector2(0,0)

        # while left click is pressed, update the mouse position 
        elif event.type == pygame.MOUSEMOTION and clicked_object is not None:
            mouse_position = pygame.mouse.get_pos()
            
        # apply a vector to an object when left click is released
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and clicked_object is not None:
            force_vector = Vector2(mouse_position[0] - clicked_object.position[0], 
                                    mouse_position[1] - clicked_object.position[1])
            clicked_object.apply_force(force_vector)  # apply the computed force to the clicked object
            # need to convert in in Newtons depending on its coordinates, then display it in the vectors information
            print(f"Force applied : {force_vector}") # delete that after complete debug
            
            last_clicked = clicked_object
            # gives update to the vector applied to the clicked object
            if clicked_object == test_object :
                vector_applied1 = True
                vector1_coords = force_vector
                vector1_angle = compute_angle(vector1_coords.x,vector1_coords.y) #computes the angle between axis x and vector, in degrees
            if clicked_object == second_object :
                vector_applied2 = True
                vector2_coords = force_vector
                vector2_angle = compute_angle(vector2_coords.x,vector2_coords.y) #computes the angle between axis x and vector, in degrees
            clicked_object = None
            
            
            #il faut encore récupérer toutes ces informations pour afficher une équation de trajectoire


    if game_state == "running" : # the physics is calculated only during play mode
        vector_applied1 = False #reset the vectors applied to our object
        vector_applied2 = False
        
        test_position_x_before = test_object.position.x
        test_position_y_before = test_object.position.y
        
        
        # Update physics engine based on time delta
        dt = clock.get_time() / 100.0  # Convert milliseconds to a suitable scale
        resolve_collision(test_object,second_object)
        physics_engine.update(dt, ground_level)  # Pass ground_level as display_height - 20 (or whatever your ground level is)




    # Draw frame
    screen.fill((0, 0, 0))  # Clear screen
    if game_state != "menu":
        pygame.draw.circle(screen, (255, 0, 0), (int(test_object.position.x), int(test_object.position.y)), test_object.radius)  # Draw first object
        pygame.draw.circle(screen, (0, 0, 255), (int(second_object.position.x), int(second_object.position.y)), second_object.radius)  # Draw second object

        if clicked_object != None and game_state == "paused" : # Draws a white line between clicked object and mouse position (during vector construction and 'paused')
            pygame.draw.line(screen, (255, 255, 255), clicked_object.position, mouse_position, 5)

    # Draw all buttons in the correct order
    new_scene = level_manager.current_scene #verify if we changed of scene
    running_scene = new_scene
    for button in level_manager.button_list:
        if (pygame.mouse.get_pos()[0] < button.position[0] + button.width/2) and (pygame.mouse.get_pos()[0] > button.position[0] - button.width/2) and (pygame.mouse.get_pos()[1] < button.position[1] + button.height/2) and (pygame.mouse.get_pos()[1] > button.position[1] - button.height/2) :
            button.hover(screen)   
            if click :
                click_sound.play()
                button.is_pressed(display_width, display_height)
                game_state = button.game_state
                new_scene = level_manager.current_scene #verify if we changed of scene
                click = False
                if game_state!= "menu": #we load new objects if the scene changed
    
                    test_object = level_manager.object_list[-1] 
                    physics_engine.add_object(test_object)
                    second_object = level_manager.object_list[-2]
                    physics_engine.add_object(second_object)
        else :
            button.draw(screen)
                    

    # Display debug positions
    font = pygame.font.SysFont("Arial", 24)
    position_text_1 = font.render(f"Position 1: ({int(test_object.position.x)}, {-int(test_object.position.y)})", True, (255, 255, 255))
    position_text_2 = font.render(f"Position 2: ({int(second_object.position.x)}, {-int(second_object.position.y)})", True, (255, 255, 255))
    screen.blit(position_text_1, (10, 10))
    screen.blit(position_text_2, (10, 40))
    
    
    if vector_applied1 == True and vector1_coords!= Vector2(0,0):
        vector_1 = font.render(f"Vector on test_object: ({int(vector1_coords.x)}, {int(vector1_coords.y)}), angle : {round(vector1_angle,2)}", True, (255, 255, 255))
        screen.blit(vector_1, (10, 70))
        
        
        """
        (test) Simulation of the trajectory for test_object
        """
        
        
        """based on acceleration"""
        v0 = Vector2((test_object.position.x - test_position_x_before)/dt , (test_object.position.y - test_position_y_before)/dt) #in PIXELS / dt²
        acceleration = vector1_coords / test_object.mass #is a Vector2 --> pixels / kg --> coordinates of ax and ay
        predicted_velocity = v0 + acceleration
        print(f"v0 = {v0}")
        print(f"acceleration = {acceleration}")
        print(f"predicted_velocity = {predicted_velocity}")
        
        
        predicted_positions = []
        simulated_position = test_object.position.copy()  # Copie pour éviter les références
        simulated_velocity = predicted_velocity.copy()  # Copie pour éviter les références

        dt_sim = 0.1  # Pas de temps pour la simulation

        for _ in range(50):  # Simuler sur 50 frames (~5s)
            simulated_velocity.y += newton_to_force(9.81) * dt  # Ajouter la gravité à chaque nouvelle frame
            simulated_position.x += newton_to_force(simulated_velocity.x) * dt  # Mettre à jour la position X
            simulated_position.y += newton_to_force(simulated_velocity.y) * dt  # Mettre à jour la position Y

            predicted_positions.append(simulated_position.copy())  # Sauvegarder une COPIE

        # Dessiner la trajectoire en jaune
        for point in predicted_positions:
            pygame.draw.circle(screen, (255, 255, 0), (int(point.x), int(point.y)), 3)  # Petit point jaune


        
        """
        Last time test : based on vectorial sum
        
        
        
        norm, angle = norm_and_angle_computation(test_position_x_before , test_position_y_before, test_object.position.x , test_object.position.y, vector1_coords, dt)
        print(f" x = t*{norm}*{cos(radians(angle)) + vector1_coords[0]} + {test_object.position.x}")
        print(f" y = {0.5*9.81}*t² + t*{norm}*{sin(radians(angle)) + vector1_coords[1]} + {test_object.position.y}")
        
        print(f"norm = {norm} pixels")
        print(f"angle = {angle} degrees")
        print(f"last x : {position_x_before}")
        print(f"last y : {test_position_y_before}")
        
        for i in range (0,100,5) :
            pygame.draw.circle(screen, (255, 255, 0), (int((dt*i) *(norm*cos(radians(angle)) + vector1_coords[0]) + test_object.position.x), 
                                                        int(0.5*9.81*(dt*i)**2 + (dt*i)*(norm*sin(radians(angle)) + vector1_coords[1]) + test_object.position.y)), 
                                                        test_object.radius)
        """
    
    
    
    if vector_applied2 == True and vector2_coords!= Vector2(0,0): 
        vector_2 = font.render(f"Vector on second_object: ({int(vector2_coords.x)}, {int(vector2_coords.y)}), angle : {round(vector2_angle,2)}", True, (255, 255, 255))
        screen.blit(vector_2, (10, 90))

    pygame.display.flip()  # Refresh screen
    clock.tick(120)  # Limit FPS to 120



# Quit Pygame
pygame.quit()
