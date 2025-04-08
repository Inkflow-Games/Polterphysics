"""
Polterphysics
level_manager.py

A script that handle the different scenes and change of them
Features include:
- Button class
- Handleing button behaviour
- Loading the objects corresponding to the scene

Last Updated: Apr 2025
Python Version: 3.12.9
Dependencies: pygame, core.sound, data, objects.object
"""
import pygame
from objects.object import *
import json
from data import *
# Dictionary storing level numbers as keys and lists of objects as values
import pygame
from core.sound import play_music

class Button:
    """
    A class representing a Button.

    This class defines the structure and behavior of the object, including its
    attributes, methods, and any necessary calculations or interactions.

    Attributes:
        image (string): The path to the image which is display for the button
        imageHover (string): The path to the image which is diplay while the button is hovered
        position (array of int): representing the x and y position for the button with coefficients (0 to 1)
        height (int) : representing the height of the image
        width (int) : representing the width of the image
        action (string) : a string representing the action of the button

    Methods:
        is_pressed(self, display_width, display_height): The function called when a button is pressed
        hover(self, screen): The function to display the button when hovered
        draw(self, screen): The function to display the button otherwise
    """

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
            case "Pause" :
                self.game_state = "paused"
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
                if (current_scene + 1 > max_scene) : 
                    load_scene(current_scene, screen_width, screen_height)
                else :
                    load_scene(current_scene+1, screen_width, screen_height)
            case "Load Main Menu" :
                #load_scene(0)
                self.game_state = "menu"
                load_scene(0, screen_width, screen_height)
            case "Load Level Menu" :
                #load_scene(1)
                self.game_state = "menu"
                load_scene(1, screen_width, screen_height)
            case "1" | "2" | "3" :
                self.game_state = "paused"
                load_scene(int(self.action)+1, screen_width, screen_height)

                   
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

def load_button(button, screen_width, screen_height):
    """
    This function allow us to turn the button from json dictionnaries to a Button object

    Parameters:
    button (dictionnary): the json of the button we want to load
    screen_width (int): The screen width
    screen_height (int)

    Returns:
    Button: The button now turned into a button object.
    """
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

def load_objects(object):
    """
    This function allow us to turn the json object into objects

    Parameters:
    object (dictionnary): the json of the object we want to load

    Returns:
    Object: The object now turned into a object.
    """
    new =  Object(mass = object[0], position = Vector2(object[1]), max_speed = object[2], radius = object[3],bounciness = object[4], damping_coefficient = object[5], static = object[6])
    return new

current_scene = 0
max_scene = 4
playing_music = ""

def load_scene(n: int, screen_width, screen_height):
    """
    This function allow us to load the correct scene each time

    Parameters:
    n (int): the index of the scene we want
    screen_width (int) : the screen width
    screen_height(int) : the screen height

    """
    global button_list
    global object_list
    global current_scene 
    global playing_music
    display_width, display_height = screen_width, screen_height
    current_scene = n
    object_list = []
    button_list = []
    
    match n:
        case 0: # Loading the main menu
            for button in main_menu_buttons.values(): #loading the buttons we have to draw each frame
                button_list.append(load_button(button, screen_width, screen_height))

            if playing_music != "data/Music/menu.mp3" :
                play_music(f"data/Music/menu.mp3")
                playing_music = "data/Music/menu.mp3"

        case 1: #Loading the level manager menu
            for button in level_menu_buttons.values():
                button_list.append(load_button(button, screen_width, screen_height))
            if playing_music != "data/Music/menu.mp3" :
                play_music(f"data/Music/menu.mp3")
                playing_music = "data/Music/menu.mp3"
            
        case _:  #The default case is used to load the next level each time
            for button in buttons["{}".format(n-1)].values():
               button_list.append(load_button(button, screen_width, screen_height))
            for object in levels["{}".format(n-1)].values() :
                object_list.append(load_objects(object))
            if playing_music != f"data/Music/level{n-1}.mp3" :
                play_music(f"data/Music/level{n-1}.mp3")
                playing_music = f"data/Music/level{n-1}.mp3"

