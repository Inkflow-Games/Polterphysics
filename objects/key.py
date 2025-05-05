import pygame
from pygame.math import Vector2

class Key:
    """
    A class representing a key object in the game.

    Attributes:
    coordinates (list): The coordinates of the key in the game world.
    detection_radius (float): The radius within which the key can be detected.
    end_object_name (str): The name of the object that the key unlocks.
    """

    def __init__(self, coordinates=[0, 0], detection_radius=0, end_object_name=""):
        self.coordinates = Vector2(coordinates)
        self.detection_radius = detection_radius
        self.end_object_name = end_object_name
        self.sprite_path = "data/Decor/key.png"
        self.image = pygame.image.load(self.sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=(self.coordinates[0], self.coordinates[1]))

    def display(self, screen):
        """
        Display the key sprite on the given surface.

        Parameters:
        surface (pygame.Surface): The surface on which to draw the key.
        """
        screen.blit(self.image, self.rect)

    def update(self, objects, screen) :
        self.display(screen)
        for object in objects :
            if object.name == self.end_object_name :
                if self.coordinates.distance_to(object.shape.centroid) <= self.detection_radius :
                    print("Key detected")