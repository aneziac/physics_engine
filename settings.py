import pygame as pg
import materials as mat

pg.init()

SCR_WIDTH, SCR_HEIGHT = 400, 400  # screen dimensions
DWLD_WIDTH, DWLD_HEIGHT = 50, 50  # default world dimensions
DSPACE_WIDTH, DSPACE_HEIGHT = 400, 400 # default space dimensions
UNIT = "m"  # unit for Y-axis scale
TICK_MARKS = 5  # number of Y-axis tick marks
FONT = pg.font.Font("Beckman-Free.otf", 30)  # regular font
FONTS = pg.font.Font("Beckman-Free.otf", 20)  # small font
FONTT = pg.font.Font("Beckman-Free.otf", 10) # tiny font
SHOW_VECTORS = False  # displays acceleration and velocity vectors
EVENT_LOG = False
STARS_AMOUNT = 50
DEFAULT_SIM_SPEED = 1 # speed of simulation. 1 is real time.
FLUID = mat.Air
SPACE_GRAVITY_CATALYST = 100000
