"""
Polterphysics
main.py

A script that demonstrates the functionality of the game's physics engine
Features include:
- Object movement with applied forces
- Collision detection with the ground
- Debugging display of object position
- Two controllable objects (balls) to collide with each other

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
from ui.main_menu import *
from core.input_handler import *
from utils.math_utils import WIDTH, HEIGHT, FPS
import core.level_manager as lman
import json

# Initialize Pygame
pygame.init()

# Configure the window
display_width, display_height = 1000, 800
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Physics Engine Test")

# Initialize physics engine
physics_engine = PhysicsEngine()

lman.load_scene(0) #initialize the main menu scene

# Create a test object (simulating a basketball)
# test_object = Object(mass=0.6, position=(400, 100), radius=15, max_speed=100, bounciness=0.8, damping_coefficient=0.02)
test_object = lman.object_list[-1]
physics_engine.add_object(test_object)

# Create a second test object (another basketball)
# second_object = Object(mass=2, position=(600, 100), radius=25, max_speed=200, bounciness=0.07, damping_coefficient=0)
second_object = lman.object_list[-2]
physics_engine.add_object(second_object)

# Clock to control frame rate
clock = pygame.time.Clock()
running = True

# Dictionary to track key states for the first object
key_state_1 = {
    pygame.K_RIGHT: False,
    pygame.K_LEFT: False,
    pygame.K_DOWN: False,
    pygame.K_UP: False
}

# Dictionary to track key states for the second object (ZQSD control)
key_state_2 = {
    pygame.K_d: False,
    pygame.K_q: False,
    pygame.K_s: False,
    pygame.K_z: False, 
    pygame.K_SPACE: False
}

# Ground level (just above the bottom of the window)
ground_level = display_height - 20


game_state = "paused"


# Main game loop
while running:
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else :
            if GetMouseInput(event):  # Get the click input
                click = True

    # Get key states for the first object (Arrow keys)
    keys = pygame.key.get_pressed()

    # Get key states for the second object (ZQSD keys)
    keys_2 = pygame.key.get_pressed()

    if game_state == "paused" : # only check input when the game is paused

        # Apply force to the first object (Arrow keys)
        if keys[pygame.K_RIGHT] and not key_state_1[pygame.K_RIGHT]:
            test_object.apply_force(Vector2(newton_to_force(30), 0))  # Apply force to the right
            key_state_1[pygame.K_RIGHT] = True

        if keys[pygame.K_LEFT] and not key_state_1[pygame.K_LEFT]:
            test_object.apply_force(Vector2(-newton_to_force(30), 0))  # Apply force to the left
            key_state_1[pygame.K_LEFT] = True

        if keys[pygame.K_DOWN] and not key_state_1[pygame.K_DOWN]:
            test_object.apply_force(Vector2(0, newton_to_force(30)))  # Apply force downward
            key_state_1[pygame.K_DOWN] = True

        if keys[pygame.K_UP] and not key_state_1[pygame.K_UP]:
            test_object.apply_force(Vector2(0, -newton_to_force(30)))  # Apply force upward
            key_state_1[pygame.K_UP] = True


        # Apply force to the second object (ZQSD keys)
        if keys_2[pygame.K_d] and not key_state_2[pygame.K_d]:
            second_object.apply_force(Vector2(newton_to_force(46), 0))
            key_state_2[pygame.K_d] = True

        if keys_2[pygame.K_q] and not key_state_2[pygame.K_q]:
            second_object.apply_force(Vector2(-newton_to_force(46), 0))
            key_state_2[pygame.K_q] = True

        if keys_2[pygame.K_s] and not key_state_2[pygame.K_s]:
            second_object.apply_force(Vector2(0, newton_to_force(46)))
            key_state_2[pygame.K_s] = True

        if keys_2[pygame.K_z] and not key_state_2[pygame.K_z]:
            second_object.apply_force(Vector2(0, -newton_to_force(46)))
            key_state_2[pygame.K_z] = True

    # Check if we pause the game with space
    if keys_2[pygame.K_SPACE] and not key_state_2[pygame.K_SPACE] :
        key_state_2[pygame.K_SPACE] = True
        if game_state == 'paused' :
            game_state = 'running'
        else : 
            game_state = "paused"

    # Reset key state when key is released
    for key in key_state_1:
        if not keys[key]:
            key_state_1[key] = False

    for key in key_state_2:
        if not keys_2[key]:
            key_state_2[key] = False

    if game_state == "running" : # the physics is calculated only during play mode
        # Update physics engine based on time delta
        dt = clock.get_time() / 100.0  # Convert milliseconds to a suitable scale
        resolve_collision(test_object,second_object)
        physics_engine.update(dt, ground_level)  # Pass ground_level as display_height - 20 (or whatever your ground level is)

    # Draw frame
    screen.fill((0, 0, 0))  # Clear screen
    pygame.draw.circle(screen, (255, 0, 0), (int(test_object.position.x), int(test_object.position.y)), test_object.radius)  # Draw first object
    pygame.draw.circle(screen, (0, 0, 255), (int(second_object.position.x), int(second_object.position.y)), second_object.radius)  # Draw second object


    # Draw all buttons in the correct order
    for button in lman.button_list:
        if (pygame.mouse.get_pos()[0] < button.position[0] + button.width/2) and (pygame.mouse.get_pos()[0] > button.position[0] - button.width/2) and (pygame.mouse.get_pos()[1] < button.position[1] + button.height/2) and (pygame.mouse.get_pos()[1] > button.position[1] - button.height/2) :
            button.hover(screen)   
            if click :
                button.is_pressed()
                game_state = button.game_state
                click = False
        else :
            button.draw(screen)

    # Display debug positions
    font = pygame.font.SysFont("Arial", 24)
    position_text_1 = font.render(f"Position 1: ({int(test_object.position.x)}, {-int(test_object.position.y)})", True, (255, 255, 255))
    position_text_2 = font.render(f"Position 2: ({int(second_object.position.x)}, {-int(second_object.position.y)})", True, (255, 255, 255))
    screen.blit(position_text_1, (10, 10))
    screen.blit(position_text_2, (10, 40))

    pygame.display.flip()  # Refresh screen
    clock.tick(120)  # Limit FPS to 120



# Quit Pygame
pygame.quit()
