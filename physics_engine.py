import pygame as pg
import random as rm
from math import sqrt, pi
from numpy import sign
import common as cm
import settings as st

# independent universal constants
gc = 0.000000000066743  # gravitational constant
em = 5972370000000000000000000  # earth's mass (kg)
er = 6371000  # earth's radius (m)

# dependent universal constants
eg = round((gc * em) / (er ** 2), 3)  # earth gravity calculation

def reset_all():
    for instance in Object.instances:
        instance.reset()

# defines properties of all objects
class Object():
    instances = []

    def __init__(self, name, pos, vel, acc, mat, c, e):
        self.name = name
        # 'i' prefix = intial
        self.ix, self.iy = pos[0], pos[1]  # x position, y position
        self.ixv, self.iyv = vel[0], vel[1]  # x velocity, y velocity
        self.ixa, self.iya = acc[0], acc[1]  # x acceleration, y acceleration
        self.mat = mat # material
        self.ic = c  # color
        self.ie = -e  # COR - determine by material?
        Object.instances.append(self)

    def reset(self):
        self.x = self.ix
        self.y = self.iy
        self.xv = self.ixv
        self.yv = self.iyv
        self.xa = self.ixa
        self.ya = self.iya
        self.m = self.mat.d * self.v # mass
        self.c = self.ic
        self.e = self.ie
        self.eclock = 0
        self.equilibrium = False
        self.tyv = self.iyv

    def update(self, dt):
        if dt < 0:
            self.e = 1 / self.ie
        else:
            self.e = self.ie

        super().physics(dt)
        self.xv += self.xa * dt
        self.yv += self.ya * dt
        self.x += round(self.xv) * dt
        self.y += round(self.yv) * dt
        #if self.name == "ball 4":
        #    cm.events.append(str(round(self.y, 2)) + "\n")

    def render_vectors(self):
        pg.draw.line(cm.SCREEN, (255, 100, 0), cm.tcirc((super().scl(self.x), super().scl(self.y))), cm.tcirc((super().scl(self.x + (self.xa)), super().scl(self.y + (self.ya)))), 3)
        pg.draw.line(cm.SCREEN, (2, 100, 100), cm.tcirc((super().scl(self.x), super().scl(self.y))), cm.tcirc((super().scl(self.x + (self.xv)), super().scl(self.y + (self.yv)))), 3)
        
    def scl(self, x):
        return int((x * st.SCR_HEIGHT) / cm.wld_height)

class SPhysics():  # Space physics
    def physics(self, dt):
        for obj in Object.instances:
            if self.x != obj.x and self.y != obj.y:

                # calculates magnitude of acceleration vector
                self.am = -(gc * obj.m) * st.SPACE_GRAVITY_CATALYST / sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)
                # calculates acceleration vector
                if self.name != "star":
                    self.xa = self.am * ((self.x - obj.x) / sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2))
                    self.ya = self.am * ((self.y - obj.y) / sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2))

class EPhysics():  # Earth physics
    def __init__(self, dc, ra, m):
        self.dc = dc  # drag coefficient
        self.ra = ra  # reference area
        #self.w = eg * m # weight

    def physics(self, dt):
        # gravity
        self.ya = -eg
        # drag
        self.xa = -((st.FLUID.d * (self.xv ** 2) * self.dc * self.ra) / 2) / self.m * sign(self.xv)
        self.ya -= ((st.FLUID.d * (self.yv ** 2) * self.dc * self.ra) / 2) / self.m * sign(self.yv)
        # buoyancy
        self.ya += (self.v * st.FLUID.d * eg) / self.m
        # random velocity changes to test collisions
        #self.xv += ((rm.random() * 2) - 1) * 4

