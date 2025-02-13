import pygame 
pygame.init()

def GetMouseInput() :
    for event in pygame.event.get() :
        return event.type == pygame.MOUSEBUTTONDOWN
