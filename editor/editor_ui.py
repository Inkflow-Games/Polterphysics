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
            object_data = json.load(f)
            self.available_objects = [
                Object(
                    object_data[name]["mass"],
                    object_data[name]["position"],
                    object_data[name]["radius"],
                    object_data[name]["max_speed"],
                    object_data[name]["bounciness"],
                    object_data[name]["damping_coefficient"],
                    object_data[name]["static"]
                ) for name in object_data
            ]

    def draw(self):
        """ Affiche l'interface de l'éditeur de niveau """
        self.screen.fill((0, 0, 0))  # Fond noir
        self.ui.draw_left_panel()
        self.ui.draw_right_panel()

        # Afficher les objets placés sur le niveau
        for obj in self.objects_on_level:
            pygame.draw.circle(self.screen, (255, 0, 0), (int(obj.position.x), int(obj.position.y)), obj.radius)

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
        if self.selected_object:  # Si un objet est sélectionné
            print(f"Dessin du panneau de droite avec l'objet {self.selected_object}")
            pygame.draw.rect(self.screen, (50, 50, 50), (1560, 0, 360, 1080))  # Fond du panneau
            pygame.draw.rect(self.screen, (100, 100, 100), (1560, 0, 360, 1080), 10)  # Bordure

            # Afficher les informations sur l'objet sélectionné
            font = pygame.font.SysFont(None, 36)
            text = font.render(f"Objet : {self.selected_object}", True, (255, 255, 255))
            self.screen.blit(text, (1580, 50))

            # Affichage de la taille de l'objet
            size_text = font.render(f"Taille : {self.selected_object.radius}", True, (255, 255, 255))
            self.screen.blit(size_text, (1580, 100))




    def check_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Si clic gauche
                self.handle_click(pygame.mouse.get_pos())

    def handle_click(self, position):
        print(f"Clic détecté à {position}")  # Vérifie bien que la fonction est appelée

        if 0 < position[0] < 360:  # Clic sur le panneau latéral
            y_offset = 10
            for obj in self.available_objects:
                print(f"Test objet à y={y_offset}, rayon={obj.radius}")  # Vérifie les coordonnées de chaque objet
                if y_offset < position[1] < y_offset + obj.radius * 2:
                    self.selected_object = obj
                    print(f"Objet sélectionné : {self.selected_object}")
                    pygame.display.update()  # Force le rafraîchissement
                    break
                y_offset += obj.radius * 2 + 20  # Marge ajoutée
        print(f"Objet sélectionné final : {self.selected_object}")


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
