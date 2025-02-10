from pygame.math import Vector2

class Object:
    """
    A class representing a physical object with mass, velocity, position,
    and forces applied to it. This object will be affected by gravity and
    any external forces.

    Attributes:
        mass (float): The mass of the object.
        position (Vector2): The position of the object in 2D space.
        velocity (Vector2): The velocity of the object in 2D space.
        acceleration (Vector2): The acceleration of the object.
        damping_coefficient (Vector2): The rate at which the object's velocity decreases over time on each axis.
        max_speed (float): The maximum speed the object can reach.
        forces (list): A list of forces currently applied to the object.

    Methods:
        apply_force(force: Vector2): Applies a force to the object.
        update(dt: float): Updates the position and velocity of the object based on the forces applied.
    """

    def __init__(self, mass, position, damping_coefficient, max_speed=100):
        """
        Initializes the Object instance with mass, position, and optional damping and speed limits.

        Args:
            mass (float): The mass of the object.
            position (tuple): The initial position of the object as a (x, y) tuple.
            damping_coefficient (Vector2, optional): A vector containing values between 0 and 1 to simulate energy loss over time on the 2 axes.
            max_speed (float, optional): The maximum speed the object can achieve.
        """
        self.mass = mass
        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.damping_coefficient = damping_coefficient
        self.max_speed = max_speed
        self.forces = []
        # Apply gravity (constant force downwards)
        gravity = Vector2(0, 9.81)  # Gravitational acceleration in m/s²
        self.apply_force(gravity * self.mass)  # Force due to gravity: F = m * g

    def apply_force(self, force):
        """
        Applies an external force to the object.

        Args:
            force (Vector2): The force to be applied to the object.
        """
        self.forces.append(force)

    def update(self, dt):
        """
        Updates the position and velocity of the object based on the forces applied.
        This method is called every frame to simulate the movement of the object.
        
        Args:
            dt (float): The time step, representing the time passed since the last frame, used for proper physics simulation.
        """

        # Calculate the net force (sum of all forces applied)
        total_force = sum(self.forces, Vector2(0, 0))  # Sum all the forces
        acceleration = total_force / self.mass  # F = m * a => a = F / m (Newton's first law)
        self.velocity += acceleration * dt  # Update velocity based on acceleration

        # Apply maximum speed (terminal velocity)
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)  # Scale velocity to max speed

        # Update position based on velocity
        self.position += self.velocity * dt  # Position update: p = p0 + v * t

        # Clear forces after each update
        print(self.forces)
        for force in self.forces[1:] :
            # Apply damping to each axis to simulate energy loss
            force.x *= self.damping_coefficient.x
            force.y *= self.damping_coefficient.y
            if force.length() <= 0.01 :
                self.forces.remove(force)  # Remove small forces to avoid numerical instability
