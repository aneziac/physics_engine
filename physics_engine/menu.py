import pygame as pg
import sys
from physics_engine.data import settings as st, assets as at, colors
from physics_engine.common import common as cm


class Menu:
    def __init__(self):
        self.trans = cm.Transform()
        self.text = cm.Text()
        self.active = False

    def reset(self, SCREEN, SIM_NAMES):
        self.active = True
        SCREEN.fill(colors.WHITE)  # blanks screen
        while self.active:
            buttons, spacing = self.graphics(SCREEN, SIM_NAMES)
            result = self.controls(SIM_NAMES, buttons, spacing)
        return result

    def graphics(self, SCREEN, SIM_NAMES):
        self.text.center_text(SCREEN, "Choose simulation", colors.BLACK, at.FONTS["LARGE_FONT"], st.SCR_HEIGHT - 80)
        buttons = []
        spacing = (st.SCR_HEIGHT - 200) / len(SIM_NAMES)
        for x in range(len(SIM_NAMES)):
            bheight = st.SCR_HEIGHT - 200 - (x * spacing)
            buttons.append(pg.draw.rect(SCREEN, colors.BLACK, self.trans.trect(st.SCR_WIDTH / 2 - 75, bheight, 150, min(spacing / 2, 70))))
            self.text.center_text(SCREEN, SIM_NAMES[x], colors.GREEN, at.FONTS["FONT"], bheight + at.FONTS["FONT"].size(SIM_NAMES[x])[1] + (spacing / 8))

        return buttons, spacing

    def controls(self, SIM_NAMES, buttons, spacing):
        keys = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_q]:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                clicked = [c for c in buttons if c.collidepoint(pg.mouse.get_pos())]

                if len(clicked) == 1:
                    self.active = False
                    return SIM_NAMES[int(((clicked[0][1]) / spacing))]

        pg.display.update()


menu = Menu()
