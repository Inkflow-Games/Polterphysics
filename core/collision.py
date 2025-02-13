from pygame.math import Vector2
import math


def squarecircle(rectobj,circobj):
    #commente pas ce code, je vai le modif,il sert a rien
    circx = circobj.position.x
    circy = circobj.position.y
    circrad = 10
    rectx = rectobj.position.x
    recty = rectobj.position.y
    rectwid = rectobj.hitbox.l
    rectlen = rectobj.hitbox.h
    print(circx,circy,rectx,recty,rectlen,rectwid)

    distancex = abs(circx - rectx)
    distancey = abs(circy - recty)
    if (distancex > rectwid/2 + circrad): return False
    if (distancex > rectlen/2 + circrad): return False
    if (distancex <= (rectwid/2)): return True
    if (distancex <= (rectlen/2)): return True
    dist = math.pow((distancex - rectwid/2),2) + math.pow((distancey - rectlen/2),2)
    return (dist <= math.pow(circrad,2))

def dist(c1,c2):
    dx = c2.x - c1.x
    dy = c2.y - c1.y
    return round(math.sqrt((dx**2)+(dy**2)),6),Vector2(dx,dy)

def p2pcd(circle1,circle2):
        dis,nor_vec = dist(circle1.position,circle2.position)
        radius1 = circle1.radius
        radius2 = circle2.radius
        velocity1 = circle1.velocity
        velocity2 = circle2.velocity
        if  int(dis) <= int(radius1+radius2):
            newvel = Vector2(circle2.velocity.x - circle1.velocity.x, circle2.velocity.y - circle1.velocity.y)
            if nor_vec.dot(newvel) <= 0:
                un = nor_vec/(dist(Vector2(0,0),nor_vec)[0])
                ut = Vector2(-un.y,un.x)
                m1 = circle1.mass
                m2 = circle2.mass
                v1n = un.dot(velocity1)
                v1t = ut.dot(velocity1)
                v2n = un.dot(velocity2)
                v2t = ut.dot(velocity2)
                vp1n = (v1n*(m1-m2) + 2*(m2*v2n))/(m1+m2)
                vp2n = (v2n*(m2-m1) + 2*(m1*v1n))/(m1+m2)
                vp1n = un*vp1n
                vp2n = un*vp2n
                vp1t = ut*v1t
                vp2t = ut*v2t
                vp1 = vp1n+vp1t
                vp2 = vp2n+vp2t
                circle1.velocity = vp1
                circle2.velocity = vp2
                return
        return