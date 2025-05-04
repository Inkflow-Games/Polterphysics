from tkinter import SEL
import pygame
from objects.object import *
import json
from data import *
from utils.vector_utils import *
# Dictionary storing level numbers as keys and lists of objects as values
import pygame
import core.physics_engine as phy
from core.sound import play_music
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


    def is_pressed(self, display_width, display_height,object_list):
        max_scene = 4
        screen_width, screen_height = display_width, display_height
        global tries
        #Action to perform for the button using a match case to determine the action to do
        match self.action :
            case "Play" :
                self.game_state = "running"
            case "Pause" :
                self.game_state = "paused"
            case "Stop" :
                #close the window
                pygame.quit()
            case "Restart Level":
                self.game_state = "paused"
                tries+=1
                reset_level_vectors(object_list.objects) # Proper reset of all the objects of the scene
                for obj in object_list.objects :
                    update_mouse(obj, position = Vector2(0,0))
                load_scene(current_scene, screen_width, screen_height,object_list)
            case "Next Level" :
                #load_scene(n+1)
                self.game_state = "paused"
                tries = 0
                if (current_scene + 1 > max_scene) : 
                    load_scene(current_scene, screen_width, screen_height,object_list)
                else :
                    load_scene(current_scene+1, screen_width, screen_height,object_list)
            case "Load Main Menu" :
                #load_scene(0)
                self.game_state = "menu"
                load_scene(0, screen_width, screen_height,object_list)
            case "Load Level Menu" :
                #load_scene(1)
                self.game_state = "menu"
                load_scene(1, screen_width, screen_height,object_list)
            case "1" | "2" | "3" :
                self.game_state = "paused"
                tries = 0
                print('qdq')
                load_scene(int(self.action)+1, screen_width, screen_height,object_list)
            case "Option":
                self.game_state = "options"
                load_scene(-1, screen_width, screen_height,object_list)


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
    tutorial_menu_buttons = buttons["tutorial_menu"]

with open("data/levels.json", "r") as f : #load the different objects for the level
    levels = json.load(f)

button_list = []
object_list = []

def load_button(button, screen_width, screen_height):
    new_button = Button(
        size=button["size"],
        image=button["image"],
        imageHover=button["imageHover"],
        position=Vector2(button["position"][0]*screen_width, button["position"][1]*screen_height),
        height=button["height"],
        width=button["width"],
        action=button["action"]
        )
    return new_button

def load_objects(object_infos):
    #new =  Object(mass = l[0], position = Vector2(l[1]), max_speed = l[2], radius = l[3],bounciness = l[4], damping_coefficient = l[5], static = l[6])
    #g = Object(False, False, 3, 0.8, None, 50, Vector2(100,100))
    new = Object(polygon=object_infos["polygon"], grabable=object_infos["grabable"], mass=object_infos["mass"], restitution_coefficient=object_infos["restitution_coefficient"], radius=object_infos["radius"], mouse=object_infos["mouse"], applied_coords=object_infos["applied_coords"], applied_angle=object_infos["applied_angle"], simulated=object_infos["simulated"], name=object_infos["name"], centroid=transform_Vector2(object_infos["centroid"])[0], vertices=transform_Vector2(object_infos["vertices"]))
    return new

current_scene = 0

def transform_Vector2(infos) :
    arr = []
    for elem in infos:
        arr.append(Vector2(*elem))
    return arr

playing_music = ""

def load_scene(n: int, screen_width, screen_height,object_list):
    object_list.objects = []
    global current_scene 
    global button_list
    current_scene = n
    button_list = []

    global playing_music
    global background


    match n:
        case -1:  # Tutorial
            for button in tutorial_menu_buttons.values():  
                button_list.append(load_button(button, screen_width, screen_height))
            if playing_music != "data/Music/menu.mp3":
                play_music("data/Music/menu.mp3")
                playing_music = "data/Music/menu.mp3"
        case 0:  # Menu principal
            for button in main_menu_buttons.values():
                button_list.append(load_button(button, screen_width, screen_height))
            if playing_music != "data/Music/menu.mp3":
                play_music("data/Music/menu.mp3")
                playing_music = "data/Music/menu.mp3"
        case _:  # Autres niveaux
            for button in buttons["{}".format(n-1)].values():
               button_list.append(load_button(button, screen_width, screen_height))

            for object in levels["{}".format(n-1)].keys() :
                if object != "background":
                    object_list.add_object(load_objects(levels["{}".format(n-1)][object]))
                else :
                    background = pygame.image.load(levels["{}".format(n-1)][object])
            if playing_music != f"data/Music/level{n-1}.mp3":
                play_music(f"data/Music/level{n-1}.mp3")
                playing_music = f"data/Music/level{n-1}.mp3"

            print("level {} loaded".format(n-1))

