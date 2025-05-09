"""
Polterphysics
sprite_manager.py

A script that defines a SpriteManager class used for updating objects sprites and the Key object.

Last Updated: Feb 2025
Python Version: 3.12.9
Dependencies: pygame.math (Vector2), math
"""

import pygame

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


    def draw_sprites(self, sprites, screen):
        """
        Loads and draws sprites on the given screen based on the provided sprite data.

        Parameters:
        sprites (dict): Dictionary containing sprite data with keys as sprite names and values as dictionaries
        screen (pygame.Surface): Surface on which to render the sprites.
        """
        for sprite_name, data in sprites.items():
            image = pygame.image.load(data["path"]).convert_alpha()
            image = pygame.transform.scale(image, tuple(data["size"]))
            rotated_image = pygame.transform.rotate(image, data.get("rotation", 0))
            rect = rotated_image.get_rect(center=tuple(data["coordinates"]))
            screen.blit(rotated_image, rect)


    def update(self, surface, objects, sprites):
        """
        Draws all sprites in the group on the surface and updates the key if present.
        If the key becomes detected during the update, sets the manager's `detected` flag.

        Parameters:
        surface (pygame.Surface): Surface on which to render the sprites.
        objects (list): List of game objects passed to the key's update method.
        """
        # Draw all managed sprites
        self.draw_sprites(sprites, surface)

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

