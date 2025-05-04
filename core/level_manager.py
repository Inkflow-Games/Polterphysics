from tkinter import SEL
import pygame
from objects.object import *
import json
from data import *
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


    def is_pressed(self, display_width, display_height):
        screen_width, screen_height = display_width, display_height
        match self.action:
            case "Play":
                self.game_state = "running"
                print("Le jeu est lancé")
            case "Pause":
                self.game_state = "paused"
                print("Le jeu est en pause")
            case "Stop":
                pygame.quit()
            case "Restart Level":
                self.game_state = "paused"
                load_scene(current_scene, screen_width, screen_height)
            case "Next Level":
                self.game_state = "paused"
                load_scene(current_scene+1, screen_width, screen_height)
            case "Load Main Menu":
                self.game_state = "menu"
                load_scene(0, screen_width, screen_height)
            case "Load Level Menu":
                self.game_state = "menu"
                load_scene(1, screen_width, screen_height)
            case "Level1":
                self.game_state = "paused"
                load_scene(2, screen_width, screen_height)
            case "Level2":
                self.game_state = "paused"
                load_scene(3, screen_width, screen_height)
            case "Level3":
                self.game_state = "paused"
                load_scene(4, screen_width, screen_height)
            case "Option":
                self.game_state = "options"
                load_scene(-1, screen_width, screen_height)  # Load options menu
            case default:
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

def load_objects(l):
    new =  Object(mass = l[0], position = Vector2(l[1]), max_speed = l[2], radius = l[3],bounciness = l[4], damping_coefficient = l[5], static = l[6])
    return new

current_scene = 0

def load_scene(n: int, screen_width, screen_height):
    global button_list
    global object_list
    global current_scene 
    display_width, display_height = screen_width, screen_height
    current_scene = n
    object_list = []
    button_list = []
    
    
playing_music = ""

def load_scene(n: int, screen_width, screen_height):
    global button_list
    global object_list
    global current_scene
    global playing_music
    global background
    display_width, display_height = screen_width, screen_height
    current_scene = n
    object_list = []
    button_list = []

    match n:
        case -1:  # Tutorial
            for button in buttons["tutorial_menu"].values():  
                button_list.append(load_button(button, screen_width, screen_height))
            background = pygame.image.load("data/Background/back1-tuto.png")
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
            for object in levels["{}".format(n-1)].keys():
                if object != "background":
                    object_list.append(load_objects(levels["{}".format(n-1)][object]))
                else:
                    background = pygame.image.load(levels["{}".format(n-1)][object])
            if playing_music != f"data/Music/level{n-1}.mp3":
                play_music(f"data/Music/level{n-1}.mp3")
                playing_music = f"data/Music/level{n-1}.mp3"
