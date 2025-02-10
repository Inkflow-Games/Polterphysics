from pygame.math import Vector2

GRAVITY = 9.81
FRICTION_COEFFICIENT = 10 # Maybe we could replace it later with a more realistic system

class PhysicsEngine:
    def __init__(self):
        self.objects = [] 

    def add_object(self, obj):
        """Adds an object to the physics simulation"""
        self.objects.append(obj)

    def apply_force_to_object(self, obj, force):
        """Applies a force to an object"""
        obj.apply_force(force)

    def update(self, dt):
        """Updates the position of all the objects and the time interval"""
        for obj in self.objects:
            self.update_object(obj, dt)

    def update_object(self, obj, dt):
        """Updates an object with the applied forces"""
        if obj.mass > 0:
            total_force = sum(obj.forces, Vector2(0, 0)) + Vector2(0, GRAVITY * obj.mass)
            friction = -obj.velocity * FRICTION_COEFFICIENT
            total_force += friction
            acceleration = total_force / obj.mass
            obj.velocity += acceleration * dt
            obj.position += obj.velocity * dt

        if obj.inertia > 0:
            # Rotation handling to be implemented
            pass

        obj.forces.clear()
        obj.torques.clear()
