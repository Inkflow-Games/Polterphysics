"""
collision.py

A script that provides functions for detecting and resolving collisions 
between objects using physics-based calculations.

Features include:
- Compute Euclidean distance and direction vector between two points.
- Resolve collisions between two circular objects.
- Update object velocities based on mass and direction of impact.

Author: Clément Moussy
Last Updated: Feb 2025
Python Version: 3.12.9
Dependencies: pygame.math (Vector2), math
"""

from pygame.math import Vector2
from math import *

def compute_distance_and_direction(point1, point2):
    """
    Computes the Euclidean distance and direction vector between two points.

    Parameters:
    point1 (Vector2): First point (or object's position).
    point2 (Vector2): Second point (or object's position).

    Returns:
    tuple: A tuple containing:
        - float: The rounded Euclidean distance between the two points.
        - Vector2: The direction vector from `point1` to `point2`.
    """
    dx = point2.x - point1.x  # Difference in x-coordinates
    dy = point2.y - point1.y  # Difference in y-coordinates
    distance = round(sqrt(dx**2 + dy**2), 6)  # Compute Euclidean distance
    direction_vector = Vector2(dx, dy)  # Create direction vector
    return distance, direction_vector

def resolve_collision(circle1, circle2):
    """
    Resolves collisions between two circular objects.

    This function updates the velocities of both objects based on their masses, positions,
    and velocities.

    Parameters:
    circle1 (Object): First circular object.
    circle2 (Object): Second circular object.
    """
    # Compute the distance and the direction vector between both objects
    distance, direction_vector = compute_distance_and_direction(circle1.position, circle2.position)
    
    # Retrieve key properties of both objects
    radius1, radius2 = circle1.radius, circle2.radius
    velocity1, velocity2 = circle1.velocity, circle2.velocity
    mass1, mass2 = circle1.mass, circle2.mass

    # Check if the objects are colliding (distance is less than or equal to sum of radii)
    if int(distance) <= int(radius1 + radius2):

        # Compute relative velocity (how fast they approach each other)
        relative_velocity = Vector2(velocity2.x - velocity1.x, velocity2.y - velocity1.y)

        # Check if the objects are actually moving towards each other (avoids unnecessary calculations)
        if direction_vector.dot(relative_velocity) <= 0:

            # Compute unit normal and tangent vectors
            unit_normal = direction_vector / (compute_distance_and_direction(Vector2(0, 0), direction_vector)[0])
            unit_tangent = Vector2(-unit_normal.y, unit_normal.x)

            # Decompose velocities into normal and tangential components
            velocity1_normal = unit_normal.dot(velocity1)
            velocity1_tangent = unit_tangent.dot(velocity1)
            velocity2_normal = unit_normal.dot(velocity2)
            velocity2_tangent = unit_tangent.dot(velocity2)

            # Compute new normal velocities after elastic collision
            new_velocity1_normal = (velocity1_normal * (mass1 - mass2) + 2 * (mass2 * velocity2_normal)) / (mass1 + mass2)
            new_velocity2_normal = (velocity2_normal * (mass2 - mass1) + 2 * (mass1 * velocity1_normal)) / (mass1 + mass2)

            # Convert new normal velocities into vector form
            new_velocity1_normal_vector = unit_normal * new_velocity1_normal
            new_velocity2_normal_vector = unit_normal * new_velocity2_normal
            new_velocity1_tangent_vector = unit_tangent * velocity1_tangent
            new_velocity2_tangent_vector = unit_tangent * velocity2_tangent

            # Compute final velocity vectors by combining normal and tangential components
            circle1.velocity = new_velocity1_normal_vector + new_velocity1_tangent_vector
            circle2.velocity = new_velocity2_normal_vector + new_velocity2_tangent_vector
