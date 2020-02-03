import pygame as pg
import sys
import time
import random as rm
from math import sqrt, floor
from numpy import sign


def engine():

    # Initialization
    pg.init()
    pg.display.init()
    SCR_HEIGHT, SCR_WIDTH = 400, 400  # screen
    WLD_HEIGHT, WLD_WIDTH = 200, 100  # world
    UNIT = "m"
    TICK_MARKS = 5  # number of Y-axis tick marks
    SCREEN = pg.display.set_mode([SCR_WIDTH, SCR_HEIGHT])
    SCREEN.fill((255, 255, 255))  # white screen
    pg.display.set_caption("physics_engine v.0.1")
    font = pg.font.Font(None, 30)

    # defines properties of all objects
    class Object():
        instances = []

        def __init__(self, x, y, xv, yv, m, c, xa, ya):
            # 'i' prefix = intial
            self.ix = x  # x position
            self.iy = y  # y position
            self.ixv = xv  # x velocity
            self.iyv = yv  # y velocity
            self.im = m  # mass
            self.ic = c  # color
            self.ixa = xa
            self.iya = ya
            Object.instances.append(self)

        def reset(self):
            self.x = self.ix
            self.y = self.iy
            self.xv = self.ixv
            self.yv = self.iyv
            self.m = self.im
            self.c = self.ic
            self.xa = self.ixa
            self.ya = self.iya

        def update(self):
            self.xv += self.xa
            self.yv += self.ya
            self.y += round(self.yv)
            self.x += round(self.xv)

        def reset_all():
            for instance in Object.instances:
                instance.reset()

    class SObject(Object):  # "Space" objects
        bodies = []
        gc = 1

        def __init__(self, x, y, xv, yv, m, c, xa, ya):
            super().__init__(x, y, xv, yv, m, c, xa, ya)
            SObject.bodies.append(self)

        def update(self):
            for obj in SObject.bodies:
                if self.x == obj.x and self.y == obj.y:
                    pass
                else:
                    self.a = (SObject.gc * obj.m) / ((self.x-obj.x)**2 + (self.y-obj.y)**2)
                    self.xa += self.a*((obj.x-self.x)/200)
                    self.ya += self.a*((obj.y-self.y)/200)
            super().update()

    class Satellite(SObject):
        def __init__(self, x, y, xv, yv, m, c, xa, ya, r):
            super().__init__(x, y, xv, yv, m, c, xa, ya)
            self.r = round((r*SCR_HEIGHT)/WLD_HEIGHT)  # radius

        def update(self):
            super().update()
            pg.draw.circle(SCREEN, self.c, tcirc((self.x, self.y)), self.r)
            #print (self.xa)
            #self.xa = -1*(((self.x)-200)/150)
            #self.ya = -1*(((self.y)-200)/150)
            for obj in SObject.bodies:
                if self.x != obj.x and self.y != obj.y:
                    if sqrt(((self.x-obj.x)**2 + (self.y-obj.y)**2)) < max(self.r, obj.r):
                        self.xv *= -0.8
                        self.yv *= -0.8
                        self.xa = 0
                        self.ya = 0

    #sat = Satellite(200,380,15,0,0,(0,0,0),0,-1,5)
    sat1 = Satellite(200, 380, 0, 0, 10, (0, 0, 0), 0, 0, 5)
    sat2 = Satellite(100, 50, 0, 0, 20, (0, 0, 0), 0, 0, 10)

    class EObject(Object):  # "Earth" objects
        instances = []

        # physical settings
        b = -0.8  # bounciness

        def __init__(self, x, y, xv, yv, m, c, xa, ya):
            super().__init__(x, y, xv, yv, m, c, xa, ya)
            EObject.instances.append(self)

        def update(self):
            super().update()
            self.xv += round((rm.random()*2)-1, 2)

        def reset(self):
            super().reset()
            self.ya = -0.8  # gravity setting -0.5

    class Ball(EObject):
        def __init__(self, x, y, xv, yv, m, c, xa, ya, r):
            super().__init__(x, y, xv, yv, m, c, xa, ya)
            self.r = round((r*SCR_HEIGHT)/WLD_HEIGHT)  # radius

        def update(self):
            super().update()

            # object to object collisions
            for obj in EObject.instances:
                # if the balls are intersecting
                if self.x != obj.x and self.y != obj.y and sqrt(((self.x-obj.x)**2 + (self.y-obj.y)**2)) <= self.r + obj.r:
                    # pg.draw.circle(SCREEN,(255,0,0),tcirc((self.x,self.y)),self.r)

                    # calculates distance between centers of balls
                    self.p = sqrt(((self.x-obj.x)**2 + (self.y-obj.y)**2))

                    # calculates the coordinates of the furthest intersecting point for each ball
                    self.sintx, self.sinty = self.x + (((self.r * abs(obj.x - self.x))/self.p) * sign(obj.x - self.x)), self.y + (((self.r * abs(obj.y - self.y))/self.p) * sign(obj.y - self.y))  # self intersection
                    self.ointx, self.ointy = self.x + (((obj.r * abs(obj.x - self.x))/self.p) * sign(obj.x - self.x)), self.y + (((obj.r * abs(obj.y - self.y))/self.p) * sign(obj.y - self.y))  # obj intersection

                    # calculates the distance between the intersecting points and creates move values
                    self.h = sqrt((self.sintx - self.ointx) ** 2 + (self.sinty - self.ointy) ** 2) / 2
                    self.movex, self.movey = (self.h * abs(obj.x-self.x)) / self.p, (self.h * abs(obj.y-self.y)) / self.p

                    # moves the objects accordingly
                    self.x += floor(self.movex * sign(self.x - obj.x))
                    obj.x += floor(self.movex * sign(obj.x - self.x))
                    self.y += floor(self.movey * sign(self.y - obj.y))
                    obj.y += floor(self.movey * sign(obj.y - self.y))
                    self.xv *= EObject.b
                    self.yv *= EObject.b
                    print(round(sqrt(((self.x-obj.x)**2 + (self.y-obj.y)**2)) - (self.r+obj.r)))
                    # pg.draw.circle(SCREEN,(255,0,0),tcirc((self.x,self.y)),self.r)

            # side wall collisions
            if self.x <= self.r:
                self.x = self.r
                self.xv *= EObject.b
            elif self.x >= (SCR_WIDTH-self.r):
                self.x = SCR_WIDTH-self.r
                self.xv *= EObject.b

            # ground collisons
            if self.y <= self.r:
                self.y = self.r
                self.yv *= EObject.b

            pg.draw.circle(SCREEN, self.c, tcirc((self.x, self.y)), self.r)

    class Cube(EObject):
        def __init__(self, x, y, xv, v, m, c, xd, yd):
            super().__init__(x, y, xv, v, m)
            self.xd = xd  # x dim
            self.yd = yd  # y dim

        def update(self):
            super().update()

    ball_1 = Ball(200, 390, 0, 0, 0, (0, 255, 0), 0, 0, 10)
    ball_2 = Ball(350, 390, 0, 0, 0, (0, 0, 255), 0, 0, 5)

    # QIV -> QI transformations
    def trect(coords):  # transform rectangle (4 inputs)
        return (coords[0]+coords[2], SCR_HEIGHT-coords[1], -1*coords[2], -1*coords[3])

    def tcirc(coords):  # transform circle (2 inputs)
        return (coords[0], SCR_HEIGHT-coords[1])

    def rect(coords):  # quickly draw a black rectangle
        pg.draw.rect(SCREEN, (0, 0, 0), trect(coords))

    Object.reset_all()

    # main loop
    while True:

        # enables quitting by pressing q or clicking red x
        keys = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_q]:
                pg.quit()
                sys.exit()

        if keys[pg.K_r]:
            Object.reset_all()

        if keys[pg.K_s]:
            time.sleep(0.1)

        if keys[pg.K_d]:
            time.sleep(0.25)

        # builds Y-axis scale
        for x in range(TICK_MARKS):
            a = x*round(SCR_HEIGHT/TICK_MARKS)
            rect((0, a, 5, 2))
            SCREEN.blit(font.render(str(int((x*WLD_HEIGHT)/TICK_MARKS)) + UNIT, True, pg.Color('black')), trect((2, a+10, 10, a+5)))
        
        for instance in Object.instances:
            instance.update()

        # updates frame and resets
        pg.display.update()
        SCREEN.fill((255, 255, 255))


engine()
