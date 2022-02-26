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

# Classes
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel
    
    def off_screen(self, height):
        return  not (self.y <= height and self.y >= 0)
    
    def collision(self, obj):
        return collide(obj, self)

class Ship:
    COOLDOWN = 30
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
        for laser in self.lasers:
            laser.draw(window)
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
    
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
    
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    
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
        
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    
    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height()+ 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

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
        
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 10, self.y, self.laser_img)
            self.lasers.append(laser)

# Functions
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# Game Loop
def main():
    # game variables
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont('comicsans', 30)
    lost_font = pygame.font.SysFont('comicsans', 40)
    clock = pygame.time.Clock()
    
    player_vel = 5
    player = Player(300, 600)
    
    enemies = []
    enemy_vel = 2
    wave_length = 5
    
    laser_vel = 5
    
    lost = False
    lost_count = 0
    # window logic
    def redraw_window():
        WIN.blit(BG, (0, 0))
        # text labels
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        
        # show text
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (HEIGHT - level_label.get_width() - 10, 10))
        # show enemy
        for enemy in enemies:
            enemy.draw(WIN)
        # show player
        player.draw(WIN)
        # lost text logic
        if lost:
            lost_label = lost_font.render('You Lost!!', 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH//2 - lost_label.get_width()//2, 350))
            
        pygame.display.update()
    # Game logic
    while run:
        clock.tick(FPS)
        redraw_window()
        
        if lives == 0 or player.health <= 0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > FPS * 3:
                run = False
                break
            else:
                continue
        
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(['red', 'blue', 'green']))
                enemies.append(enemy)
        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
        keys = pygame.key.get_pressed()
        # Player movement logic
        if keys[pygame.K_a] and player.x - player_vel > 0: # Left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # Right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # Up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # Down
            player.y += player_vel
        # Enemy movement logic
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            # Enemy shooting logic
            if random.randrange(0, 3*60) == 1:
                enemy.shoot()
            # Enemy collisions
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        # Player shooting logic
        player.move_lasers(-laser_vel, enemies)

# MAIN MENU
def main_menu():
    title_font = pygame.font.SysFont('comicsans', 40)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render('Press the mouse button to begin...', 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH//2 - title_label.get_width()//2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

###
if __name__ == '__main__':
    main_menu()