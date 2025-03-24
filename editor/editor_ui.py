# editor/editor_ui.py
import pygame
import json
from pygame.locals import *
from objects.object import *
from core.level_manager import Button
from data import *

class LevelEditorUI:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.selected_object = None

        # Charger les objets disponibles
        with open("Data/objects.json", "r") as f:
            object_data = json.load(f) # Dictionary of dictionaries
            self.available_objects = [Object(object_data[name]["mass"], object_data[name]["position"], object_data[name]["radius"], object_data[name]["max_speed"], object_data[name]["bounciness"], object_data[name]["damping_coefficient"], object_data[name]["static"]) for name in object_data]

    def draw(self):
        self.screen.fill((50, 50, 50))
        # Dessiner les objets disponibles à gauche
        self.draw_side_panel()

    def draw_side_panel(self):
        pygame.draw.rect(self.screen, (100, 100, 100), (600, 0, 200, 600))  # Le panneau latéral
        y_offset = 10
        for obj in self.available_objects:
            # Simuler un sprite
            pygame.draw.circle(self.screen, (255, 0, 0), (610, y_offset + 25), 20)  # Représente l'objet
            y_offset += 60

    def check_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Si clic gauche
                self.handle_click(pygame.mouse.get_pos())

    def handle_click(self, position):
        # Si un objet dans la liste est cliqué, sélectionne-le
        if 600 < position[0] < 800:  # Clic sur le panneau latéral
            y_offset = 10
            for obj in self.available_objects:
                if y_offset < position[1] < y_offset + 60:
                    self.selected_object = obj
                    break
                y_offset += 60

    def save_level(self):
        level_data = []
        for obj in self.objects:
            level_data.append({
                'mass': obj.mass,
                'position': [obj.position.x, obj.position.y],
                'radius': obj.radius,
                'max_speed': obj.max_speed,
                'bounciness': obj.bounciness,
                'damping_coefficient': obj.damping_coefficient,
                'static': obj.static
            })
        with open('Data/levels.json', 'w') as f:
            json.dump({'level_1': level_data}, f)
