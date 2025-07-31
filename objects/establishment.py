from settings import m
import pygame as pg


class Establishment:
    width = height = m(15)
    color = (160, 80, 120)

    def __init__(self, x:int, y:int):
        self.rect = pg.Rect(x, y, self.width, self.height)

    def draw(self, window:pg.Surface, offset:tuple[int, int]) -> None:
        x = offset[0] + self.rect.x
        y = offset[1] + self.rect.y
        pg.draw.rect(window, self.color, (x, y, self.width, self.height))

class School(Establishment):
    color = (120, 200, 169)
