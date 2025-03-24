import pygame
import json
from objects.object import Object 

# Dictionary storing level numbers as keys and lists of objects as values
levels = {1: [], 2: [],3:[]}  # The ground is assumed to be a non-possessable object

# Global variable to track the current level
current_level = 1



def change_level(n: int = None) -> int:
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

# Json containing various objects with their properties
items = {
    "ping_pong_ball": {
        "mass": 0.003,  
        "position": (0, 0),
        "max_speed": 116,
        "radius": 0.022,
        "bounciness": 0.88,
        "damping_coefficient": 0.06,
        "static": False,
    },
    "soccer_ball": {
        "mass": 0.43,
        "position": (0, 0),
        "max_speed": 30,
        "radius": 0.11,
        "bounciness": 0.75,
        "damping_coefficient": 0.04,
        "static": False,
    },
    "basketball": {
        "mass": 0.62,
        "position": (0, 0),
        "max_speed": 20,
        "radius": 0.12,
        "bounciness": 0.85,
        "damping_coefficient": 0.05,
        "static": False,
    },
    "tennis_ball": {
        "mass": 0.058,
        "position": (0, 0),
        "max_speed": 70,
        "radius": 0.033,
        "bounciness": 0.9,
        "damping_coefficient": 0.03,
        "static": False,
    },
    "bowling_ball": {
        "mass": 6.35,  
        "position": (0, 0),
        "max_speed": 10,
        "radius": 0.1085,
        "bounciness": 0.1,
        "damping_coefficient": 0.1,
        "static": False,
    },
    "petanque_ball": {
        "mass": 0.7,
        "position": (0, 0),
        "max_speed": 15,
        "radius": 0.037,
        "bounciness": 0.4,
        "damping_coefficient": 0.08,
        "static": False,
    },
    "bloc" : {
        "mass": 0.7,
        "position": (0, 0),
        "max_speed": 15,
        "radius": 0.037,
        "bounciness": 0.4,
        "damping_coefficient": 0.08,
        "static": True,
    }
}

pygame.init()    
