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
            mouse_position[0] - clicked_object.position[0],
            mouse_position[1] - clicked_object.position[1]
        )
        clicked_object.apply_force(force_vector)
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







# WIDTH = 1000
# HEIGHT = 500
# fps = 60
# timer = pygame.time.Clock()
# screen = pygame.display.set_mode([WIDTH,HEIGHT])


# ghost_image = pygame.image.load("assets/sprites/sprite_ghost.png")
# ghost_image = pygame.transform.scale(ghost_image, (100, 100))

# is_possessing = False
# click_ready = True


# run = True
# while run :
#     screen.fill('white')
#     timer.tick(fps)
#     pygame.mouse.set_visible(False) #make the mouse cursor invisible
#     mouse_position = pygame.mouse.get_pos() #obtain the position of the mouse in real time and store it in an array
#     mouse_x = mouse_position[0] #can be deleted if not necessary for the calculations of the forces
#     mouse_y = mouse_position[1] #can be deleted if not necessary for the calculations of the forces
    
    
#     # not useful at the moment (--> use of an event for possession)
#     left_clicked = pygame.mouse.get_pressed()[0] #return a boolean : if left click is pressed or not (maintaining keep returning True)  
    
    
    
    
#     if is_possessing is False:
#         screen.blit(ghost_image, (mouse_x - ghost_image.get_width() // 2, mouse_y - ghost_image.get_height() // 2))  #display the ghost sprite such that the mouse is the center of the sprite
    
    
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
            
            
#         # At the pressure of left click, possession state changes
#         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and click_ready: # "DOWN" = button pressed ; "button == 1" = left click is pressed
#             is_possessing = not is_possessing  # possession state change
#             click_ready = False  # if left click is maintained, the possession state cannot be changed until the release of it

#         if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # "UP" = release of the button
#             click_ready = True  # once left click is released, give the permission to change the state of possession again
    
#     pygame.display.flip()
# pygame.quit()