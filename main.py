# Imports
from re import S
import pygame
import os 
import random

# Pygame initializations
pygame.init()
pygame.font.init()

# Window
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders')

### Assets 
## Window
BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background-black.png')), (WIDTH, HEIGHT))
## Laser
BLUE_LASER = pygame.image.load(os.path.join('Assets', 'pixel_laser_blue.png'))
GREEN_LASER = pygame.image.load(os.path.join('Assets', 'pixel_laser_green.png'))
RED_LASER = pygame.image.load(os.path.join('Assets', 'pixel_laser_red.png'))
YELLOW_LASER = pygame.image.load(os.path.join('Assets', 'pixel_laser_yellow.png'))
## Ship
# Enemy
BLUE_SHIP = pygame.image.load(os.path.join('Assets', 'pixel_ship_blue_small.png'))
GREEN_SHIP = pygame.image.load(os.path.join('Assets', 'pixel_ship_green_small.png'))
RED_SHIP = pygame.image.load(os.path.join('Assets', 'pixel_ship_red_small.png'))
# Player
YELLOW_SHIP = pygame.image.load(os.path.join('Assets', 'pixel_ship_yellow.png'))

# Classes
class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
    
    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

class Enemy(Ship):
    COLOR_MAP = {
        'red': (RED_SHIP, RED_LASER),
        'green': (GREEN_SHIP, GREEN_LASER),
        'blue': (BLUE_SHIP, BLUE_LASER)
    }
    def __init__(self, x, y, color ,health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self, vel):
        self.y += vel
        
# Game Loop
def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    player_vel = 5
    player = Player(200,200)
    main_font = pygame.font.SysFont('comicsans', 30)
    clock = pygame.time.Clock()
    
    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (HEIGHT - level_label.get_width() - 10, 10))
        
        player.draw(WIN)
        
        pygame.display.update()
    
    while run:
        clock.tick(FPS)
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a] and player.x - player_vel > 0: # Left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # Right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # Up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT: # Down
            player.y += player_vel
        
        
            
if __name__ == '__main__':
    main()