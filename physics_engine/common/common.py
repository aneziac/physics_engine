import pygame as pg
from physics_engine.data import settings as st, colors
import time
import os


# QIV -> QI transformations
class Transform:
    def trect(self, x, y, a, b):  # transform rectangle (4 inputs)
        return (x + a, st.SCR_HEIGHT - y, -a, -b)

    def rect(self, surface, x, y, a, b):  # quickly draw a black rectangle
        pg.draw.rect(surface, colors.BLACK, self.trect(x, y, a, b))

    def tcirc(self, x, y):  # transform circle (2 inputs)
        return (x, st.SCR_HEIGHT - y)


class Text:
    def __init__(self):
        self.trans = Transform()

    def center_text(self, surface, text, color, font, height):
        rendered_text = font.render(text, True, color)
        surface.blit(rendered_text, self.trans.tcirc(int((st.SCR_WIDTH) / 2) - (font.size(text)[0] / 2), height))


class Files:
    def num_files(self, directory):
        return len([name for name in os.listdir(directory) if name != '.DS_Store'])


class Clock:
    def __init__(self, sim_speed):
        self.isim_speed = sim_speed
        self.frame = 0
        self.total_time = 0
        self.mem = []
        self.sample = 30
        self.reset_speed()

    def reset_speed(self):
        self.sim_speed = self.isim_speed

    def update(self):
        self.now = time.time()

    def update_info(self, dt):
        self.frame += 1 * self.relative_speed()
        self.total_time += dt

    def scale_speed(self, factor):
        self.sim_speed *= factor

    def relative_speed(self):
        return self.sim_speed / self.isim_speed

    def elapsed(self):
        return (time.time() - self.now) * self.sim_speed

    def fps(self, dt):
        dt /= self.sim_speed

        if dt != 0:
            self.mem.append(dt)
            if len(self.mem) > self.sample:
                del self.mem[0]
                avg = sum(self.mem) / self.sample
            else:
                avg = dt

            return round(1 / avg)

        else:
            return 60

    def current_time(self):
        return time.ctime(time.time())


clock = Clock(st.DEFAULT_SIM_SPEED)
