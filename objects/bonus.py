"""
Polterphysics
bonus.py

A script that defines a Bonus class used for giving the player extra launch.

Last Updated: May 2025
Python Version: 3.12.9
Dependencies: pygame.math (Vector2), math
"""

import pygame
from pygame.math import Vector2

class Bonus:
    """
    Represents a Bonus in the game world

    Attributes:
    coordinates (Vector2): Position of the bonus's top-left corner in the game world.
    detection_radius (float): Radius within which the bonus detects a matching object.
    target (str): Name of the object that needs to touch the bonus.
    sprite_path (str): Path to the bonus's sprite image.
    image (pygame.Surface): Scaled image used for rendering the bonus.
    rect (pygame.Rect): Rectangle representing the image's position on screen.
    center (Vector2): Center point of the bonus image used for detection range.
    detected (bool): Indicates whether the bonus has successfully detected the corresponding object.
    enabled (bool): Indicates whether the bonus has been already used or not, if yes, disable it
    """

    def __init__(self, coordinates=[0, 0], detection_radius=0, target=""):
        self.coordinates = Vector2(coordinates)
        self.detection_radius = detection_radius
        self.target = target
        self.sprite_path = "data/Decor/door.png"
        self.enabled = True
        
        # Load and scale the Bonus image
        self.image = pygame.image.load(self.sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        
        # Define the position of the image on screen
        self.rect = self.image.get_rect(topleft=self.coordinates)
        self.center = Vector2(self.rect.center)
        self.detected = False

    def display(self, screen):
        """
        Renders the Bonus sprite onto the screen.

        Parameters:
        screen (pygame.Surface): The surface on which the Bonus will be drawn.
        """
        screen.blit(self.image, self.rect)

    def update(self, objects, screen):
        """
        Updates the bonus state and displays it on screen.
        Sets `detected` to True if the associated object is within detection radius.

        Parameters:
        objects (list): List of game objects to check for interaction.
        screen (pygame.Surface): Surface on which to draw the bonus.
        """
        if self.enabled :
            self.display(screen)
            for object in objects:
                if object.name == self.target:
                    if self.center.distance_to(object.shape.centroid) <= self.detection_radius:
                        self.detected = True
                        object.playable = True
                        self.enabled = False