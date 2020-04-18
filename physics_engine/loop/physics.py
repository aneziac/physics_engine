import random as rm
from math import sqrt
import pygame as pg
import physics_engine.data.colors as colors


class Constants:
    def __init__(self):
        # independent universal constants
        self.gc = 0.000000000066743  # gravitational constant
        self.em = 5972370000000000000000000  # earth's mass (kg)
        self.er = 6371000  # earth's radius (m)

        # dependent universal constants
        self.eg = round((self.gc * self.em) / (self.er ** 2), 3)  # earth gravity calculation

    def sign(self, x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            return 0


class Physics():
    cons = Constants()

    def __init__(self, pos, vel=[0, 0], acc=[0, 0]):
        # 'i' prefix means intial
        self.ipos = pos
        self.ivel = vel
        self.iacc = acc

    @staticmethod
    def physics_settings(fluid, temperature, gravity_catalyst):
        Physics.fluid = fluid
        Physics.temperature = temperature
        Physics.gravity_catalyst = gravity_catalyst

    def reset_physics(self):
        self.x, self.y = self.ipos
        self.xv, self.yv = self.ivel
        self.xa, self.ya = self.iacc

    def physics(self, dt):
        self.xv += self.xa * dt
        self.yv += self.ya * dt
        self.x += self.xv * dt
        self.y += self.yv * dt

    def collision(self, obj, colCOR):
        self.xv = ((colCOR * obj.m) * (obj.xv - self.xv) + (self.m * self.xv) + (obj.m * obj.xv)) / (self.m + obj.m)
        obj.xv = ((colCOR * self.m) * (self.xvo - obj.xv) + (self.m * self.xvo) + (obj.m * obj.xv)) / (self.m + obj.m)

        if self.r != self.y or obj.r != obj.y:
            self.yv = ((colCOR * obj.m) * (obj.yv - self.yv) + (self.m * self.yv) + (obj.m * obj.yv)) / (self.m + obj.m)
            obj.yv = ((colCOR * self.m) * (self.yvo - obj.yv) + (self.m * self.yvo) + (obj.m * obj.yv)) / (self.m + obj.m)

    def render_vectors(self, SCREEN, wld_dims):
        def draw_line(a, b, color):
            def scale(x):
                return super().scl(x, wld_dims)
            pg.draw.line(SCREEN, color, self.trans.tcirc(scale(self.x), scale(self.y), self.trans.tcirc(scale(self.x + a), scale(self.y + b))), 3)

        draw_line(self.xv, self.yv, colors.ORANGE)
        draw_line(self.xa, self.ya, colors.PURPLE)


class SpacePhysics(Physics):  # Space physics
    def __init__(self, pos, vel, acc):
        super().__init__(pos, vel, acc)

    def physics(self, dt, instances):
        super().physics(dt)

        for obj in instances:
            if self.x != obj.x and self.y != obj.y:

                # calculates magnitude of acceleration vector
                self.am = -(Physics.cons.gc * obj.m) * Physics.gravity_catalyst / sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)

                # calculates acceleration vector
                if self.name != "star":
                    self.xa = self.am * ((self.x - obj.x) / sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2))
                    self.ya = self.am * ((self.y - obj.y) / sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2))


class EarthPhysics(Physics):  # Earth physics
    def __init__(self, pos, vel, acc, dc, ra):
        super().__init__(pos, vel, acc)
        self.dc = dc  # drag coefficient
        self.ra = ra  # reference area

    def physics(self, dt, instances):
        super().physics(dt)

        # gravity
        self.ya = -Physics.cons.eg * Physics.gravity_catalyst

        # drag
        self.xa = -((Physics.fluid.d * (self.xv ** 2) * self.dc * self.ra) / 2) / self.m * self.cons.sign(self.xv)
        self.ya -= ((Physics.fluid.d * (self.yv ** 2) * self.dc * self.ra) / 2) / self.m * self.cons.sign(self.yv)

        # buoyancy
        self.ya += (self.v * self.fluid.d * self.cons.eg) / self.m

        # random velocity changes to test collisions
        self.xv += ((rm.random() * 2) - 1) * 4
