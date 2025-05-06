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

    def __init__(self, key=None):
        """
        Initializes the sprite manager.

        Parameters:
        key (Key, optional): A key object to be updated alongside the sprite group.
        """
        self.group = pygame.sprite.Group()
        self.key = key
        self.detected = False

    def add_image(self, image_path, position, size=(32, 32)):
        """
        Loads an image, scales it, creates a sprite, and adds it to the group.

        Parameters:
        image_path (str): File path to the image.
        position (tuple): Top-left (x, y) position for placing the sprite.
        size (tuple): Width and height to scale the image to (default: (32, 32)).
        """
        # Load and scale the image
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, size)
        
        # Create a basic Sprite object and assign the image and position
        sprite = pygame.sprite.Sprite()
        sprite.image = image
        sprite.rect = image.get_rect(topleft=position)
        
        # Add the sprite to the group for rendering
        self.group.add(sprite)

    def update(self, surface, objects):
        """
        Draws all sprites in the group on the surface and updates the key if present.
        If the key becomes detected during the update, sets the manager's `detected` flag.

        Parameters:
        surface (pygame.Surface): Surface on which to render the sprites.
        objects (list): List of game objects passed to the key's update method.
        """
        # Draw all managed sprites
        self.group.draw(surface)

        # Update key detection logic if key is assigned
        if self.key:
            self.key.update(objects, surface)
            if self.key.detected:
                self.key.detected = False
                self.detected = True
