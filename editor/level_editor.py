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
        self.selected_object = None  # Pour la modification de taille

    def draw(self):
        """ Affiche l'interface de l'éditeur de niveau """
        self.screen.fill((0, 0, 0))  # Fond noir
        self.ui.draw_left_panel()
        self.ui.draw_right_panel()

        # Afficher les objets placés sur le niveau
        for obj in self.objects_on_level:
            pygame.draw.circle(self.screen, (255, 0, 0), (int(obj.position.x), int(obj.position.y)), obj.radius)

        pygame.display.flip()

    def handle_event(self, event):
        """ Gère les événements de la souris et du clavier """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < 360:  # Si dans la zone de sélection des objets
                self.select_object(mouse_pos)
            else:
                self.start_drag(mouse_pos)

        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                self.update_drag(mouse_pos)  # Mettre à jour la position de l'objet en déplaçant la souris

        elif event.type == pygame.MOUSEBUTTONUP:
            self.end_drag()  # Fin du déplacement de l'objet, relâchement du bouton de la souris

        elif event.type == pygame.KEYDOWN:
            if self.selected_object:
                self.modify_object_size(event)



    def select_object(self, mouse_pos):
        """ Sélectionne un nouvel objet ou change l'objet sélectionné actuel """
        for obj in self.ui.objects:  # Vérifie tous les objets de la liste
            # Calculer la distance entre la souris et l'objet
            distance = math.sqrt((mouse_pos[0] - obj.position[0]) ** 2 + (mouse_pos[1] - obj.position[1]) ** 2)

            if distance <= obj.radius:  # Si la souris est dans le rayon de l'objet
                if self.selected_object != obj:  # Si l'objet est différent de l'actuel
                    self.selected_object = obj  # Change l'objet sélectionné
                    print(f"Objet sélectionné : {self.selected_object}")  # Affiche l'objet sélectionné
                break


    def start_drag(self, mouse_pos):
        """ Démarre le déplacement d'un objet sélectionné """
        for obj in self.objects_on_level:
            # Vérifie si la souris est sur l'objet
            distance = math.sqrt((mouse_pos[0] - obj.position[0]) ** 2 + (mouse_pos[1] - obj.position[1]) ** 2)
            if distance <= obj.radius:  # Vérification de la sélection basée sur la distance
                self.selected_object = obj  # Sélectionne l'objet
                self.is_dragging = True  # Commence à déplacer l'objet
                print(f"Début du drag pour l'objet : {obj}")
                break

    
    def update_drag(self, mouse_pos):
        """ Met à jour la position de l'objet en mouvement """
        if self.is_dragging and self.selected_object:
            # Si un objet est sélectionné et qu'on est en train de le déplacer
            self.selected_object.position = mouse_pos  # Met à jour la position de l'objet avec la position de la souris
            print(f"Nouvelle position de l'objet : {self.selected_object.position}")


    
    def stop_drag(self):
        """ Arrête le déplacement de l'objet """
        if self.is_dragging:
            self.is_dragging = False  # On arrête de déplacer l'objet
            print(f"Fin du drag, objet final : {self.selected_object}")





    def modify_object_size(self, event):
        """ Permet d'agrandir ou rétrécir un objet sélectionné """
        if event.key == pygame.K_UP:
            self.selected_object.radius += 5
        elif event.key == pygame.K_DOWN:
            self.selected_object.radius = max(5, self.selected_object.radius - 5)

    def save_level(self, path="Data/levels.json"):
        """ Sauvegarde les objets du niveau dans un fichier JSON """
        level_data = []
        for obj in self.objects_on_level:
            level_data.append({
                'name': obj.name,
                'position': [obj.position[0], obj.position[1]],
                'radius': obj.radius,
            })

        with open(path, 'w') as f:
            json.dump(level_data, f, indent=4)
