import pygame
import time

from entities.player import Player
from entities.villain import Villain
from constants.GameConstants import GameConstants
from constants.ViewConstants import ViewConstans

class Level():
    def __init__(self,control,reaction_villian, villain_life, villain_actions,villain_prob_move, enemy_prob_move, prob_items,path_level):
        super().__init__()
        self.running=True
        self.control=control
        self.double_damage=False
        self.frezee_flag=False
        self.hit_count=0
        self.stopping=False
        self.max_hits=0
        self.player=Player(GameConstants.LANES.value, self)
        self.villain=Villain(GameConstants.LANES.value,reaction_villian,villain_life, villain_actions,villain_prob_move,enemy_prob_move,prob_items,path_level, self)
        pygame.mixer.init()
        back_music = pygame.mixer.Sound(f"resources/music/{path_level}/back.mp3")
        pygame.mixer.Sound.play(back_music, -1) 
    
    def get_frezee_flag(self):
        return self.frezee_flag
    
    def set_frezee_flag(self, value):
        self.frezee_flag=value
    
    def damage_player(self, value):
        dead=self.player.decrease_energy(value)
        hp_sound = pygame.mixer.Sound("resources/music/hit_player.wav")
        pygame.mixer.Sound.play(hp_sound)
        if dead:
            self.stop()
    
    def ultimate_villain(self):
        dead=self.villain.ultimate_villain()
        if dead:
            self.stop()
    
    def draw(self, screen):
        background_image = pygame.image.load("resources/images/bg1.png").convert()
        background_image = pygame.transform.scale(background_image, ViewConstans.WINDOW_SIZE.value)
        screen.blit(background_image, (0, 0))  # Dibujar imagen de fondo
        if self.player!=None:
            self.player.draw(screen)
        if self.villain!=None:
            self.villain.draw(screen)
    
    def collisions(self, projectile):
        colls = pygame.sprite.spritecollide(projectile, self.villain.getEnemies(), True)
        if self.running:
            for e in colls:
                ve_sound = pygame.mixer.Sound("resources/music/hit.wav")
                pygame.mixer.Sound.play(ve_sound)
                self.player.increaseEnergy(10)
                e.kill()
                projectile.kill()
            collsI = pygame.sprite.spritecollide(projectile, self.villain.getItems(), True)
            for i in collsI:
                self.powerup(i.get_power())
                i.kill()
                projectile.kill()
                
            villian_hit=projectile.get_rect().colliderect(self.villain.get_rect())
            if villian_hit:
                vh_sound = pygame.mixer.Sound("resources/music/hit_villain.wav")
                pygame.mixer.Sound.play(vh_sound)
                projectile.kill()
                self.player.increaseEnergy(40)
                
                dead=self.villain.decrease_life(self.calculate_damage(GameConstants.DAMAGE_SHOT.value))
                if dead:
                    self.stop()
        
    def kill(self):
        self.running=False
        self.villain.stop()
        self.player.stop()
        
    def calculate_damage(self, damage):
        if self.double_damage:
            if self.hit_count<=self.max_hits:
                self.hit_count+=1
                return damage*2
            else:
                self.double_damage=False
                self.hit_count=0
                self.max_hits=0
                return damage
        else:
            return damage
    
    def double_power(self):
        double_sound = pygame.mixer.Sound("resources/music/double.wav")
        pygame.mixer.Sound.play(double_sound)
        self.double_damage=True
        self.max_hits+=GameConstants.HITS_COUNT.value
        
    def powerup(self, power):
        if power=="frezee":
            self.frezee()
        elif power=="double":
            self.double_power()
        elif power=="energy":
            energy_sound = pygame.mixer.Sound("resources/music/energy.wav")
            pygame.mixer.Sound.play(energy_sound)
            self.player.increaseEnergy(20)
    
    def frezee(self):
        frezee_sound = pygame.mixer.Sound("resources/music/frezee.wav")
        pygame.mixer.Sound.play(frezee_sound)
        self.frezee_flag=True
        self.villain.add_frezee_time(GameConstants.FREEZE_COUNT_FLAG.value)
        
    def isWin(self):
        return self.player.is_alive() and not self.villain.is_alive()

    def stop(self):
        if not self.stopping:
            self.stopping=True
            self.kill()
            pygame.mixer.quit()
            if self.isWin():
                self.villain=None
                self.player=None
                self.control.next_level()
            else:
                time.sleep(0.6)
                self.control.finish_level()