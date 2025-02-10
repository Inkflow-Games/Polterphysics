from pygame.math import Vector2

class PhysicsEngine:
    """
    A class responsible for managing and updating all physical objects in the game.

    Attributes:
        objects (list): A list of all objects currently being simulated by the engine.

    Methods:
        add_object(obj: Object): Adds an object to the physics engine.
        remove_object(obj: Object): Removes an object from the physics engine.
        update(dt: float): Updates all objects within the engine, calling their `update` method.
    """

    def __init__(self):
        """
        Initializes the PhysicsEngine instance, with an empty list of objects.
        """
        self.objects = []

    def add_object(self, obj):
        """
        Adds an object to the physics engine.

        Args:
            obj (Object): The object to be added to the engine.
        """
        self.objects.append(obj)
    
    def remove_object(self, obj):
        """
        Removes an object from the physics engine.
        
        Args:
            obj (Object): The object to be removed from the engine.
        """
        if obj in self.objects:
            self.objects.remove(obj)

    def update(self, dt):
        """
        Updates all objects in the engine, calling their `update` method.

        Args:
            dt (float): The time step, representing the time passed since the last frame.
        """
        for obj in self.objects:
            obj.update(dt)
