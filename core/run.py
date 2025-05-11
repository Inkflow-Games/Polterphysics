"""
POLTERPHYSICS
run.py

Main loop for Polterphysics game.
Features:
- Scene handling and transitions
- Physics updates with user vector interaction
- Simple pause system
- Object drawing with optional debug vectors
- Button UI and audio feedback

Last Updated: May 2025
Python Version: 3.12+
Dependencies: pygame, pygame.math, random, sys, core.physics_engine, core.collision, objects.object, utils.math_utils, utils.vector_utils, utils.sprites_utils, core.input_handler, objects.Quadtree, core.level_manager, core.sound
"""

import pygame
from pygame.math import Vector2
from random import randint
import sys
from core.physics_engine import PhysicsEngine
from core.collision import *
from objects.object import *
from utils.math_utils import *
from utils.vector_utils import *
from utils.sprites_utils import *
from core.input_handler import *
from objects.Quadtree import RectangleQ, Quadtree
import core.level_manager as level_manager
from core.sound import play_sound_fx


def main() :
    # === Initialization ===
    pygame.init()
    pygame.mixer.init()

    clock = pygame.time.Clock()
    running = True

    clicked_object = None # Object that will receive the user-applied vector
    vectors_applied = False # Prevents repeated vector application
    particles = []

    # Screen configuration
    display_info = pygame.display.Info()
    display_width, display_height = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Physics Engine Test")

    # Backgrounds
    pictureBackground = pygame.transform.scale(pygame.image.load("data/background/back1.png"), (display_width, display_height))
    pictureOption = pygame.transform.scale(pygame.image.load("data/background/back1-tuto.png"), (display_width, display_height))
    win = pygame.transform.scale(pygame.image.load("data/background/win_back.png"), (display_width, display_height))
    game_over = pygame.transform.scale(pygame.image.load("data/background/game_over_back.png"), (display_width, display_height))

    # Physics engine and spatial partitioning
    physics_engine = PhysicsEngine()
    bounding_box = RectangleQ(-1000, -1000, 3400, 2200)
    quadtree = Quadtree(bounding_box, 20)

    # Keyboard states (e.g. pause key)
    key_state = {
        pygame.K_SPACE: False,
    }

    # Load first level/scene
    level_manager.load_scene(0, display_width, display_height, physics_engine, screen)
    game_state = "menu"


    # === Main Game Loop ===
    while running:
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Mouse click detection
                click = True

        keys = pygame.key.get_pressed()

        # Toggle pause with spacebar
        if keys[pygame.K_SPACE] and not key_state[pygame.K_SPACE]:
            key_state[pygame.K_SPACE] = True
            if (game_state == "running" or game_state == "paused") :
                game_state = "running" if game_state == "paused" else "paused"
                
        for key in key_state:
            if not keys[key]:
                key_state[key] = False

        if game_state == "paused":
            vectors_applied = False # Allow applying vectors again
            clicked_object = vector_application(event, physics_engine.objects, clicked_object, quadtree)

        if game_state == "running":
            dt = clock.get_time() / 100.0

            for obj in physics_engine.objects:
                quadtree.insert(obj)
            interactions = quadtree.searchelements(physics_engine.objects)
            
            
            # Apply all the vectors entered by the user during transition from "paused" state to "running" state --> prevent vector stacking 
            if vectors_applied == False :
                for obj in physics_engine.objects :
                    if (obj.applied_coords != [0,0]) and (obj.grabable == True) and (obj.playable == True): # general application of the forces
                        obj.shape.velocity += (Vector2(obj.applied_coords) /  obj.shape.mass) # Instant increase of the speed of the object 
                        obj.playable = False # Allow for only 1 vector applied per object
                vectors_applied = True
            
            for obj in physics_engine.objects :
                if (obj.grabable == True) and (len(obj.zone) == 8) : # A zone is entered
                    if obj.zone[0] == "wind" :
                        if obj.shape.centroid[0] <= obj.zone[4] and obj.shape.centroid[0] >= obj.zone[3] and obj.shape.centroid[1] >= obj.zone[5] and obj.shape.centroid[1] <= obj.zone[6] :
                            obj.shape.velocity += (Vector2(obj.zone[1]) / obj.shape.mass)
            
            
            # Reset the vectors info and mouse position for all the objects loaded in the physics engine
            reset_level_vectors(physics_engine.objects) 
            for elements in physics_engine.objects :
                update_mouse(elements, Vector2(0,0))


            for group in interactions:
                if len(group) >= 2:
                    for other in group[1:]:
                        gjk = GJK2D(group[0], other)
                        collision = gjk.detection()
                        resolution = gjk.EPA(collision)
                        if collision is not None and not (group[0].grabable == other.grabable == False):
                            gjk.find_contact_features(gjk.shape1, gjk.shape2, resolution)
                            gjk.resolve(resolution, dt)

            physics_engine.update(dt)

        # === Drawing ===
        if game_state == "menu":
            screen.blit(pictureBackground, (0, 0))
            level_manager.sprite_manager.draw_sprites(screen = screen, game_state = game_state)
        elif game_state == "tuto":
            screen.blit(pictureOption, (0, 0))
        elif game_state == "game_over":
            screen.blit(game_over, (0,0))
        elif game_state == "win" :
            screen.blit(win, (0,0))
        else:
            screen.blit(level_manager.background, (0, 0))

            for elements in physics_engine.objects:
                if (elements.name != "RightPanel" and elements.name != "LeftPanel") :
                    
                    if elements.name in phantoms_names:
                        if elements.playable == True : 
                            elements.shape.draw(screen,phantoms_color[elements.name])
                        else : # If a vector has already been applied, then it is drawn in gray
                            elements.shape.draw(screen,(170,170,170))
                    else : 
                        elements.shape.draw(screen,(194,86,63))


            level_manager.sprite_manager.update(screen, physics_engine.objects, level_manager.sprites, game_state)
            if level_manager.sprite_manager.keydetected:
                level_manager.sprite_manager.keydetected = False
                game_state = "paused"
                level_manager.attempts_left = 6
                reset_level_vectors(physics_engine.objects)
                for obj in physics_engine.objects:
                    update_mouse(obj, position = Vector2(0,0)) # Reset mouse vector
                if level_manager.current_scene + 1 > level_manager.max_scene:
                    level_manager.load_scene(-2, display_width, display_height, physics_engine,screen)
                    game_state  = "win"
                else:
                    level_manager.load_scene(level_manager.current_scene + 1, display_width, display_height, physics_engine,screen)
            if level_manager.sprite_manager.bonusdetected:
                level_manager.sprite_manager.bonusdetected = False
                
            # Display text elements
            if game_state == "paused" or game_state == "running" :
                screen.blit(level_manager.text_list[0], (0.02 * display_width, 0.15 * display_height))
                screen.blit(level_manager.text_list[1], (0.02 * display_width, 0.30 * display_height))
                screen.blit(level_manager.text_list[2], (0.02 * display_width, 0.35 * display_height))

            # Display user-applied vectors and trajectory prediction
            if game_state == "paused":
                for obj in physics_engine.objects:
                    lines_and_positions(physics_engine.objects, screen, game_state, level_manager.realisticTrajectory)

        # === Buttons ===
        for button in level_manager.button_list:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (
                button.position[0] - button.width / 2 < mouse_x < button.position[0] + button.width / 2 and
                button.position[1] - button.height / 2 < mouse_y < button.position[1] + button.height / 2
            ):
                button.hover(screen)
                if click:
                    play_sound_fx("data/Music/pwomp.mp3" if randint(0, 50) == 30 else "data/Music/click.mp3")
                    button.is_pressed(display_width, display_height, physics_engine,screen)
                    #check the gamestate for the button play/pause
                    if (button.action == "Play" and game_state == "running" ) :
                        game_state = "paused"
                    elif (button.action == "Play" and game_state == "paused" ) :
                        game_state = "running"
                    else :
                        game_state = button.game_state
                    click = False
            elif "data\\Phantoms\\" in  button.image:
                for elem in range (len(physics_engine.objects)) :
                    if (physics_engine.objects[elem].name == button.action):
                        if (physics_engine.objects[elem].applied_coords != [0,0]) :
                            button.hover(screen)
                        else : 
                            button.draw(screen)

            else :
                button.draw(screen)
        
        # Allow for the drawing of the single zone of wind
        vector_zone = Vector2(0,0)
        for obj in physics_engine.objects :
            if len(obj.zone) == 8 and obj.zone[0] == "wind":
                vector_zone = Vector2(obj.zone[1])
                x_left = obj.zone[3]
                x_right = obj.zone[4]
                y_up = obj.zone[5]
                y_down = obj.zone[6]
        if vector_zone != Vector2(0,0) :
            draw_wind_particles(screen, particles, vector_zone, x_left, x_right, y_up, y_down, 1/120,
                            density=30, particle_length=8)
        pygame.display.flip()
        clock.tick(120)

    pygame.quit()
    sys.exit()
