"""
physics_engine.py

A simple physics engine that manages a collection of objects and handles collisions.

Features include:
- Adding and removing objects from the simulation
- Checking for collisions between objects (currently a placeholder)
- Resolving collisions (currently a placeholder)
- Updating object states and handling ground collisions

Author: Rafael Véclin
Last Updated: Feb 2025
Python Version: 3.12.9
Dependencies: None
"""
from pygame import Vector2

class PhysicsEngine:
    """A simple physics engine that manages a collection of objects and handles collisions."""
    
    def __init__(self):
        """Initializes the PhysicsEngine instance with an empty list of objects."""
        self.objects = []

    def add_object(self, obj):
        """
        Adds an object to the physics engine for simulation.

        Parameters:
        obj (Object): The object to be added.
        """
        self.objects.append(obj)
    
    def remove_object(self, obj):
        """
        Removes an object from the physics engine.

        Parameters:
        obj (Object): The object to be removed. If the object is not in the list, this method does nothing.
        """
        if obj in self.objects:
            self.objects.remove(obj)

    def update_polygon(self,object,dt):
        table = {True:1,False:0}
        object.shape.velocity += (Vector2(0,9.8) * dt * table[object.grabable]) # computes new velocity after applying acceleration for dt period
        object.shape.add(object.shape.velocity*dt* table[object.grabable])
        object.shape.rotate(object.shape.angular_velocity*dt* table[object.grabable])
        #object.shape.velocity *= (0.99)
        #object.shape.angular_velocity *= (0.99)
        # Update the minimum enclosing circle if applicable
        object.updatemc(dt)

        
    '''def update_polygon(self,object,dt):
        table = {True:0,False:1}
        object.shape.add(object.shape.velocity*dt*table[object.static])    #potential replace by grabable
        object.shape.rotate(object.shape.angular_velocity*dt*table[object.static])
        object.shape.velocity *= (0.99*table[object.static])
        object.shape.angular_velocity *= (0.99*table[object.static])
        object.mincircle.x = object.shape.centroid.x
        object.mincircle.y = object.shape.centroid.y'''

    def update(self, dt):
        """
        Updates all objects in the physics engine by calling the `update` methods.

        Parameters:
        dt (float): Time step elapsed since the last update (in seconds).
        """
        for obj1 in self.objects:
            self.update_polygon(obj1,dt)
