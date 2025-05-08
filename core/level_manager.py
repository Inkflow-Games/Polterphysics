"""
Polterphysics
level_manager.py

A script that handles the different scenes and transitions between them.
Features include:
- Button class
- Handling button behaviour
- Loading the objects corresponding to each scene

Last Updated: Apr 2025
Python Version: 3.12.9
Dependencies: pygame, core.sound, data, objects.object
"""

import pygame
import json

from objects.object import *
from data import *
from utils import sprites_utils
from utils.vector_utils import *
from core.sound import play_music
from objects.key import Key
from core.sprite_manager import SpriteManager


# === Load Buttons and Levels from JSON Files ===
with open("data/buttons.json", "r") as file:
    buttons = json.load(file)
    main_menu_buttons = buttons["main_menu"]
    tutorial_menu_buttons = buttons["tutorial_menu"]
    game_over_buttons = buttons["game_over"]
    win_buttons = buttons["win"]

with open("data/levels.json", "r") as f:
    levels = json.load(f)

# === Global Variables ===
button_list = []
object_list = []
current_scene = 0
max_scene = 4
playing_music = ""
tries = 0


class Button:
    """
    A class representing a clickable Button on the screen.

    This class defines a button with associated images, position, and action.
    It can detect clicks and determine whether it's being hovered.

    Attributes:
        image (str): Path to the normal image.
        imageHover (str): Path to the hover image.
        position (Vector2): Button position (as ratio of screen size).
        height (int): Height of the button.
        width (int): Width of the button.
        action (str): Action associated with this button.
        size (float): Scale factor (from JSON).
        game_state (str): Current game state after pressing the button.

    Methods:
        is_pressed(display_width, display_height, object_list): Handle click on the button.
        hover(screen): Draw hover image.
        draw(screen): Draw default image.
    """

    def __init__(self, image, imageHover,  size, position, height, width, action=''):
        self.size = size
        self.image = image
        self.imageHover = imageHover
        self.position = position
        self.height = height
        self.width = width
        self.action = action
        self.game_state = ""


    def is_pressed(self, display_width, display_height, object_list):
        """
        Handles the action associated with a button click.
        Uses a match-case to select the corresponding behavior.
        """
        max_scene = 4
        screen_width, screen_height = display_width, display_height
        global attempts_left

        match self.action :
            case "Play" :
                self.game_state = "running"

            case "Pause" :
                self.game_state = "paused"

            case "Stop" :
                pygame.quit()

            case "Restart Level":
                self.game_state = "paused"
                attempts_left -= 1
                reset_level_vectors(object_list.objects)
                for obj in object_list.objects:
                    update_mouse(obj, position = Vector2(0,0)) # Reset mouse vector
                if (attempts_left == 0) :
                    game_over(screen_width, screen_height, object_list)
                    self.game_state = "game_over"
                else :
                    load_scene(current_scene, screen_width, screen_height, object_list)

            case "Next Level" :
                attempts_left = 3
                reset_level_vectors(object_list.objects)
                for obj in object_list.objects:
                    update_mouse(obj, position = Vector2(0,0)) # Reset mouse vector
                if (current_scene + 1 > max_scene) : 
                    load_scene(-2, screen_width, screen_height, object_list)
                    self.game_state = "win"
                else :
                    self.game_state = "paused"
                    load_scene(current_scene + 1, screen_width, screen_height, object_list)

            case "Load Main Menu" :
                self.game_state = "menu"
                load_scene(0, screen_width, screen_height, object_list)

            case "1" | "2" | "3" :
                self.game_state = "paused"
                attempts_left = 3
                load_scene(int(self.action) + 1, screen_width, screen_height, object_list)

            case "Option":
                self.game_state = "options"
                load_scene(-1, screen_width, screen_height, object_list)

            case "Ballman" | "Polter" | "Rospirit" :
                for obj in object_list.objects :
                    if obj.name == self.action : 
                        update_mouse(obj)
                        update_vector(obj)
                self.game_state = "paused"
            case "Fathome" :
                for obj in object_list.objects :
                    if obj.name == "Fathome" : 
                        update_mouse(obj)
                        update_vector(obj)
                self.game_state = "paused"
            case "Trickandle" :
                for obj in object_list.objects :
                    if obj.name == "Trickandle" : 
                        update_mouse(obj)
                        update_vector(obj)
                self.game_state = "paused"


    def hover(self, screen):
        """
        Draws the hover image of the button on the screen.
        """
        img = pygame.image.load(self.imageHover)
        if self.action in sprites_utils.phantoms_names :
            screen.blit(img, (self.position.x - (self.width)/1.5, self.position.y - (self.height)/1.5))
        else :
            screen.blit(img, (self.position.x - (self.width)/2, self.position.y - (self.height)/2))


    def draw(self, screen):
        """
        Draws the default image of the button on the screen.
        """
        img = pygame.image.load(self.image)
        screen.blit(img, (self.position.x - (self.width)/2, self.position.y - (self.height)/2))
        pass


