import pygame

class Button:
    def __init__(self, size, position, height, width, action=''):
        self.size = size
        self.position = position
        self.height = height
        self.width = width
        self.action = action
        


    def is_pressed(self):
        #Action to perform for the button using a match case to determine the action to do
        pass
           

    def draw(self, screen):
        pygame.draw.rect(screen, "blue", pygame.Rect(self.position.x - self.width / 2, self.position.y - self.height / 2, self.width, self.height))




