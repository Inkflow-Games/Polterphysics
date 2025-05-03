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

import pygame
from pygame.math import Vector2
from core.collision import * 
from objects.mincircle import convert
from objects.Quadtree import CircleQ

class Object:
    """
    A class representing a physical object with mass, velocity, and rotation.

    Attributes:
        TO UPDATE
    """
    
    def __init__(self, polygon=True, grabable =False, mass=1, restitution_coefficient=0.8, vertices=None, radius=None, centroid=None,name='Object', mouse=[0,0], applied_coords =[0,0], applied_angle = 500, simulated =[]):
        """
        Initializes an Object instance with the specified properties.

        Parameters:
            TO UPDATE
        """
        self.name = name
        self.polygon = polygon
        self.restitution_coefficient = restitution_coefficient
        self.grabable = grabable
        self.mouse = mouse
        self.applied_coords = applied_coords
        self.applied_angle = applied_angle
        self.simulated = simulated
        if polygon :
            self.shape = Polygon(vertices, mass)
        else :
            self.shape = Circle(centroid, radius, mass)
        temp = self.minimumcircle()
        self.mincircle = temp[0]
        self.mincircledist = temp[1]
        self.mincircleangle = temp[2]

    def minimumcircle(self):
        if hasattr(self.shape,'radius'):
            #return (CircleQ(self.shape.centroid.x,self.shape.centroid.y,self.shape.radius),0,0)
            return (CircleQ(self.shape.centroid.x,self.shape.centroid.y,self.shape.radius),0,0)
        else:
            temp = convert(self.shape)
            #return (CircleQ(temp[0].c.x,temp[0].c.y,temp[0].r),temp[1],temp[2])
            return (CircleQ(temp[0].c.x,temp[0].c.y,temp[0].r),temp[1],temp[2])
    
    def updatemc(self,dt):
        self.mincircleangle = (self.mincircleangle + (self.shape.angular_velocity * dt))%(2*pi)
        self.mincircle.x = self.shape.centroid.x + self.mincircledist * cos(self.mincircleangle)
        self.mincircle.y = self.shape.centroid.y + self.mincircledist * sin(self.mincircleangle)



class Polygon:
    def __init__(self, vertices=[], mass=1):
        self.vertices = vertices
        self.length = len(vertices)
        self.centroid = self.center()
        self.angular_velocity = 0
        self.mass = mass
        self.inertia = self.calculate_inertia()
        self.velocity = Vector2(0,0)

    def calculate_inertia(self):
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

    def rotate(self, rad):

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
    
    def add(self, vector):
        for i in range(self.length):
            self.vertices[i] += vector
        self.centroid += vector
        return
    
    def draw(self, surface, color):
        #self.add(centerpos-self.centroid)
        centerpos = self.centroid
        pygame.draw.polygon(surface,color,self.vertices)
        pygame.draw.circle(surface,(0,255,0),self.center(),3)
        return
            
    def support(self, direction):
        return find_furthest(direction,self.vertices)
    
    def apply_force(self, force):
        """
        Applies a force to the object, modifying its velocity.

        Parameters:
        force (Vector2): The force vector applied to the object.
        """
        self.velocity += force / self.mass #this is the acceleration vector of the object --> you add an acceleration not a force

class Circle:
    def __init__(self, centre=Vector2(0,0), radius=10, mass=1):
        self.radius = radius
        self.centroid = centre
        self.angular_velocity = 0
        self.mass = mass
        self.velocity = Vector2(0,0)
        self.inertia = self.calculate_inertia()

    def support(self, direction):
        if direction.length() == 0:
            return self.centroid + self.radius * Vector2(0,0.00000001)
        else : return self.centroid + self.radius * direction.normalize()

    def calculate_inertia(self):
        temp = (1/2)*self.mass*(self.radius**2)
        return temp
    
    def add(self, vector):
        self.centroid += vector
        return
    
    def rotate(self, rad):
        return
    
    def draw(self, surface, color):
        pygame.draw.circle(surface,color,self.centroid,self.radius)
        pygame.draw.circle(surface,(0,255,0),self.centroid,3)
        return

    def move_center(self, position):
        temp = position - self.centroid
        self.add(temp)

    def apply_force(self, force):
        """
        Applies a force to the object, modifying its velocity.

        Parameters:
        force (Vector2): The force vector applied to the object.
        """

        self.velocity += force / self.mass #this is the acceleration vector of the object --> you add an acceleration not a force
