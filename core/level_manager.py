import pygame
from objects.object import *
import json
from Data import *
# Dictionary storing level numbers as keys and lists of objects as values
levels = {1: [], 2: [],3:[]}  # The ground is assumed to be a non-possessable object

# Global variable to track the current level

current_level = 0
button_list = []

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
    global current_level  
    if n is None:
        n = current_level + 1
    current_level = n
    return current_level

def load_scene(n: int):
    match n :
        case 0 :
            for button in main
        case 1 :
            pass
        case 2 :
            pass
        case 3 :
            pass
        case 4 :
            pass

