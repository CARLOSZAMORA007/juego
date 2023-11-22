import pygame
import sys
import json
import vlc
import keyboard

from entities.level import Level 
from constants.GameConstants import GameConstants

class GameController():
    def __init__(self, screen,level ,menus):
        self.number_level=level
        self.write_level()
        self.actual_level=None
        self.screen=screen
        self.menus=menus
        self.running_level=False
        self.init()
        
    def write_level(self):
        path = "resources/config/level.json"
        level_dict={
            'level':self.number_level
        }
        with open(path, "w") as file:
            json.dump(level_dict, file)
        
    def get_number_level(self):
        return self.number_level
    
    def get_font(self, size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("resources/assets/font.ttf", size)
    
        
    def init(self):
        self.get_level_instance()
        clock = pygame.time.Clock()
        self.running_level=True
        while self.running_level:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_level=False
                    if self.actual_level!=None:
                        self.actual_level.kill()
                    sys.exit()
            if self.actual_level!=None:
                self.actual_level.draw(self.screen)
            
            pygame.display.update()
            
    def finish_level(self):
        self.running_level=False
        self.actual_level=None
        self.menus.restart()
    
    def next_level(self):
        if (self.number_level+1)>GameConstants.MAX_LEVELS.value:
            self.running_level=False
            self.number_level=1
            self.write_level()
            
            instance = vlc.Instance()
            player = instance.media_player_new()
            media = instance.media_new("resources/kinematics/7-fin.mp4")
            player.set_media(media)
            player.set_fullscreen(True)
            player.play()
        
            def close_video():
                player.stop()
            
            keyboard.on_press_key("space", lambda _: close_video())
        
            while player.get_state() != vlc.State.Stopped:
                pass
            
            self.menus.end()
        else:
            self.number_level=self.number_level+1
            self.write_level()
            self.get_level_instance()

    def get_level_instance(self):
        # gamecontroller, time V. reaction, V. life, Matrix Marko V. Actions, V. Left/Right, E Left/rifgt, Prob Type items, path level to resources
        if self.number_level==1:
            
            instance = vlc.Instance()            
            player = instance.media_player_new()      
            media = instance.media_new("resources/kinematics/primer.mp4")            
            player.set_media(media)
            player.set_fullscreen(True)
            player.play()
        
            def close_video():
                player.stop()
            
            keyboard.on_press_key("space", lambda _: close_video())
        
            while player.get_state() != vlc.State.Stopped:
                pass
            #0.5 is reaction villian (accion por markov)
            #300 vida
            #probabilidades accion
            #movimiento izq derecha villano
            #movimiento enemigos moverse izq,quedearse,derecha
            #probabilidad pociones
            #nombre carpetas
            self.actual_level = Level(self,0.5, 300, [
            #columna siguiente estado
            #fila estado condicion
            #enemy-move-stop-good
            [0.04, 0.9, 0.01, 0.05],  # enemy
            [0.05, 0.4, 0.5, 0.05],  # move
            [0.1, 0.8, 0.001, 0.009],  # stop
            [0.2, 0.8, 0.15, 0.05]  # good
            #                                   ["frezee", "double", "energy"]
            ], [0.7, 0.3], [0.0000001, 0.999998, 0.0000001], [0.33, 0.33, 0.34], 'level1')
            
        elif self.number_level==2:
            instance = vlc.Instance()
            player = instance.media_player_new()
            media = instance.media_new("resources/kinematics/segundo.mp4")
            player.set_media(media)
            player.set_fullscreen(True)
            player.play()
        
            def close_video():
                player.stop()
            
            keyboard.on_press_key("space", lambda _: close_video())
        
            while player.get_state() != vlc.State.Stopped:
                pass
            self.actual_level = Level(self,0.4, 500, [
            [0.06, 0.9, 0.01, 0.03],  # enemy
            [0.2, 0.5, 0.01, 0.29],  # move
            [0.1, 0.8, 0.001, 0.009],  # stop
            [0.1, 0.8, 0.001, 0.099]  # good
            ], [0.35, 0.65], [0.0001, 0.9998, 0.0001], [0.3, 0.3, 0.4], 'level2')

        elif self.number_level==3:
            instance = vlc.Instance()
            player = instance.media_player_new()
            media = instance.media_new("resources/kinematics/tercer.mp4")
            player.set_media(media)
            player.set_fullscreen(True)
            player.play()
        
            def close_video():
                player.stop()
            
            keyboard.on_press_key("space", lambda _: close_video())
        
            while player.get_state() != vlc.State.Stopped:
                pass
            self.actual_level = Level(self,0.3, 800, [
            [0.04, 0.9, 0.03, 0.02],  # enemy
            [0.2, 0.5, 0.1, 0.2],  # move
            [0.15, 0.8, 0.001, 0.049],  # stop
            [0.1, 0.8, 0.05, 0.05]  # good
            ], [0.6, 0.4], [0.005, 0.99, 0.005], [0.15, 0.25, 0.6], 'level3')

        elif self.number_level==4:
            instance = vlc.Instance()
            player = instance.media_player_new()
            media = instance.media_new("resources/kinematics/cuarto.mp4")
            player.set_media(media)
            player.set_fullscreen(True)
            player.play()
        
            def close_video():
                player.stop()
            
            keyboard.on_press_key("space", lambda _: close_video())
        
            while player.get_state() != vlc.State.Stopped:
                pass
            self.actual_level = Level(self,0.2, 1000, [
            [0.05, 0.9, 0.02, 0.03],  # enemy
            [0.2, 0.6, 0.05, 0.15],  # move
            [0.1, 0.8, 0.001, 0.009],  # stop
            [0.1, 0.8, 0.05, 0.05]  # good
            ], [0.4, 0.6], [0.0025, 0.995, 0.0025], [0.1, 0.4, 0.5], 'level4')

        elif self.number_level==5:
            instance = vlc.Instance()
            player = instance.media_player_new()
            media = instance.media_new("resources/kinematics/quinto.mp4")
            player.set_media(media)
            player.set_fullscreen(True)
            player.play()
        
            def close_video():
                player.stop()
            
            keyboard.on_press_key("space", lambda _: close_video())
        
            while player.get_state() != vlc.State.Stopped:
                pass
            self.actual_level = Level(self,0.15, 3000, [
            [0.08, 0.9, 0.01, 0.01],  # enemy
            [0.3, 0.6, 0.01, 0.09],  # move
            [0.1, 0.8, 0.001, 0.009],  # stop
            [0.1, 0.8, 0.01, 0.09]  # good
            ], [0.5, 0.5], [0.01, 0.98, 0.01], [0.05, 0.35, 0.6], 'level5')
        else:
            self.actual_level=None