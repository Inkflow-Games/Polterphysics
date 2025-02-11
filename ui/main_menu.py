import pygame
from core.input_handler import *

clickPress = False
stop_running = False

class Button:
    def __init__(self, size, x, y, height, width, action=''):
        self.size = size
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.action = action
        


    def is_pressed(self):
        #Action to perform for the button using a match case to determine the action to do
        if self.action == "Stop" :
            stop_running = True
           

    def draw(self, screen):
        pygame.draw.rect(screen, "blue", pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height))




