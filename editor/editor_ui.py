import pygame
import json
from pygame.locals import *
from objects.object import *
from core.level_manager import Button
from data import *

class LevelEditorUI:
    def __init__(self, screen):
        self.screen = screen
        self.selected_object = None
        self.objects_on_level = []

        # Charger les objets disponibles
        with open("Data/objects.json", "r") as f:
            object_data = json.load(f)
            self.available_objects = [
                Object(
                    object_data[id]["name"],
                    object_data[id]["mass"],
                    object_data[id]["position"],
                    object_data[id]["radius"],
                    object_data[id]["max_speed"],
                    object_data[id]["bounciness"],
                    object_data[id]["damping_coefficient"],
                    object_data[id]["static"]
                ) for id in object_data
            ]

    def draw(self):
        """ Affiche l'interface de l'éditeur de niveau """
        self.screen.fill((0, 0, 0))  # Fond noir
        self.draw_left_panel()
        self.draw_right_panel()

        # Afficher les objets placés sur le niveau
        for obj in self.objects_on_level:
            pygame.draw.circle(self.screen, (255, 0, 0), (int(obj.position.x), int(obj.position.y)), obj.radius)

        # Si un objet est sélectionné, l'afficher à l'endroit du clic
        if self.selected_object:
            pygame.draw.circle(self.screen, (0, 255, 0), (int(self.selected_object.position.x), int(self.selected_object.position.y)), self.selected_object.radius)

        pygame.display.flip()

    def draw_left_panel(self):
        pygame.draw.rect(self.screen, (50, 50, 50), (0, 0, 360, 1080))  # Panneau latéral gauche
        pygame.draw.rect(self.screen, (100, 100, 100), (0, 0, 360, 1080), 10)

        y_offset = 30
        FIXED_MARGIN = 20
        for obj in self.available_objects:
            pygame.draw.circle(self.screen, (255, 0, 0), (180, y_offset + obj.radius), obj.radius)
            y_offset += obj.radius * 2 + FIXED_MARGIN

    def draw_right_panel(self):
        """ Dessine les informations de l'objet sélectionné dans le panneau de droite """
        pygame.draw.rect(self.screen, (50, 50, 50), (1560, 0, 360, 1080))  # Fond du panneau
        pygame.draw.rect(self.screen, (100, 100, 100), (1560, 0, 360, 1080), 10)  # Bordure

        # Afficher les informations sur l'objet sélectionné
        font = pygame.font.SysFont(None, 36)
        if self.selected_object:  # Si un objet est sélectionné
            text = font.render(f"Objet : {self.selected_object}", True, (255, 255, 255))
            size_text = font.render(f"Taille : {self.selected_object.radius}", True, (255, 255, 255))
            self.screen.blit(size_text, (1580, 100))
        else:
            text = font.render("None", True, (255, 255, 255))
        self.screen.blit(text, (1580, 50))
