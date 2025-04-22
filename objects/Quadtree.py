class RectangleQ:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        return (self.x <= point.x and
                self.x + self.w > point.x and
                self.y <= point.y and
                self.y + self.h > point.y)

    def intersect(self, rang):
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
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.radius = r

    def contains(self, point):
        point_distance_x = point.x - self.x
        point_distance_y = point.y - self.y
        return (self.radius+point.radius)**2 >= (point_distance_x**2) + (point_distance_y**2)
        

class Quadtree:
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
        drawing.append([self.boundary.x,self.boundary.y, self.boundary.w, self.boundary.h])
        #pyxel.rect(self.boundary.x,self.boundary.y, self.boundary.w, self.boundary.h,2)

        if self.divided:
            self.northeast.draw(drawing)
            self.northwest.draw(drawing)
            self.southeast.draw(drawing)
            self.southwest.draw(drawing)

    def insertall(self,listofobjects):
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
    