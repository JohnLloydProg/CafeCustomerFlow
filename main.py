from settings import WINDOW_WIDTH, WINDOW_HEIGHT, MAP_SIZE, m, FONTS
from objects.customer import Customer, Student
from objects.cafe import Cafe
from objects.establishment import Establishment, School
from ui import InputField, TextButton, EditMenu
from time import time_ns
import pygame
import random
import math

pygame.init()
class Simulation:
    time_multiplier = 80
    sec_event = pygame.USEREVENT + 1
    update_event = pygame.USEREVENT + 2
    create_event = pygame.USEREVENT + 3
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    x_offset = 0
    y_offset = 0
    x_offset_vel = 0
    y_offset_vel = 0
    running = True
    paused = True
    playing = False
    owner_cafe = None
    agents:list[Customer] = []
    cafes:list[Cafe] = []
    establishments:list[Establishment] = []
    counter = 0
    people_per_hour = random.normalvariate(12.25, 6.386369413502032)
    number_competitions = 4
    number_estalblishments = 8
    current_input = None
    selected_cafe = None

    def __init__(self):
        pygame.display.set_caption('Cafe Flow Simulation')
        self.buttons = {
            'pause_btn': TextButton(1090, 800, 75, 50, self.start, (0, 255, 0), 'Start'),
            'restart_btn': TextButton(1175, 800, 75, 50, self.reset, (0, 0, 255), 'Restart')
        }
        self.input_fields = {
            'number_competitions': InputField(1090, 50, 200, 50, 'number_competitions', 'Number of Competition', lambda: setattr(self, 'current_input', 'number_competitions'), str(self.number_competitions)),
            'number_establishments': InputField(1090, 130, 200, 50, 'number_establishments', 'Number of Establishments', lambda: setattr(self, 'current_input', 'number_establishments'), str(self.number_estalblishments)),
            'time_multiplier': InputField(1090, 210, 200, 50, 'time_multiplier', 'Time Multiplier', lambda: setattr(self, 'current_input', 'time_multiplier'), str(self.time_multiplier))
        }
        self.reset()
        
    
    def loop(self):
        pygame.time.set_timer(self.sec_event, 1000, -1)
        record = time_ns()
        move_time = time_ns()
        change = self.counter
        self.fps = 0
        while self.running:
            key_pressed = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                elif event.type == self.sec_event:
                    self.fps = self.counter - change
                    change = self.counter
                        
                elif event.type == pygame.KEYDOWN:
                    for input_field in self.input_fields.values():
                        input_field.handle_text(event, self.current_input)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and mouse_pos[0] < WINDOW_WIDTH - 400 and not self.owner_cafe:
                        x = mouse_pos[0] - int(Cafe.width/2) - self.x_offset
                        y = mouse_pos[1] - int(Cafe.height/2) - self.y_offset
                        EditMenu(x, y)
                        
                    for button in self.buttons.values():
                        button.clicked(event)

                    for input_field in self.input_fields.values():
                        input_field.clicked(event)
                
                elif event.type == self.update_event:
                    setattr(self, event.dict['attribute'], event.dict['value'])
                    self.current_input = None
                
                elif event.type == self.create_event:
                    self.owner_cafe = Cafe(event.dict['pos'][0], event.dict['pos'][1], event.dict['base_price'], event.dict['has_outlet'], event.dict['maximum_capacity'], event.dict['all_day'], True)
                    self.cafes.append(self.owner_cafe)

            if ((time_ns() - record) > ((10**9)/self.time_multiplier)):
                record = time_ns()
                self.event_per_simulation_time()
                
            
            if ((time_ns() - move_time) > ((10**9)/60)):
                move_time = time_ns()
                self.x_offset += self.x_offset_vel
                self.y_offset += self.y_offset_vel
        
            self.camera_movement_handler(key_pressed)

            self.buttons['pause_btn'].clickable = self.owner_cafe != None
            self.selected_cafe = self.owner_cafe
            for cafe in self.cafes:
                x = mouse_pos[0] - self.x_offset
                y = mouse_pos[1] - self.y_offset
                if (cafe.rect.collidepoint(x, y)):
                    self.selected_cafe = cafe

            self.draw()
        print('Exiting the simulation')
        pygame.quit()
        quit()
    
    def start(self):
        self.paused = not self.paused
        self.buttons['pause_btn'].content = 'Start' if self.paused else 'Pause'
        self.buttons['pause_btn'].background_color = (0, 255, 0) if self.paused else (255, 0, 0)
    
    def reset(self):
        self.playing = False
        self.owner_cafe = None
        self.agents.clear()
        self.establishments.clear()
        self.cafes.clear()
        for i in range(self.number_competitions):
            x = random.randint(Cafe.width//2 + 10, m(MAP_SIZE) - Cafe.width//2)
            y = random.randint(Cafe.height//2 + 10, m(MAP_SIZE) - Cafe.height//2)
            self.cafes.append(Cafe(x, y, random.randrange(55, 180, 30), random.random() < 0.5, random.randrange(40, 80, 5), random.random() < 0.2))
        for i in range(3):
            x = random.randint(Establishment.width//2 + 10, m(MAP_SIZE) - Establishment.width//2)
            y = random.randint(Establishment.height//2 + 10, m(MAP_SIZE) - Establishment.height//2)
            self.establishments.append(School(x, y))
        for i in range(self.number_estalblishments):
            x = random.randint(Establishment.width//2 + 10, m(MAP_SIZE) - Establishment.width//2)
            y = random.randint(Establishment.height//2 + 10, m(MAP_SIZE) - Establishment.height//2)
            self.establishments.append(Establishment(x, y))
        self.counter = 0
    
    def camera_movement_handler(self, key_pressed):
        if key_pressed[pygame.K_a] and self.x_offset < 0:
            self.x_offset_vel += 1
            self.x_offset_vel = min(self.x_offset_vel, 20)
        elif  key_pressed[pygame.K_d] and self.x_offset > -1 * (m(MAP_SIZE) - WINDOW_WIDTH + 400):
            self.x_offset_vel -= 1
            self.x_offset_vel = max(self.x_offset_vel, -20)
        else:
            self.x_offset_vel = 0
        
        if key_pressed[pygame.K_w] and self.y_offset < 0:
            self.y_offset_vel += 1
            self.y_offset_vel = min(self.y_offset_vel, 20)
        elif key_pressed[pygame.K_s] and self.y_offset > -1 * (m(MAP_SIZE) - WINDOW_HEIGHT):
            self.y_offset_vel -= 1
            self.y_offset_vel = max(self.y_offset_vel, -20)
        else:
            self.y_offset_vel = 0
    
    def event_per_simulation_time(self):
        if (not self.paused):
            self.counter += 1
            for agent in self.agents:
                if (agent.target):
                    if (agent.rect.colliderect(agent.target.rect)):
                        if (not agent.target.enter(agent)):
                            agent.decide(self.cafes)
                    else:
                        agent.move()
                else:
                    self.agents.remove(agent)
                
                if (agent.served and agent.waiting_time == 0):
                    self.agents.remove(agent)
            
            for cafe in self.cafes:
                cafe.serving(self.counter)

            if (self.counter % 3600 == 0):
                self.people_per_hour = random.normalvariate(12.25, 6.386369413502032)
            
            if (self.counter % (3600//self.people_per_hour) == 0):
                customer_class = Customer
                if (random.random() < 0.5):
                    customer_class = Student
                spawn_point:Establishment = random.choice(list(filter(lambda establishment: type(establishment)==customer_class.source, self.establishments)))
                customer = customer_class(spawn_point.rect.centerx, spawn_point.rect.centery, random.random() < 0.3, random.choice([0.1, 0.15, 0.2, 0.25, 0.3]))
                customer.reselect(self.cafes)
                self.agents.append(customer)
    
    def get_time(self):
        days = self.counter // 86400
        hours = (self.counter - (days * 86400)) // 3600
        minutes = (self.counter - (days * 86400) - (hours * 3600))//60
        seconds = (self.counter - (days * 8600) - (hours * 3600) - (minutes * 60))

        return f'Day {str(days)} {str(hours)}:{str(minutes)}:{str(seconds)}'

    def draw(self):
        self.window.fill((255, 255, 255))

        for i in range(0, m(MAP_SIZE), 100):
            pygame.draw.line(self.window, (0, 0, 0), (self.x_offset + i, 0), (self.x_offset + i, m(MAP_SIZE)))
            pygame.draw.line(self.window, (0, 0, 0), (self.x_offset + 0, self.y_offset + i), (self.x_offset + m(MAP_SIZE), self.y_offset + i))
        for agent in self.agents:
            agent.draw(self.window, (self.x_offset, self.y_offset))
        for cafe in self.cafes:
            cafe.draw(self.window, (self.x_offset, self.y_offset))
        for establishment in self.establishments:
            establishment.draw(self.window, (self.x_offset, self.y_offset))
        
        time = FONTS.get('large').render(self.get_time(), True, (0, 0, 0))
        self.window.blit(time, time.get_rect(topright=(WINDOW_WIDTH-410, 10)))

        fps = FONTS.get('large').render(f'FPS: {str(self.fps)}', True, (0, 0, 0))
        self.window.blit(fps, fps.get_rect(topleft=(10, 10)))

        
        pygame.draw.rect(self.window,  (100, 100, 100), (WINDOW_WIDTH-400, 0, 400, WINDOW_HEIGHT))
        for button in self.buttons.values():
            button.draw(self.window)
        for inputField in self.input_fields.values():
            inputField.draw(self.window, self.current_input)
        
        occupancies = FONTS.get('large').render(f'Average Occupancy: {str(self.selected_cafe.get_average_occupancies()) if self.selected_cafe else '0'}', True, (255, 255, 255))
        self.window.blit(occupancies, occupancies.get_rect(topleft=(1090, 310)))
        customers_server = FONTS.get('large').render(f'Customers Served: {str(self.selected_cafe.customers_served) if self.selected_cafe else '0'}', True, (255, 255, 255))
        self.window.blit(customers_server, customers_server.get_rect(topleft=(1090, 340)))
        revenue = FONTS.get('large').render(f'Minimum Revenue: {str(self.selected_cafe.get_minimum_revenue()) if self.selected_cafe else '0'}', True, (255, 255, 255))
        self.window.blit(revenue, revenue.get_rect(topleft=(1090, 370)))
        cost = FONTS.get('large').render(f'Electricity & Rent: {str(round(self.selected_cafe.get_cost(), 2)) if self.selected_cafe else '0'}', True, (255, 255, 255))
        self.window.blit(cost, cost.get_rect(topleft=(1090, 400)))

        for i, instruction in enumerate(["Move Camera Left: a key", "Move Camera Right: d key", "Move Camera Up: w key", "Move Camera Down: s key"]):
            text = FONTS.get('large').render(instruction, True, (255, 255, 255))
            self.window.blit(text, text.get_rect(topleft=(1090, 460 + (i * 30))))


        pygame.display.flip()

if (__name__ == '__main__'):
    Simulation().loop()