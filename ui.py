import pygame as pg
from settings import FONTS
from typing import Callable
from tkinter import *
from tkinter import ttk

class ButtonBehavior:
    def __init__(self, left:float, top:float, width:float, height:float, on_press:Callable|None):
        self.rect = pg.Rect(left, top, width, height)
        self.clickable:bool = True
        self.on_press = on_press
    
    def clicked(self, event:pg.event.Event) -> bool:
        if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
            if (self.rect.collidepoint(pg.mouse.get_pos()) and self.clickable):
                if (self.on_press):
                    self.on_press()
                return True
        return False

class ImageButton(ButtonBehavior):
    def __init__(self, left:float, top:float, width:float, height:float, on_press:Callable, image:pg.Surface):
        super().__init__(left, top, width, height, on_press)
        self.image = image
    
    def draw(self, window:pg.Surface) -> None:
        window.blit(self.image, self.rect)


class TextButton(ButtonBehavior):
    def __init__(self, left: float, top: float, width: float, height: float, on_press: Callable, background_color:tuple[int, int, int], content:str='', size:str='large'):
        super().__init__(left, top, width, height, on_press)
        self.surface = pg.Surface((width, height), pg.SRCALPHA)
        self.surface.fill((0, 0, 0, 100))
        self.background_color = background_color
        self.content = content
        self.size = size
    
    def get_text(self) -> tuple[pg.Surface, pg.Rect]:
        text = FONTS.get(self.size).render(self.content, True, (0, 0, 0))
        return (text, text.get_rect(center=self.rect.center))
    
    def draw(self, window:pg.Surface) -> None:
        pg.draw.rect(window, self.background_color, self.rect)
        if (not self.clickable):
            window.blit(self.surface, self.rect)
        if (self.content):
            text, rect = self.get_text()
            window.blit(text, rect)

class ToolButton(TextButton):
    def __init__(self, left:float, top:float, width:float, height:float, on_press:Callable, background_color:tuple[int, int, int], content:str=''):
        super().__init__(left, top, width, height, on_press, background_color, content)
    
    def get_text(self) -> tuple[pg.Surface, pg.Rect]:
        text = FONTS.get('small').render(self.content, True, (0, 0, 0))
        return (text, text.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 5)))


class InputField(TextButton):
    def __init__(self, left, top, width, height, attribute, label, on_press, content='', size = 'medium'):
        super().__init__(left, top, width, height, on_press, (0, 0, 0), content, size)
        self.attribute = attribute
        self.label = label
    
    def handle_text(self, event:pg.event.Event, current_pressed):
        assert event.type == pg.KEYDOWN
        if (current_pressed == self.attribute):
            if (event.key == pg.K_BACKSPACE):
                self.content = self.content[:-1]
            elif (event.unicode.isnumeric()):
                self.content += event.unicode
            elif (event.key == pg.K_RETURN):
                event = pg.event.Event(pg.USEREVENT + 2, {'attribute':self.attribute, 'value':int(self.content)})
                pg.event.post(event)
    
    def draw(self, window:pg.Surface, current_pressed) -> None:
        pg.draw.rect(window, (255, 255, 255), self.rect)
        pg.draw.rect(window, self.background_color if self.attribute != current_pressed else (0, 255, 0), self.rect, width=2)
        text = FONTS.get(self.size).render(self.label, True, (255, 255, 255))
        window.blit(text, text.get_rect(bottomleft=(self.rect.left, self.rect.top - 5)))
        if (not self.clickable):
            window.blit(self.surface, self.rect)
        if (self.content):
            text, rect = self.get_text()
            window.blit(text, rect)

class EditMenu:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.root = Tk()
        
        self.base_price = StringVar()
        self.has_outlet = BooleanVar(value=False)
        self.all_day = BooleanVar(value=False)
        self.max_capacity = StringVar()


        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill="both", expand=True, padx=20, pady=20)

        frm.grid_columnconfigure(1, weight=1)
        ttk.Label(frm, text='Cafe Properties').grid(column=0, row=0, pady=2, columnspan=2)

        ttk.Label(frm, text='Minimum Price').grid(column=0, row=1, sticky='ew', columnspan=2)
        ttk.Entry(frm, textvariable=self.base_price).grid(column=0, row=2, pady=2, sticky='ew', columnspan=2)
        ttk.Label(frm, text='Maximum Capacity').grid(column=0, row=3, sticky='ew', columnspan=2)
        ttk.Entry(frm, textvariable=self.max_capacity).grid(column=0, row=4, pady=2, sticky='ew', columnspan=2)
        ttk.Checkbutton(frm, variable=self.has_outlet).grid(column=0, row=5, )
        ttk.Label(frm, text='Has Outlet').grid(column=1, row=5, sticky='w')
        ttk.Checkbutton(frm, variable=self.all_day).grid(column=0, row=6, )
        ttk.Label(frm, text='All Day Open').grid(column=1, row=6, sticky='w')
        ttk.Button(frm, text='Create', command=self.create).grid(column=0, row=7, pady=2, sticky='ew', columnspan=2)
        self.root.minsize(300, self.root.winfo_height())
        self.root.resizable(False, False)
        self.root.mainloop()
    
    def create(self):
        if (not self.base_price.get().isnumeric()):
            self.base_price.set("Give a number!")
            return
        if (not self.max_capacity.get().isnumeric()):
            self.max_capacity.set("Give a number!")
            return
        pg.event.post(pg.event.Event(pg.USEREVENT+3, {'base_price':float(self.base_price.get()), 'maximum_capacity':int(self.max_capacity.get()), 'has_outlet':self.has_outlet.get(), 'pos':(self.x, self.y), 'all_day':self.all_day.get()}))
        self.root.destroy()