class Sphere(Object):
    def __init__(self, name, pos, vel, acc, mat, c, e, r):
        super().__init__(name, pos, vel, acc, mat, c, e)
        self.r = r
        self.v = 4/3 * pi * (r ** 3)

    def update(self, dt):
        super().update(dt)

        # object to object collisions
        for obj in Object.instances:

            # if the balls are intersecting
            if self.x != obj.x and self.y != obj.y and sqrt(((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)) <= (self.r + obj.r + (0 * cm.wld_height / st.SCR_HEIGHT)):  # calculate on per case basis
                self.xvo, self.yvo = self.xv, self.xv  # saves original values

                # calculates distance between centers of balls
                self.p = round(sqrt((((self.x - obj.x) ** 2) + ((self.y - obj.y) ** 2))), 2)

                # calculates the coordinates of the furthest intersecting point for each ball
                self.sintx, self.sinty = self.x + ((self.r * (obj.x - self.x)) / self.p), self.y + ((self.r * (obj.y - self.y)) / self.p)   # self intersection
                self.ointx, self.ointy = obj.x + ((obj.r * (self.x - obj.x)) / self.p), obj.y + ((obj.r * (self.y - obj.y)) / self.p)   # obj intersection

                # calculates the distance between the intersecting points and creates move values
                self.h = round(sqrt(((self.sintx - self.ointx) ** 2) + ((self.sinty - self.ointy) ** 2)) / 2, 2)
                self.movex, self.movey = (self.h * (self.x-obj.x) / self.p), (self.h * (self.y-obj.y) / self.p)

                self.colCOR = (self.e + obj.e) / 2  # collision coefficient of restitution

                # moves the objects accordingly, resolving the collision, then changes their velocities according to the conservation of momentum
                self.x += self.movex
                obj.x -= self.movex
                self.y += self.movey
                obj.y -= self.movey
                self.xv = ((self.colCOR * obj.m) * (obj.xv-self.xv) + (self.m * self.xv) + (obj.m * obj.xv)) / (self.m + obj.m)
                obj.xv = ((self.colCOR * self.m) * (self.xvo-obj.xv) + (self.m * self.xvo) + (obj.m * obj.xv)) / (self.m + obj.m)

                # come up with better way to test for in air
                if self.r != self.y or obj.r != obj.y:
                    self.yv = ((self.colCOR * obj.m) * (obj.yv-self.yv) + (self.m * self.yv) + (obj.m * obj.yv)) / (self.m + obj.m)
                    obj.yv = ((self.colCOR * self.m) * (self.yvo-obj.yv) + (self.m * self.yvo) + (obj.m * obj.yv)) / (self.m + obj.m)

                cm.events.append("Collision: %s on %s at %.2f secs\n" % (self.name, obj.name, cm.total_time))

    def render(self):
        pg.draw.circle(cm.SCREEN, self.c, cm.tcirc((super().scl(self.x), super().scl(self.y))), super().scl(self.r))

class Ball(Sphere, EPhysics):
    def __init__(self, name, pos, vel, acc, mat, c, e, r):
        Sphere.__init__(self, name, pos, vel, acc, mat, c, e, r)
        EPhysics.__init__(self, 0.47, round(pi * (self.r ** 2), 2), mat)

    def update(self, dt):
        super().update(dt)

        # wall collisions
        if self.x <= self.r:
            self.x = 2 * self.r - self.x
            self.xv *= self.e
            cm.events.append("Collision: %s on left wall at %.2f secs\n" % (self.name, cm.total_time))
        elif self.x >= (cm.wld_width - self.r):
            self.x = ((2 * cm.wld_width) - (2 * self.r) - self.x)
            self.xv *= self.e
            cm.events.append("Collision: %s on right wall at %.2f secs\n" % (self.name, cm.total_time))

        # ground collisons
        if self.y <= self.r:
            if self.yv * self.e * sign(dt) > -self.ya * dt * sign(dt):
                #if self.name == "ball 3": print((self.yv * sign(dt) * self.e) / (-self.ya * dt * sign(dt)))
                self.tyv = self.yv
                self.yv *= self.e
                self.ty = self.y
                self.y = 2 * self.r - (self.y)
                cm.events.append("Collision: %s on ground at %.2f secs\n" % (self.name, cm.total_time))

            else:
                self.eclock += dt
                self.equilibrium = True
                self.y = self.r
                self.yv = 0

            if self.eclock <= 0 and self.equilibrium:
                self.eclock = 0
                self.yv = self.tyv
                self.y = self.ty
                self.equilibrium = False

class Satellite(Sphere, SPhysics):
    # self.yv = sqrt((gc*self.m)/self.r) # circular orbit? return to
    pass
