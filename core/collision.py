"""
collision.py

A script that provides functions for detecting and resolving collisions 
between objects using physics-based calculations.

Features include:
- Compute Euclidean distance and direction vector between two points.
- Resolve collisions between two circular objects.
- Update object velocities based on mass and direction of impact.

Author: Clément Moussy
Last Updated: Feb 2025
Python Version: 3.12.9
Dependencies: pygame.math (Vector2), math
"""

import pygame
from pygame.math import Vector2
from math import *

def findfurthest(D, vertices):
    max_point = vertices[0]
    max_dot = max_point.dot(D)

    for v in vertices[1:]:
        dot_product = v.dot(D)
        if dot_product > max_dot:
            max_dot = dot_product
            max_point = v
            
    return max_point

def findfurthests(D,vertices):
    print(vertices,D)
    temp = [round(vert.dot(D),1) for vert in vertices]
    print(temp)
    maximum = max(temp)
    max_indices = [i for i, num in enumerate(temp) if num == maximum]
    return max_indices

def Support(D,A,B):
    a = findfurthest(D,A)
    b = findfurthest(-D,B)
    opmax = a - b
    return opmax
       
class GJK2D:
    def __init__(self,ShapeA,ShapeB):
        self.vertices = []
        self.A = ShapeA
        self.B = ShapeB
        self.typecol = None
        self.colpoint = 0
      
    def find_contact_features(self,polyA, polyB, mtd):
        if hasattr(polyA,'radius'):
            self.colpoint = polyA.support(mtd)
            #pygame.draw.circle(screen,(50,50,50),self.colpoint,3)
        elif hasattr(polyB,'radius'):
            self.colpoint = polyB.support(mtd)
            #pygame.draw.circle(screen,(50,50,50),self.colpoint,3)
        else:
            polyA = self.A.vertices
            polyB = self.B.vertices
            supportA = findfurthests(mtd, polyA)
            supportB = findfurthests(-mtd, polyB)
            #supportA = find_furthests(polyA, mtd)
            #supportB = find_furthests(polyB,-mtd)
            print(supportA,supportB)


            # Classify contact type
            if len(supportA) == 1 and len(supportB) == 2:
                self.typecol = (supportA[0], supportB, "vertex-edge")
                self.colpoint = self.vertextoedge(self.B.vertices[supportB[0]],self.B.vertices[supportB[1]],self.A.vertices[supportA[0]])

            elif len(supportA) == 2 and len(supportB) == 1:
                self.typecol = (supportA, supportB[0], "edge-vertex")
                self.colpoint = self.vertextoedge(self.A.vertices[supportA[0]],self.A.vertices[supportA[1]],self.B.vertices[supportB[0]])

            elif len(supportA) == 2 and len(supportB) == 2:
                self.typecol = (supportA, supportB, "edge-edge")
                self.colpoint = self.edgetoedge(self.A.vertices[supportA[0]],self.A.vertices[supportA[1]],self.B.vertices[supportB[0]],self.B.vertices[supportB[1]])

            else : self.typecol = (None, None, "unknown")

    def vertextoedge(self,SegmentA,SegmentB,vertex):
        #pygame.draw.line(screen,(200,200,200),SegmentA,SegmentB,5)
        AB = SegmentA - SegmentB
        AP = vertex - SegmentA
        t = Vector2.dot(AP,AB) / Vector2.dot(AB,AB)
        contact = SegmentA + (t * AB)
        #pygame.draw.circle(screen,(100,100,100),contact,10)
        return contact
    
    def edgetoedge(self,A1,A2,B1,B2):
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
        print(start_point,end_point)
        #pygame.draw.line(screen,(200,200,200),start_point,end_point,5)
        #pygame.draw.circle(screen,(150,150,150),(end_point + start_point)/2,3)
        print("e")
        return (end_point + start_point)/2
   
    def calcsupport(self,direction):
        temp = self.A.support(direction) - self.B.support(-direction)
        return temp
    
    def TripleProduct(self,a,b,c):
        z = a.x * b.y - a.y * b.x
        return Vector2(-c.y * z, c.x * z)

    def detection(self):
        #direction = Vector2(1,1)
        direction = self.A.centroid
        a = self.calcsupport(direction)
        direction = -direction
        b = self.calcsupport(direction)
        if b.dot(direction) <= 0: return None

        ab = b-a
        direction = self.TripleProduct(ab,-a,ab)

        for i in range(20):
            c = self.calcsupport(direction)
            if c.dot(direction) <=0 : return None

            c0 = -c
            cb = b - c
            ca = a - c
            cbnorm = self.TripleProduct(ca,cb,cb)
            canorm = self.TripleProduct(cb,ca,ca)

            if canorm.dot(c0) > 0:
                b = c
                direction = canorm
            elif cbnorm.dot(c0) > 0:
                a = c
                direction = cbnorm
            else: 
                self.vertices = [a,b,c]
                return [a,b,c]
     
    def findClosestEdge(self):     
        closestdistance = float("inf")
        closest = None
        for i in range(len(self.vertices)):
            p , q = self.vertices[i], self.vertices[(i+1)%len(self.vertices)]
            line = q - p
            print(self.vertices)
            print("triple",self.TripleProduct(line,p,line))
            norm = Vector2.normalize(self.TripleProduct(line,p,line))
            dist = norm.dot(p)
            if dist<closestdistance:
                closestdistance = dist
                closest = (dist, i, p, q, norm)
        return closest
                
    def EPA(self,polyptote):
        if self.detection() is not None:
            minIndex = 0
            minDistance = float("inf")
            while (minDistance == float("inf")):
                for i in range(len(polyptote)):
                    j = (i+1)%len(polyptote)
                    vertexI = polyptote[i]
                    vertexJ = polyptote[j]
                    ij = vertexJ - vertexI
                    normal = Vector2(ij.y,-ij.x).normalize()
                    distance = normal.dot(vertexI)

                    if (distance < 0):
                        distance *= -1
                        normal = -normal
                    
                    if (distance < minDistance):
                        minDistance = distance
                        minNormal = normal
                        minIndex = j
            
                support = self.calcsupport(minNormal)
                sDistance = minNormal.dot(support)
                #print(sDistance,support,minDistance,minIndex,minNormal)

                if abs(sDistance - minDistance) > 0.001:
                    minDistance = float("inf")
                    polyptote.insert(minIndex,support)
                    #print(polyptote)
            return minNormal * (minDistance + 0.001)
        return Vector2(0,0)
       
    def resolve(self,penetrationvector,restitution=0.6):
        #print(self.A.vertices,self.B.vertices,self.typecol)
        #pygame.draw.polygon(screen,(255,255,225),self.A.vertices)
        #pygame.draw.polygon(screen,(255,255,225),self.B.vertices)
        #print(self.A.centroid,self.B.centroid)
        #print("ae",self.A.velocity,self.A.inertia,self.A.angular_velocity)
        #print("be",self.B.velocity,self.B.inertia,self.B.angular_velocity)
        contact_point = self.colpoint
        #pygame.draw.line(screen,(120,20,100),contact_point,(contact_point+penetrationvector)*10)
        normal = penetrationvector.normalize()
        #pygame.draw.line(screen,(50,50,50),contact_point,(contact_point-normal)*10)
        rA = contact_point - self.A.centroid
        rB = contact_point - self.B.centroid
        vA = self.A.velocity + Vector2(-self.A.angular_velocity * rA.y, self.A.angular_velocity * rA.x)
        vB = self.B.velocity + Vector2(-self.B.angular_velocity * rB.y, self.B.angular_velocity * rB.x)
        relative_velocity = vB - vA

        # Check if bodies are separating
        vel_along_normal = relative_velocity.dot(normal)
        if vel_along_normal > -0.01:
            return  # Objects are already separating

        # Compute impulse scalar
        inv_mass1 = 1 / self.A.mass if self.A.mass > 0 else 0
        inv_mass2 = 1 / self.B.mass if self.B.mass > 0 else 0
        inv_I1 = 1 / self.A.inertia if self.A.inertia > 0 else 0
        inv_I2 = 1 / self.B.inertia if self.B.inertia > 0 else 0

        rA_cross_N = rA.cross(normal)
        rB_cross_N = rB.cross(normal)
        denominator = inv_mass1 + inv_mass2 + (rA_cross_N ** 2) * inv_I1 + (rB_cross_N ** 2) * inv_I2
        j = -(1 + restitution) * vel_along_normal / denominator
        bias = max(0,penetrationvector.magnitude() - 0.06) * 0.8 / (1/60)
        j += bias

        # Apply impulse to linear velocity
        impulse = j * normal
        self.A.velocity -= impulse * inv_mass1
        self.B.velocity += impulse * inv_mass2
        a = Vector2(0,0)

        # Apply angular impulse
        #print("rA",rA.cross(impulse)* inv_I1)
        #print(impulse * inv_mass1,impulse * inv_mass2)
        #print("rB",rB.cross(impulse)* inv_I2)
        self.A.angular_velocity -= rA.cross(impulse) * inv_I1
        self.B.angular_velocity += rB.cross(impulse) * inv_I2
        #print("a",self.A.velocity,self.A.inertia,self.A.angular_velocity)
        #print("b",self.B.velocity,self.B.inertia,self.B.angular_velocity)
        return
    
def circlealgorithm(points):
    return

def update(poly):
    poly.add(poly.velocity/60)
    poly.rotate(poly.angular_velocity/60)
    poly.velocity *= 0.995
    poly.angular_velocity *= 0.995
