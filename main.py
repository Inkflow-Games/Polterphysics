"""
Polterphysics
main.py

A script that demonstrates the functionality of the game's physics engine.
Features include:
- Object movement with applied forces
- Collision detection with the ground
- Debugging display of object position
- Two controllable objects (balls) to collide with each other
- Eight additional physics objects that interact with the environment

Last Updated: Feb 2025
Python Version: 3.12.9
Dependencies: pygame, core.physics_engine, objects.object
"""

import pygame
from pygame.math import Vector2
from core.physics_engine import PhysicsEngine
from core.collision import resolve_collision
from objects.object import Object
from utils.math_utils import *

# Initialize Pygame
pygame.init()

# Configure the window
display_width, display_height = 1000, 800
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Physics Engine Test")

# Initialize physics engine
physics_engine = PhysicsEngine()

# Create the 10 objects (including the two controllable ones)
objects = []

# First controllable object
test_object = Object(mass=1, position=(400, 100), radius=15, max_speed=1500, bounciness=1, damping_coefficient = 0)
objects.append(test_object)

# Second controllable object
second_object = Object(mass=5, position=(600, 100), radius=25, max_speed=200, bounciness=0.07, damping_coefficient=0)
objects.append(second_object)

# Add 8 additional random objects
import random
for _ in range(8):
    obj = Object(
        mass=random.uniform(0.5, 3.0),
        position=(random.randint(100, 900), random.randint(100, 600)),
        radius=random.randint(10, 30),
        max_speed=random.randint(50, 150),
        bounciness=random.uniform(0.1, 0.9),
        damping_coefficient=random.uniform(0.01, 0.05)
    )
    objects.append(obj)

# Add objects to physics engine
for obj in objects:
    physics_engine.add_object(obj)

# Clock to control frame rate
clock = pygame.time.Clock()
running = True

# Key states for controllable objects
key_state_1 = {pygame.K_RIGHT: False, pygame.K_LEFT: False, pygame.K_DOWN: False, pygame.K_UP: False}
key_state_2 = {pygame.K_d: False, pygame.K_q: False, pygame.K_s: False, pygame.K_z: False}

# Ground level (just above the bottom of the window)
ground_level = display_height - 20

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states
    keys = pygame.key.get_pressed()

    # Apply forces to the first object (Arrow keys)
    if keys[pygame.K_RIGHT] and not key_state_1[pygame.K_RIGHT]:
        test_object.apply_impulsion(Vector2(30, 0))
        key_state_1[pygame.K_RIGHT] = True
    if keys[pygame.K_LEFT] and not key_state_1[pygame.K_LEFT]:
        test_object.apply_impulsion(Vector2(-30, 0))
        key_state_1[pygame.K_LEFT] = True
    if keys[pygame.K_DOWN] and not key_state_1[pygame.K_DOWN]:
        test_object.apply_impulsion(Vector2(0, 30))
        key_state_1[pygame.K_DOWN] = True
    if keys[pygame.K_UP] and not key_state_1[pygame.K_UP]:
        test_object.apply_impulsion(Vector2(0, -30))
        key_state_1[pygame.K_UP] = True

    # Apply forces to the second object (ZQSD keys)
    if keys[pygame.K_d] and not key_state_2[pygame.K_d]:
        second_object.apply_impulsion(Vector2(30, 0))
        key_state_2[pygame.K_d] = True
    if keys[pygame.K_q] and not key_state_2[pygame.K_q]:
        second_object.apply_impulsion(Vector2(-30, 0))
        key_state_2[pygame.K_q] = True
    if keys[pygame.K_s] and not key_state_2[pygame.K_s]:
        second_object.apply_impulsion(Vector2(0, 30))
        key_state_2[pygame.K_s] = True
    if keys[pygame.K_z] and not key_state_2[pygame.K_z]:
        second_object.apply_impulsion(Vector2(0, -30))
        key_state_2[pygame.K_z] = True

    # Reset key states
    for key in key_state_1:
        if not keys[key]:
            key_state_1[key] = False
    for key in key_state_2:
        if not keys[key]:
            key_state_2[key] = False

    # Update physics engine
    dt = clock.tick(120) / 1000  # Convertit en secondes

    # Check for collisions between all objects
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            resolve_collision(objects[i], objects[j])

    physics_engine.update(dt, ground_level)

    # Draw frame
    screen.fill((0, 0, 0))  # Clear screen

    # Draw objects
    for obj in objects:
        color = (255, 0, 0) if obj == test_object else (0, 0, 255) if obj == second_object else (200, 200, 200)
        pygame.draw.circle(screen, color, (int(obj.position.x), int(obj.position.y)), obj.radius)

    # Display debug positions
    font = pygame.font.SysFont("Arial", 24)
    position_text_1 = font.render(f"Position 1: ({int(test_object.position.x)}, {-int(test_object.position.y)})", True, (255, 255, 255))
    position_text_2 = font.render(f"Position 2: ({int(second_object.position.x)}, {-int(second_object.position.y)})", True, (255, 255, 255))
    screen.blit(position_text_1, (10, 10))
    screen.blit(position_text_2, (10, 40))

    pygame.display.flip()  # Refresh screen
    clock.tick(120)  # Limit FPS to 120
    if dt and 10/dt < 100:
        print(10 / dt)

# Quit Pygame
pygame.quit()
