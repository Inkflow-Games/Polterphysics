from tkinter import SEL
import pygame
from objects.object import *
import json
from data import *
# Dictionary storing level numbers as keys and lists of objects as values
import pygame
import ast
import core.physics_engine as phy

class Button:
    def __init__(self, image, imageHover,  size, position, height, width, action=''):
        self.size = size
        self.image = image
        self.imageHover = imageHover
        self.position = position # It is is percentage to correctly fit for every screen
        self.height = height
        self.width = width
        self.action = action
        self.game_state = ""


    def is_pressed(self, display_width, display_height):
        
        screen_width, screen_height = display_width, display_height
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
            case "Restart Level" :
                #load_scene(n)
                self.game_state = "paused"
                load_scene(current_scene, screen_width, screen_height)
            case "Next Level" :
                #load_scene(n+1)
                self.game_state = "paused"
                load_scene(current_scene+1, screen_width, screen_height)
            case "Load Main Menu" :
                #load_scene(0)
                self.game_state = "menu"
                load_scene(0, screen_width, screen_height)
            case "Load Level Menu" :
                #load_scene(1)
                self.game_state = "menu"
                load_scene(1, screen_width, screen_height)
            case "Level1" :
                #load_scene(2)
                self.game_state = "paused"
                load_scene(2, screen_width, screen_height)
            case "Level2" :
                #load_scene(3)
                self.game_state = "paused"
                load_scene(3, screen_width, screen_height)
            case "Level3" :
                #load_scene(4)
                self.game_state = "paused"
                load_scene(4, screen_width, screen_height)
            case default :
                self.game_state = 'menu'
                load_scene(current_scene, screen_width, screen_height)

           
    def hover(self, screen): # The function which changes the sprite when hovered
        img = pygame.image.load(self.imageHover)
        # img = pygame.transform.scale(img, (self.width, self.height)*self.size)
        screen.blit(img, (self.position.x - (self.width)/2, self.position.y - (self.height)/2))


    def draw(self, screen): # THe way we draw the sprite if not hovered
        img = pygame.image.load(self.image)
        # img = pygame.transform.scale(img, (self.width, self.height)*self.size)
        screen.blit(img, (self.position.x - (self.width)/2, self.position.y - (self.height)/2))
        pass

# Global variable to track the current level

with open("data/buttons.json", "r") as file : #load all the buttons and split them into multiple lists
    buttons = json.load(file)
    main_menu_buttons = buttons["main_menu"]
    level_menu_buttons = buttons["level_selection"]

with open("data/levels.json", "r") as f : #load the different objects for the level
    levels = json.load(f)

button_list = []
object_list = []

def load_button(b, screen_width, screen_height):
    new_button = Button(
        size=b["size"],
        image=b["image"],
        imageHover=b["imageHover"],
        position=Vector2(b["position"][0]*screen_width, b["position"][1]*screen_height),
        height=b["height"],
        width=b["width"],
        action=b["action"]
        )
    return new_button

def load_objects(object_infos):
    #new =  Object(mass = l[0], position = Vector2(l[1]), max_speed = l[2], radius = l[3],bounciness = l[4], damping_coefficient = l[5], static = l[6])
    #g = Object(False, False, 3, 0.8, None, 50, Vector2(100,100))
    print(transform_Vector2(object_infos["centroid"]))
    new = Object(polygon=object_infos["polygon"], static=object_infos["static"], mass=object_infos["mass"], restitution_coefficient=object_infos["restitution_coefficient"], radius=object_infos["radius"], grabable=object_infos["grabable"], name=object_infos["name"], centroid=transform_Vector2(object_infos["centroid"])[0], vertices=transform_Vector2(object_infos["vertices"]))
    return new

current_scene = 0

def transform_Vector2(infos) :
    arr = []
    for elem in infos:
        arr.append(Vector2(*elem))
    return arr

def load_scene(n: int, screen_width, screen_height):
    global button_list
    global object_list
    global current_scene 
    display_width, display_height = screen_width, screen_height
    current_scene = n
    object_list = []
    button_list = []
    
    match n:
        case 0: # Loading the main menu
            for button in main_menu_buttons.values(): #loading the buttons we have to draw each frame
                button_list.append(load_button(button, screen_width, screen_height))
            print("main menu loaded", len(button_list))

        case 1: #Loading the level manager menu
            for button in level_menu_buttons.values():
                button_list.append(load_button(button, screen_width, screen_height))
            print("level manager loaded", len(button_list))

        case _:  #The default case is used to load the next level each time
            for button in buttons["{}".format(n-1)].values():
               button_list.append(load_button(button, screen_width, screen_height))

            for object in levels["{}".format(n-1)].values() :
                object_list.append(load_objects(object))



            print("level {} loaded".format(n-1))

