import pygame as pg
import os


IMAGES = {
    "PLAY": 'play.png',
    "PAUSE": 'pause.png',
    "IPLAY": 'iplay.png',
    "IPAUSE": 'ipause.png'
}

FONTS = {
    "LARGE_FONT": ['Beckman-Free.otf', 30],
    "FONT": ['Beckman-Free.otf', 20],
    "SMALL_FONT": ['Beckman-Free.otf', 10]
}


class LoadAssets:
    def __init__(self):
        self.load_images(IMAGES)
        self.load_fonts(FONTS)

    def load_images(self, images):
        for x in images:
            IMAGES[x] = pg.image.load(os.path.join('physics_engine/assets/images', IMAGES[x]))

    def load_fonts(self, fonts):
        for x in fonts:
            FONTS[x] = pg.font.Font(os.path.join('physics_engine/assets/fonts', FONTS[x][0]), FONTS[x][1])
