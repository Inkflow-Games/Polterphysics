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
Dependencies: math : degrees, sqrt, atan2
              pygame.math : Vector2
"""

from math import degrees, sqrt, atan2
from pygame.math import Vector2



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