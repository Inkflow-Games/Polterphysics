import pygame
from objects.object import *
import json
#from ui.main_menu import *
from Data import *
# Dictionary storing level numbers as keys and lists of objects as values
import pygame
import core.level_manager as lmanager

class Button:
    def __init__(self, image, image2,  size, position, height, width, action=''):
        self.size = size
        self.image = image
        self.image2 = image2
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
        #pygame.draw.rect(screen, "red", pygame.Rect(self.position.x - (self.width+5) / 2, self.position.y - (self.height+5) / 2, self.width+5, self.height+5))
        screen.blit(pygame.image.load(self.image2).convert(), (self.position.x - (self.width+5)/2, self.position.y - (self.height+5)/2))


    def draw(self, screen):
        #pygame.draw.rect(screen, "blue", pygame.Rect(self.position.x - self.width / 2, self.position.y - self.height / 2, self.width, self.height))
        screen.blit(pygame.image.load(self.image).convert(), (self.position.x - (self.width+5)/2, self.position.y - (self.height+5)/2))
        pass




levels = {1: [], 2: [],3:[]}  # The ground is assumed to be a non-possessable object

# Global variable to track the current level

with open("Data/buttons.json", "r") as file :
    buttons = json.load(file)
    main_menu_buttons = buttons["main_menu"]
    level_menu_buttons = buttons["level_selection"]
    level_1 = buttons["level1"]
    level_2 = buttons["level2"]
    level_3 = buttons["level3"]

def scene_selector(n: int = None) -> int:
    """
    Changes the current level.
    If no argument is given, it increments the current level by 1.

    :param n: The new level number (optional, defaults to current_level + 1)
    :return: The updated level number
    """

button_list = []

def load_scene(n: int):
    global button_list
    
    match n:
        case 0:
            button_list = []
            for button in main_menu_buttons.values():
                new_button = Button(
                    size=button["size"],
                    image=button["image"],
                    image2=button["image2"],
                    position=Vector2(button["position"][0], button["position"][1]),
                    height=button["height"],
                    width=button["width"],
                    action=button["action"]
                )
                button_list.append(new_button)
            print("main menu loaded", len(button_list))

        case 1:
            button_list = []
            for button in level_menu_buttons.values():
                new_button = Button(
                    size=button["size"],
                    image=button["image"],
                    image2=button["image2"],
                    position=Vector2(button["position"][0], button["position"][1]),
                    height=button["height"],
                    width=button["width"],
                    action=button["action"]
                )
                button_list.append(new_button)
            print("level manager loaded", len(button_list))

        case 2:
            button_list = []
            for button in level_1.values():
                new_button = Button(
                    size=button["size"],
                    image=button["image"],
                    image2=button["image2"],
                    position=Vector2(button["position"][0], button["position"][1]),
                    height=button["height"],
                    width=button["width"],
                    action=button["action"]
                )
                button_list.append(new_button)
            print("level 1 loaded")

        case 3:
            button_list = []
            for button in level_2.values():
                new_button = Button(
                    size=button["size"],
                    image=button["image"],
                    image2=button["image2"],
                    position=Vector2(button["position"][0], button["position"][1]),
                    height=button["height"],
                    width=button["width"],
                    action=button["action"]
                )
                button_list.append(new_button)
            print("level 2 loaded")

        case 4:
            button_list = []
            for button in level_3.values():
                new_button = Button(
                    size=button["size"],
                    image=button["image"],
                    image2=button["image2"],
                    position=Vector2(button["position"][0], button["position"][1]),
                    height=button["height"],
                    width=button["width"],
                    action=button["action"]
                )
                button_list.append(new_button)
            print("level 3 loaded")

        case _:
            print(f"Scene {n} not recognized")

