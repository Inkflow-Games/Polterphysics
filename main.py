import pygame
from ui.main_menu import *
from core.input_handler import *
from Data.Buttons import *

pygame.init()


timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

run = True
while run:
    # Clear the screen with a white background just once at the beginning of the loop
    screen.fill('white')
    
    # Draw all buttons in the correct order
    for button in buttons.values():
        button.Button.draw()

    # Event handling
    for event in pygame.event.get():
        if (event.type == pygame.QUIT) or stop_running:
            run = False

    # Flip the display to update the screen after everything has been drawn
    pygame.display.flip()

    # Control the frame rate
    timer.tick(fps)

pygame.quit()

def StopRunning():
    pygame.quit()