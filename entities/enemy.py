import pygame
import threading
import time
import ctypes

from sim.dynamics import mru
from sim.montecarlo import montecarlo

from constants.ViewConstants import ViewConstans
from constants.GameConstants import GameConstants

from utilities.random_number import RandomNumber

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, number_lanes, lane,enemy_prob_move,path_level, villain):
        super().__init__()
        self.in_time=0
        self.villain=villain
        self.path_level=path_level
        self.life = 2
        self.y_pos= 115
        self.enemy_prob_move=enemy_prob_move
        self.number_lanes= number_lanes
        self.lane= lane
        self.running=True
        self.killing=False
        self.x_pos = self.get_pixel()
        self.random= RandomNumber()
        self.rect= pygame.Rect((self.x_pos-(ViewConstans.WIDTH.value/2)), self.y_pos, ViewConstans.WIDTH.value, ViewConstans.HEIGHT.value)
        self.image=pygame.image.load(f"resources/images/{self.path_level}/enemy.png")
        self.thread = threading.Thread(target=self.start_enemy)
        self.thread.start()
    
    def move(self, move):
        if ((self.lane +move)>= 1) and ((self.lane + move)<=self.number_lanes):
            self.lane+=move
            self.x_pos= self.get_pixel()
            
    def set_running(self,value):
        self.running=value
        
    def move_y(self):
        self.y_pos+=mru(GameConstants.ENEMY_VEL.value, self.in_time)
        
        if not self.running:
            self.running=False
            self.kill()
        else:
            if ((self.y_pos+ViewConstans.HEIGHT.value)>=650) :
                if self.running and self.villain!=None:
                    self.villain.enemy_impact(self)
                self.kill()
            else:
                self.select_move()
        
    def kill(self):
        if not self.killing:
            self.killing=True
            self.running=False
            self.life=0
            if self.villain!=None:
                self.villain.remove_enemy(self)
            self.stop()
            self.villain=None
        
    def get_pixel(self):
        width=500 - ViewConstans.HEIGHT.value - ViewConstans.MARGIN.value
        t=width/self.number_lanes
        p= (t*(self.lane-1)) + ViewConstans.MARGIN.value 
        return int(p)
    
    def select_move(self):
        
        movimiento= montecarlo(GameConstants.ENEMY_MOVE.value, self.enemy_prob_move, self.random.calculate_ni())
        self.move(movimiento)
        
    def draw(self, screen):
        self.rect = pygame.Rect((self.x_pos-(ViewConstans.WIDTH.value/2)), self.y_pos, ViewConstans.WIDTH.value, ViewConstans.HEIGHT.value)
        screen.blit(self.image, self.rect) 
    
    def start_enemy(self):
        while self.running:
            self.in_time+=GameConstants.OBJ_THREAD_TIME.value
            self.move_y()
            time.sleep(GameConstants.OBJ_THREAD_TIME.value)
        self.kill()
        
    def stop(self):
        try:
            thread_id = self.thread.ident
            thread_object = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), ctypes.py_object(SystemExit))
            if thread_object == 0:
                raise ValueError("El hilo no pudo ser detenido")
        except:
            return