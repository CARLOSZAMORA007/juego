import pygame
import threading
import time
import random
import ctypes

from sim.dynamics import free_fall
from sim.montecarlo import montecarlo

from constants.ViewConstants import ViewConstans
from constants.GameConstants import GameConstants

class Item(pygame.sprite.Sprite):
    
    def __init__(self, number_lanes, lane,power, villain):
        super().__init__()
        self.in_time=0
        self.villain=villain
        self.power=power
        self.life = 2
        self.image=None
        self.set_image_by_power()
        self.y_pos= 115
        self.number_lanes= number_lanes
        self.lane= lane
        self.running=True
        self.x_pos = self.get_pixel()
        self.rect= pygame.Rect((self.x_pos-(ViewConstans.WIDTH.value/2)), self.y_pos, ViewConstans.WIDTH.value, ViewConstans.HEIGHT.value)
        self.thread = threading.Thread(target=self.start_item)
        self.thread.start()
        
    
    def set_image_by_power(self):
        if self.power=="frezee":
            self.image=pygame.image.load("resources/images/items/frezee.png")
        elif self.power=="double":
            self.image=pygame.image.load("resources/images/items/double.png")
        else:
            self.image=pygame.image.load("resources/images/items/energy.png")
        
    def get_power(self):
        return self.power
    
    def move_y(self):
        self.y_pos+=free_fall(GameConstants.ITEM_GRAVITY.value, self.in_time)
        if ((self.y_pos+ViewConstans.HEIGHT.value)>=650) :
            self.kill()
        
    def kill(self):
        self.running=False
        self.life=0
        self.villain.remove_item(self)
        
    def get_pixel(self):
        width=500 - ViewConstans.HEIGHT.value - ViewConstans.MARGIN.value
        t=width/self.number_lanes
        p= (t*(self.lane-1)) + ViewConstans.MARGIN.value 
        return int(p)
    
    def select_move(self):
        
        movimiento= montecarlo(GameConstants.ENEMY_MOVE.value, self.enemy_prob_move, random.random())
        self.move(movimiento)
        
    def draw(self, screen):
        if self.running:
            self.rect = pygame.Rect((self.x_pos-(ViewConstans.WIDTH.value/2)), self.y_pos, ViewConstans.WIDTH.value, ViewConstans.HEIGHT.value)
            screen.blit(self.image, self.rect) 
    
    
    def start_item(self):
        while self.running:
            self.in_time+=GameConstants.OBJ_THREAD_TIME.value
            self.move_y()
            time.sleep(GameConstants.OBJ_THREAD_TIME.value)
        self.stop()
        
    def stop(self):
        try:
            self.kill()
            if self.thread.is_alive():
                thread_id = self.thread.ident
                thread_object = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), ctypes.py_object(SystemExit))
                if thread_object == 0:
                    raise ValueError("El hilo no pudo ser detenido")
        except:
            return