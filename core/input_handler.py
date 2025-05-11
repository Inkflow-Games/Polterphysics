"""
POLTERPHYSICS
input_handler.py

Library of functions that handle the possible actions of the user.

Features include:
- Define if left click is pressed
- Vector application during paused game script

Last Updated: May 2025
Python Version: 3.12+
Dependencies: pygame, pygame.math, utils.vector_utils, core.collision, objects.Quadtree, objects.object
"""

import pygame 
from pygame.math import Vector2
from utils.vector_utils import * 
from core.collision import *
from objects.Quadtree import RectangleQ, Quadtree
from objects.object import *

pygame.init()

def GetMouseInput(event) :
    """
    Return 1/0 if left click pressed/not

    Parameters:
    event (<class 'pygame.event.Event'>) : defined class that detects events
    """
    return event.type == pygame.MOUSEBUTTONDOWN #autorise qu'un seul clic gauche jusqu'au relachement de la touche  --> on peut pas maintenir la touche pour faire clic gauche continuellement


def vector_application(
    event,
    objects_list,
    clicked_object = Object,
    quadtree = Quadtree(RectangleQ(-100,-100,3400,2200),4),
    
) :
    """
    Handles the inputs from the user to apply vectors

    Parameters:
        event (bool) : 1/0 is left click/no left click from the user
        object_list (list of references) : physics_engine.objects : list of all the objects instanced in physics_engine
        clicked_object : reference of the object that the user is applying the vector to
        quadtree (Quadtree) : need precisions 
        
    Dependencies : 
        Quadtree functions
        compute_angle
        update_vector
        update_mouse
        compute_positions
    """
    
    mouse_position = Vector2(pygame.mouse.get_pos())
    
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and clicked_object == None: # left click + when no object is clicked 
        for elements in objects_list:
            quadtree.insert(elements) 
        potential = []
        mini = float("inf")
        quadtree.query(Object(False,False,1,1,[],1,mouse_position, "mouse", False), potential) #creates a circle of radius 1 to detect intersection with objects around the area
        for elements in potential :
            if elements.playable == True :
                if elements.polygon == False : # If the object is a circle
                    if elements.shape.centroid.distance_squared_to(mouse_position) < mini :
                        mini = elements.shape.centroid.distance_squared_to(mouse_position)  # obtain the distance between mouse and nearest centroid
                        clicked_object = elements  #obtain the object that is the closest to the mouse
                elif elements.polygon == True : # If object is a polygon
                    for i in range(len(elements.shape.vertices)) :
                        if elements.shape.vertices[i].distance_squared_to(mouse_position) < mini and elements.shape.centroid.distance_squared_to(mouse_position) < 5000:
                            mini = elements.shape.vertices[i].distance_squared_to(mouse_position)  # obtain the distance between mouse and nearest centroid
                            clicked_object = elements
        for elements in objects_list :
            quadtree.delpoint(elements)
        return clicked_object
    
    elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] and clicked_object != None: # left click + object clicked
        if 360<=mouse_position.x<=1560 and 0<=mouse_position.y<=1080 :
            update_mouse(clicked_object, mouse_position)
            direction_vector = Vector2(
                mouse_position[0] - clicked_object.shape.centroid[0],
                mouse_position[1] - clicked_object.shape.centroid[1]
            )
            # Cap the force vector if too large
            if direction_vector == Vector2(0,0) : 
                capped_vector = Vector2(0,0)
            else : 
                capped_vector = direction_vector.normalize() * min(direction_vector.length(), 260) * 5  # Same effect as (direction * coeff), 260*5=1300
            if -1300<=capped_vector.x<=1300 and -1300<=capped_vector.y<=1300 : 
                vector_angle = compute_angle(capped_vector.x, capped_vector.y) # Not used anywhere for now
                update_vector(clicked_object, capped_vector, vector_angle)
    
    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and clicked_object != None: # when click is released
        if 360<=mouse_position.x<=1560 and 0<=mouse_position.y<=1080 :
            update_mouse(clicked_object, mouse_position)
            direction_vector = Vector2(
                mouse_position[0] - clicked_object.shape.centroid[0],
                mouse_position[1] - clicked_object.shape.centroid[1]
            )
            # Cap the force vector if too large
            if direction_vector == Vector2(0,0) : 
                capped_vector = Vector2(0,0)
            else : 
                capped_vector = direction_vector.normalize() * min(direction_vector.length(), 260) * 5  # max 1300 norm
            if -1300<=capped_vector.x<=1300 and -1300<=capped_vector.y<=1300 : 
                vector_angle = compute_angle(capped_vector.x, capped_vector.y) 
                update_vector(clicked_object, capped_vector, vector_angle)
            
            computes_positions(clicked_object, simulation_steps=20, dt_sim=0.1)
            
            clicked_object = None
            return clicked_object
    return clicked_object