import pygame
import json
from pygame.locals import *
from objects.object import *
from core.level_manager import Button
from data import *

class LevelEditorUI:
    def __init__(self, screen, placed_objects = []):
        self.screen = screen
        self.placed_objects = placed_objects

        # Charger les objets disponibles
        with open("Data/objects.json", "r") as f:
            object_data = json.load(f)
            self.available_objects = [
                Object(
                    polygon=object_data[id]["polygon"],
                    static=object_data[id]["static"],
                    mass=object_data[id]["mass"],
                    restitution_coefficient=object_data[id]["restitution_coefficient"],
                    vertices=(),
                    centroid=Vector2(object_data[id]["centroid"]),
                    radius=object_data[id]["radius"],
                    name=object_data[id]["name"]
                ) for id in object_data
            ]

    def draw(self, selected_object=None):
        """ Affiche l'interface de l'éditeur de niveau """
        self.screen.fill((0, 0, 0))  # Fond noir
        self.draw_left_panel()
        self.draw_right_panel(selected_object)

    def draw_left_panel(self):
        pygame.draw.rect(self.screen, (50, 50, 50), (0, 0, 360, 1080))  # Panneau latéral gauche
        pygame.draw.rect(self.screen, (100, 100, 100), (0, 0, 360, 1080), 10)

        y_offset = 30
        FIXED_MARGIN = 20
        for obj in self.available_objects:
            pygame.draw.circle(self.screen, (255, 0, 0), (180, y_offset + obj.shape.radius), obj.shape.radius)
            y_offset += obj.shape.radius * 2 + FIXED_MARGIN

    def draw_right_panel(self, selected_object):
        """ Dessine les informations de l'objet sélectionné dans le panneau de droite """
        pygame.draw.rect(self.screen, (50, 50, 50), (1560, 0, 360, 1080))  # Fond du panneau
        pygame.draw.rect(self.screen, (100, 100, 100), (1560, 0, 360, 1080), 10)  # Bordure

        # Afficher les informations sur l'objet sélectionné
        font = pygame.font.SysFont(None, 36)
        if selected_object:  # Si un objet est sélectionné
            text = font.render(f"Objet : {selected_object.name}", True, (255, 255, 255))
            size_text = font.render(f"Taille : {selected_object.shape.radius}", True, (255, 255, 255))
            self.screen.blit(size_text, (1580, 100))
        else:
            text = font.render("None", True, (255, 255, 255))
        self.screen.blit(text, (1580, 50))
