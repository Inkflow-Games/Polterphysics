import math
import random

# Structure to represent a 2D point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Structure to represent a 2D circle
class Circle:
    def __init__(self, c, r):
        self.c = c
        self.r = r

# Function to return the euclidean distance between two points
def dist(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

# Function to check whether a point lies inside or on the boundaries of the circle
def isInside(c, p):
    return dist(c.c, p) <= c.r

# Helper method to get a circle defined by 3 points
def getCircleCenter(bx, by, cx, cy):
    b = bx * bx + by * by
    c = cx * cx + cy * cy
    d = bx * cy - by * cx
    return Point((cy * b - by * c) / (2 * d), (bx * c - cx * b) / (2 * d))

# Function to return a unique circle that intersects three points
def circleFrom(a, b, c):
    i = getCircleCenter(b.x - a.x, b.y - a.y, c.x - a.x, c.y - a.y)
    i.x += a.x
    i.y += a.y
    return Circle(i, dist(i, a))

# Function to return the smallest circle that intersects 2 points
def circleFromTwo(a, b):
    c = Point((a.x + b.x) / 2.0, (a.y + b.y) / 2.0)
    return Circle(c, dist(a, b) / 2.0)

# Function to check whether a circle encloses the given points
def isValidCircle(c, p):
    return all(isInside(c, point) for point in p)

# Function to return the minimum enclosing circle for N <= 3
def minCircleTrivial(p):
    assert len(p) <= 3
    if not p:
        return Circle(Point(0, 0), 0)
    elif len(p) == 1:
        return Circle(p[0], 0)
    elif len(p) == 2:
        return circleFromTwo(p[0], p[1])

    for i in range(3):
        for j in range(i + 1, 3):
            c = circleFromTwo(p[i], p[j])
            if isValidCircle(c, p):
                return c
    return circleFrom(p[0], p[1], p[2])

# Returns the MEC using Welzl's algorithm
def welzlHelper(p, r, n):
    if n == 0 or len(r) == 3:
        return minCircleTrivial(r[:])  # Ensure we pass a copy

    idx = random.randint(0, n - 1)
    pnt = p[idx]
    p[idx], p[n - 1] = p[n - 1], p[idx]

    d = welzlHelper(p, r, n - 1)

    if isInside(d, pnt):
        return d

    return welzlHelper(p, r + [pnt], n - 1)  # Append without modifying original r

def welzl(shape):
    polygon = list(shape.vertices)
    random.shuffle(polygon)
    return welzlHelper(polygon, [], len(polygon))

def convert(shape):
    mec = welzl(shape)
    dx = mec.c.x - shape.centroid.x
    dy = mec.c.y - shape.centroid.y
    r = math.hypot(dx,dy)
    theta = math.atan2(dy,dx)
    return (mec,r,theta)


