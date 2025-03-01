"""
math_utils.py

A script that provides utility functions for force conversions.

Features include:
- Conversion of force values to Newtons
- Conversion of Newtons back to force units

Author: Rafael Véclin
Last Updated: Feb 2025
Python Version: 3.12.9
Dependencies: None
"""

def force_to_newton(force=0):
    """
    Converts a given force value to Newtons.

    Parameters:
    force (float, optional): The force value to convert. Default is 0.

    Returns:
    float: The equivalent value in Newtons.
    """
    return force / 150

def newton_to_force(newton=0):
    """
    Converts a given value in Newtons back to force units.

    Parameters:
    newton (float, optional): The Newton value to convert. Default is 0.

    Returns:
    float: The equivalent value in force units.
    """
    return newton * 150
