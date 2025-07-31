from settings import m
from objects.establishment import Establishment, School
import pygame as pg
import random
import math


class Customer:
    width = m(1.4)
    height = m(1.6)
    stayed = 0
    served = False
    target = None
    source = Establishment
    color = (255, 0, 0)

    def __init__(self, x, y, has_gadget:bool, impatience:float):
        self.rect = pg.Rect(x, y, self.width, self.height)
        self.velocity = m(random.normalvariate(1.34, 0.26))
        if (has_gadget):
            self.waiting_time = int(random.normalvariate(171.875, 95.187332) * 60)
        else:
            self.waiting_time = int(random.normalvariate(44.840351, 42.290102) * 60)
        self.impatience = impatience
        self.chance_of_leaving = impatience
        self.previous = []
        self.counter = 0
        self.has_gadget = has_gadget
    
    def move(self):
        if self.rect.centerx > self.target.rect.centerx:
            self.rect.x -= self.velocity
        if self.rect.centerx < self.target.rect.centerx:
            self.rect.x += self.velocity
        if self.rect.centery > self.target.rect.centery:
            self.rect.y -= self.velocity
        if self.rect.centery < self.target.rect.centery:
            self.rect.y += self.velocity
    
    def decide(self, cafes:list):
        self.counter += 1
        if (self.counter % 60 == 0):
            if random.random() <= self.chance_of_leaving:
                self.reselect(cafes)
                self.counter = 0
            else:
                self.stayed += 1
                self.chance_of_leaving += self.stayed * 0.0001

    
    def reselect(self, cafes:list):
        if (self.target):
            self.previous.append(self.target)
        if (len(cafes) == 0):
            print('empty list!')
        selection = cafes.copy()
        if len(selection) > 1:
            for cafe in cafes:
                if cafe in self.previous or not cafe.open:
                    selection.remove(cafe)
                elif self.has_gadget and not cafe.has_outlets:
                    selection.remove(cafe)
            try:
                nearest_cafe = min(selection, key=lambda cafe: math.dist(self.rect.center, cafe.rect.center))
                self.target = nearest_cafe
                self.stayed = 0
                self.chance_of_leaving = self.impatience
                return True
            except ValueError:
                return False
        else:
            self.target = selection[0]
            return True
    
    def draw(self, window:pg.Surface, offset):
        x = offset[0] + self.rect.x
        y = offset[1] + self.rect.y
        if (not self.served):
            pg.draw.rect(window, self.color, (x, y, self.width, self.height))


class Student(Customer):
    color = (0, 255, 0)
    source = School

    def __init__(self, x, y, has_gadget:bool, impatience:float):
        super().__init__(x, y, has_gadget, impatience)
        if (has_gadget):
            self.waiting_time = int(random.normalvariate(107.914286, 44.650753) * 60)
        else:
            self.waiting_time = int(random.normalvariate(68.341667, 63.006816) * 60)
        self.budget = random.normalvariate(128.68852459016392, 60.17960368308811)
    
    def reselect(self, cafes:list):
        if (self.target):
            self.previous.append(self.target)
        selection = cafes.copy()
        if len(selection) > 1:
            for cafe in cafes:
                if cafe in self.previous or not cafe.open:
                    selection.remove(cafe)
                elif self.has_gadget and not cafe.has_outlets:
                    selection.remove(cafe)
            try:
                nearest_cafe = min(selection, key=lambda cafe: math.dist(self.rect.center, cafe.rect.center))
                self.target = nearest_cafe
                self.stayed = 0
                self.chance_of_leaving = self.impatience
                return True
            except ValueError:
                return False
        else:
            self.target = selection[0]
            return True
    
    def reselect(self, cafes:list):
        if (self.target):
            self.previous.append(self.target)
        selection = cafes.copy()
        for cafe in cafes:
            if cafe in self.previous or not cafe.open:
                selection.remove(cafe)
            elif self.has_gadget and not cafe.has_outlets:
                selection.remove(cafe)
            elif self.budget < cafe.base_price:
                selection.remove(cafe)
        try:
            nearest_cafe = min(selection, key=lambda cafe: math.dist(self.rect.center, cafe.rect.center))
            self.target = nearest_cafe
            self.stayed = 0
            self.chance_of_leaving = self.impatience
            return True
        except ValueError:
            return False
