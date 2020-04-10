import pygame as pg
import random as rm
from physics_engine.data import settings as st, assets as at, colors
from physics_engine.common import common as cm


class Backgrounds:
    def __init__(self):
        self.trans = cm.Transform()

        self.STARS = []
        for x in range(st.STARS_AMOUNT):
            self.STARS.append([(rm.randint(0, st.SCR_WIDTH), rm.randint(0, st.SCR_HEIGHT)), rm.randint(2, 3)])

    def reset(self, sim_type):
        self.sim_type = sim_type

    def render(self, SCREEN, wld_dims):
        SCREEN.fill(colors.WHITE)

        if self.sim_type == "Earth":
            # builds Y-axis scale
            for x in range(st.TICK_MARKS):
                if x == 0:
                    n = 8
                else:
                    n = 0

                a = x * round(st.SCR_HEIGHT / st.TICK_MARKS)

                if x % 2 == 0:
                    pg.draw.rect(SCREEN, colors.GRAY, self.trans.trect(0, a, st.SCR_WIDTH, st.SCR_HEIGHT / st.TICK_MARKS))
                self.trans.rect(SCREEN, 0, a, 5, 2)

                rendered_text = at.FONTS["FONT"].render(str(int((x * wld_dims[1]) / st.TICK_MARKS)) + " " + st.UNIT, True, colors.BLACK)
                SCREEN.blit(rendered_text, self.trans.trect(2, a + 13 + n, 10, a))

                for x in range(st.SMALL_TICK_MARKS - 1):
                    b = (x + 1) * (round(st.SCR_HEIGHT / st.TICK_MARKS) / st.SMALL_TICK_MARKS)
                    self.trans.rect(SCREEN, 0, a + b, 3, 1)

        elif self.sim_type == "Space":
            SCREEN.fill(colors.BLACK)
            for x in range(st.STARS_AMOUNT):
                pg.draw.circle(SCREEN, colors.WHITE, self.STARS[x][0], self.STARS[x][1])
