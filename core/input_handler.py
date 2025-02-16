import pygame 
pygame.init()

def GetMouseInput(event) :
    return event.type == pygame.MOUSEBUTTONDOWN
