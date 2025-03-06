import pygame
import core.level_manager as lmanager

class Button:
    def __init__(self, size, position, height, width, action=''):
        self.size = size
        self.position = position
        self.height = height
        self.width = width
        self.action = action
        self.game_state = ""


    def is_pressed(self):
        
        #Action to perform for the button using a match case to determine the action to do
        match self.action :
            case "Play" :
                self.game_state = "running"
                print("game's running")
            case "Pause" :
                self.game_state = "paused"
                print("game's paused")
            case "Stop" :
                #close the window
                pygame.quit()
            case "Load Main Menu" :
                #load_scene(0)
                lmanager.load_scene(0)
            case "Load Level Menu" :
                #load_scene(1)
                lmanager.load_scene(1)
            case "Level1" :
                #load_scene(2)
                lmanager.load_scene(2)
            case "Level2" :
                #load_scene(3)
                lmanager.load_scene(3)
            case "Level3" :
                #load_scene(4)
                lmanager.load_scene(4)
           
    def hover(self, screen):
        pygame.draw.rect(screen, "red", pygame.Rect(self.position.x - (self.width+5) / 2, self.position.y - (self.height+5) / 2, self.width+5, self.height+5))


    def draw(self, screen):
        pygame.draw.rect(screen, "blue", pygame.Rect(self.position.x - self.width / 2, self.position.y - self.height / 2, self.width, self.height))




