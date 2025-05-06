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

from math import degrees, atan2, radians, cos, sin
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
    obj.simulated = [] # Reset the field if a zone have been entered (in case, simulation_steps + 1 positions in the field != simulation_steps)
    v0 = obj.shape.velocity  # Initial velocity of the object : pixels.dt^-1
    force_applied = Vector2(obj.applied_coords)
    # acceleration vector = obj.shape.mass * (sum)forces vectors
    
    predicted_positions = []
    original = obj.shape.centroid  # Starting position
    simulated_position = original.copy()  # Copy for simulation steps
    
    """
    Use the necessary fields depending on the type of zone
    
    
    if len(obj.zone) == 8 : # If there is a zone for the object
        vector_zone = Vector2(obj.zone[1])
        center_zone = Vector2(obj.zone[2])
        x_left = obj.zone[3]
        x_right = obj.zone[4]
        y_up = obj.zone[5]
        y_down = obj.zone[6]
        radius = obj.zone[7]
    """
    
    # Realistic equations models
    if realistic == True : 
        for i in range(1, simulation_steps + 1):
            """
            Need to implement the realistic equations if a potential zone is met 
            --> we need to take the new v0 each time the object is touched by the vector of a zone + update the original position at the same time
            --> when exiting a zone, take v0 and the original position as the new v0 and original for the computations (until entering a zone, ...) 
            
            
            if obj.zone[0] != "magnetism" : # Wind zone --> no : vector_zone, center_zone, radius
                if simulated_position[0] <= x_right and simulated_position[0] >= x_left and simulated_position[1] <= y_up and simulated_position[1] >= y_down: # If on the zone
                    
                    x = 0.5*( (force_applied.x + vector_zone.x) / obj.shape.mass )*((dt_sim*i)**2)) + v0[0]*dt_sim*i + simulated_position[0]
                    y = 0.5*((force_applied.y + vector_zone.y ) /obj.shape.mass + 9.81 )*((dt_sim*i)**2)) + v0[1]*dt_sim*i + simulated_position[1]
            """
                
            x = 0.5*(force_applied.x*((dt_sim*i)**2))/obj.shape.mass + v0[0]*dt_sim*i + simulated_position[0]
            y = 0.5*((force_applied.y/obj.shape.mass + 9.81)*((dt_sim*i)**2)) + v0[1]*dt_sim*i + simulated_position[1]
            predicted_positions.append([int(x), int(y)])
    
    else : 
        # Initial speed = inertia + applied velocity by the vector
        # The applied vector is NOT a CONTINUOUS force
        simulated_velocity = obj.shape.velocity + (Vector2(obj.applied_coords) / obj.shape.mass)

        predicted_positions = [simulated_position.copy()] # Copy the initial position at the beginning of the list 

        # If there is a field "zone" = ["wind", ...] in the object
        if len(obj.zone) == 8 and obj.zone[0] == "wind":
            vector_zone = Vector2(obj.zone[1])
            x_left = obj.zone[3]
            x_right = obj.zone[4]
            y_up = obj.zone[5]
            y_down = obj.zone[6]
        else:
            vector_zone = Vector2(0, 0)  # No zone defined for this object

        for _ in range(simulation_steps):
            # If the centroid position of an object is inside a rectangle zone
            if (
                len(obj.zone) == 8 and
                x_left <= simulated_position.x <= x_right and
                y_up <= simulated_position.y <= y_down
            ):
                # Add the vector of the zone to the speed of the object (this force is CONTINUOUS)
                simulated_velocity += vector_zone / obj.shape.mass

            # Application of the gravity
            simulated_velocity.y += newton_to_force(9.81) * dt_sim

            # Computation of a position
            simulated_position.x += newton_to_force(simulated_velocity.x) * dt_sim
            simulated_position.y += newton_to_force(simulated_velocity.y) * dt_sim

            predicted_positions.append(simulated_position.copy())
            
    # Store simulated positions for later use
    obj.simulated = predicted_positions



def draw_arrow(screen, color, start, end, width, head_length, head_angle):
    """
    Draws the arrow that represents the vector

    Parameters:
        screen (pygame display): reference to the window where the game is taking place
        color (tuple int : in 0-255) : color of the arrow
        start (int/float) : center of the object
        end (int/float) : mouse position
        width (int) : of the line
        head_length (int) : of the arrow
        head_angle (int) : orientation
    """
    # Draw the line
    pygame.draw.line(screen, color, start, end, width)

    # Computes arrow direction
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = atan2(dy, dx)

    # Computes left and right points of the arrow 
    left = (
        end[0] - head_length * cos(angle - radians(head_angle)),
        end[1] - head_length * sin(angle - radians(head_angle))
    )
    right = (
        end[0] - head_length * cos(angle + radians(head_angle)),
        end[1] - head_length * sin(angle + radians(head_angle))
    )

    # Draw the triangle
    pygame.draw.polygon(screen, color, [end, left, right])




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
                draw_arrow(screen, (255, 255, 255), obj.shape.centroid, obj.mouse, 5, 20, 25)

                # Draw simulated positions as a trajectory (yellow points)
                for i in range(len(obj.simulated)):
                    pygame.draw.circle(screen, (255, 255, 0), (int(obj.simulated[i][0]), int(obj.simulated[i][1])), 3)