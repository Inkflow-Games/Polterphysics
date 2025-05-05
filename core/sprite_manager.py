import pygame

class SpriteManager:
    """
    A manager for static Pygame sprites.

    Each sprite is simply a surface with an image and a position.
    """

    def __init__(self, key=None):
        self.group = pygame.sprite.Group()
        self.key = key

    def add_image(self, image_path, position, size=(32, 32)):
        """
        Load an image from file, resize it, and add it as a sprite at the given position.

        Parameters:
        image_path (str): Path to the image file.
        position (tuple): (x, y) position where to place the sprite.
        size (tuple): Size to scale the image to (default: (32, 32)).
        """
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, size)
        sprite = pygame.sprite.Sprite() # Crée un Sprite sans sous-classe
        sprite.image = image # Définit l'image
        sprite.rect = image.get_rect(topleft=position) # Définit sa position
        self.group.add(sprite) # Ajoute au groupe

    def update(self, surface, objects):
        """
        Draw all sprites on the given surface.

        Parameters:
        surface (pygame.Surface): The surface on which to draw the sprites.
        """
        self.group.draw(surface)
        self.key.update(objects, surface)

