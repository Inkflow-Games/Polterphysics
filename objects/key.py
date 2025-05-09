"""
Polterphysics
key.py

A script that defines a Key class used for switching to the next in-game level.

Last Updated: Feb 2025
Python Version: 3.12.9
Dependencies: pygame.math (Vector2), math
"""

import pygame
from pygame.math import Vector2
from utils import sprites_utils

class Key:
    """
    Represents a key in the game world, used to travel to the next level.

    Attributes:
    coordinates (Vector2): Position of the key's top-left corner in the game world.
    detection_radius (float): Radius within which the key detects a matching object.
    end_object_name (str): Name of the object that needs to touch the key.
    sprite_path (str): Path to the key's sprite image.
    image (pygame.Surface): Scaled image used for rendering the key.
    rect (pygame.Rect): Rectangle representing the image's position on screen.
    center (Vector2): Center point of the key image used for detection range.
    detected (bool): Indicates whether the key has successfully detected the corresponding object.
    """

    def __init__(self, coordinates=[0, 0], detection_radius=0, end_object_name=""):
        self.coordinates = Vector2(coordinates)
        self.detection_radius = detection_radius
        self.end_object_name = end_object_name
        self.sprite_path = ["data/Decor/polter_key.png","data/Decor/ballman_key.png" ,"data/Decor/rospirit_key.png" ,"data/Decor/trickandle_key.png" ,"data/Decor/fathome_key.png" ]
        # Load and scale the key image
        for i in range (0, len(sprites_utils.phantoms_names)):
            if (sprites_utils.phantoms_names[i] == end_object_name) :
                self.image = pygame.image.load(self.sprite_path[i]).convert_alpha()
                self.image = pygame.transform.scale(self.image, (100, 100))
        
        # Define the position of the image on screen
        self.rect = self.image.get_rect(topleft=self.coordinates)
        self.center = Vector2(self.rect.center)
        self.detected = False

    def display(self, screen):
        """
        Renders the key sprite onto the screen.

        Parameters:
        screen (pygame.Surface): The surface on which the key will be drawn.
        """
        screen.blit(self.image, self.rect)

    def update(self, objects, screen):
        """
        Updates the key state and displays it on screen.
        Sets `detected` to True if the associated object is within detection radius.

        Parameters:
        objects (list): List of game objects to check for interaction.
        screen (pygame.Surface): Surface on which to draw the key.
        """
        self.display(screen)
        for object in objects:
            if object.name == self.end_object_name:
                if self.center.distance_to(object.shape.centroid) <= self.detection_radius:
                    self.detected = True
