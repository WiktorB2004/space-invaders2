# Imports
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

# Game Loop
def main():
    run = True
    FPS = 60
    score = 1
    lives = 5
    clock = pygame.time.Clock()
    
    def redraw_window():
        WIN.blit(BG, (0, 0))
        pygame.display.update()
    
    while run:
        clock.tick(FPS)
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
if __name__ == '__main__':
    main()