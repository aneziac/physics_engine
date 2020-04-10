import random as rm
from math import sqrt


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

    @staticmethod
    def physics_settings(fluid, temperature, gravity_catalyst):
        Physics.fluid = fluid
        Physics.temperature = temperature
        Physics.gravity_catalyst = gravity_catalyst

    def physics(self, dt):
        self.xv += self.xa * dt
        self.yv += self.ya * dt
        self.x += round(self.xv) * dt
        self.y += round(self.yv) * dt


class SPhysics(Physics):  # Space physics
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


class EPhysics(Physics):  # Earth physics
    def __init__(self, dc, ra):
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
