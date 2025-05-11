"""
Polterphysics
collision.py

A script that provides functions for detecting and resolving collisions 
between objects using physics-based calculations.

Features include:  
- Compute Minkowski Difference support points  
- Run the GJK algorithm to detect collision  
- Run EPA to compute penetration vector  
- Identify contact feature (vertex-edge, edge-edge, etc.)  
- Resolve collisions using impulses with restitution and friction  
- Apply positional correction to prevent overlap  

Author: Clément Moussy
Last Updated: Feb 2025
Python Version: 3.12.9
Dependencies: pygame.math (Vector2), math
"""

from pygame.math import Vector2
from math import *
import pygame

def find_furthest(D, vertices):
    """
    Returns the vertex in 'vertices' that is furthest along direction D.

    Parameters:
    D (Vector2): Search direction.
    vertices (list of Vector2): Polygon vertices.

    Returns:
    Vector2: Furthest point in direction D.
    """
    max_point = vertices[0]
    max_dot = max_point.dot(D)

    for v in vertices[1:]:
        dot_product = v.dot(D)
        if dot_product > max_dot:
            max_dot = dot_product
            max_point = v
            
    return max_point

def find_furthests(D,vertices):
    """
    Returns indices of vertices that are furthest along direction D.

    Parameters:
    D (Vector2): Search direction.
    vertices (list of Vector2): Polygon vertices.

    Returns:
    list of int: Indices of furthest vertices.
    """
    temp = [round(vert.dot(D),1) for vert in vertices]
    maximum = max(temp)
    max_indices = [i for i, num in enumerate(temp) if num == maximum]
    return max_indices

def Support(D,A,B):
    """
    Computes the support point in the Minkowski difference of shapes A and B.

    Parameters:
    D (Vector2): Search direction.
    A (list of Vector2): Vertices of shape A.
    B (list of Vector2): Vertices of shape B.

    Returns:
    Vector2: Support point in Minkowski difference.
    """
    a = find_furthest(D,A)
    b = find_furthest(-D,B)
    opmax = a - b
    return opmax
       
