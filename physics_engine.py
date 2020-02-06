import pygame as pg
import sys
import time
import random as rm
from math import sqrt, floor, ceil


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
    
    #list of constants
    gc = 1 #gravitational constant
    em = 1000 #earth's mass (kg)
    er = 40 #earth's radius (m)
    
    # QIV -> QI transformations
    def trect(coords):  # transform rectangle (4 inputs)
        return (coords[0]+coords[2], SCR_HEIGHT-coords[1], -1*coords[2], -1*coords[3])

    def tcirc(coords):  # transform circle (2 inputs)
        return (coords[0], SCR_HEIGHT-coords[1])

    def rect(coords):  # quickly draw a black rectangle
        pg.draw.rect(SCREEN, (0, 0, 0), trect(coords))

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

        def __init__(self, x, y, xv, yv, m, c, xa, ya):
            super().__init__(x, y, xv, yv, m, c, xa, ya)
            SObject.bodies.append(self)

        def update(self):
            for obj in SObject.bodies:
                if self.x != obj.x and self.y != obj.y:
                    #calculates magnitude of acceleration vector
                    self.am = -1 * (gc * obj.m) / sqrt((self.x-obj.x)**2 + (self.y-obj.y)**2)                    
                    #calculates acceleration vector
                    self.xa = self.am*((self.x-obj.x)/sqrt((self.x-obj.x)**2 + (self.y-obj.y)**2))
                    self.ya = self.am*((self.y-obj.y)/sqrt((self.x-obj.x)**2 + (self.y-obj.y)**2))            
            super().update()

    class Satellite(SObject):
        def __init__(self, x, y, xv, yv, m, c, xa, ya, r):
            super().__init__(x, y, xv, yv, m, c, xa, ya)
            self.r = round((r*SCR_HEIGHT)/WLD_HEIGHT)  # radius
            self.b = -0.8

        def update(self):
            super().update()
            
            #make this a function later

            for obj in SObject.bodies:
                if self.x != obj.x and self.y != obj.y and sqrt(((self.x-obj.x)**2 + (self.y-obj.y)**2)) < (self.r + obj.r):
                    
                    self.p = round(sqrt(((self.x-obj.x)**2 + (self.y-obj.y)**2)),3)

                    # calculates the coordinates of the furthest intersecting point for each ball
                    self.sintx, self.sinty = self.x + ((self.r * (obj.x - self.x))/self.p), self.y + ((self.r * (obj.y - self.y))/self.p)  # self intersection
                    self.ointx, self.ointy = obj.x + ((obj.r * (self.x - obj.x))/self.p), obj.y + ((obj.r * (self.y - obj.y))/self.p)  # obj intersection

                    # calculates the distance between the intersecting points and creates move values
                    self.h = sqrt((self.sintx - self.ointx) ** 2 + (self.sinty - self.ointy) ** 2) / 2
                    self.movex, self.movey = floor((self.h * (self.x-obj.x)) / self.p)-1, floor((self.h * (self.y-obj.y)) / self.p)

                    # moves the objects accordingly
                    self.x += self.movex
                    obj.x += self.movex * -1
                    self.y += self.movey
                    obj.y += self.movey * -1
                    self.xv *= self.b
                    self.yv *= self.b
            
            pg.draw.circle(SCREEN, self.c, tcirc((self.x, self.y)), self.r)

    #sat1 = Satellite(200, 380, 0, 0, 5, (0, 0, 0), 0, 0, 5)
    #sat2 = Satellite(100, 50, 0, 0, 30, (0, 0, 0), 0, 0, 10)

    class EObject(Object):  # "Earth" objects
        instances = []

        def __init__(self, x, y, xv, yv, m, c, xa, ya):
            super().__init__(x, y, xv, yv, m, c, xa, ya)
            EObject.instances.append(self)

        def update(self):
            self.xv += round((rm.random()*2)-1, 2)
            super().update()

        def reset(self):
            super().reset()
            self.ya = -(gc*em)/(er**2)  # gravity setting -0.5

    class Ball(EObject):
        def __init__(self, x, y, xv, yv, m, c, xa, ya, r, b):
            super().__init__(x, y, xv, yv, m, c, xa, ya)
            self.r = round((r*SCR_HEIGHT)/WLD_HEIGHT)  # radius
            self.b = -1 * b #bounciness

        def update(self):
            super().update()

            # object to object collisions
            for obj in EObject.instances:
                # if the balls are intersecting
                if self.x != obj.x and self.y != obj.y and ceil(sqrt(((self.x-obj.x)**2 + (self.y-obj.y)**2))) <= (self.r + obj.r):
                    
                    #print(round(sqrt(((self.x-obj.x)**2 + (self.y-obj.y)**2)) - (self.r+obj.r)), " before ",end='')

                    # calculates distance between centers of balls
                    self.p = round(sqrt(((self.x-obj.x)**2 + (self.y-obj.y)**2)),3)

                    # calculates the coordinates of the furthest intersecting point for each ball
                    self.sintx, self.sinty = self.x + ((self.r * (obj.x - self.x))/self.p), self.y + ((self.r * (obj.y - self.y))/self.p)  # self intersection
                    self.ointx, self.ointy = obj.x + ((obj.r * (self.x - obj.x))/self.p), obj.y + ((obj.r * (self.y - obj.y))/self.p)  # obj intersection

                    # calculates the distance between the intersecting points and creates move values
                    self.h = sqrt((self.sintx - self.ointx) ** 2 + (self.sinty - self.ointy) ** 2) / 2
                    self.movex, self.movey = ceil((self.h * (self.x-obj.x)) / self.p), ceil((self.h * (self.y-obj.y)) / self.p)

                    # moves the objects accordingly
                    self.x += self.movex
                    obj.x += self.movex * -1
                    self.y += self.movey
                    obj.y += self.movey * -1
                    self.xv *= self.b
                    self.yv *= self.b
                    
                    #print(round(sqrt(((self.x-obj.x)**2 + (self.y-obj.y)**2)) - (self.r+obj.r))," after")

            # side wall collisions
            if self.x <= self.r:
                self.x = self.r
                self.xv *= self.b
            elif self.x >= (SCR_WIDTH-self.r):
                self.x = SCR_WIDTH-self.r
                self.xv *= self.b

            # ground collisons
            if self.y <= self.r:
                self.y = self.r
                self.yv *= self.b

            pg.draw.circle(SCREEN, self.c, tcirc((self.x, self.y)), self.r)

    class Cube(EObject):
        def __init__(self, x, y, xv, v, m, c, xd, yd):
            super().__init__(x, y, xv, v, m)
            self.xd = xd  # x dim
            self.yd = yd  # y dim

        def update(self):
            super().update()

    ball_1 = Ball(200, 390, 0, 0, 0, (0, 255, 0), 0, 0, 10, 0.6)
    ball_2 = Ball(350, 390, 0, 0, 0, (0, 0, 255), 0, 0, 5, 0.8)

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
