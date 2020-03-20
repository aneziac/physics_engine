import pygame as pg
from data import common as cm, settings as st, sims, assets as at

clock = pg.time.Clock()

def render(keys):

    # time
    cm.SCREEN.blit(at.FONTS.render(str(round(cm.total_time, 2)), True, pg.Color('blue')), cm.trect((st.SCR_WIDTH - 55, st.SCR_HEIGHT - 10, 0, 0)))

    # time controls
    if abs(cm.sim_speed / st.DEFAULT_SIM_SPEED) < 1:
        if keys[pg.K_t]:
            tcoffset = round(100 * 2 / 7) # time control offset
        else:
            tcoffset = round(100 * 4 / 7)
    elif cm.sim_speed / st.DEFAULT_SIM_SPEED > 1:
        if keys[pg.K_t]:
            tcoffset = round(100 * 0 / 7)
        else:
            tcoffset = round(100 * 6 / 7)
    else:
        if keys[pg.K_t]:
            tcoffset = round(100 * 1 / 7)
        else:
            tcoffset = round(100 * 5 / 7)

    pg.draw.rect(cm.SCREEN, (200, 200, 200), cm.trect((10 + tcoffset, st.SCR_HEIGHT - 35, 14, 20)))
    cm.SCREEN.blit(at.FONTT.render(str(cm.sim_speed) + "x", True, cm.uicolor), cm.tcirc((53, st.SCR_HEIGHT - 35)))

    if cm.pause:
        if sims.SIM_TYPE == 0:
            cm.SCREEN.blit(at.PAUSE, cm.tcirc((10, st.SCR_HEIGHT - 15)))
        else:
            cm.SCREEN.blit(at.IPAUSE, cm.tcirc((10, st.SCR_HEIGHT - 15)))
    else:
        if sims.SIM_TYPE == 0:
            cm.SCREEN.blit(at.PLAY, cm.tcirc((10, st.SCR_HEIGHT - 15)))
        else:
            cm.SCREEN.blit(at.IPLAY, cm.tcirc((10, st.SCR_HEIGHT - 15)))

    # zoom
    if sims.SIM_TYPE == 0:
        pg.draw.rect(cm.SCREEN, (200, 200, 200), cm.trect(((at.FONTS.size("1 2 3 4 5")[0] / 5) * st.ZOOMS.index(cm.wld_height / st.DWLD_HEIGHT) + (st.SCR_WIDTH - 80), st.SCR_HEIGHT - 35 - at.FONTS.size("1 2 3 4 5")[1], at.FONTS.size("1 2 3 4 5")[0] / 5, at.FONTS.size("1 2 3 4 5")[1])))
    elif sims.SIM_TYPE == 1:
        pg.draw.rect(cm.SCREEN, (200, 200, 200), cm.trect(((at.FONTS.size("1 2 3 4 5")[0] / 5) * st.ZOOMS.index(cm.wld_height / st.DSPACE_HEIGHT) + (st.SCR_WIDTH - 80), st.SCR_HEIGHT - 35 - at.FONTS.size("1 2 3 4 5")[1], at.FONTS.size("1 2 3 4 5")[0] / 5, at.FONTS.size("1 2 3 4 5")[1])))

    cm.SCREEN.blit(at.FONTS.render("1 2 3 4 5", True, cm.uicolor), cm.tcirc((st.SCR_WIDTH - 80, st.SCR_HEIGHT - 35)))

    # fps
    clock.tick(30)
    cm.SCREEN.blit(at.FONTS.render(str(int(clock.get_fps())) + " fps", True, cm.uicolor), cm.tcirc((15, st.SCR_HEIGHT - 50)))