class GJK2D:
    """
    A class that implements the GJK and EPA algorithms for 2D convex collision detection
    and resolution.

    Attributes:
        shape1 (Shape): First shape involved in collision.
        shape2 (Shape): Second shape.
        res1 (float): Restitution of shape1.
        res2 (float): Restitution of shape2.
        typecol (tuple): Contact type info (vertex/edge).
        colpoint (Vector2): Collision contact point.
        vertices (list of Vector2): Simplex from GJK.
    """
    def __init__(self, Object1, Object2):
        self.vertices = []
        self.res1 = Object1.restitution_coefficient
        self.res2 = Object2.restitution_coefficient
        self.shape1 = Object1.shape
        self.shape2 = Object2.shape
        self.typecol = None
        self.colpoint = 0
      
    def find_contact_features(self,polyA, polyB, mtd):
        """
        Identifies contact point and type between two shapes using support features.

        Parameters:
        polyA (Shape): First shape.
        polyB (Shape): Second shape.
        mtd (Vector2): Minimum translation direction.
        """
        #checks if its a circle or not, applies different collision points
        if hasattr(polyA,'radius'):
            self.colpoint = polyA.support(mtd)
            #pygame.draw.circle(screen,(50,50,50),self.colpoint,3)
        elif hasattr(polyB,'radius'):
            self.colpoint = polyB.support(-mtd)
            #pygame.draw.circle(screen,(50,50,50),self.colpoint,3)
        else:
            
            polyA = self.shape1.vertices
            polyB = self.shape2.vertices
            supportA = find_furthests(mtd, polyA)
            supportB = find_furthests(-mtd, polyB)
            #computes the support functions for both shapes for the detection of collision type

            # Classify contact type
            if len(supportA) == 1 and len(supportB) == 2:
                self.typecol = (supportA[0], supportB, "vertex-edge")
                self.colpoint = self.vertextoedge(self.shape2.vertices[supportB[0]],self.shape2.vertices[supportB[1]],self.shape1.vertices[supportA[0]])

            elif len(supportA) == 2 and len(supportB) == 1:
                self.typecol = (supportA, supportB[0], "edge-vertex")
                self.colpoint = self.vertextoedge(self.shape1.vertices[supportA[0]],self.shape1.vertices[supportA[1]],self.shape2.vertices[supportB[0]])

            elif len(supportA) == 2 and len(supportB) == 2:
                self.typecol = (supportA, supportB, "edge-edge")
                self.colpoint = self.edgetoedge(self.shape1.vertices[supportA[0]],self.shape1.vertices[supportA[1]],self.shape2.vertices[supportB[0]],self.shape2.vertices[supportB[1]])

            else : 
                self.typecol = (None, None, "unknown")

    def vertextoedge(self,SegmentA,SegmentB,vertex):
        """
        Projects a vertex onto a segment to find the closest point.

        Parameters:
        SegmentA (Vector2): First point of segment.
        SegmentB (Vector2): Second point of segment.
        vertex (Vector2): Vertex to project.

        Returns:
        Vector2: Closest point on segment to vertex.
        """
        #pygame.draw.line(screen,(200,200,200),SegmentA,SegmentB,5)
        AB = SegmentA - SegmentB
        AP = vertex - SegmentA
        t = Vector2.dot(AP,AB) / Vector2.dot(AB,AB)
        contact = SegmentA + (t * AB)
        #pygame.draw.circle(screen,(100,100,100),contact,10)
        return contact
    
    def edgetoedge(self,A1,A2,B1,B2):
        """
        Returns midpoint of overlap between two edge segments projected onto a common axis.

        Parameters:
        A1, A2 (Vector2): Edge of first shape.
        B1, B2 (Vector2): Edge of second shape.

        Returns:
        Vector2: Midpoint of projection overlap.
        """
        d = A2 - A1
        D = d.normalize()
        t_A1, t_A2 = A1.dot(D),A2.dot(D)
        t_B1, t_B2 = B1.dot(D),B2.dot(D)
        if t_A1 > t_A2:
            t_A1,t_A2 = t_A2,t_A1
        if t_B1 > t_B2:
            t_B1,t_B2 = t_B2,t_B1
        start_t = max(t_A1,t_B1)
        end_t = min(t_A2,t_B2)
        start_point = A1 + (start_t - A1.dot(D)) * D
        end_point = A1 + (end_t - A1.dot(D)) * D
        #print(start_point,end_point)
        #pygame.draw.line(screen,(200,200,200),start_point,end_point,5)
        #pygame.draw.circle(screen,(150,150,150),(end_point + start_point)/2,3)
        return (end_point + start_point)/2
   
    def calcsupport(self,direction):
        """
        Gets the support point in the Minkowski difference along a given direction.

        Parameters:
        direction (Vector2): Direction to search.

        Returns:
        Vector2: Support point.
        """
        temp = self.shape1.support(direction) - self.shape2.support(-direction)
        return temp
    
    def TripleProduct(self,a,b,c):
        """
        Returns perpendicular vector using the scalar triple product.

        Parameters:
        a, b, c (Vector2): Input vectors.

        Returns:
        Vector2: Resulting perpendicular vector.
        """
        z = a.x * b.y - a.y * b.x
        return Vector2(-c.y * z, c.x * z)

    def detection(self):
        """
        Performs GJK collision detection.

        Returns:
        list of Vector2 or None: Simplex if collision detected; else None.
        """
        #starts in a pseudo-random direction to start searching for the simplex
        direction = self.shape1.centroid
        a = self.calcsupport(direction)
        direction = -direction
        b = self.calcsupport(direction)
        # If the dot product is not positive, the origin is outside the Minkowski difference
        if b.dot(direction) <= 0: return None
        #Compute AB and the perpendicular direction toward the origin using triple product
        ab = b-a
        direction = self.TripleProduct(ab,-a,ab)

        for i in range(20):
            #Add a new support point in the current search direction
            c = self.calcsupport(direction)
            if c.dot(direction) <=0 : return None
            #Shift simplex to origin for next iteration logic
            c0 = -c
            cb = b - c
            ca = a - c
             #Generate new perpendicular directions toward the origin
            cbnorm = self.TripleProduct(ca,cb,cb)
            canorm = self.TripleProduct(cb,ca,ca)
            #Choose the next edge to keep and update direction accordingly
            if canorm.dot(c0) > 0:
                b = c
                direction = canorm
            elif cbnorm.dot(c0) > 0:
                a = c
                direction = cbnorm
            else: 
                # Origin is inside the triangle (simplex encloses it)
                self.vertices = [a,b,c]
                return [a,b,c]
     
    def findClosestEdge(self):   
        """
        Finds the closest edge from the origin in the simplex.

        Returns:
        tuple: (distance, index, p, q, normal) of the closest edge.
        """  
        closestdistance = float("inf")
        closest = None
        for i in range(len(self.vertices)):
            p , q = self.vertices[i], self.vertices[(i+1)%len(self.vertices)]
            line = q - p
            norm = Vector2.normalize(self.TripleProduct(line,p,line))
            dist = norm.dot(p)
            if dist<closestdistance:
                closestdistance = dist
                closest = (dist, i, p, q, norm)
        return closest
                
    def EPA(self,polyptote):
        """
        Performs the EPA algorithm to compute the penetration vector.

        Parameters:
        polyptote (list of Vector2): Initial simplex from GJK.

        Returns:
        Vector2: Penetration vector.
        """
         # Only proceed if a collision was confirmed by GJK
        if self.detection() is not None:
            minIndex = 0
            minDistance = float("inf")
            # Continue expanding the polytope until the new support point is very close to an existing edge
            while (minDistance == float("inf")):
                for i in range(len(polyptote)):
                    j = (i+1)%len(polyptote)
                    vertexI = polyptote[i]
                    vertexJ = polyptote[j]
                    ij = vertexJ - vertexI
                    normal = Vector2(ij.y,-ij.x).normalize()
                    distance = normal.dot(vertexI)

                    # If the normal is pointing toward the origin, flip it
                    if (distance < 0):
                        distance *= -1
                        normal = -normal

                    # Track the edge that is closest to the origin
                    if (distance < minDistance):
                        minDistance = distance
                        minNormal = normal
                        minIndex = j

                # Get a new support point in the direction of the closest edge's normal
                support = self.calcsupport(minNormal)
                sDistance = minNormal.dot(support)

                # If the new point is not close enough to the current edge, add it to the polytope
                if abs(sDistance - minDistance) > 0.001:
                    minDistance = float("inf")
                    polyptote.insert(minIndex,support)

            # Return the final penetration vector, slightly extended to avoid numerical issues
            return minNormal * (minDistance + 0.001)
        return Vector2(0,0)
       
    def resolve(self,penetrationvector,dt):
        """
        Resolves collision between two shapes by applying impulses,positional correction and friction.

        Parameters:
        penetrationvector (Vector2): Minimum translation vector.
        dt (float): Time step.
        """
        contact_point = self.colpoint
        restitution = min(self.res1,self.res2)
        # Coulomb's law: μ = friction coefficient (can be per-object or global)
        mu = 0.4
        normal = penetrationvector.normalize()
        # Compute rA and rB, the contact point relative to the centers of mass
        rA = contact_point - self.shape1.centroid
        rB = contact_point - self.shape2.centroid
        vA = self.shape1.velocity + Vector2(-self.shape1.angular_velocity * rA.y, self.shape1.angular_velocity * rA.x)
        vB = self.shape2.velocity + Vector2(-self.shape2.angular_velocity * rB.y, self.shape2.angular_velocity * rB.x)
        relative_velocity = vB - vA

        # Check if bodies are separating
        vel_along_normal = relative_velocity.dot(normal)
        if vel_along_normal > -0.01:
            return  # Objects are already separating

        # Compute impulse scalar
        inv_mass1 = 1 / self.shape1.mass if self.shape1.mass > 0 else 0
        inv_mass2 = 1 / self.shape2.mass if self.shape2.mass > 0 else 0
        inv_I1 = 1 / self.shape1.inertia if self.shape1.inertia > 0 else 0
        inv_I2 = 1 / self.shape2.inertia if self.shape2.inertia > 0 else 0

        # Calculate the rotational effects (torque response) at the contact point
        rA_cross_N = rA.cross(normal)
        rB_cross_N = rB.cross(normal)
        denominator = inv_mass1 + inv_mass2 + (rA_cross_N ** 2) * inv_I1 + (rB_cross_N ** 2) * inv_I2
        # Impulse scalar (normal impulse magnitude)
        j = -(1 + restitution) * vel_along_normal / denominator
        # Apply Baumgarte stabilization: bias impulse to reduce sinking
        bias = max(0,penetrationvector.magnitude() - 0.05) * (0.2 / dt)
        j += bias

        # Apply impulse to linear velocity
        impulse = j * normal
        self.shape1.velocity -= impulse * inv_mass1
        self.shape2.velocity += impulse * inv_mass2

        self.shape1.angular_velocity -= rA.cross(impulse) * inv_I1
        self.shape2.angular_velocity += rB.cross(impulse) * inv_I2
       
       #Compute friction impulse
        if relative_velocity.length() > 0:
            tangent = relative_velocity - (relative_velocity.dot(normal)) * normal
            if tangent.length() > 0:
                tangent = tangent.normalize()
                # Compute tangential impulse magnitude
                jt = -relative_velocity.dot(tangent)  # Friction force along the tangent direction
                jt = max(min(jt, j * mu), -j * mu)  # Clamp to Coulomb friction
                friction_impulse = jt * tangent

                # Apply friction impulse
                self.shape1.velocity -= friction_impulse * inv_mass1
                self.shape2.velocity += friction_impulse * inv_mass2
                self.shape1.angular_velocity -= rA.cross(friction_impulse) * inv_I1
                self.shape2.angular_velocity += rB.cross(friction_impulse) * inv_I2
        #Another position correction to also prevent sinking
        percent = 0.6 # Penetration percentage to correct (60%)
        slop = 0.03 # Allow small overlap tolerance
        correction_mag = max(penetrationvector.length() - slop, 0) / (inv_mass1 + inv_mass2)
        correction = correction_mag * percent * normal
        self.shape1.add(-(correction * inv_mass1))
        self.shape2.add(correction * inv_mass2)

        return


