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

    def update_polygon(self,poly):
        poly.add(poly.velocity/60)
        poly.rotate(poly.angular_velocity/60)
        poly.velocity *= 0.99
        poly.angular_velocity *= 0.99

    def update(self, dt, ground_level):
        """
        Updates all objects in the physics engine by calling their `update` methods.

        Parameters:
        dt (float): Time step elapsed since the last update (in seconds).
        ground_level (float): The y-coordinate of the ground level for collision detection
                              (e.g., objects cannot fall below this).
        """
        for obj1 in self.objects:
            self.update_polygon(obj1)
