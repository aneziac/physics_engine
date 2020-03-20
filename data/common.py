import pygame as pg
import data.settings as st

# QIV -> QI transformations
def trect(coords):  # transform rectangle (4 inputs)
    return (coords[0]+coords[2], st.SCR_HEIGHT-coords[1], -coords[2], -coords[3])

def rect(coords):  # quickly draw a black rectangle
    pg.draw.rect(SCREEN, (0, 0, 0), trect(coords))
    
def tcirc(coords):  # transform circle (2 inputs)
    return (coords[0], st.SCR_HEIGHT - coords[1])

total_time = 0
events = []
pause = False
uicolor = (0, 0, 0)
fluid = 0
sim_speed = 0
wld_height, wld_width = st.DWLD_HEIGHT, st.DWLD_HEIGHT
SCREEN = pg.display.set_mode([st.SCR_WIDTH, st.SCR_HEIGHT])  # creates screen
