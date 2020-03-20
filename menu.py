import pygame as pg
import sys
import settings as st
import common as cm
import sims

def menu():
    while True:

        cm.SCREEN.blit(st.FONT.render("Choose simulation", True, pg.Color('black')), cm.tcirc((int((st.SCR_WIDTH / 2) - (st.FONT.size("Choose simulation")[0] / 2)), st.SCR_HEIGHT - 80)))
        buttons = []
        spacing = (st.SCR_HEIGHT - 200) / len(sims.SIM_NAMES)
        for x in range(len(sims.SIM_NAMES)):
            buttons.append(pg.draw.rect(cm.SCREEN, (0, 0, 0), cm.trect((st.SCR_WIDTH / 2 - 75, st.SCR_HEIGHT - 200 - (x * spacing), 150, spacing / 2))))
            cm.SCREEN.blit(st.FONTS.render(sims.SIM_NAMES[x], True, (0, 200, 0)), cm.tcirc((int((st.SCR_WIDTH / 2) - (st.FONTS.size(sims.SIM_NAMES[x])[0] / 2)), st.SCR_HEIGHT - 200 - (x * spacing) + st.FONTS.size(sims.SIM_NAMES[x])[1] + (spacing / 8))))
        keys = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_q]:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                clicked = [c for c in buttons if c.collidepoint(pg.mouse.get_pos())]

                if len(clicked) == 1:
                    return int(((clicked[0][1]) / spacing)) - 1

        pg.display.update()
