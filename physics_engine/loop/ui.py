import pygame as pg
from physics_engine.data import settings as st, assets as at, colors
from physics_engine.common import common as cm


class UI:
    def __init__(self):
        self.trans = cm.Transform()

    def reset(self, sim_type):
        if sim_type == "Earth":
            self.color = colors.BLACK
            self.secondary = colors.YELLOW
        elif sim_type == "Space":
            self.color = colors.WHITE
            self.secondary = colors.BLUE
        self.sim_type = sim_type

    def render(self, SCREEN, keys, dt, pause, scl_index):
        self.time(SCREEN)
        self.time_controls(SCREEN, keys, pause)
        self.zoom(SCREEN, scl_index)
        self.fps(SCREEN, dt)

    def time(self, SCREEN):
        rendered_text = at.FONTS["FONT"].render(str(round(cm.clock.total_time, 2)), True, colors.BLUE)
        SCREEN.blit(rendered_text, self.trans.tcirc(st.SCR_WIDTH - 55, st.SCR_HEIGHT - 10))

    def time_controls(self, SCREEN, keys, pause):
        if abs(cm.clock.relative_speed()) < 1:
            if keys[pg.K_t]:
                tcoffset = round(100 * 2 / 7)  # time control offset
            else:
                tcoffset = round(100 * 4 / 7)
        elif cm.clock.relative_speed() > 1:
            if keys[pg.K_t]:
                tcoffset = round(100 * 0 / 7)
            else:
                tcoffset = round(100 * 6 / 7)
        else:
            if keys[pg.K_t]:
                tcoffset = round(100 * 1 / 7)
            else:
                tcoffset = round(100 * 5 / 7)

        pg.draw.rect(SCREEN, self.secondary, self.trans.trect(10 + tcoffset, st.SCR_HEIGHT - 35, 14, 20))
        SCREEN.blit(at.FONTS["SMALL_FONT"].render(str(cm.clock.sim_speed) + "x", True, self.color), self.trans.tcirc(53, st.SCR_HEIGHT - 35))

        if pause:
            if self.sim_type == "Earth":
                SCREEN.blit(at.IMAGES["PAUSE"], self.trans.tcirc(10, st.SCR_HEIGHT - 15))
            else:
                SCREEN.blit(at.IMAGES["IPAUSE"], self.trans.tcirc(10, st.SCR_HEIGHT - 15))
        else:
            if self.sim_type == "Earth":
                SCREEN.blit(at.IMAGES["PLAY"], self.trans.tcirc(10, st.SCR_HEIGHT - 15))
            else:
                SCREEN.blit(at.IMAGES["IPLAY"], self.trans.tcirc(10, st.SCR_HEIGHT - 15))

    def zoom(self, SCREEN, scl_index):
        width = at.FONTS["FONT"].size("1 2 3 4 5")[0] / 5
        height = at.FONTS["FONT"].size("1 2 3 4 5")[1]
        pg.draw.rect(SCREEN, self.secondary, self.trans.trect(width * scl_index + (st.SCR_WIDTH - 80), st.SCR_HEIGHT - 35 - height, width, height))

        SCREEN.blit(at.FONTS["FONT"].render("1 2 3 4 5", True, self.color), self.trans.tcirc(st.SCR_WIDTH - 80, st.SCR_HEIGHT - 35))

    def fps(self, SCREEN, dt):
        SCREEN.blit(at.FONTS["FONT"].render(str(int(cm.clock.fps(dt))) + " fps", True, self.color), self.trans.tcirc(15, st.SCR_HEIGHT - 50))
