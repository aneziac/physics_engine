import pygame as pg
from math import sqrt, pi, ceil
from physics_engine.common import common as cm
from physics_engine.data import settings as st, materials as mats
from physics_engine.loop import physics as phys


# defines properties of all objects
class Object():
    instances = []

    def __init__(self, name, pos, vel=[0, 0], acc=[0, 0], mat=mats.Iron, c=(255, 255, 255), e=0.7):
        self.name = name
        # 'i' prefix = intial
        self.ix, self.iy = pos[0], pos[1]  # x position, y position
        self.ixv, self.iyv = vel[0], vel[1]  # x velocity, y velocity
        self.ixa, self.iya = acc[0], acc[1]  # x acceleration, y acceleration
        self.mat = mat  # material
        self.ic = c  # color
        self.ie = -e  # COR - determine by material?

        Object.instances.append(self)
        self.trans = cm.Transform()

    def reset(self):
        self.x = self.ix
        self.y = self.iy
        self.xv = self.ixv
        self.yv = self.iyv
        self.xa = self.ixa
        self.ya = self.iya
        self.m = self.mat.d * self.v  # mass
        self.c = self.ic
        self.e = self.ie
        self.locs = [[self.x, self.y]]

    @staticmethod
    def reset_all():
        for instance in Object.instances:
            instance.reset()
        cm.clock.total_time = 0
        cm.clock.frame = 0

    @staticmethod
    def hide_all():
        for instance in Object.instances:
            instance.show = False

    def update(self, dt, events, wld_dims):
        if dt < 0:
            try:
                self.x, self.y = self.locs[round(cm.clock.frame)][0], self.locs[round(cm.clock.frame)][1]
            except IndexError:
                print("ERROR")

        elif dt > 0:
            super().physics(dt, Object.instances)

            rspeed = cm.clock.relative_speed()
            if rspeed <= 1 and round(cm.clock.frame) % round(1 / (rspeed)) == 0:
                self.locs.append([self.x, self.y])
            else:
                # linear interpolation to estimate lost data
                oldx, oldy = self.locs[-1][0], self.locs[-1][1]
                xstep, ystep = (self.x - oldx) / rspeed, (self.y - oldy) / rspeed
                for x in range(ceil(rspeed)):
                    self.locs.append([round(x * xstep) + oldx, round(x * ystep) + oldy])

    def render_vectors(self, SCREEN, wld_dims):
        def draw_line(a, b, color):
            def scale(x):
                return super().scl(x, wld_dims)
            pg.draw.line(SCREEN, color, self.trans.tcirc(scale(self.x), scale(self.y), self.trans.tcirc(scale(self.x + a), scale(self.y + b))), 3)

        draw_line(self.xv, self.yv, (255, 100, 0))
        draw_line(self.xa, self.ya, (2, 100, 100))

    def scl(self, x, wld_dims):
        return int((x * st.SCR_HEIGHT) / wld_dims[1])


class Sphere(Object):
    def __init__(self, name, pos, vel, acc, mat, c, e, r):
        super().__init__(name, pos, vel, acc, mat, c, e)
        self.r = r
        self.v = 4 / 3 * pi * (r ** 3)

    def update(self, dt, events, wld_dims):
        super().update(dt, events, wld_dims)

        # object to object collisions
        for obj in Object.instances:

            # if the balls are intersecting
            if self.x != obj.x and self.y != obj.y and sqrt(((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)) <= self.r + obj.r:
                self.xvo, self.yvo = self.xv, self.xv  # saves original values

                # calculates distance between centers of balls
                self.p = round(sqrt((((self.x - obj.x) ** 2) + ((self.y - obj.y) ** 2))), 2)

                # calculates the coordinates of the furthest intersecting point for each ball
                self.sintx, self.sinty = self.x + ((self.r * (obj.x - self.x)) / self.p), self.y + ((self.r * (obj.y - self.y)) / self.p)   # self intersection
                self.ointx, self.ointy = obj.x + ((obj.r * (self.x - obj.x)) / self.p), obj.y + ((obj.r * (self.y - obj.y)) / self.p)   # obj intersection

                # calculates the distance between the intersecting points and creates move values
                self.h = round(sqrt(((self.sintx - self.ointx) ** 2) + ((self.sinty - self.ointy) ** 2)) / 2, 2)
                self.movex, self.movey = (self.h * (self.x - obj.x) / self.p), (self.h * (self.y - obj.y) / self.p)

                self.colCOR = (self.e + obj.e) / 2  # collision coefficient of restitution

                # moves the objects accordingly, resolving the collision, then changes their velocities according to the conservation of momentum
                self.x += self.movex
                obj.x -= self.movex
                self.y += self.movey
                obj.y -= self.movey
                self.xv = ((self.colCOR * obj.m) * (obj.xv - self.xv) + (self.m * self.xv) + (obj.m * obj.xv)) / (self.m + obj.m)
                obj.xv = ((self.colCOR * self.m) * (self.xvo - obj.xv) + (self.m * self.xvo) + (obj.m * obj.xv)) / (self.m + obj.m)

                # come up with better way to test for in air
                if self.r != self.y or obj.r != obj.y:
                    self.yv = ((self.colCOR * obj.m) * (obj.yv - self.yv) + (self.m * self.yv) + (obj.m * obj.yv)) / (self.m + obj.m)
                    obj.yv = ((self.colCOR * self.m) * (self.yvo - obj.yv) + (self.m * self.yvo) + (obj.m * obj.yv)) / (self.m + obj.m)

                events.append("Collision: %s on %s at %.2f secs\n" % (self.name, obj.name, cm.clock.total_time))

    def render(self, SCREEN, wld_dims):
        pg.draw.circle(SCREEN, self.c, self.trans.tcirc(super().scl(self.x, wld_dims), super().scl(self.y, wld_dims)), super().scl(self.r, wld_dims))


class Ball(Sphere, phys.EPhysics):
    def __init__(self, name, pos, vel, acc, mat, c, e, r):
        Sphere.__init__(self, name, pos, vel, acc, mat, c, e, r)
        phys.EPhysics.__init__(self, 0.47, round(pi * (self.r ** 2)))

    def update(self, dt, events, wld_dims):
        super().update(dt, events, wld_dims)

        # wall collisions
        if self.x <= self.r:
            self.x = 2 * self.r - self.x
            self.xv *= self.e
            events.append("Collision: %s on left wall at %.2f secs\n" % (self.name, cm.clock.total_time))

        elif self.x >= (wld_dims[0] - self.r):
            self.x = ((2 * wld_dims[0]) - (2 * self.r) - self.x)
            self.xv *= self.e
            events.append("Collision: %s on right wall at %.2f secs\n" % (self.name, cm.clock.total_time))

        # ground collisons
        if self.y <= self.r:
            self.yv *= self.e
            self.y = 2 * self.r - (self.y)
            events.append("Collision: %s on ground at %.2f secs\n" % (self.name, cm.clock.total_time))


class Satellite(Sphere, phys.SPhysics):
    # self.yv = sqrt((gc*self.m)/self.r) # circular orbit? return to
    pass
