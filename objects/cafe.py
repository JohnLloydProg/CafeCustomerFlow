from settings import m, FONTS
from objects.customer import Customer
import pygame as pg
import random


class Cafe:
    width = height = m(15)
    customers_served = 0
    rental_price_per_capacity = 1800

    def __init__(self, x:int, y:int, base_price:int, has_outlets:bool, maximum_capacity:int, all_day:bool, owner_cafe:bool = False):
        self.rect = pg.Rect(x, y, self.width, self.height)
        self.customers = []
        self.occupancies = []
        self.max_capacity = maximum_capacity
        self.owner_cafe = owner_cafe
        self.has_outlets = has_outlets
        self.all_day = all_day
        self.base_price = base_price
        self.open = self.all_day
        self.utility_cost = 0
    
    def serving(self, counter:int):
        days = counter // 86400
        hours = (counter - (days * 86400)) // 3600

        self.open = self.all_day or (8<=hours<=22)
        if (self.open):
            for customer in self.customers:
                customer.waiting_time -= 1
                if (customer.has_gadget):
                    if (counter % 60 == 0):
                        self.utility_cost += 0.00915
                if customer.waiting_time == 0:
                    self.customers.remove(customer)
            
            if ((counter % (20 * 60)) == 0):
                self.occupancies.append(len(self.customers) / self.max_capacity)
            
            if ((counter % 3600) == 0):
                self.utility_cost += random.randint(11, 21) + (self.max_capacity * 0.085)
        
    
    def get_average_occupancies(self):
        average = round((sum(self.occupancies) / len(self.occupancies)) * 100) if len(self.occupancies) > 0 else 0
        return average
    
    def get_minimum_revenue(self):
        return self.customers_served * (self.base_price * 0.50)

    def get_cost(self):
        return (self.rental_price_per_capacity * self.max_capacity) + self.utility_cost
    
    def enter(self, customer:Customer):
        if (len(self.customers) < self.max_capacity and not customer.served):
            self.customers.append(customer)
            self.customers_served += 1
            customer.served = True
            return True
        return False
    
    def draw(self, window:pg.Surface, offset):
        x = offset[0] + self.rect.x
        y = offset[1] + self.rect.y
        pg.draw.rect(window, (75, 58, 38) if self.owner_cafe else (120, 120, 120), (x, y, self.width, self.height))
        pg.draw.rect(window, (0, 255, 0) if self.open else (255, 0, 0), (x, y, self.width, self.height), width=2)
        text = FONTS['medium'].render(f'{str(len(self.customers))}/{str(self.max_capacity)}', False, (255, 255, 255))
        window.blit(text, text.get_rect(center=(offset[0]+self.rect.centerx,offset[1]+self.rect.centery)))
