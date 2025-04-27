"""
input_handler.py

Library of functions that handle the possible actions of the user.

Features include:
- Define if left click is pressed
- (to modify) Detect if a left click is on/in a circle (currently --> must be in an object later on)
- Vector application during paused game script

Author: Maxime Noudelberg
Last Updated: April 2025
Python Version: 3.12.10
Dependencies: pygame, pygame.math, utils.vector_utils
"""

import pygame 
from pygame.math import Vector2
from utils.vector_utils import * 
pygame.init()

def GetMouseInput(event) :
    """
    Return 1/0 if left click pressed/not

    Parameters:
    event (<class 'pygame.event.Event'>) : defined class that detects events
    """
    return event.type == pygame.MOUSEBUTTONDOWN #autorise qu'un seul clic gauche jusqu'au relachement de la touche  --> on peut pas maintenir la touche pour faire clic gauche continuellement

#verifies if the mouse is in the radius of a clicked circle
def is_point_in_circle(point, circle_center, radius):
    """
    Return 1/0 if mouse position is between the center of a circle and its radius/not

    Parameters:
    point (tuple of integers): The position of the mouse
    circle_center (array of integers (?)) : Actual coordinates of the center of our circle
    radius (integer) : Radius of this same circle
    """
    dx = point[0] - circle_center[0]
    dy = point[1] - circle_center[1]
    return dx**2 + dy**2 <= radius**2


def vector_application(
    event, 
    test_object, second_object,
    clicked_object, vector_applied1, vector_applied2, 
    vector1_coords, vector2_coords, 
    vector1_angle, vector2_angle
):
    
    """
    Handles the application of a Vector2 on circle (modify for an object later on) : can apply up to 2 vectors at the same time (1 per object)
    Updates the variables clicked_object, vector_applied1, vector_applied2, vector1_coords, vector2_coords, vector1_angle, vector2_angle, mouse_position
    depending on the actions of the user 

    Parameters:
    clicked_object (object from the objects.json (?)) : The object manipulated bu the user
    vector_applied1 (boolean) : Defines if the user has applied a vector to test_object during game_state = "paused" 
    vector_applied2 (boolean) : Defines if the user has applied a vector to second_object during game_state = "paused" 
    vector1_coords (Vector2) : Coordinates of the vector (if) applied to test_object
    vector2_coords (Vector2) : Coordinates of the vector (if) applied to second_object
    vector1_angle (integer) : angle between center of circle (test_object) and position of the mouse, in the normal plane (x>0 to the right, y>0 upwards) 
    vector2_angle (integer) : angle between center of circle (second_object) and position of the mouse, in the normal plane (x>0 to the right, y>0 upwards) 
    mouse_position (tuple of integers): The position of the mouse
    """
    
    mouse_position = pygame.mouse.get_pos()

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if is_point_in_circle(mouse_position, test_object.position, test_object.radius):
            clicked_object = test_object
            if vector_applied1:
                force_vector = -vector1_coords
                test_object.apply_force(force_vector)
                vector_applied1 = False
                vector1_coords = Vector2(0, 0)

        elif is_point_in_circle(mouse_position, second_object.position, second_object.radius):
            clicked_object = second_object
            if vector_applied2:
                force_vector = -vector2_coords
                second_object.apply_force(force_vector)
                vector_applied2 = False
                vector2_coords = Vector2(0, 0)

    elif event.type == pygame.MOUSEMOTION and clicked_object is not None:
        pass  # Rien à faire ici, mais tu peux gérer un affichage de curseur par exemple

    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and clicked_object is not None:
        force_vector = Vector2(
            mouse_position[0] - clicked_object.position[0],
            mouse_position[1] - clicked_object.position[1]
        )
        clicked_object.apply_force(force_vector)
        print(f"Force applied : {force_vector}")

        if clicked_object == test_object:
            vector_applied1 = True
            vector1_coords = force_vector
            vector1_angle = compute_angle(vector1_coords.x, vector1_coords.y)
        elif clicked_object == second_object:
            vector_applied2 = True
            vector2_coords = force_vector
            vector2_angle = compute_angle(vector2_coords.x, vector2_coords.y)

        clicked_object = None

    return clicked_object, vector_applied1, vector_applied2, vector1_coords, vector2_coords, vector1_angle, vector2_angle, mouse_position
