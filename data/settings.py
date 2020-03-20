import pygame as pg

SCR_WIDTH, SCR_HEIGHT = 600, 600  # screen dimensions
DWLD_WIDTH, DWLD_HEIGHT = 50, 50  # default world dimensions
DSPACE_WIDTH, DSPACE_HEIGHT = 400, 400 # default space dimensions
UNIT = "m"  # unit for Y-axis scale
TICK_MARKS = 5  # number of Y-axis tick marks
SHOW_VECTORS = False  # displays acceleration and velocity vectors
EVENT_LOG = False
STARS_AMOUNT = 50
DEFAULT_SIM_SPEED = 1 # speed of simulation. 1 is real time.
ZOOMS = [0.2, 0.5, 1, 2, 5]
SPEEDS = [2, 10, 50, 100]
SPACE_GRAVITY_CATALYST = 100000
