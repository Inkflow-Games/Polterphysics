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
from core.collision import *
from core.force_calculator import *
from objects.object import *
from utils.math_utils import *
from utils.vector_utils import *
from core.input_handler import *
from objects.Quadtree import RectangleQ,Quadtree
import core.level_manager as level_manager
import json


"""Must integrate it elsewhere in the program after debug"""
#possibility to stack the minus vectors if called multiple times
def reset_vectors_applied (vector1_cd, vector2_cd):# must give the Vector2 (=coordinates) of the vectors
    if vector1_cd != Vector2(0,0) :
        c.apply_force(-vector1_cd)
        vector1_coords = Vector2(0,0)
        c = Vector2(0,0)
    if vector1_cd != Vector2(0,0) :
        c.apply_force(-vector2_cd)
        vector2_coords = Vector2(0,0)




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
second_position_x_before = 0
second_position_y_before = 0




# Initialize Pygame
pygame.init()
pygame.mixer.init() #to play music


# Get the size of the screen
display_info = pygame.display.Info()

# Configure the window in full screen
display_width, display_height = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((display_width, display_height-50))
pygame.display.set_caption("Physics Engine Test")


# Initialize physics engine
physics_engine = PhysicsEngine()
bounding_box = RectangleQ(0,0,display_width,display_height)
quadtree = Quadtree(bounding_box,4)

# # Create a test object (simulating a basketball)
# #test_object = Object("OBject1",False, False, mass=1, restitution_coefficient=0.8, vertices=None, radius=30, centroid=(400, 100))
#c = Object(polygon=True,static= False, mass=400000000, restitution_coefficient=0.8, vertices=[Vector2(0 ,800),Vector2(1300, 800),Vector2(1300, 900),Vector2(0, 900)],name="OBjectc")
#physics_engine.add_object(c)

# # Create a second test object (another basketball)
#second_object = Object("OBject2",False, False, mass=2, restitution_coefficient=0.8, vertices=None, radius=30, centroid=(600, 100))
#g = Object(polygon=False, static=False, mass=50, restitution_coefficient=0.8,vertices= None,radius= 30,centroid= Vector2(100,100),name="OBjectg")
#physics_engine.add_object(g)

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
ground_level = display_height - 20

level_manager.load_scene(0, display_width, display_height,physics_engine)

game_state = "menu"



