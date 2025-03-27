import pygame
import json
import math
from editor.editor_ui import LevelEditorUI
from pygame.locals import *
from objects.object import Object

class LevelEditor:
    def __init__(self, screen, placed_objects = []):
        self.screen = screen
        self.placed_objects = placed_objects
        self.ui = LevelEditorUI(screen, placed_objects)
        self.selected_object = None

    def draw(self):
        """ Affiche l'interface de l'éditeur de niveau """
        self.ui.draw(self.selected_object)

    def handle_event(self, event):
        """ Gère les événements de la souris """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1 :
                if mouse_pos[0] < 360:  # Sélection d'un objet dans le panneau gauche
                    self.select_object(mouse_pos)
                elif self.selected_object and 365 + self.selected_object.radius < mouse_pos[0] < 1555 - self.selected_object.radius :  # Placer l'objet à l'endroit du clic
                    self.place_selected_object(mouse_pos)
            elif event.button == 3:  # Clic droit pour sauvegarder
                self.save_level()

    def select_object(self, mouse_pos):
        """ Sélectionne un nouvel objet dans le panneau gauche """
        y_offset = 30
        FIXED_MARGIN = 20
        for obj in self.ui.available_objects:
            if y_offset < mouse_pos[1] < y_offset + obj.radius * 2:
                self.selected_object = obj
                print(f"Objet sélectionné : {self.selected_object}")
                break
            y_offset += obj.radius * 2 + FIXED_MARGIN
        self.draw()

    def place_selected_object(self, mouse_pos):
        """ Place un objet sélectionné à l'endroit du clic """
        if self.selected_object:
            # Placer l'objet sélectionné à la position du clic
            new_obj = Object(
                self.selected_object.name,
                self.selected_object.mass,
                (mouse_pos[0], mouse_pos[1]),  # Utilise les coordonnées du clic
                self.selected_object.radius,
                self.selected_object.max_speed,
                self.selected_object.bounciness,
                self.selected_object.damping_coefficient,
                self.selected_object.static
            )
            self.placed_objects.append(new_obj)
            print(f"Objet placé à {mouse_pos}")
    
    def display_objects(self):
        """ Affiche les objets placés sur le niveau """
        for obj in self.placed_objects:
            pygame.draw.circle(self.screen, (255, 0, 0), (int(obj.position.x), int(obj.position.y)), obj.radius)
    
    def update(self) :
        """ Met à jour les objets du niveau et les affiche """
        self.draw()
        self.display_objects()
        pygame.display.flip()

    def save_level(self, path="Data/levels.json"):
        """ Sauvegarde les objets du niveau dans un fichier JSON """
        # Créer un dictionnaire pour contenir les niveaux
        with open(path, "r") as file:
            levels_data = json.load(file)

        level_id = str(len(levels_data) + 1)  # ID du niveau à sauvegarder
        level_data = {}

        # Ajoutez les objets placés sur le niveau sous forme de dictionnaire
        id = 1
        for obj in self.placed_objects :
            # Format: "nom_objet": [masse, position, rayon, vitesse_max, rebond, coeff_amortissement, statique]
            level_data[id] = [
                obj.name,
                obj.mass,
                [obj.position.x, obj.position.y],  # Position en [x, y]
                obj.radius,
                obj.max_speed,
                obj.bounciness,
                obj.damping_coefficient,
                obj.static
            ]
            id += 1

        # Ajout de ce niveau au dictionnaire global des niveaux
        levels_data[level_id] = level_data

        # Sauvegarder dans le fichier JSON
        with open(path, 'w') as f:
            json.dump(levels_data, f, indent=4)

        print(f"Niveau sauvegardé dans {path}")
