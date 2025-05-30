"""
POLTERPHYSICS
sprite_manager.py

A script that defines a SpriteManager class used for updating objects sprites and the Key object.
Features:
- Draws static sprites on the screen.
- Updates a key object if assigned.
- Detects if the key is detected during the update phase.
- Optionally manages a bonus object.


Last Updated: May 2025
Python Version: 3.12+
Dependencies: pygame, core.level_manager
"""

import pygame
import core.level_manager as level_manager

class SpriteManager:
    """
    Manages static Pygame sprites and updates a key object if assigned.
    This class is useful for drawing background or UI elements, and optionally linking
    a `Key` object to trigger detection logic during the update phase.

    Attributes:
    group (pygame.sprite.Group): Group containing all static sprites to render.
    key (Key or None): Optional key object managed alongside sprites.
    detected (bool): Flag set to True if the associated key is detected.
    """

    def __init__(self, key=None, bonus=None):
        """
        Initializes the sprite manager.

        Parameters:
        key (Key, Bonus, optional): A key object and a bonus to be updated alongside the sprite group.
        """
        self.key = key
        self.bonus = bonus
        self.keydetected = False
        self.bonusdetected = False


    def draw_sprites(self, sprites = None, screen = None, game_state = None):
        """
        Loads and draws sprites on the given screen based on the provided sprite data.

        Parameters:
        sprites (dict): Dictionary containing sprite data with keys as sprite names and values as dictionaries
        screen (pygame.Surface): Surface on which to render the sprites.
        """
        if sprites == None :
            # Draw default background image based on realisticTrajectory setting
            if level_manager.realisticTrajectory == False :
                image = pygame.image.load("data/Decor/Box.png").convert_alpha()
                screen.blit(image, (1101, 858))
            else :
                image = pygame.image.load("data/Decor/BoxTicked.png").convert_alpha()
                screen.blit(image, (1100, 850))
        else :
            for sprite_name, data in sprites.items():
                # Draw Play or Pause icon based on game state
                if (game_state == "running" and sprite_name == "Play") :
                    image = pygame.image.load("data/Decor/PlayIcon.png").convert_alpha()
                    rotated_image = pygame.transform.rotate(image, data.get("rotation", 0))
                    rect = rotated_image.get_rect(center=tuple(data["coordinates"]))
                    screen.blit(rotated_image, rect)
                elif(game_state == "paused" and sprite_name == "Paused") :
                    image = pygame.image.load("data/Decor/PauseIcon.png").convert_alpha()
                    rotated_image = pygame.transform.rotate(image, data.get("rotation", 0))
                    rect = rotated_image.get_rect(center=tuple(data["coordinates"]))
                    screen.blit(rotated_image, rect)
            


    def update(self, surface, objects, sprites, game_state):
        """
        Draws all sprites in the group on the surface and updates the key if present.
        If the key becomes detected during the update, sets the manager's `detected` flag.

        Parameters:
        surface (pygame.Surface): Surface on which to render the sprites.
        objects (list): List of game objects passed to the key's update method.
        """
        # Draw all managed sprites
        self.draw_sprites(sprites, surface, game_state)

        # Update key detection logic if key is assigned
        if self.key:
            self.key.update(objects, surface)
            if self.key.detected:
                self.key.detected = False
                self.keydetected = True
        if self.bonus and self.bonus.enabled:
            self.bonus.update(objects, surface)
            if self.bonus.detected:
                self.bonus.detected = False
                self.bonusdetected = True

