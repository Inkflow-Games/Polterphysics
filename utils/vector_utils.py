"""
vector_utils.py

A script that provides utility functions to obtain information on vectors / make computations with them.

Features include:
- Compute the angle between a vector and the regular frame of reference (x,y) with x to the right and y upwards --> (in our simulation, y is DOWNWARDS)
(- From inertia and the new vector applied : consider them as 2 vectors and computes the norm and the angle of their vectorial sum
 - Computes the norm of a vector and divide it by dt) 

Author: Maxime Noudelberg
Last Updated: Feb 2025
Python Version: 3.12.9
Dependencies: json
              math : degrees, sqrt, atan2
              pygame.math : Vector2
"""

from math import degrees, sqrt, atan2
from utils.math_utils import newton_to_force
import core.physics_engine
import pygame
from pygame.math import Vector2
import json



def compute_angle(coord1, coord2):
    """
    Computes the angle between axis x and the vector applied by the user 

    Parameters:
        coord1 (int/float) : x coordinate (of a vector)
        coord2 (int/float) : y coordinate (of a vector)

    Dependencies : 
        degrees
        atan2
    """
    return -degrees(atan2(coord2, coord1))


# (NOT USED) (to delete) : only used in the trajectory simulation based on vectorial sum
def norm_and_angle_computation(x_before =0 , y_before =0, x_now =0 , y_now =0, force_vector = Vector2(0,0), dt = 1/120) : # before <=> dt-1  and now <=> actual position
    vx = (x_now - x_before)/dt
    vy = (y_now - y_before)/dt  # if vy is positive <=> the object is going down
    
    v0 = Vector2(vx + force_vector[0] , vy + force_vector[1])
    norm_vector = sqrt(v0[0]**2 + v0[1]**2)     # give the norm in pixels
    angle = compute_angle(v0[0], v0[1])
    return norm_vector, angle



#currently not used (to delete)
def initial_speed_computation(x_before = 0, y_before = 0, x_now = 0, y_now = 0, dt = 1/120) :
    return (sqrt((x_now - x_before)**2 + (y_now - y_before)**2))/dt



# to comment
def objects_running_info(test_object, second_object, vector_applied1 = False, vector_applied2 = False) :
        vector_applied1 = False #reset the vectors applied to our object
        vector_applied2 = False
        
        test_position_x_before = test_object.shape.centroid.x #obtain the position of the objects at the previous frame (if "frame_already_passed" >0)
        test_position_y_before = test_object.shape.centroid.y
        
        second_position_x_before = second_object.shape.centroid.x
        second_position_y_before = second_object.shape.centroid.y
        
        return vector_applied1, vector_applied2, test_position_x_before, test_position_y_before, second_position_x_before, second_position_y_before


def update_vector(obj, coords = Vector2(0,0), angle = 0.0) :
    """
    Updates the info of "applied_coords" and "applied_angle" of the object according to the vector applied by the user

    Parameters:
        obj (Object) : reference of the object to update (in physics_engine.objects)
        coords (Vector2) : coordinates of the vector
        angle (int/float) : angle of the vector
    """
    obj.applied_coords[0] = round(coords[0])
    obj.applied_coords[1] = round(coords[1])
    obj.applied_angle = angle



def update_mouse(obj, position = Vector2(0,0)) :
    """
    Updates the info of "mouse" of the object according to the vector applied by the user

    Parameters:
        obj (Object) : reference of the object to update (in physics_engine.objects)
        position (Vector2) : coordinates of the mouse
    """
    obj.mouse[0] = round(position[0])
    obj.mouse[1] = round(position[1])



def reset_level_vectors(list_obj) :
    """
    Resets all the vectors applied to the objects from a given scene

    Parameters:
        list_obj (we need to give physics_engine.objects): list of all the initialized objects of a scene
    """
    for obj in list_obj :
        obj.applied_coords[0] = 0
        obj.applied_coords[1] = 0
        obj.applied_angle = 0


def computes_positions(obj, simulation_steps=20, dt_sim=0.1):
    """
    Computes "simulation_steps" positions to visualize the application of a vector

    Parameters:
        obj (Object) : reference of the object to update (in physics_engine.objects)
        simulation_steps (int) : number of positions to compute
        dt_sim (float) : time difference between 2 positions
    """
    v0 = obj.shape.velocity  # Initial velocity of the object
    added_accel = Vector2(obj.applied_coords) / (0.02 * obj.shape.mass)  # Applied acceleration
    speed = v0 + added_accel  # Total speed (initial + applied acceleration)

    predicted_positions = []
    original = obj.shape.centroid  # Starting position
    simulated_position = original.copy()  # Copy for simulation steps

    # Simulate trajectory
    for _ in range(1, simulation_steps + 1):
        speed.y += 9.81 * 2.5 * dt_sim  # Apply gravity
        simulated_position.x += speed.x * dt_sim  # Update X position
        simulated_position.y += speed.y * dt_sim  # Update Y position
        predicted_positions.append([int(simulated_position.x), int(simulated_position.y)])

    # Store simulated positions for later use
    obj.simulated = predicted_positions


def lines_and_positions(objects_list, screen, game_state="running"):
    """
    Draws the vectors applied and the simulated positions

    Parameters:
        objects_list: list of all the initialized objects of a scene
        screen (pygame display): reference to the window where the game is taking place
        game_state (str): the name of the game state --> set to != "menu" for us here
    """
    if game_state == "paused":
        for obj in objects_list:
            if (obj.applied_coords != [0, 0]) and obj.grabable:
                # Recalculate positions on each frame, allowing dynamic updates
                computes_positions(obj)

                # Draw applied force line (white)
                pygame.draw.line(screen, (255, 255, 255), obj.shape.centroid, obj.mouse, 5)

                # Draw simulated positions as a trajectory (yellow points)
                for i in range(len(obj.simulated)):
                    pygame.draw.circle(screen, (255, 255, 0), (int(obj.simulated[i][0]), int(obj.simulated[i][1])), 3)



#keep this just in case for movement equations
"""
def computes_positions(object, vector_coords, dt, position_x_before, position_y_before, simulation_steps=50, dt_sim=0.1):

    #doesn't take into account "frottements" and other external forces
    
    #in PIXELS / dt²
    v0 = Vector2(
        (object.shape.centroid.x - position_x_before) / dt,
        (object.shape.centroid.y - position_y_before) / dt
    )

    #is a Vector2 --> pixels / kg --> coordinates of ax and ay
    acceleration = vector1_coords / object.shape.mass

    predicted_velocity = v0 + acceleration

    print(f"v0 = {v0}")
    print(f"acceleration = {acceleration}")
    print(f"predicted_velocity = {predicted_velocity}")

    predicted_positions = []
    simulated_position = object.shape.centroid # Copie pour éviter les références
    simulated_velocity = predicted_velocity  # Copie pour éviter les références

    for _ in range(simulation_steps): # Simulate on 50 frames 
        simulated_velocity.y += newton_to_force(9.81) * dt_sim  # Add gravity each frame
        simulated_position.x += newton_to_force(simulated_velocity.x) * dt_sim
        simulated_position.y += newton_to_force(simulated_velocity.y) * dt_sim
        predicted_positions.append(simulated_position.copy())

    return predicted_positions

"""