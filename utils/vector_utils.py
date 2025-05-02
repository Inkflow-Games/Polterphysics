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
    return -degrees(atan2(coord2, coord1))


#only used in the trajectory simulation based on vectorial sum
def norm_and_angle_computation(x_before =0 , y_before =0, x_now =0 , y_now =0, force_vector = Vector2(0,0), dt = 1/120) : # before <=> dt-1  and now <=> actual position
    vx = (x_now - x_before)/dt
    vy = (y_now - y_before)/dt  # if vy is positive <=> the object is going down
    
    v0 = Vector2(vx + force_vector[0] , vy + force_vector[1])
    norm_vector = sqrt(v0[0]**2 + v0[1]**2)     # give the norm in pixels
    angle = compute_angle(v0[0], v0[1])
    return norm_vector, angle



#currently not used
def initial_speed_computation(x_before = 0, y_before = 0, x_now = 0, y_now = 0, dt = 1/120) :
    return (sqrt((x_now - x_before)**2 + (y_now - y_before)**2))/dt




def objects_running_info(test_object, second_object, vector_applied1 = False, vector_applied2 = False) :
        vector_applied1 = False #reset the vectors applied to our object
        vector_applied2 = False
        
        test_position_x_before = test_object.shape.centroid.x #obtain the position of the objects at the previous frame (if "frame_already_passed" >0)
        test_position_y_before = test_object.shape.centroid.y
        
        second_position_x_before = second_object.shape.centroid.x
        second_position_y_before = second_object.shape.centroid.y
        
        return vector_applied1, vector_applied2, test_position_x_before, test_position_y_before, second_position_x_before, second_position_y_before


def computes_50_position(object, vector1_coords, dt, position_x_before, position_y_before, simulation_steps=50, dt_sim=0.1):

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




def update_vector(obj_name = "", scene = 0, coords = [0,0], angle = 0) :
    """
    Write in the json the info of the vector applied to the user to an object from a given scene

    Parameters:
        obj_name (str) : the name of the object to change (NEED to give its name according to "levels.json" --> "scene"["name"])
        scene (int): The integer of the number of a scene (in "levels.json"). Defaults to 0.
        coords (array of int size 2) : the coordinates of the vector applied by the user (NEED to be converted from Vector2 to array of int)
        angle (int) : measure in degrees (?) of the angle of the vector applied
    """
    
    with open("data/levels.json", "r") as f:
        data = json.load(f)

    scene_str = str(scene)
    data[scene_str][obj_name]["applied_coords"][0] = coords[0]
    data[scene_str][obj_name]["applied_coords"][1] = coords[1]
    data[scene_str][obj_name]["applied_angle"] = angle

    # Save changes
    with open("data/levels.json", "w") as f:
        json.dump(data, f, indent=2, separators=(',', ': '))


def reset_level_vectors(list_obj, scene = 0) :
    """
    Resets all the vectors applied to the objects from a given scene

    Parameters:
        list_obj (we need to give physics_engine.objects): list of all the initialized objects of a scene
        scene (int): The integer of the number of a scene (in "levels.json"). Defaults to 0.
    """


    with open("data/levels.json", "r") as f:
        data = json.load(f)

    scene_str = str(scene)
    for obj in list_obj :
        obj_name = obj.name
        data[scene_str][obj_name]["applied_coords"][0] = 0
        data[scene_str][obj_name]["applied_coords"][1] = 0
        data[scene_str][obj_name]["applied_angle"] = 1  # Need to change to 0 after debug


    # Save changes
    with open("data/levels.json", "w") as f:
        json.dump(data, f, indent=2, separators=(',', ': '))