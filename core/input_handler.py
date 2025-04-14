import pygame 
from pygame.math import Vector2
from utils.vector_utils import * 
from core.collision import *
pygame.init()

def GetMouseInput(event) :
    return event.type == pygame.MOUSEBUTTONDOWN #autorise qu'un seul clic gauche jusqu'au relachement de la touche  --> on peut pas maintenir la touche pour faire clic gauche continuellement

#verifies if the mouse is in the radius of a clicked circle
def is_point_in_circle(point, circle_center, radius):
    dx = point[0] - circle_center[0]
    dy = point[1] - circle_center[1]
    return dx**2 + dy**2 <= radius**2


def vector_application(
    event, 
    test_object, second_object,
    clicked_object, vector_applied1, vector_applied2, 
    vector1_coords, vector2_coords, 
    vector1_angle, vector2_angle
):
    mouse_position = pygame.mouse.get_pos()

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if (test_object.polygon == False) :

            if is_point_in_circle(mouse_position, test_object.shape.centroid, test_object.shape.radius):
                clicked_object = test_object
                if vector_applied1:
                    force_vector = -vector1_coords
                    test_object.apply_force(force_vector)
                    vector_applied1 = False
                    vector1_coords = Vector2(0, 0)

        elif is_point_in_circle(mouse_position, second_object.shape.centroid, second_object.shape.radius):
            clicked_object = second_object
            if vector_applied2:
                force_vector = -vector2_coords
                second_object.apply_force(force_vector)
                vector_applied2 = False
                vector2_coords = Vector2(0, 0)

    elif event.type == pygame.MOUSEMOTION and clicked_object is not None:
        pass  # Rien à faire ici, mais tu peux gérer un affichage de curseur par exemple

    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and clicked_object is not None:
        force_vector = Vector2(
            mouse_position[0] - clicked_object.shape.centroid[0],
            mouse_position[1] - clicked_object.shape.centroid[1]
        )
        clicked_object.shape.apply_force(force_vector)
        print(f"Force applied : {force_vector}")

        if clicked_object == test_object:
            vector_applied1 = True
            vector1_coords = force_vector
            vector1_angle = compute_angle(vector1_coords.x, vector1_coords.y)
        elif clicked_object == second_object:
            vector_applied2 = True
            vector2_coords = force_vector
            vector2_angle = compute_angle(vector2_coords.x, vector2_coords.y)

        clicked_object = None

    return clicked_object, vector_applied1, vector_applied2, vector1_coords, vector2_coords, vector1_angle, vector2_angle, mouse_position

