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
import pygame
from pygame.math import Vector2
from core.collision import * 

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
    
    def __init__(self, mass, position, max_speed=70, bounciness=0.8, damping_coefficient=0, static=False):
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
        moment_of_inertia = self.mass * 0.1  # Approximate moment of inertia
        angular_acceleration = spin_force / moment_of_inertia
        self.angular_velocity += angular_acceleration
    
    def update(self, dt, ground_level):
        """
        Updates the object's position, velocity, and handles collisions.

        Parameters:
        dt (float): The time step for the simulation.
        ground_level (float): The y-coordinate representing the ground level.
        """
        # Apply gravity force
        self.apply_force(self.gravity * dt)

        # Compute dynamic damping
        self.damping = 0.01 + self.damping_coefficient * (self.velocity.length() / self.max_speed)
        self.velocity *= (1 - self.damping * dt)

        # Update position based on velocity
        self.position += self.velocity * dt

        # Apply rotation effect (spin can slightly affect trajectory)
        self.rotate()

class Polygon:
    def __init__(self,points,mass):
        self.vertices = points
        self.length = len(points)
        self.centroid = self.center()
        self.angular_velocity = 0
        self.mass = mass
        self.inertia = self.calcinertia()
        self.velocity = Vector2(0,0)

    def calcinertia(self):
        I = 0
        A_total = 0

        for i in range(self.length):
            j = (i+1) % self.length
            v1, v2 = self.vertices[i] - self.centroid, self.vertices[j] - self.centroid
            cross = v1.cross(v2)
            area = 0.5 * cross
            A_total += area

            I_triangle = (1/12) * (v1.dot(v1) + v1.dot(v2) + v2.dot(v2)) * cross
            I += I_triangle

        return (self.mass / A_total) * abs(I)

    def center(self):
        ans = Vector2(0,0)
        n=len(self.vertices)
        signedarea = 0
        for i in range(n):
            x0 = self.vertices[i].x
            y0 = self.vertices[i].y
            x1 = self.vertices[(i+1)%n].x
            y1 = self.vertices[(i+1)%n].y
            A = (x0 * y1) - (x1 * y0)
            signedarea += A

            ans.x += (x0 + x1) * A
            ans.y += (y0 + y1) * A
        signedarea *= 0.5
        ans.x = round((ans.x) / (6 * signedarea),1)
        ans.y = round((ans.y) / (6 * signedarea),1)
        return ans

    def rotate(self,rad):

        angle_rad = rad
        for i in range(self.length):
            # Shift the point so that center_point becomes the origin
            new_point = (self.vertices[i][0] - self.centroid[0], self.vertices[i][1] - self.centroid[1])
            new_point = (new_point[0] * cos(angle_rad) - new_point[1] * sin(angle_rad),
                    new_point[0] * sin(angle_rad) + new_point[1] * cos(angle_rad))
            # Reverse the shifting we have done
            new_point = Vector2(new_point[0] + self.centroid[0], new_point[1] + self.centroid[1])
            self.vertices[i] = new_point
        return
    
    def add(self,vector):
        for i in range(self.length):
            self.vertices[i] += vector
        self.centroid += vector
        return
    
    def draw(self,surface,color):
        #self.add(centerpos-self.centroid)
        centerpos = self.centroid
        pygame.draw.polygon(surface,color,self.vertices)
        pygame.draw.circle(surface,(0,255,0),self.center(),3)
        return
            
    def support(self,direction):
        return findfurthest(direction,self.vertices)
    
    def apply_force(self, force):
        self.velocity += force / self.mass

  
class circle:
    def __init__(self,centre, radius, mass):
        self.radius = radius
        self.centroid = centre
        self.angular_velocity = 0
        self.mass = mass
        self.velocity = Vector2(0,0)
        self.inertia = self.calcinertia()

    def support(self, direction):
        if direction.length() == 0:
            return self.centroid + self.radius * Vector2(0,0.00000001)
        else : return self.centroid + self.radius * direction.normalize()

    def calcinertia(self):
        temp = (1/2)*self.mass*(self.radius**2)
        return temp
    
    def add(self,vector):
        self.centroid += vector
        return
    
    def rotate(self,angle):
        return
    
    def draw(self,surface,color):
        pygame.draw.circle(surface,color,self.centroid,self.radius)
        pygame.draw.circle(surface,(0,255,0),self.centroid,3)
        return
    
    def apply_force(self, force):
        self.velocity += force / self.mass

    def move_center(self,position):
        temp = position - self.centroid
        self.add(temp)
        