def load_button(button, screen_width, screen_height):
    """
    Convert a JSON-defined button into a Button object.

    Parameters:
    button (dict): Button info from JSON.
    screen_width (int): Width of the screen.
    screen_height (int): Height of the screen.

    Returns:
    Button: The Button object.
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


def load_objects(object_infos):
    """
    Convert JSON data into an Object instance.

    Parameters:
    object_infos (dict): Dictionary from JSON file.

    Returns:
    Object: The constructed physics object.
    """
    new = Object(
        polygon=object_infos["polygon"],
        grabable=object_infos["grabable"],
        mass=object_infos["mass"],
        restitution_coefficient=object_infos["restitution_coefficient"],
        radius=object_infos["radius"],
        mouse=object_infos["mouse"],
        applied_coords=object_infos["applied_coords"],
        applied_angle=object_infos["applied_angle"],
        simulated=object_infos["simulated"],
        name=object_infos["name"],
        centroid=transform_Vector2(object_infos["centroid"])[0],
        vertices=transform_Vector2(object_infos["vertices"]),
        zone=object_infos["zone"],
        playable=True
    )
    return new


def transform_Vector2(infos):
    """
    Convert a list of [x, y] into a list of Vector2.

    Parameters:
    infos (list): List of coordinate pairs.

    Returns:
    list: List of Vector2 instances.
    """
    arr = []
    for elem in infos:
        arr.append(Vector2(*elem))
    return arr

def game_over(screen_width, screen_height, object_list):
    """
    End the try and display the game over screen

    Parameters:
    screen_width (int): Width of the screen.
    screen_height (int): Height of the screen.
    object_list (ObjectList): Container for game objects from the physics engine.

    Returns:
    """
    load_scene(-3, screen_width, screen_height, object_list)


def load_scene(n: int, screen_width, screen_height, object_list):
    """
    Load a scene by its index and update global objects/buttons accordingly.

    Parameters:
    n (int): Scene index.
    screen_width (int): Width of the screen.
    screen_height (int): Height of the screen.
    object_list (ObjectList): Container for game objects from the physics engine.
    """
    object_list.objects = []
    global current_scene 
    global button_list
    global playing_music
    global background
    global text_list
    global tries
    global sprite_manager
    global sprites
    key = None

    current_scene = n
    button_list = []
    text_list = []

    match n:
        case -3:  # Game over menu
            for button in game_over_buttons.values():  
                button_list.append(load_button(button, screen_width, screen_height))
            if playing_music != "data/Music/menu.mp3":
                play_music("data/Music/menu.mp3")
                playing_music = "data/Music/menu.mp3"

        case -2:  # Win screen
            for button in win_buttons.values():  
                button_list.append(load_button(button, screen_width, screen_height))
            if playing_music != "data/Music/menu.mp3":
                play_music("data/Music/menu.mp3")
                playing_music = "data/Music/menu.mp3"

        case -1:  # Tutorial menu
            for button in tutorial_menu_buttons.values():  
                button_list.append(load_button(button, screen_width, screen_height))
            if playing_music != "data/Music/menu.mp3":
                play_music("data/Music/menu.mp3")
                playing_music = "data/Music/menu.mp3"

        case 0:  # Main menu
            for button in main_menu_buttons.values():
                button_list.append(load_button(button, screen_width, screen_height))
            if playing_music != "data/Music/menu.mp3":
                play_music("data/Music/menu.mp3")
                playing_music = "data/Music/menu.mp3"

        case _:  # Gameplay levels
            for button in buttons["{}".format(n-1)].values():
                button_list.append(load_button(button, screen_width, screen_height))
            for object in levels["{}".format(n-1)].keys():
                if object == "background":
                    background = pygame.image.load(levels["{}".format(n-1)][object])
                elif object == "key":
                    key = Key(
                        coordinates=levels["{}".format(n-1)][object]["coordinates"],
                        detection_radius=levels["{}".format(n-1)][object]["detection_radius"],
                        end_object_name=levels["{}".format(n-1)][object]["end_object_name"]
                    )
                elif object == "sprites" :
                    sprites = levels["{}".format(n-1)][object]
                else:
                    object_list.add_object(load_objects(levels["{}".format(n-1)][object]))

                sprite_manager = SpriteManager(key)

            if playing_music != f"data/Music/level{n-1}.mp3":
                play_music(f"data/Music/level{n-1}.mp3")
                playing_music = f"data/Music/level{n-1}.mp3"

            # Setup text overlays for level and tries
            font = pygame.font.SysFont("Snap itc", 40)
            font.set_bold(False)
            index_of_the_level = font.render("LEVEL : {}".format(n-1), True, (255, 255, 255))
            number_of_tries = font.render("ATTEMPTS", True, (255, 255, 255))
            number_of_tries2 = font.render("LEFT : {}".format(attempts_left), True, (255, 255, 255))
            text_list.append(index_of_the_level)
            text_list.append(number_of_tries)
            text_list.append(number_of_tries2)
