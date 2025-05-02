"""
QUADTREE SPATIAL PARTITIONING MODULE  
quadtree.py  

Implements a quadtree structure for efficient spatial partitioning and query of circular objects.  
Features include:  
- Axis-aligned rectangular boundaries (RectangleQ)  
- Circular range queries (CircleQ)  
- Object insertion, deletion, and spatial querying  
- Recursive subdivision of space for dynamic density  

Author: Clément Moussy  
Last Updated: April 2025  
Python Version: 3.11.0  
Dependencies: None  
"""

class RectangleQ:
    """
    Represents a rectangle defined by top-left corner (x, y), width, and height.

    Attributes:
        x (float): X-coordinate of top-left corner.
        y (float): Y-coordinate of top-left corner.
        w (float): Width of the rectangle.
        h (float): Height of the rectangle.
    """
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        """
        Checks whether a circle's center is inside the rectangle.

        Parameters:
            point (CircleQ): The circular object with center and radius.

        Returns:
            bool: True if circle center is inside rectangle.
        """
        return (self.x <= point.x and
                self.x + self.w > point.x and
                self.y <= point.y and
                self.y + self.h > point.y)

    def intersect(self, rang):
        """
        Checks if a circular area intersects with the rectangle.

        Parameters:
            rang (CircleQ): The circular query region.

        Returns:
            bool: True if circle intersects the rectangle.
        """
        circle_distance_x = abs(rang.x - (self.x + self.w / 2))
        circle_distance_y = abs(rang.y - (self.y + self.h / 2))
        if circle_distance_x > self.w / 2 + rang.radius:
            return False
        if circle_distance_y > self.h / 2 + rang.radius:
            return False
        if circle_distance_x <= self.w / 2:
            return True
        if circle_distance_y <= self.h / 2:
            return True
        corner_distance_sq = (circle_distance_x - self.w /
                              2)**2 + (circle_distance_y - self.h / 2)**2
        return corner_distance_sq <= rang.radius**2
    
class CircleQ:
    """
    Represents a circular area for spatial queries or object bounds.

    Attributes:
        x (float): X-coordinate of the center.
        y (float): Y-coordinate of the center.
        radius (float): Radius of the circle.
    """
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.radius = r

    def contains(self, point):
        """
        Checks if this circle fully contains another circle.

        Parameters:
            point (CircleQ): Another circular object.

        Returns:
            bool: True if the other circle lies within or on this circle.
        """
        point_distance_x = point.x - self.x
        point_distance_y = point.y - self.y
        return (self.radius+point.radius)**2 >= (point_distance_x**2) + (point_distance_y**2)
        
class Quadtree:
    """
    Implements a quadtree to manage 2D spatial objects efficiently.

    Attributes:
        boundary (RectangleQ): The rectangle region this node represents.
        capacity (int): Max number of elements before subdivision.
        points (list): Stored objects within this node (until subdivided).
        northeast, northwest, southeast, southwest (Quadtree): Child quadrants.
        divided (bool): Indicates whether this node has been subdivided.

    Methods:
        subdivide(): Divides this node into four children.
        insert(Object): Inserts an object into the quadtree.
        delpoint(Object): Removes an object from the quadtree.
        query(Object, found): Queries for objects intersecting a circular region.
        draw(drawing): Appends boundary data for visualization.
        insertall(list): Inserts a list of objects.
        searchelements(list): Queries and removes all elements in list.
    """
    def __init__(self, boundary, n):
        self.boundary = boundary
        self.capacity = n
        self.points = []
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None
        self.divided = False

    def subdivide(self):
        """
        Splits the current region into four smaller quadrants.
        """
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
        ne = RectangleQ(x + w/2, y, w/2, h/2)
        self.northeast = Quadtree(ne, self.capacity)
        nw = RectangleQ(x, y, w/2, h/2)
        self.northwest = Quadtree(nw, self.capacity)
        se = RectangleQ(x + w/2, y + h/2, w/2, h/2)
        self.southeast = Quadtree(se, self.capacity)
        sw = RectangleQ(x, y + h/2, w/2, h/2)
        self.southwest = Quadtree(sw, self.capacity)
        self.divided = True

    def insert(self, Object):
        """
        Inserts an object with a .mincircle (CircleQ) into the quadtree.

        Parameters:
            Object: An object with a .mincircle attribute representing its bounds.
        """
        if not self.boundary.contains(Object.mincircle):
            return
        if not self.divided:
            if len(self.points) < self.capacity:
                self.points.append(Object)
            else:
                self.subdivide()
                self.points.append(Object)
                for pnt in self.points:
                    self.northeast.insert(pnt)
                    self.northwest.insert(pnt)
                    self.southeast.insert(pnt)
                    self.southwest.insert(pnt)
                self.points = []
        else:
            self.northeast.insert(Object)
            self.northwest.insert(Object)
            self.southeast.insert(Object)
            self.southwest.insert(Object)
            
    def delpoint(self,Object):
        """
        Removes an object from the quadtree.

        Parameters:
            Object: Object to remove.
        """
        if self.divided:
            self.northwest.delpoint(Object)
            self.northeast.delpoint(Object)
            self.southwest.delpoint(Object)
            self.southeast.delpoint(Object)
        else:
            for elm in self.points:
                if elm is Object:
                    self.points.remove(elm)
            
    def query(self, Object, found=None):
        """
        Finds all objects in the quadtree whose bounds are within the given object's mincircle.

        Parameters:
            Object: The querying object with .mincircle (CircleQ).
            found (list): Optional list to populate with results.

        Returns:
            list: List of matching objects (if `found` is None).
        """
        if found is None:
            found = []
        if not self.boundary.intersect(Object.mincircle):
            return
        else:
            for p in self.points:
                if Object.mincircle.contains(p.mincircle):
                    found.append(p)
        if self.divided:
            self.northeast.query(Object, found)
            self.northwest.query(Object, found)
            self.southeast.query(Object, found)
            self.southwest.query(Object, found)
            return found
        
    def draw(self,drawing):
        """
        Appends this node's boundary to a drawing list for visualization.

        Parameters:
            drawing (list): A list to store drawing rectangles [x, y, w, h].
        """
        drawing.append([self.boundary.x,self.boundary.y, self.boundary.w, self.boundary.h])
        #pyxel.rect(self.boundary.x,self.boundary.y, self.boundary.w, self.boundary.h,2)

        if self.divided:
            self.northeast.draw(drawing)
            self.northwest.draw(drawing)
            self.southeast.draw(drawing)
            self.southwest.draw(drawing)

    def insertall(self,listofobjects):
        """
        Inserts all elements from a list into the quadtree.

        Parameters:
            listofobjects (list): List of objects.
        """
        for elements in listofobjects:
            self.insert(elements)

    def searchelements(self,elements):
        interactions = []
        for i in range(len(elements)):
            temp = []
            self.query(elements[i],temp)
            interactions.append(temp)
            self.delpoint(elements[i])
        return interactions
    