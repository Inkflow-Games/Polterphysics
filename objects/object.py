"""
object.py

A script that defines a physical object with mass, position, velocity, and interactions such as forces, spin, and collisions.

Features include:
- Application of forces (including gravity)
- Handling of damping and velocity limits
- Collision detection with a ground level and bounce effect

Author: Rafael Véclin
Last Updated: Feb 2025
Python Version: 3.12.9
Dependencies: math, pygame.math.Vector2
"""

import math
from pygame.math import Vector2

class Object:
    """
    A class representing a physical object with mass, velocity, and rotation.

    Attributes:
        mass (float): The mass of the object.
        position (Vector2): The position of the object in 2D space.
        velocity (Vector2): The velocity of the object in 2D space.
        max_speed (float): The maximum speed limit for the object.
        radius (float): The radius of the object, used for collision detection.
        gravity (Vector2): The gravitational force acting on the object.
        bounciness (float): The coefficient of restitution for bounce calculations.
        angular_velocity (float): The rotational speed of the object in radians per second.
        damping_coefficient (float): The coefficient affecting the damping effect.
        static (bool): Whether the object is immovable and unaffected by forces.
    """
    
    def __init__(self, mass, position, radius=0, max_speed=70, bounciness=0.8, damping_coefficient=0, static=False):
        """
        Initializes an Object instance with the specified properties.

        Parameters:
        mass (float): The mass of the object.
        position (tuple or Vector2): The initial position of the object.
        radius (float, optional): The object's radius (default is 0).
        max_speed (float, optional): The maximum speed limit (default is 70).
        bounciness (float, optional): The bounce coefficient (default is 0.8).
        damping_coefficient (float, optional): The damping effect coefficient (default is 0).
        static (bool, optional): If True, the object does not move (default is False).
        """
        self.mass = mass
        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)
        self.max_speed = max_speed
        self.radius = radius
        self.gravity = Vector2(0, 9.81 * self.mass)
        self.bounciness = bounciness
        self.angular_velocity = 0
        self.damping_coefficient = damping_coefficient
        self.static = static
    
    def apply_force(self, force):
        """
        Applies a force to the object, modifying its velocity.

        Parameters:
        force (Vector2): The force vector applied to the object.
        """
        acceleration = force / self.mass
        self.velocity += acceleration
    
    def apply_spin(self, spin_force):
        """
        Applies a rotational force (spin) to the object.

        Parameters:
        spin_force (float): The force applied to generate angular acceleration.
        """
        pass
    """
        moment_of_inertia = self.mass * 0.1  # Approximate moment of inertia
        angular_acceleration = spin_force / moment_of_inertia
        self.angular_velocity += angular_acceleration
    """
    
    def update(self, dt, ground_level):
        """
        Updates the object's position, velocity, and handles collisions.

        Parameters:
        dt (float): The time step for the simulation.
        ground_level (float): The y-coordinate representing the ground level.
        """
        # Apply gravity force
        self.apply_force(self.gravity * dt)
        # Update position based on velocity
        self.position += self.velocity * dt
        # Collision detection with the ground
        if self.position.y + self.radius >= ground_level:  # If the object touches the ground
            self.position.y = ground_level - self.radius  # Adjust position to stay on the ground
            self.velocity.y = -self.velocity.y * self.bounciness  # Apply bounce effect (invert and reduce velocity)














"""
class Object:
    
    # The class `Object` is a blueprint for creating physical objects in a 2D space simulation. It
    # defines the properties and behaviors of these objects, including mass, position, velocity,
    # rotation, and interactions with forces and collisions. Here's a breakdown of what each attribute
    # represents:
    # A class representing a physical object with mass, velocity, and rotation.

    # Attributes:
    #     mass (float): The mass of the object.
    #     position (Vector2): The position of the object in 2D space.
    #     velocity (Vector2): The velocity of the object in 2D space.
    #     max_speed (float): The maximum speed limit for the object.
    #     radius (float): The radius of the object, used for collision detection.
    #     gravity (Vector2): The gravitational force acting on the object.
    #     bounciness (float): The coefficient of restitution for bounce calculations.
    #     angular_velocity (float): The rotational speed of the object in radians per second.
    #     damping_coefficient (float): The coefficient affecting the damping effect.
    #     static (bool): Whether the object is immovable and unaffected by forces.
    
    
    def __init__(self, mass, position, radius=0, max_speed=70, bounciness=0.8, damping_coefficient=0, static=False):
        
        # Initializes an Object instance with the specified properties.

        # Parameters:
        # mass (float): The mass of the object.
        # position (tuple or Vector2): The initial position of the object.
        # radius (float, optional): The object's radius (default is 0).
        # max_speed (float, optional): The maximum speed limit (default is 70).
        # bounciness (float, optional): The bounce coefficient (default is 0.8).
        # damping_coefficient (float, optional): The damping effect coefficient (default is 0).
        # static (bool, optional): If True, the object does not move (default is False).
        
        self.mass = mass
        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)
        self.max_speed = max_speed
        self.radius = radius
        self.gravity = Vector2(0, 9.81 * self.mass)
        self.bounciness = bounciness
        self.angular_velocity = 0
        self.damping_coefficient = damping_coefficient
        self.static = static
    
    def apply_force(self, force):
        
        # Applies a force to the object, modifying its velocity.

        # Parameters:
        # force (Vector2): The force vector applied to the object.
        
        acceleration = force / self.mass
        self.velocity += acceleration
    
    def apply_spin(self, spin_force):
        
        # Applies a rotational force (spin) to the object.

        # Parameters:
        # spin_force (float): The force applied to generate angular acceleration.
        
        moment_of_inertia = self.mass * 0.1  # Approximate moment of inertia
        angular_acceleration = spin_force / moment_of_inertia
        self.angular_velocity += angular_acceleration
    
    def update(self, dt, ground_level):
        
        Updates the object's position, velocity, and handles collisions.

        # Parameters:
        # dt (float): The time step for the simulation.
        # ground_level (float): The y-coordinate representing the ground level.
        
        # Apply gravity force
        self.apply_force(self.gravity * dt)

        # Compute dynamic damping
        self.damping = 0.01 + self.damping_coefficient * (self.velocity.length() / self.max_speed)
        self.velocity *= (1 - self.damping * dt)

        # Gradually limit speed instead of hard clamping
        if self.velocity.length() > self.max_speed:
            excess_speed = self.velocity.length() - self.max_speed
            self.velocity.scale_to_length(self.velocity.length() - excess_speed * 0.1)

        # Update position based on velocity
        self.position += self.velocity * dt

        # Apply rotation effect (spin can slightly affect trajectory)
        self.position += Vector2(math.cos(self.angular_velocity), math.sin(self.angular_velocity)) * dt

        # Collision detection with the ground
        if self.position.y + self.radius >= ground_level:  # If the object touches the ground
            self.position.y = ground_level - self.radius  # Adjust position to stay on the ground
            self.velocity.y = -self.velocity.y * self.bounciness  # Apply bounce effect (invert and reduce velocity)
        """