# Main game loop
while running:


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

    '''
    if game_state != "menu" : # only check input when the game is paused
        # Apply force to the first object (Arrow keys)
        if keys[pygame.K_RIGHT] and not key_state_1[pygame.K_RIGHT]:
            c.shape.apply_force(Vector2(newton_to_force(30), 0))  # Apply force to the right
            key_state_1[pygame.K_RIGHT] = True

        if keys[pygame.K_LEFT] and not key_state_1[pygame.K_LEFT]:
            c.shape.apply_force(Vector2(-newton_to_force(30), 0))  # Apply force to the left
            key_state_1[pygame.K_LEFT] = True

        if keys[pygame.K_DOWN] and not key_state_1[pygame.K_DOWN]:
            c.shape.apply_force(Vector2(0, newton_to_force(30)))  # Apply force downward
            key_state_1[pygame.K_DOWN] = True

        if keys[pygame.K_UP] and not key_state_1[pygame.K_UP]:
            c.shape.apply_force(Vector2(0, -newton_to_force(30)))  # Apply force upward
            key_state_1[pygame.K_UP] = True


        # Apply force to the second object (ZQSD keys)
        if keys_2[pygame.K_d] and not key_state_2[pygame.K_d]:
            g.shape.apply_force(Vector2(newton_to_force(46), 0))
            key_state_2[pygame.K_d] = True

        if keys_2[pygame.K_q] and not key_state_2[pygame.K_q]:
            g.shape.apply_force(Vector2(-newton_to_force(46), 0))
            key_state_2[pygame.K_q] = True

        if keys_2[pygame.K_s] and not key_state_2[pygame.K_s]:
            g.shape.apply_force(Vector2(0, newton_to_force(46)))
            key_state_2[pygame.K_s] = True

        if keys_2[pygame.K_z] and not key_state_2[pygame.K_z]:
            g.shape.apply_force(Vector2(0, -newton_to_force(46)))
            key_state_2[pygame.K_z] = True
    '''
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
        #call the function that handles the vector application process
        '''
        clicked_object, vector_applied1, vector_applied2, vector1_coords, vector2_coords, vector1_angle, vector2_angle, mouse_position = vector_application(
    event,
    test_object, second_object,
    clicked_object, vector_applied1, vector_applied2,
    vector1_coords, vector2_coords,
    vector1_angle, vector2_angle)
    '''



    if game_state == "running" : # the physics is calculated only during play mode
        #update vectors state and last position of the objects
        #vector_applied1, vector_applied2, test_position_x_before, test_position_y_before, second_position_x_before, second_position_y_before = objects_running_info(test_object, second_object, vector_applied1, vector_applied2)
        # Update physics engine based on time delta
        dt = clock.get_time() / 100.0  # Convert milliseconds to a suitable scale'
        physics_engine.objects[1].shape.velocity += (Vector2(0,9.8) * dt)
        for element in physics_engine.objects:
            quadtree.insert(element)
        tab = []
        quadtree.query(physics_engine.objects[1],tab)
        for element in physics_engine.objects:
            quadtree.delpoint(element)
        print(physics_engine.objects[0])
        print(physics_engine.objects[1])
        gjk = GJK2D(physics_engine.objects[0],physics_engine.objects[1])
        trig = gjk.detection()
        stuff = gjk.EPA(trig)
        if trig is not None:
            gjk.find_contact_features(gjk.shape1,gjk.shape2,stuff)
            gjk.resolve(stuff)
        physics_engine.objects[0].shape.velocity = Vector2(0,0)
        physics_engine.objects[0].shape.angular_velocity = 0
        physics_engine.update(dt)  # Pass ground_level as display_height - 20 (or whatever your ground level is)


    # Draw frame
    screen.fill((170, 170, 170))  # Clear screen
    if game_state != "menu":
        for elements in physics_engine.objects:
            elements.shape.draw(screen,(255,0,0))
        for elements in physics_engine.objects:
            pygame.draw.circle(screen,(0,255,255),Vector2(elements.mincircle.x,elements.mincircle.y),elements.mincircle.radius,2)

        # Draws a white line between clicked object and mouse position (during vector construction and 'paused')
        """Must stay in main because of where the game is taking place (screen)"""
        if clicked_object != None and game_state == "paused" : 
            pygame.draw.line(screen, (255, 255, 255), clicked_object.shape.centroid, mouse_position, 5)

    # Draw all buttons in the correct order
    new_scene = level_manager.current_scene #verify if we changed of scene
    running_scene = new_scene
    for button in level_manager.button_list:
        if (pygame.mouse.get_pos()[0] < button.position[0] + button.width/2) and (pygame.mouse.get_pos()[0] > button.position[0] - button.width/2) and (pygame.mouse.get_pos()[1] < button.position[1] + button.height/2) and (pygame.mouse.get_pos()[1] > button.position[1] - button.height/2) :
            button.hover(screen)   
            if click :
                button.is_pressed(display_width, display_height,physics_engine)
                game_state = button.game_state
                new_scene = level_manager.current_scene #verify if we changed of scene
                click = False
                if game_state!= "menu": #we load new objects if the scene changed
    
                    # test_object = level_manager.object_list[-1] 
                    # physics_engine.add_object(test_object)
                    # second_object = level_manager.object_list[-2]
                    # physics_engine.add_object(second_object)
                    pass
        else :
            button.draw(screen)


    # Display debug positions : must stay in main
    font = pygame.font.SysFont("Arial", 24)
    #position_text_1 = font.render(f"Position 1: ({int(physics_engine.objects[0].shape.centroid.x)}, {-int(physics_engine.objects[0].shape.centroid.y)})", True, (255, 255, 255))
    #position_text_2 = font.render(f"Position 2: ({int(physics_engine.objects[1].shape.centroid.x)}, {-int(physics_engine.objects[1].shape.centroid.y)})", True, (255, 255, 255))
    #screen.blit(position_text_1, (10, 10))
    #screen.blit(position_text_2, (10, 40))
    
    # Prediction of the trajectory of "test_object"
    if vector_applied1 == True and vector1_coords!= Vector2(0,0):
        predicted_positions = computes_50_position(test_object, vector1_coords, clock.get_time() / 100.0, test_position_x_before, test_position_y_before , simulation_steps=50, dt_sim=0.1)

        # Draw in yellow
        for point in predicted_positions:
            print("e",point)
            pygame.draw.circle(screen, (255, 255, 0), (int(point.x), int(point.y)), 3)  # Petit point jaune

    # Prediction of the trajectory of "second_object"
    if vector_applied2 == True and vector2_coords!= Vector2(0,0): 
        predicted_positions = computes_50_position(second_object, vector2_coords, clock.get_time() / 100.0, second_position_x_before, second_position_y_before , simulation_steps=50, dt_sim=0.1)

        # Draw in white
        for point in predicted_positions:
            pygame.draw.circle(screen, (255, 255, 255), (int(point.x), int(point.y)), 3)  # Petit point jaune

    pygame.display.flip()  # Refresh screen
    clock.tick(120)  # Limit FPS to 120



# Quit Pygame
pygame.quit()
