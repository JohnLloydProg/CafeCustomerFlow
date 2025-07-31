import pygame as pg
pg.font.init()

def m(meters) -> int:
    return int(meters * 5)


FONTS = {
    'small':pg.font.Font(None, 16), 'medium':pg.font.Font(None, 20), 'large':pg.font.Font(None, 25)
    }

WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 900

MAP_SIZE = 500
