import pygame as pg
import settings as st

# QIV -> QI transformations
def trect(coords):  # transform rectangle (4 inputs)
    return (coords[0]+coords[2], st.SCR_HEIGHT-coords[1], -coords[2], -coords[3])

def rect(coords):  # quickly draw a black rectangle
    pg.draw.rect(SCREEN, (0, 0, 0), trect(coords))
    
def tcirc(coords):  # transform circle (2 inputs)
    return (coords[0], st.SCR_HEIGHT - coords[1])

total_time = 0
events = []
wld_height, wld_width = st.DWLD_HEIGHT, st.DWLD_HEIGHT
SCREEN = pg.display.set_mode([st.SCR_WIDTH, st.SCR_HEIGHT])  # creates screen
SCREEN.fill((255, 255, 255))  # blanks screen
pg.display.set_caption("physics_engine v.0.3.1")
