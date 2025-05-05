"""
vector_utils.py

A script that provides utility functions to obtain information on vectors / make computations with them.

Features include:
- Compute the angle between a vector and the regular frame of reference (x,y) with x to the right and y upwards --> (in our simulation, y is DOWNWARDS)
- Display the info of an objects
- Update "applied_coords", "applied_angle" and "mouse" of objects
- Reset these info
- Simulate positions ( (not) realistically) after a vector application
- Draw on the main window (screen) the vectors applied and the computed positions

Author: Maxime Noudelberg
Last Updated: May 2025
Python Version: 3.12.9
Dependencies: math : degrees, sqrt, atan2
              newton_to_force in maths_utils
              pygame.math : Vector2
"""

from math import degrees, atan2
from utils.math_utils import newton_to_force
import core.physics_engine
import pygame
from pygame.math import Vector2



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


# to change : comments needed for its utility
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


def computes_positions(obj, realistic = False,simulation_steps=20, dt_sim=0.1):
    """
    Computes "simulation_steps" positions to visualize the application of a vector

    Parameters:
        obj (Object) : reference of the object to update (in physics_engine.objects)
        realistic (bool) : defines if the trajectories will be compute realistically or not (Default = False)
        simulation_steps (int) : number of positions to compute (Default = 20)
        dt_sim (float) : time difference between 2 positions (Default = 0.1)
    """
    v0 = obj.shape.velocity  # Initial velocity of the object : pixels.dt^-1
    force_applied = Vector2(obj.applied_coords)
    # acceleration vector = obj.shape.mass * (sum)forces vectors
    
    predicted_positions = []
    original = obj.shape.centroid  # Starting position
    simulated_position = original.copy()  # Copy for simulation steps
    
    # Realistic equations models
    if realistic == True : 
        for i in range(1, simulation_steps + 1):
            x = 0.5*(force_applied.x*((dt_sim*i)**2))/obj.shape.mass + v0[0]*dt_sim*i + simulated_position[0]
            y = 0.5*((force_applied.y/obj.shape.mass + 9.81)*((dt_sim*i)**2)) + v0[1]*dt_sim*i + simulated_position[1]
            predicted_positions.append([int(x), int(y)])
    
    else : 
        acceleration = Vector2(obj.applied_coords) / obj.shape.mass

        predicted_velocity = v0 + acceleration
        simulated_velocity = predicted_velocity.copy()  # Copie pour éviter les références

        for _ in range(simulation_steps): # Simulate on 50 frames 
            simulated_velocity.y += newton_to_force(9.81) * dt_sim  # Add gravity each frame
            simulated_position.x += newton_to_force(simulated_velocity.x) * dt_sim
            simulated_position.y += newton_to_force(simulated_velocity.y) * dt_sim
            predicted_positions.append(simulated_position.copy())
    
    # Store simulated positions for later use
    obj.simulated = predicted_positions



def lines_and_positions(objects_list, screen, game_state="running", realistic = False):
    """
    Draws the vectors applied and the simulated positions

    Parameters:
        objects_list: list of all the initialized objects of a scene
        screen (pygame display): reference to the window where the game is taking place
        game_state (str): the name of the game state --> set to != "menu" for us here
        realistic (bool) : defines if the trajectories will be compute realistically or not (Default = False)
    """
    if game_state == "paused":
        for obj in objects_list:
            if (obj.applied_coords != [0, 0]) and obj.grabable == True:
                # Recalculate positions on each frame, allowing dynamic updates
                computes_positions(obj, realistic)

                # Draw applied force line (white)
                pygame.draw.line(screen, (255, 255, 255), obj.shape.centroid, obj.mouse, 5)

                # Draw simulated positions as a trajectory (yellow points)
                for i in range(len(obj.simulated)):
                    pygame.draw.circle(screen, (255, 255, 0), (int(obj.simulated[i][0]), int(obj.simulated[i][1])), 3)