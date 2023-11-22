import pygame
import threading
import time

from constants.ViewConstants import ViewConstans
from constants.GameConstants import GameConstants

from sim.dynamics import mrua

class Projectile(pygame.sprite.Sprite):
    
    def __init__(self, number_lanes, lane, player):
        super().__init__()
        self.in_time=0
        self.player=player
        self.life = 1
        self.y_pos= 600
        self.number_lanes= number_lanes
        self.lane= lane
        self.x_pos = self.get_pixel()
        self.rect = pygame.Rect((self.x_pos-(ViewConstans.PROJ_WIDTH.value/2)), self.y_pos, ViewConstans.PROJ_WIDTH.value, ViewConstans.PROJ_HEIGHT.value)
        self.image = pygame.image.load("resources/images/player/proj.png")  # Cargar la imagen del disparo
        self.thread = threading.Thread(target=self.start_proj)
        
    def start(self):
        self.thread.start()
    
    def get_rect(self):
        return self.rect
    
    def move_y(self):
        self.y_pos -= mrua(GameConstants.PROJ_INITIAL_VEL.value, GameConstants.PROJ_ACELERATION.value, self.in_time)
        if self.y_pos <= 30:
            self.kill()
        self.player.validateCollisions(self)
        
    def get_pixel(self):
        width = 500 - ViewConstans.PROJ_HEIGHT.value - ViewConstans.MARGIN.value
        t = width / self.number_lanes
        p = (t * (self.lane - 1)) + ViewConstans.MARGIN.value 
        return int(p)
    
    def kill(self):
        self.life = 0
        self.player.remove_projectile(self)
        
    def draw(self, screen):
        self.rect = pygame.Rect((self.x_pos - (ViewConstans.PROJ_WIDTH.value/2)), self.y_pos, ViewConstans.PROJ_WIDTH.value, ViewConstans.PROJ_HEIGHT.value)
        screen.blit(self.image, self.rect)  # Dibujar la imagen en lugar del rectángulo
    
    def start_proj(self):
        while self.life > 0:
            self.in_time += GameConstants.OBJ_THREAD_TIME.value
            self.move_y()
            time.sleep(GameConstants.OBJ_THREAD_TIME.value)
        self.stop()
        
    def stop(self):
        try:
            self.kill()
            self.thread.join()
        except:
            return