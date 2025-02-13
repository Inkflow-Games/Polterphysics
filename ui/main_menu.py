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
        match self.action :
            case "Play" :
                #run
                print(self.action)
            case "Pause" :
                #pause the game
                print(self.action)
            case "Stop" :
                #close the window
                pygame.quit()


        pass
           
    def hover(self, screen):
        pygame.draw.rect(screen, "red", pygame.Rect(self.position.x - (self.width+5) / 2, self.position.y - (self.height+5) / 2, self.width+5, self.height+5))


    def draw(self, screen):
        pygame.draw.rect(screen, "blue", pygame.Rect(self.position.x - self.width / 2, self.position.y - self.height / 2, self.width, self.height))




