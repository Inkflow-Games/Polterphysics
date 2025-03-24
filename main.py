import pygame
from pygame.math import Vector2
from core.physics_engine import PhysicsEngine
from core.collision import resolve_collision
from objects.object import Object
from utils.math_utils import *
from core.input_handler import *
from utils.math_utils import WIDTH, HEIGHT, FPS
import core.level_manager as lman
import json
from editor.level_editor import LevelEditor

# Initialize Pygame
pygame.init()

# Configure the window
display_width, display_height = 1920, 1080
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Physics Engine Test")

# Initialize physics engine
physics_engine = PhysicsEngine()

# Create test objects (simulating basketballs)
test_object = Object(mass=0.6, position=(400, 100), radius=15, max_speed=100, bounciness=0.8, damping_coefficient=0.02)
second_object = Object(mass=2, position=(600, 100), radius=25, max_speed=200, bounciness=0.07, damping_coefficient=0)
physics_engine.add_object(test_object)
physics_engine.add_object(second_object)

# Initialize Level Editor
level_editor = None

# Clock to control frame rate
clock = pygame.time.Clock()
running = True
game_state = "menu"  # Start in the menu state
click = False

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = True  # Set click to true when mouse button is pressed

    # Menu state - Show red square to open the level editor
    if game_state == "menu":
        screen.fill((0, 0, 0))  # Black background

        # Draw the red square that will open the level editor
        pygame.draw.rect(screen, (255, 0, 0), (200, 350, 200, 100))

        # Check if the red square is clicked to open the level editor
        if click:
            mouse_pos = pygame.mouse.get_pos()
            # Detect if the mouse is inside the red square
            if 200 < mouse_pos[0] < 400 and 350 < mouse_pos[1] < 450:
                game_state = "editor"  # Switch to editor state
                level_editor = LevelEditor(screen)  # Initialize the level editor
            click = False  # Reset click state

        pygame.display.flip()

    # Level editor state - Editor UI
    elif game_state == "editor":
        if level_editor:
            level_editor.draw()  # Draw level editor UI
            for event in pygame.event.get():
                level_editor.ui.check_events(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Si c'est un clic gauche
                        mouse_pos = pygame.mouse.get_pos()
                        level_editor.select_object(mouse_pos)  # Sélectionne l'objet sous la souris
                        level_editor.start_drag(mouse_pos)  # Démarre le drag si un objet est sélectionné
                elif event.type == pygame.MOUSEMOTION:
                    if level_editor.is_dragging:
                        mouse_pos = pygame.mouse.get_pos()
                        level_editor.update_drag(mouse_pos)  # Met à jour la position de l'objet pendant le drag
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Si le clic gauche est relâché
                        level_editor.stop_drag()  # Arrête le drag

            level_editor.draw()  # Dessine tous les éléments à l'écran
            pygame.display.flip()  # Actualise l'affichage


    # Gameplay state - Draw the physics engine with objects
    elif game_state == "running":
        screen.fill((0, 0, 0))  # Clear screen
        pygame.draw.circle(screen, (255, 0, 0), (int(test_object.position.x), int(test_object.position.y)), test_object.radius)  # Draw first object
        pygame.draw.circle(screen, (0, 0, 255), (int(second_object.position.x), int(second_object.position.y)), second_object.radius)  # Draw second object

        # Update physics
        dt = clock.get_time() / 100.0  # Convert milliseconds to a suitable scale
        resolve_collision(test_object, second_object)
        physics_engine.update(dt, display_height - 20)  # Pass ground_level as display_height - 20 (or whatever your ground level is)

        pygame.display.flip()  # Refresh screen

    clock.tick(120)  # Limit FPS to 120

# Quit Pygame
pygame.quit()
