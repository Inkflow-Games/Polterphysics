import math
from pygame.math import Vector2

class Object:
    def __init__(self, mass, position, radius=0, max_speed=70, bounciness=0.8, damping_coefficient = 0, static = False):
        self.mass = mass
        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)
        self.max_speed = max_speed
        self.radius = radius  # Rayon de l'objet
        self.gravity = Vector2(0, 9.81 * self.mass)
        self.bounciness = bounciness  # Coefficient de rebond
        self.angular_velocity = 0  # Rotation de l'objet (en rad/s)
        self.damping_coefficient = damping_coefficient
        self.static = static # Static objects are not affected by forces

    def apply_force(self, force):
        acceleration = force / self.mass
        self.velocity += acceleration

    def apply_spin(self, spin_force):
        moment_of_inertia = self.mass * 0.1  # Approximation du moment d'inertie
        angular_acceleration = spin_force / moment_of_inertia
        self.angular_velocity += angular_acceleration

    def update(self, dt, ground_level):
        # Appliquer la force de gravité
        self.apply_force(self.gravity * dt)

        # Calcul du damping dynamique
        self.damping = 0.01 + self.damping_coefficient * (self.velocity.length() / self.max_speed)
        self.velocity *= (1 - self.damping * dt)

        # Limiter la vitesse de manière plus progressive
        if self.velocity.length() > self.max_speed:
            excess_speed = self.velocity.length() - self.max_speed
            self.velocity.scale_to_length(self.velocity.length() - excess_speed * 0.1)

        # Mise à jour de la position
        self.position += self.velocity * dt

        # Ajouter la rotation (spin) de l'objet (peut affecter la trajectoire)
        self.position += Vector2(math.cos(self.angular_velocity), math.sin(self.angular_velocity)) * dt

        # Gestion des collisions avec le sol
        if self.position.y + self.radius >= ground_level:  # Si l'objet touche le sol
            self.position.y = ground_level - self.radius  # Ajuste la position pour le maintenir sur le sol
            self.velocity.y = -self.velocity.y * self.bounciness  # Applique le rebond (inverser la vitesse verticale et l'ajuster selon le coefficient de rebond)
