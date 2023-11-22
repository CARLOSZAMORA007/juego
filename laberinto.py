import copy
from board import boards
import pygame
import math

# Configuración de la pantalla
WIDTH =  900 
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Otras configuraciones del juego
timer = pygame.time.Clock()
fps = 60
scenery = copy.deepcopy(boards)
wallColor = 'indianred'
sceneryColor = 'goldenrod' 
PI = math.pi

# Carga de imágenes y definición de posiciones iniciales
player_images = []
SCALE = 50
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'resources/assets/player_images/{i}.png'), (SCALE, SCALE)))
    
oscuroPng = pygame.transform.scale(pygame.image.load(f'resources/assets/spirit_images/oscuro.png'), (SCALE, SCALE))
fuegoPng = pygame.transform.scale(pygame.image.load (f'resources/assets/spirit_images/fuego.png'), (SCALE, SCALE))
aguaPng = pygame.transform.scale(pygame.image.load  (f'resources/assets/spirit_images/agua.png'), (SCALE, SCALE))
airePng = pygame.transform.scale(pygame.image.load  (f'resources/assets/spirit_images/aire.png'), (SCALE, SCALE))
tierraPng = pygame.transform.scale(pygame.image.load(f'resources/assets/spirit_images/tierra.png'), (SCALE, SCALE))

player_x = 440 
player_y = 438
direction = 0

counter = 0
direction_command = 0
player_speed = 2
powerup = False
power_counter = 0
moving = True

# Definición de la clase spirit
class Laberinto:
 # Inicializa las propiedades de la instancia con los valores proporcionados   
    def __init__(self, x_coord, y_coord, img):  
        pygame.init()  
        # Propiedades de los espiritus      
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.img = img
        self.rect = self.draw()
                
    def draw(self):
        screen.blit(self.img, (self.x_pos, self.y_pos))        

def draw_misc():
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)

def check_collisions(power):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    center_x = player_x + 23
    center_y = player_y + 24

    if 0 <= center_x // num2 < len(scenery[0]) and 0 <= center_y // num1 < len(scenery):
        if scenery[center_y // num1][center_x // num2] == 1:
            scenery[center_y // num1][center_x // num2] = 0

        if scenery[center_y // num1][center_x // num2] == 2:
            scenery[center_y // num1][center_x // num2] = 0
            power = True         
    return power

def draw_board():
    # Dibujar el tablero
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    screen.fill(sceneryColor) # fondo de la pantalla 
    for i in range(len(scenery)):
        for j in range(len(scenery[i])):
            if scenery[i][j] == 3:
                pygame.draw.line(screen, wallColor, (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 3)

            if scenery[i][j] == 4:
                pygame.draw.line(screen, wallColor, (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

            if scenery[i][j] == 5:
                pygame.draw.arc(screen, wallColor, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1], 0, PI / 2, 3)

            if scenery[i][j] == 6:
                pygame.draw.arc(screen, wallColor, [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
                
            if scenery[i][j] == 7:
                pygame.draw.arc(screen, wallColor, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3 * PI / 2, 3)

            if scenery[i][j] == 8:
                pygame.draw.arc(screen, wallColor, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2, 2 * PI, 3)

            if scenery[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
                screen.blit(fuegoPng, ((j * num2)-10 , (i * num1)- 10))                

            if scenery[i][j] == 2:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
                screen.blit(aguaPng, ((j * num2)-10 , (i * num1)- 10))    
                

def draw_player(): 
     # Lógica para dibujar al jugador   
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

def move_player(play_x, play_y):          # 0-Derecha, 1-Izquierda, 2-Arriba, 3-Abajo 
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    # comprobar las colisiones basadas en el centro x y el centro y del jugador +/- número de manipulación
    if centerx // 30 < 29:
        if direction == 0:
            if scenery[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if scenery[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if scenery[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if scenery[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if scenery[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if scenery[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if scenery[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if scenery[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True

        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if scenery[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if scenery[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if scenery[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if scenery[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

run = True
while run:    
    timer.tick(fps)     # Limita la ejecución del bucle al número de fotogramas por segundo (fps)
    if counter < 19:
        counter += 1        
        if counter > 3:
             flicker = False
    else:       
        counter = 0
        flicker = True    
        
    draw_board()
    center_x = player_x + 23
    center_y = player_y + 24
    player_circle = pygame.draw.circle(screen, sceneryColor, (center_x, center_y), 20, 2)
    
    draw_player()

    draw_misc()    
    turns_allowed = check_position(center_x, center_y) # Verifica cuántos giros están permitidos en la posición actual del jugador    
    if moving:
        player_x, player_y = move_player(player_x, player_y) # Si el jugador se está moviendo, actualiza su posición    
    powerup= check_collisions(powerup) # Verifica colisiones relacionadas con powerup y actualiza variables

    # Manejo de eventos de Pygame
    for event in pygame.event.get():
            
        if event.type == pygame.QUIT:
            run = False        
            
        if event.type == pygame.KEYDOWN:
            # Verifica qué tecla se ha presionado
            if event.key == pygame.K_d:
                direction_command = 0
            elif event.key == pygame.K_a:
                direction_command = 1
            elif event.key == pygame.K_w:
                direction_command = 2
            elif event.key == pygame.K_s:
                direction_command = 3

    # Actualiza la dirección del jugador según las teclas presionadas y los giros permitidos
    if direction_command == 0 and turns_allowed[0]:
         direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3
            
    # Actualiza la pantalla
    pygame.display.flip()      

pygame.quit()