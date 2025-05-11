"""
POLTERPHYSICS
mincircle.py  

A module for computing the Minimum Enclosing Circle (MEC) using Welzl's algorithm.  
Features include:  
- Support for points and circles in 2D space  
- Computation of exact MEC for 1-3 points  
- Recursive randomized algorithm (Welzl's) for larger sets  
- Output in polar coordinates relative to a shape's centroid  

Last Updated: May 2025
Python Version: 3.12+
Dependencies: math, random  
"""

import math
import random

class Point:
    """
    Represents a 2D point with x and y coordinates.

    Attributes:
        x (float): The x-coordinate.
        y (float): The y-coordinate.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Circle:
    """
    Represents a 2D circle with a center and a radius.

    Attributes:
        c (Point): Center of the circle.
        r (float): Radius of the circle.
    """
    def __init__(self, c, r):
        self.c = c
        self.r = r

def dist(a, b):
    """
    Calculates the Euclidean distance between two points.

    Parameters:
        a (Point): First point.
        b (Point): Second point.

    Returns:
        float: Distance between a and b.
    """
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

def isInside(c, p):
    """
    Checks whether a point lies inside or on the boundary of a circle.

    Parameters:
        c (Circle): The circle.
        p (Point): The point to test.

    Returns:
        bool: True if point is inside or on the circle, False otherwise.
    """
    return dist(c.c, p) <= c.r

def getCircleCenter(bx, by, cx, cy):
    """
    Calculates the circumcenter of a triangle formed by three points.

    Parameters:
        bx (float): x difference of second point relative to the first.
        by (float): y difference of second point relative to the first.
        cx (float): x difference of third point relative to the first.
        cy (float): y difference of third point relative to the first.

    Returns:
        Point: The center of the circle passing through the three points.
    """
    b = bx * bx + by * by
    c = cx * cx + cy * cy
    d = bx * cy - by * cx
    return Point((cy * b - by * c) / (2 * d), (bx * c - cx * b) / (2 * d))

def circleFrom(a, b, c):
    """
    Computes the unique circle passing through three points.

    Parameters:
        a (Point): First point.
        b (Point): Second point.
        c (Point): Third point.

    Returns:
        Circle: The circle passing through all three points.
    """
    #computes a circle that has as center the vertex
    i = getCircleCenter(b.x - a.x, b.y - a.y, c.x - a.x, c.y - a.y)
    i.x += a.x
    i.y += a.y
    return Circle(i, dist(i, a))

def circleFromTwo(a, b):
    """
    Computes a circle with diameter defined by two points.

    Parameters:
        a (Point): First point.
        b (Point): Second point.

    Returns:
        Circle: The smallest circle containing both points.
    """
    c = Point((a.x + b.x) / 2.0, (a.y + b.y) / 2.0)
    return Circle(c, dist(a, b) / 2.0)

def isValidCircle(c, p):
    """
    Checks if a circle encloses a list of points.

    Parameters:
        c (Circle): The circle to test.
        p (list of Point): List of points.

    Returns:
        bool: True if all points are inside or on the circle.
    """
    return all(isInside(c, point) for point in p)

def minCircleTrivial(p):
    """
    Computes the MEC for 3 or fewer points using brute force.

    Parameters:
        p (list of Point): List of up to 3 points.

    Returns:
        Circle: The minimum enclosing circle.
    """
    assert len(p) <= 3
    if not p:
        return Circle(Point(0, 0), 0)
    elif len(p) == 1:
        return Circle(p[0], 0)
    elif len(p) == 2:
        return circleFromTwo(p[0], p[1])

    # Check if any two-point circle encloses the third
    for i in range(3):
        for j in range(i + 1, 3):
            c = circleFromTwo(p[i], p[j])
            if isValidCircle(c, p):
                return c
    return circleFrom(p[0], p[1], p[2])

def welzlHelper(p, r, n):
    """
    Recursive helper for Welzl's algorithm.

    Parameters:
        p (list of Point): Points to process.
        r (list of Point): Boundary points of the MEC.
        n (int): Current number of points considered in p.

    Returns:
        Circle: The MEC for the given subset of points.
    """
    if n == 0 or len(r) == 3:
        return minCircleTrivial(r[:])  # Ensure we pass a copy

    # Randomly select a point to exclude
    idx = random.randint(0, n - 1)
    pnt = p[idx]
    p[idx], p[n - 1] = p[n - 1], p[idx]
    # Recurse without pnt
    d = welzlHelper(p, r, n - 1)

    if isInside(d, pnt):
        return d

    return welzlHelper(p, r + [pnt], n - 1)  # Append without modifying original r

def welzl(shape):
    """
    Computes the minimum enclosing circle of a shape using Welzl's algorithm.

    Parameters:
        shape (object): An object with a .vertices attribute (list of Points).

    Returns:
        Circle: The minimum enclosing circle.
    """
    polygon = list(shape.vertices)
    random.shuffle(polygon)
    return welzlHelper(polygon, [], len(polygon))

def convert(shape):
    """
    Converts the MEC of a shape to polar coordinates relative to the centroid of the shape it encloses

    Parameters:
        shape (object): An object.

    Returns:
        tuple: (Circle, float radius, float angle in radians)
    """
    mec = welzl(shape)
    dx = mec.c.x - shape.centroid.x
    dy = mec.c.y - shape.centroid.y
    r = math.hypot(dx,dy)
    theta = math.atan2(dy,dx)
    # Returns the relative distance to the centroid of the object and the angle relative to the centroid of the object
    return (mec,r,theta)


