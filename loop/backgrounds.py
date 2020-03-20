import pygame as pg
import random as rm
from data import common as cm, settings as st, sims, assets as at

STARS = []
for x in range(st.STARS_AMOUNT):
    STARS.append([(rm.randint(0, st.SCR_WIDTH), rm.randint(0, st.SCR_HEIGHT)), rm.randint(2, 3)])

def render():
    if sims.SIM_TYPE == 0:
        # builds Y-axis scale
        for x in range(st.TICK_MARKS):
            a = x * round(st.SCR_HEIGHT / st.TICK_MARKS)
            if x % 2 == 0:
                pg.draw.rect(cm.SCREEN, (240, 240, 240), cm.trect([0, a, st.SCR_WIDTH, st.SCR_HEIGHT / st.TICK_MARKS]))
            cm.rect((0, a, 5, 2))
            cm.SCREEN.blit(at.FONTS.render(str(int((x * cm.wld_height) / st.TICK_MARKS)) + " " + st.UNIT, True, pg.Color('black')), cm.trect((2, a + 13, 10, a)))

    elif sims.SIM_TYPE == 1:
        cm.SCREEN.fill((0, 0, 0))
        for x in range(st.STARS_AMOUNT):
            pg.draw.circle(cm.SCREEN, (255, 255, 255), STARS[x][0], STARS[x][1])
