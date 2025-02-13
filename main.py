import pygame
from pygame.math import Vector2
from ui.main_menu import *
from utils.math_utils import WIDTH, HEIGHT, FPS
import json


pygame.init()


timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Charger les boutons depuis le fichier JSON
with open("data/buttons.json", "r") as file:
    buttons = json.load(file)

# Accéder aux boutons du menu principal
main_menu_buttons = buttons["main_menu"]

# Liste pour stocker les objets Button
button_list = []

# Créer les instances de Button et les ajouter à la liste
for button in main_menu_buttons.values():
    new_button = Button(
        size=button["size"],
        position = Vector2(button["position"][0], button["position"][1]),
        height=button["height"],
        width=button["width"],
        action=button["action"]
    )
    button_list.append(new_button)


run = True
while run:
    # Clear the screen with a white background just once at the beginning of the loop
    screen.fill('white')
    
    # Draw all buttons in the correct order
    for button in button_list:
        if (pygame.mouse.get_pos()[0] < button.position[0] + button.width/2) and (pygame.mouse.get_pos()[0] > button.position[0] - button.width/2) and (pygame.mouse.get_pos()[1] < button.position[1] + button.height/2) and (pygame.mouse.get_pos()[1] > button.position[1] - button.height/2) :
            button.hover(screen)
        else :
            button.draw(screen)


    # Event handling
    for event in pygame.event.get():
        if (event.type == pygame.QUIT) :
            run = False

    # Flip the display to update the screen after everything has been drawn
    pygame.display.flip()

    # Control the frame rate
    timer.tick(FPS)

pygame.quit()