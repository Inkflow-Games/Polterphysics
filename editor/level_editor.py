import pygame
import json
from objects.object import Object
from editor.editor_ui import *


class LevelEditor:
    def __init__(self, screen):
        self.screen = screen
        self.ui = LevelEditorUI(screen)
        self.objects_on_level = []
        self.is_dragging = False
        self.current_object = None

    def draw(self):
        """ Affiche l'interface de l'éditeur de niveau """
        self.screen.fill((0, 0, 0))  # Fond noir
        self.ui.draw_side_panel()

        # Afficher les objets placés sur le niveau
        for obj in self.objects_on_level:
            sprite = pygame.image.load(obj.sprite)
            sprite = pygame.transform.scale(sprite, (obj.width, obj.height))
            self.screen.blit(sprite, obj.position)

        pygame.display.flip()

    def handle_event(self, event):
        """ Gère les événements de la souris et du clavier """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < 600:  # Si on est dans le panneau latéral
                self.select_object(mouse_pos)

        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            if self.current_object:
                mouse_pos = pygame.mouse.get_pos()
                self.current_object.position = mouse_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False

    def select_object(self, mouse_pos):
        """ Sélectionne un objet dans le panneau latéral pour le déplacer dans l'éditeur """
        for obj in self.ui.objects:
            if obj.sprite.get_rect(topleft=(obj.x, obj.y)).collidepoint(mouse_pos):
                self.is_dragging = True
                self.current_object = obj
                self.objects_on_level.append(Object(self.current_object.mass, mouse_pos))
                break

    def save_level(self, path="Data/levels.json"):
        """ Sauvegarde les objets du niveau dans un fichier JSON """
        level_data = []
        for obj in self.objects_on_level:
            level_data.append({
                'name': obj.name,
                'position': [obj.position.x, obj.position.y],
                'sprite': obj.sprite,
            })

        with open(path, 'w') as f:
            json.dump(level_data, f, indent=4)
