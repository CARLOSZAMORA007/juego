import pygame
import threading
import ctypes

from entities.projectile import Projectile
from constants.ViewConstants import ViewConstans
from constants.GameConstants import GameConstants

class Player(pygame.sprite.Sprite):
    
    def __init__(self, number_lanes, level):
        super().__init__()
        self.level = level
        self.running = True
        self.energy = GameConstants.INITIAL_ENERGY.value
        self.y_pos = 600
        self.number_lanes = number_lanes
        self.lane = int((number_lanes + 1) / 2)
        self.x_pos = self.get_pixel()
        self.projectiles = pygame.sprite.Group()
        # Cargar imagen del personaje
        self.image = pygame.image.load("resources/images/player/player.png").convert_alpha()
        
        # Obtener rectángulo del área ocupada por la imagen
        self.rect = self.image.get_rect()
        # Asignar posición del rectángulo
        self.rect.center = (self.x_pos, self.y_pos)
        pygame.mixer.init()
        self.thread = threading.Thread(target=self.start_player)
        self.thread.start()
        
        
    def is_alive(self):
        return self.energy>0
    
    def getProjectiles(self):
        return self.projectiles
    
    def decrease_energy(self, value):
        self.energy -= value
        return self.energy <= 0
    
    def validateCollisions(self, projectile):
        self.level.collisions(projectile)
        
    def remove_projectile(self, projectile):
        self.projectiles.remove(projectile)
        
    def shot(self):
        if self.running:
            shot_sound = pygame.mixer.Sound("resources/music/shot.wav")
            pygame.mixer.Sound.play(shot_sound)
            p=Projectile(self.number_lanes, self.lane, self)
            self.projectiles.add(p)
            p.start()
    
    def ultimate_villain(self):
        if self.running:
            if self.energy == GameConstants.MAX_ENERGY.value:
                shot_sound = pygame.mixer.Sound("resources/music/ultimate.wav")
                pygame.mixer.Sound.play(shot_sound)
                self.level.ultimate_villain()
                self.energy = GameConstants.INITIAL_ENERGY.value
    
    def move(self, move):
        if self.running:
            if 1 <= (self.lane + move) <= self.number_lanes:
                self.lane += move
                self.x_pos = self.get_pixel()
                # Actualizar la posición del rectángulo con las nuevas coordenadas
                self.rect.center = (self.x_pos, self.y_pos)

    def get_pixel(self):
        width = 500 - ViewConstans.HEIGHT.value - ViewConstans.MARGIN.value
        t = width / self.number_lanes
        p = (t * (self.lane - 1)) + ViewConstans.MARGIN.value 
        return int(p)
        
    def increaseEnergy(self, value):
        if self.energy + value <= GameConstants.MAX_ENERGY.value:
            self.energy += value
        else:
            self.energy = GameConstants.MAX_ENERGY.value
        
    def get_number_energy(self):
        return int((self.energy *24)/GameConstants.MAX_ENERGY.value)
        
    def draw(self, screen):
        number_bars=self.get_number_energy()
        for i in range(number_bars):
            #Barras de energia
            energy_rect = pygame.Rect(455, (170 + (GameConstants.MAX_ENERGY.value -((i+1)*20))), 10, 20)
            bar_image = pygame.image.load("resources/images/bar.png").convert_alpha()
            screen.blit(bar_image, energy_rect)
            
        battery_image = pygame.image.load("resources/images/battery.png").convert_alpha()
        battery_rect = pygame.Rect(450, 170, 20, GameConstants.MAX_ENERGY.value)
        screen.blit(battery_image, battery_rect)
        screen.blit(self.image, self.rect)
        for p in self.projectiles:
            p.draw(screen)
            
    def start_player(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(12)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.move(-1)
            elif keys[pygame.K_d]:
                self.move(1)
            elif keys[pygame.K_k]:
                self.shot()
            elif keys[pygame.K_l]:
                self.ultimate_villain()
        
        self.stop()
        
    def stop(self):
        try:
            for p in self.projectiles:
                p.stop()
            self.projectiles=pygame.sprite.Group()
            self.running = False
            if self.thread.is_alive():
                thread_id = self.thread.ident
                thread_object = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), ctypes.py_object(SystemExit))
                if thread_object == 0:
                    raise ValueError("El hilo no pudo ser detenido")
                
        except Exception as e:
            return
