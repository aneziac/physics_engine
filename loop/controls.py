import pygame as pg
from data import common as cm, settings as st, sims

def all(keys):
    zooms(keys)
    speeds(keys)

def zooms(keys):
    if keys[pg.K_1]:
        if sims.SIM_TYPE == 0:
            cm.wld_width, cm.wld_height = st.DWLD_WIDTH, st.DWLD_HEIGHT * st.ZOOMS[0]
        else:
            cm.wld_width, cm.wld_height = st.DSPACE_WIDTH, st.DSPACE_HEIGHT * st.ZOOMS[0]
    elif keys[pg.K_2]:
        if sims.SIM_TYPE == 0:
            cm.wld_width, cm.wld_height = st.DWLD_WIDTH, st.DWLD_HEIGHT * st.ZOOMS[1]
        else:
            cm.wld_width, cm.wld_height = st.DSPACE_WIDTH, st.DSPACE_HEIGHT * st.ZOOMS[1]
    elif keys[pg.K_3]:
        if sims.SIM_TYPE == 0:
            cm.wld_width, cm.wld_height = st.DWLD_WIDTH, st.DWLD_HEIGHT * st.ZOOMS[2]
        else:
            cm.wld_width, cm.wld_height = st.DSPACE_WIDTH, st.DSPACE_HEIGHT * st.ZOOMS[2]
    elif keys[pg.K_4]:
        if sims.SIM_TYPE == 0:
            cm.wld_width, cm.wld_height = st.DWLD_WIDTH, st.DWLD_HEIGHT * st.ZOOMS[3]
        else:
            cm.wld_width, cm.wld_height = st.DSPACE_WIDTH, st.DSPACE_HEIGHT * st.ZOOMS[3]
    elif keys[pg.K_5]:
        if sims.SIM_TYPE == 0:
            cm.wld_width, cm.wld_height = st.DWLD_WIDTH, st.DWLD_HEIGHT * st.ZOOMS[4]
        else:
            cm.wld_width, cm.wld_height = st.DSPACE_WIDTH, st.DSPACE_HEIGHT * st.ZOOMS[4]

def speeds(keys):
    cm.sim_speed = st.DEFAULT_SIM_SPEED

    if keys[pg.K_t]:
        cm.sim_speed *= -1
    if keys[pg.K_a]:
        cm.sim_speed /= st.SPEEDS[3]
    elif keys[pg.K_s]:
        cm.sim_speed /= st.SPEEDS[2]
    elif keys[pg.K_d]:
        cm.sim_speed /= st.SPEEDS[1]
    elif keys[pg.K_f]:
        cm.sim_speed /= st.SPEEDS[0]
    elif keys[pg.K_j]:
        cm.sim_speed *= st.SPEEDS[0]
    elif keys[pg.K_k]:
        cm.sim_speed *= st.SPEEDS[1]
    elif keys[pg.K_l]:
        cm.sim_speed *= st.SPEEDS[2]
    elif keys[pg.K_SEMICOLON]:
        cm.sim_speed *= st.SPEEDS[3]
