import pygame as pg
import os

PLAY = pg.image.load(os.path.join('assets','play.png'))
PAUSE = pg.image.load(os.path.join('assets', 'pause.png'))
IPLAY = pg.image.load(os.path.join('assets','iplay.png'))
IPAUSE = pg.image.load(os.path.join('assets', 'ipause.png'))
FONT = pg.font.Font(os.path.join('assets', 'Beckman-Free.otf'), 30)  # regular font
FONTS = pg.font.Font(os.path.join('assets', 'Beckman-Free.otf'), 20)  # small font
FONTT = pg.font.Font(os.path.join('assets', 'Beckman-Free.otf'), 10)  # tiny font
