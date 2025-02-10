class PhysicsEngine:
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

    def update(self, dt, ground_level):
        """
        Updates all objects in the engine, calling their `update` method.

        Args:
            dt (float): The time step, representing the time passed since the last frame.
            ground_level (float): The y-coordinate representing the ground level.
        """
        for obj in self.objects:
            obj.update(dt, ground_level)  # Pass the ground_level to update() of each object
